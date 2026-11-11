---
name: google-agents-cli-aad-findings
description: >
  Use when a user wants to review what AAD (Agent Anomaly Detection) found for
  their ADK / Agent Engine agent and act on it — "what did AAD find", "any
  anomalies / recommendations", "review my agent's findings", "review
  monitoring", "how do I improve my agent from its findings", "any security
  issues with my agent". Read-only on AAD: resolves the agent's MonitoredAgent
  id, pulls AnalyzedSessions (with per-finding recommendations), summarizes and
  ranks the highest-priority fixes, asks which to apply, then hands off to the
  ADK build/eval/deploy skills to apply them. Never mutates AAD.
metadata:
  author: Google — Project Greenpeace / AAD (PROTOTYPE, not yet shipped)
  license: Apache-2.0
  version: 0.1.0
  requires:
    bins:
      - agents-cli
      - gcloud
      - curl
      - jq
---

# Review AAD findings and recommend agent fixes (Track 2)

> PROTOTYPE. The "observe → improve" half of the AAD × agents-cli design
> (`edge/greenpeace/g3doc/agents_cli_aad_integration_design.md`, cl/959217664).
> Read-only on AAD — it only *reads* findings; the only writes are to the user's
> **agent** via the normal build loop (`google-agents-cli-adk-code` → `-eval` →
> `-deploy`). For a no-GCP demo, stub the `curl` calls (see Demo mode).

## Endpoint + auth (fixed)

Every AAD call uses ONE endpoint/region (there is **no** `us-central1` for AAD):

*   Host: `https://aiplatform.us.rep.googleapis.com/v1beta1`
*   Location segment: `us` (the AAD scope region; the agent's own deploy region
    is independent and can be any Agent Engine region).
*   Headers (both required): `-H "Authorization: Bearer $(gcloud auth
    application-default print-access-token)"` and `-H "x-goog-user-project:
    ${PROJECT}"`.

**Mint the token ONCE, to a file, and source it afterwards.** Each command you
run is a *separate shell* — nothing you export survives to the next one. If you
inline `$(gcloud auth application-default print-access-token)` in every call you
re-pay ~1.6s for the token and ~0.8s for the project id on every single command,
which is the dominant cost of this whole skill. Do this first, once:

```bash
mkdir -p /tmp/aad && cat > /tmp/aad/env.sh <<EOF
PROJECT="$(gcloud config get-value project 2>/dev/null)"
TOKEN="$(gcloud auth application-default print-access-token)"
HOST="https://aiplatform.us.rep.googleapis.com/v1beta1"
EOF
echo 'AAD="${HOST}/projects/${PROJECT}/locations/us"
TRACE="https://cloudtrace.googleapis.com/v1/projects/${PROJECT}"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "x-goog-user-project: ${PROJECT}")
TAUTH=(-H "Authorization: Bearer ${TOKEN}")' >> /tmp/aad/env.sh
```

Then begin **every** later command with `source /tmp/aad/env.sh`. The token is
good for ~60 min, far longer than this flow takes. If a call returns 401, re-run
the block above once and retry.

## Fast path — run ONE command, then write the answer

For "what did AAD find / show me the results / any anomalies", do **not** walk
the steps below by hand. They exist to explain the API and to cover cases the
script does not. The normal path is one command:

```bash
S=/config/.gemini/config/plugins/google-agents-cli-aad-findings/scripts/aad_report.py
[ -f "$S" ] || S=.agents/skills/google-agents-cli-aad-findings/scripts/aad_report.py
python3 "$S" 7                       # days; defaults to 7
```

Use that two-line form, not a bare relative path. This skill installs under
`/config/.gemini/config/plugins/`, **not** under `.agents/skills/` where the
lab's own skill lives — a measured run guessed the wrong one, failed, and
burned two searches finding it.

It mints the token once, fans every call out in parallel, and prints one JSON
object: `project`, `window`, `totals{agents,enrolled,analysed,flagged}`,
`enrolledAgents[{displayName,maUuid,reasoningEngine,state}]` (the full
enrolment roster, so you can name an agent that is **not** monitored),
`agents[{displayName,analysed,flagged}]`, and `sessions[]` — each with
`sessionId`, `severity`, `detectors[{id,severity,probability,explanation}]` and
`turns[{input,output,tool}]` already joined from Cloud Trace. Keys are stable
and missing data is `null`/`[]`, never an absent key, so you can read it
straight into the output format without probing.

⛔ **Once it has run, do not call the AAD or Cloud Trace APIs again** — no
`curl`, no `python3 -c` with `urllib`, no re-minting a token with
`subprocess.check_output(['gcloud'…])`. Everything those calls would return is
already in the JSON. A measured run re-implemented the same requests by hand in
four extra commands after the script had already fetched them, which was the
single largest remaining cost in the step.

Measured on a live project: **12s**, against several minutes and ~20 commands
doing it by hand.

A failed fetch comes back as empty rather than as an error, so an empty
`turns[]` means either the session genuinely has no transcript or the read did
not succeed — the two look the same. Never report a session with no turns as
clean or uneventful; say the transcript was unavailable, and re-run before
drawing a conclusion from it.

Read the steps below only when the script reports an error, when you need an
agent it did not list, or when you need per-invocation detail.

## Keep the command count down

Every separate command you run costs a round trip, and that — not the API — is
what makes this skill feel slow. The steps below are written as separate blocks
so each one can be explained, **not so each one becomes its own command.** Batch
them. A complete run should be about **four** commands, not fifteen:

1.  the auth block above, plus the time window, plus `ListMonitoredAgents` and
    `AggregateAnalyzedSessions` — all in one command;
2.  `ListAnalyzedSessions` + the parallel `GetAnalyzedSession` fan-out (Step
    3/3b) in one command;
3.  the transcript pull for the worst session(s) (Step 3c) in one command;
4.  the summarize jq (Step 4), if you did not already fold it into 2.

Two things that cut work without changing a word of the output:

*   **Use the wildcard `monitoredAgents/-`** for aggregate and list instead of
    looping per agent. One call covers every agent.
*   **`AggregateAnalyzedSessions` already returns per-agent display names and
    counts** in `agentAggregates[]`, so when you only need "which agents, how
    many sessions, how many flagged", Step 1 is redundant — skip it. Run Step 1
    only when you need an agent that has *no* analysed sessions (it will be
    absent from the aggregate) or when you must map a specific RE id to its MA
    UUID.

Do not re-run a call to "check" something you already fetched; re-read the JSON
you saved under `/tmp/aad/`.

## Flow

### Step 0 — Ask the time window FIRST (if not given)

AAD filters findings by a `detection_time` window. **If the user didn't say how
far back to look, ASK:** *"How many days of findings should I review? (default:
7)"*. Then compute an RFC-3339 window — both bounds are required by the API:

```bash
DAYS="${DAYS:-7}"
START=$(date -u -d "${DAYS} days ago" +%Y-%m-%dT%H:%M:%SZ)
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
WINDOW="detection_time >= \"${START}\" AND detection_time <= \"${END}\""
```

(If you pass no filter at all, `ListAnalyzedSessions` defaults to the last 7
days and `AggregateAnalyzedSessions` to the last 3 — but pass the explicit
window so the user's chosen range is honored.)

### Step 1 — Resolve agents: name ⇄ MonitoredAgent id ⇄ Reasoning Engine id

You need the **MonitoredAgent id (MA UUID)** to read findings, but users think
in **agent display names** or **Reasoning Engine ids**. Build the mapping with
`ListMonitoredAgents` (paginate; `filter=state=ACTIVE` optional):

```bash
list_agents() {  # prints one TSV row per agent: MA_UUID <tab> displayName <tab> RE_ID <tab> region <tab> state
  local tok=""
  while :; do
    resp=$(curl -s -G "${AAD}/monitoredAgents" "${AUTH[@]}" \
      --data-urlencode "pageSize=100" --data-urlencode "pageToken=${tok}")
    echo "$resp" | jq -r '.monitoredAgents[]? |
      [ (.name | sub(".*/monitoredAgents/";"")),
        (.displayName // ""),
        (.agentResource.agent | sub(".*/reasoningEngines/";"")),
        (.agentResource.location // ""),
        (.state // "") ] | @tsv'
    tok=$(echo "$resp" | jq -r '.nextPageToken // ""'); [ -z "$tok" ] && break
  done
}
list_agents
```

*   **MA UUID** = the segment of `name` after `/monitoredAgents/` (a UUID like
    `d9b6e9d3-…`, or a slug in demo data). This is the id you use for findings.
*   **RE id** = the segment of `agentResource.agent` after `/reasoningEngines/`.
*   **display name** = `displayName`; **region** = `agentResource.location`.

**Select the target(s):**

*   User named an agent / gave an RE id → pick the matching row → `MA_UUID`.
*   User said "all my agents" / didn't specify → either use the wildcard
    `monitoredAgents/-` (all agents in one call), or prioritize first with
    Step 2.

> Empty list `{}` usually means no telemetry has flowed yet or nothing is
> enrolled — send the user to `google-agents-cli-aad-debug`.

### Step 2 — Prioritize with `AggregateAnalyzedSessions` (the cheap overview)

**This is the fastest prioritization signal — do it before pulling per-session
detail.** One aggregate call (wildcard `-` = all agents, or a specific
`MA_UUID`) returns a rollup whose `summary.severities` tells you, per severity
bucket, *which detectors fire* and *how many sessions* — and `agentAggregates[]`
breaks the same down per agent. (Aggregate does **not** accept a `severity`
filter — it groups by severity; empty filter = last 3 days.)

```bash
curl -s -G "${AAD}/monitoredAgents/-/analyzedSessions:aggregate" "${AUTH[@]}" \
  --data-urlencode "filter=${WINDOW}" --data-urlencode "pageSize=100" > /tmp/agg.json

# Overall: per severity — session count + which detectors fired (worst first)
jq -r '.summary.severities | to_entries
  | map({sev:.key, n:.value.sessionsCount, det:(.value.detectorIds|join(","))})
  | sort_by(.n) | reverse | .[] | "\(.sev): \(.n) sessions  [\(.det)]"' /tmp/agg.json

# Per agent: rank by anomalous sessions
jq -r '.agentAggregates[]? | [.agentDisplayName, .anomalousSessionsCount, .totalSessionsCount] | @tsv' \
  /tmp/agg.json | sort -t$'\t' -k2 -nr
```

This already gives detector × severity × frequency across the whole window. Use
it to decide which agent + which detectors to dig into. Step 3–3b then enrich
the worst sessions with the actual explanations + recommendations.

### Step 3 — Enumerate the flagged sessions (BASIC list, worst first)

> **Important (verified against a live env):** `ListAnalyzedSessions` returns
> only each session's `severities` breakdown and `sessionState` — its
> `assessment` is **null even in `view=FULL`**. The per-finding `explanation` +
> `recommendations[]` come from **`GetAnalyzedSession` (FULL)** in Step 3b. So
> list is just for *enumerating* the flagged sessions; don't bother with FULL
> here.

List the target agent's sessions (or `-` for all), newest-worst first, and keep
`orderBy` identical across every page (page tokens are bound to it):

```bash
enum_flagged() {  # $1 = MA_UUID or "-"; prints flagged session resource names, worst first
  local parent="$1" tok=""
  while :; do
    resp=$(curl -s -G "${AAD}/monitoredAgents/${parent}/analyzedSessions" "${AUTH[@]}" \
      --data-urlencode "filter=${WINDOW}" \
      --data-urlencode "orderBy=max_severity_rank desc, latest_detection_time desc" \
      --data-urlencode "pageSize=100" --data-urlencode "pageToken=${tok}")
    echo "$resp" | jq -r '.analyzedSessions[]? | select(.sessionState=="SESSION_STATE_FLAGGED") | .name'
    tok=$(echo "$resp" | jq -r '.nextPageToken // ""'); [ -z "$tok" ] && break
  done
}
SESSION_NAMES=$(enum_flagged "${MA_UUID}")   # or "-" for all agents
```

Filter grammar (AIP-160 subset, `AND`-joined, each clause ≤ once): a **closed
`detection_time` window (both bounds required)**, an optional `severity`
equality using the **canonical** enum name (`SEVERITY_CRITICAL` /
`SEVERITY_HIGH` / `SEVERITY_MEDIUM` / `SEVERITY_LOW` — short forms rejected),
and an optional `agent_type` equality. To enumerate only the worst, append `AND
severity = "SEVERITY_CRITICAL"` to `${WINDOW}` (empty filter = last 7 days).

### Step 3b — Pull findings + recommendations (`GetAnalyzedSession` FULL)

For the flagged sessions (worst first — **cap the count**, e.g. top 40, to bound
the calls), fetch each in FULL view to get its `assessment.detectorFindings[]`:

Fetch them **in parallel** — they are independent GETs, and doing them one at a
time is the second-biggest cost in this skill after the token. Each response
goes to its own file so concurrent writes cannot interleave:

```bash
source /tmp/aad/env.sh
rm -rf /tmp/aad/full; mkdir -p /tmp/aad/full
i=0
for n in $(echo "$SESSION_NAMES" | head -40); do
  i=$((i+1))
  curl -s -G "${HOST}/${n}" "${AUTH[@]}" \
       --data-urlencode "view=ANALYZED_SESSION_VIEW_FULL" > "/tmp/aad/full/$i.json" &
done
wait
FULL=$(jq -s '.' /tmp/aad/full/*.json)
```

(The old serial version also re-parsed the whole accumulator on every iteration,
which is O(n²) in the number of sessions. Building the array once at the end
with `jq -s` avoids that.)

Each `assessment.detectorFindings[]` carries: `detectorId`, `severity`,
`explanation`, `probability` (0–1), `recommendations[]` (AAD's own suggested
fixes), and sometimes `displayName` (may be absent — fall back to `detectorId`).
Real detectors seen: `tool_misuse`, `rogue_agent`, `identity_privilege_abuse`,
`cascading_failures`, `resource_exhaustion`.

*(Per-invocation verdicts, rarely needed:* `GET
.../analyzedSessions/{SID}/analyzedInvocations` *then `GetAnalyzedInvocation`;
may be empty when analysis is session-level.)*

> **AAD has no conversation API — don't go looking for one.** An
> `AnalyzedInvocation` carries exactly four fields: `name`, `invocationId`,
> `assessment` and `invocationState`. There is **no** prompt, response or tool
> argument anywhere in the AAD surface. AAD tells you *what it concluded*, never
> *what was said*. For the transcript, use Step 3c.

### Step 3c — Read what actually happened in the session (Cloud Trace)

A verdict without the conversation is unreviewable: the leader cannot judge
"unauthorized bulk extraction" without seeing the turn that caused it. The
transcript lives in **the customer project's own Cloud Trace**, not in AAD, and
is read-only.

The join key is `gen_ai.conversation.id`, which **equals the AAD session id**.

```bash
source /tmp/aad/env.sh                # TRACE and TAUTH come from here
SID="<analyzed session id>"           # e.g. db0cfa4d-f214-42bb-be10-83cba01bcbcb
TSTART="<RFC-3339, a little before the session>"
TEND="<RFC-3339, a little after>"

# 1. every trace belonging to that session. ONE page is enough -- see the cap
#    below; do not paginate unless the first page comes back empty.
curl -s -G "${TRACE}/traces" "${TAUTH[@]}" \
  --data-urlencode "filter=gen_ai.conversation.id:${SID}" \
  --data-urlencode "startTime=${TSTART}" --data-urlencode "endTime=${TEND}" \
  --data-urlencode "pageSize=100" --data-urlencode "view=MINIMAL" \
  | jq -r '.traces[]?.traceId' > /tmp/aad/traces.txt

# 2. the turns. Fetch only the FIRST FEW traces, in parallel -- Step 4b quotes
#    at most two turns, so pulling all 60 buys nothing and costs 60 round trips.
rm -rf /tmp/aad/tr; mkdir -p /tmp/aad/tr
i=0
for t in $(head -5 /tmp/aad/traces.txt); do
  i=$((i+1))
  curl -s "${TRACE}/traces/${t}" "${TAUTH[@]}" > "/tmp/aad/tr/$i.json" &
done
wait
jq -r '.spans[] | .labels as $l | select($l["gen_ai.input.messages"] or $l["gen_ai.tool.name"]) |
  [ .name,
    ($l["gen_ai.input.messages"]  // "" | .[0:400]),
    ($l["gen_ai.output.messages"] // "" | .[0:400]),
    ($l["gen_ai.tool.name"] // "") ] | @tsv' /tmp/aad/tr/*.json
```

**Cap the trace fetch.** A 60-turn session is ~60 traces, but the output format
in Step 4b quotes **at most two turns per session**. The first few traces carry
the opening turn, which is the one that establishes intent and is almost always
the one worth quoting. Say how many turns the session had (from
`wc -l < /tmp/aad/traces.txt`) rather than reading them all to count.

Labels worth reading: `gen_ai.input.messages` (the user turn),
`gen_ai.output.messages` (the reply, or the tool call the model chose),
`gen_ai.tool.name`, `gcp.vertex.agent.tool_call_args`,
`gcp.vertex.agent.tool_response`, and `gen_ai.system_instructions` (what the
agent was told it may do — the thing a governance leader most often wants).

A 60-turn session is ~60 traces. **Do not paste them.** Read them and write the
narrative in Step 4: who asked for what, what the agent did about it, and where
it went wrong. Quote at most one or two short turns as evidence.

### Step 4 — Extract + summarize

Flatten every finding across the fetched FULL sessions and group by detector:

```bash
echo "$FULL" | jq -r '
  def rank: {"SEVERITY_LOW":1,"SEVERITY_MEDIUM":2,"SEVERITY_HIGH":3,"SEVERITY_CRITICAL":4}[.] // 0;
  [ .[] | .name as $s | (.assessment.detectorFindings[]? | . + {session:$s}) ]
  | group_by(.detectorId)
  | map({
      detector: (.[0].displayName // .[0].detectorId),
      detectorId: .[0].detectorId,
      sessions: (map(.session) | unique | length),
      maxSeverity: (max_by(.severity | rank).severity),
      avgProbability: ((map(.probability // 0) | add) / length),
      explanation: (.[0].explanation // ""),
      recommendations: ([ .[].recommendations[]? ] | group_by(.)
        | map({r: .[0], n: length}) | sort_by(.n) | reverse | .[0:5] | map(.r)),
      examples: (map(.session) | unique | .[0:3])
    })
  | sort_by([(.maxSeverity | rank), .sessions]) | reverse'
```

Combine the two signals: **whole-window frequency + severity from Step 2's
aggregate**, enriched with the **explanations + concrete recommendations from
Step 3b**. Produce a short human summary per detector — how many sessions it
fired in, its max severity, a representative `explanation`, and its top
`recommendations`.

> **AAD emits many near-duplicate recommendations** (observed: 30+ slight
> rephrasings of the same fix per detector). The jq above already keeps only the
> top 5 by frequency — then **cluster those into 1–3 distinct concrete changes**
> when you present them (don't paste the raw list). Frequency ≈ how consistently
> the judge recommends that fix, so it's a good relevance signal.

### Step 4b — Output format (use this shape; do not invent your own)

Lead with the estate, then one block per flagged session. Every block answers
the same four questions in the same order, so two sessions can be compared at a
glance. **The story comes first and the detector names come last** — a reader
should understand what happened before meeting the word `resource_exhaustion`.

⛔ **Emit real Markdown bullets, exactly as below.** Do not align the labels
with spaces: a single newline between plain lines is a soft break, so the whole
block renders as one run-on paragraph and the labels vanish into the prose.
Each `-` is its own line, with a blank line after the session heading.

```markdown
**AAD monitoring** — <N> agents enrolled, <M> sessions analysed, <F> flagged
Window: <start> to <end> · analysed up to <latest detection time>

**<Agent display name>** — session `<id>` · **<SEVERITY>**

- **What happened:** 2-4 sentences, from the Step 3c transcript, in plain
  English: what the user asked for, what the agent did, how far it got. No
  detector names, no jargon.
- **Why it matters:** one sentence on the actual exposure, in the leader's
  terms (records reached, control bypassed, data crossed).
- **What AAD saw:**
  - `<detector>` (**<SEVERITY>**, probability `<p>`) — the finding's own
    explanation, trimmed. One nested bullet per detector, worst first.
- **Evidence:**
  - User turn: *"<one short quoted turn from the transcript>"*
  - Session `<id>` · agent `<resource>` · detected `<time>`
- **Recommended:**
  1. 1-3 distinct fixes, clustered from `recommendations[]` (§Step 4). Name
     the tool each one binds to.
```

A blank line between session blocks, so two never run together.

Rules for the block:

*   **Never show a verdict without the story.** If Step 3c returned nothing for
    a session, say the transcript was unavailable and why — do not quietly
    print the finding alone.
*   One block per session, worst severity first; within a session, worst
    detector first.
*   Quote at most two turns per session, each one line.
*   Say `unknown` for any field you could not read, with the command that would
    resolve it. Never infer a value.
*   Clean sessions are a count in the header, not a block each.

### Step 5 — Rank the highest-priority fixes and ASK which to apply

Rank the detector groups into a **fix list**, ordered by:

1.  **max severity** (CRITICAL > HIGH > MEDIUM > LOW — the `Severity` enum is
    ordered LOW=1 … CRITICAL=4),
2.  then **frequency** (distinct sessions affected),
3.  then **avg probability**.

Present the top candidates as a numbered list and **ask the user which one(s) to
apply** — don't auto-apply. For each:

```
N. [CRITICAL] tool_misuse — 12 sessions, avg prob 0.86
   Why: <one-line explanation from the finding>
   Fix: <AAD's recommendations[], mapped to a concrete agent change>
   Examples: <1–2 session deep links>
```

Prefer AAD's own `recommendations[]` verbatim (they're specific, e.g.
"Rate-limit list_inventory calls per user session"), then map each detector to a
concrete agent change:

| Detector                   | Typical agent fix                               |
| -------------------------- | ----------------------------------------------- |
| `tool_misuse`              | Restrict tool scope; add tool-call              |
:                            : preconditions / allow-list                      :
| `identity_privilege_abuse` | Add authorization checks; scope down            |
:                            : credentials / roles the agent can use           :
| `resource_exhaustion`      | Rate-limit / paginate tool calls; cap bulk data |
:                            : access per session                              :
| `rogue_agent`              | Harden system instruction; add input guardrail  |
:                            : / injection filter; add a safety callback       :
| `cascading_failures`       | Add error handling / retries with backoff;      |
:                            : circuit-break dependent tool chains             :

### Step 6 — Apply, then loop back

For the fix(es) the user picks, hand off to the existing ADK skills — don't edit
blindly:

*   `google-agents-cli-adk-code` — edit `app/agent.py` / instructions / tools /
    callbacks to implement the chosen fix.
*   `google-agents-cli-eval` — validate the change actually reduces the anomaly
    (reuse `-optimize` if tuning).
*   `google-agents-cli-deploy` — redeploy the updated agent.

Then loop: after the agent handles new traffic, re-run this skill to confirm the
finding rate dropped, and move to the next agent from Step 1/2. Never change the
model or unrelated code unprompted.

## Notes & gotchas

*   **Read-only on AAD.** This skill never calls a mutating AAD RPC. The only
    writes are to the user's agent via the build loop.
*   **MA UUID ≠ RE id.** Findings are keyed by the MonitoredAgent UUID (parsed
    from `name`), NOT the Reasoning Engine id (parsed from
    `agentResource.agent`). Using the RE id / URN as the `monitoredAgents/{…}`
    segment returns zero rows.
*   **Both `detection_time` bounds are required** whenever you pass a filter; a
    half-open window is rejected.
*   **`orderBy` must be identical on every page** of a paginated list (page
    tokens are bound to it), else `INVALID_ARGUMENT`.
*   **List never returns `assessment` — `GetAnalyzedSession` does.**
    `ListAnalyzedSessions` returns only `severities` + `sessionState` **even in
    `view=FULL`** (verified live). The per-finding `explanation` +
    `recommendations[]` come only from `GetAnalyzedSession` with
    `view=ANALYZED_SESSION_VIEW_FULL`. So enumerate with list, detail with get.
*   `summary` on a `ListAnalyzedSessions` response is **page-scoped**; for
    whole-window totals use `AggregateAnalyzedSessions` (`summary.severities` +
    per-agent `agentAggregates[]`).
*   **Finding `displayName` may be absent** — fall back to `detectorId`.
*   **A session that just happened may not be analysed yet — this is the single
    most common false alarm.** Inference runs in windows (observed: a 1-hour
    lookback on the first run after a scope is created, then roughly every two
    minutes), and a session is invisible to AAD until the window containing it
    completes. Measured on a real lab project: three abuse sessions were
    generated back to back, the first landed 6 minutes inside the window and
    was flagged, and the other two landed **5 and 9 seconds after the window
    closed** — so a query one minute later reported "7 sessions, 1 flagged" and
    looked like two detectors had failed. Both flagged a few minutes later,
    unchanged. Before concluding a scenario did not fire: compare the session's
    start time against the newest `latestAnalyzedTime` you can see, say plainly
    that analysis is still catching up, and re-run. Do not report an
    un-analysed session as clean.

## Demo mode (no GCP)

Stub the calls: (1) `ListMonitoredAgents` → two agents with
`name`/`displayName`/`agentResource.agent`; (2) `AggregateAnalyzedSessions` →
`summary.severities` (detector × severity × count) + per-agent
`agentAggregates[]`; (3) `ListAnalyzedSessions` → a few `SESSION_STATE_FLAGGED`
sessions with a `severities` map (no `assessment`); (4) `GetAnalyzedSession`
(FULL) → one session's `assessment.detectorFindings` carrying `severity`,
`explanation`, and `recommendations`. That lets a coding agent narrate resolve →
prioritize → enumerate → detail → summarize → rank → ask → hand-off end to end
without touching Google Cloud.

## Related skills

*   `google-agents-cli-aad-debug` — read-only: "why no findings / is monitoring
    on" (use when this skill finds nothing).
*   `google-agents-cli-security-monitoring` — enroll / enable monitoring (Track
    1).
*   `google-agents-cli-adk-code` / `-eval` / `-deploy` — apply the chosen fixes.
