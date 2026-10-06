# M3 Step 4 — Prove the attacks are blocked · the procedure

> Read this when the leader reaches **M3 Step 4**, together with `m3-step1.md` (§4 the replay, §5 reading
> what came back). `../SKILL.md` and `m3.md` still apply: §9 holds the 23 rows, §7 the evidence ranking, §5
> the resolve lines. **Start every block with the resolve lines.**
>
> ⛔ **A verify step: zero mutations.** The wait, the four calls and the reads are required; none changes
> anything. **The scorecard is the one write, at the end, run directly in the shell.** A failing row is
> reported, never repaired: no retune, no rebuild, no re-binding this turn. No floor setting.
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the wait and the calls run for minutes and often go to
> the background. Await "finished with result", then `cat` the checkpoint file, before writing any entry
> line, row, picture or answer.

## 1. The gate — all four before any claim

1. **`wait-done` is at least 300 s after `attach-done`, and `T0` follows it** — both printed from
   `$W/step4_ids.txt` this turn (§2).
2. **The four Step 1 requests went again this turn** with `same-text True` for each (`m3-step1.md` §4), and
   the reader printed every reply.
3. **"Blocked", "refused", "proof", "verified"** as affirmative claims only once the refused call's body is
   in this turn's OUTPUTS and quoted in the answer. `not verified` is always allowed.
4. **Both normal requests' replies were read**: half the question is whether real customers still get an
   answer.

**The Price Match attack still got an answer?** Say what you sent and what came back, then what could
explain it, without fixing anything: the binding not yet acting (if under 7 minutes since `attach-done`,
wait 2 more minutes and send that one call once more, as a new command); the check not running with
`failOpen: true` (the inbound gateway's card, §5; the service-agents' roles); the policy target. Row 15 records the
answer; the scorecard is `FAIL`; the step to return to is Step 3, in a later turn.

## 2. The wait and `T0` — read back, never typed

```
A=$(awk '/^attach-done /{print $2}' "$W/step3_ids.txt" | tail -1); echo "attach-done ${A:-missing}"
if [ -n "$A" ]; then S=$(( 300 - ( $(date -u +%s) - $(date -u -d "$A" +%s) ) )); [ "$S" -gt 0 ] && sleep "$S"; fi
echo "wait-done $(date -u +%Y-%m-%dT%H:%M:%SZ) attach-done ${A:-missing}" | tee -a "$W/step4_ids.txt"
echo "T0 $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/step4_ids.txt"
cat "$W/step4_ids.txt"
```

State the wait in the answer with its length. `attach-done missing` → the binding was never confirmed: rows
12 and 14 are `not verified` and the scorecard is `FAIL`. Still send the four calls and record what came
back; say that no reply can be credited to a binding that was not confirmed.

## 3. The four calls

Run `m3-step1.md` §4's **Step 4** block (it writes each start and exit to `step4_ids.txt` and prints the
reader's output). If `$W/read_reply.py` is missing, write it first with `m3-step1.md` §3. Read each reply
with `m3-step1.md` §5. A 429 or no stream → wait a minute, retry that one call once, then `not verified`.

## 4. The template's block message, and the diagnostics

The refusal is tied to the screen by its words. Read the template this turn:

```
gcloud model-armor templates describe nvst-jailbreak-template --location="$REGION" --format=json > "$W/template_step4.json"; echo "describe-exit $?"
python3 -c 'import json,sys; t=json.load(open(sys.argv[1])); m=t.get("templateMetadata",{}); print("block code:", m.get("customPromptSafetyErrorCode")); print("block message:", m.get("customPromptSafetyErrorMessage")); print("filters:", json.dumps(t.get("filterConfig",{}), sort_keys=True))' "$W/template_step4.json"
```

- **The reply's body carries that message, or names Model Armor** → quote the body as the refusal, beside the
  message, with the call's start time (row 15).
- **Neither** (a bare server error, an empty body, a timeout) → not a refusal: row 15 `not verified`; say it
  may be a fault.

**Only when the Price Match attack was not refused**, two labelled diagnostics may separate *"the filter does
not catch this text"* from *"the check never ran"*. Neither is proof of anything in live traffic:

```
gcloud model-armor templates sanitize-user-prompt nvst-jailbreak-template --location="$REGION" --user-prompt-data-text="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["input"]["message"])' "$W/pma_attack.json")"
```

**The logs — secondary, never required.** The template is not set to log verdicts, and whether the
gateway's request log carries inbound refusals is not verified. If you read it, take `T0` from the file:

```
T0=$(awk '/^T0 /{print $2}' "$W/step4_ids.txt"); echo "T0 $T0"
gcloud logging read '(logName:"modelarmor" OR logName:"networkservices.googleapis.com%2Fgateway_requests") AND timestamp>="'"$T0"'"' --freshness=1h --order=asc --limit=20 --format="table(timestamp,logName,httpRequest.requestUrl,httpRequest.status,jsonPayload.authzPolicyInfo.result)"
```

An entry is corroboration with its time; none is *"no log entry recorded"*, neither a pass nor a failure.
Never promise a Cloud Logging verdict.

## 5. The state re-reads — rows 8–13, 19, 20, 22, 23

```
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:(gcp-sa-dep OR gcp-sa-aiplatform-re)" --format="table(bindings.members,bindings.role)"
gcloud beta network-services agent-gateways describe novasmart-ingress-gateway --location="$REGION" --format=yaml > "$W/ingress_gw_step4.yaml"; grep -E '^(name|createTime):|agentGatewayCard|serviceExtensionsServiceAccount' "$W/ingress_gw_step4.yaml"
gcloud beta service-extensions authz-extensions describe novasmart-ma-ext --location="$REGION" --format=yaml | grep -E 'service:|failOpen|model_armor_settings'
gcloud beta network-security authz-policies describe novasmart-ma-pol --location="$REGION" --format=yaml | grep -E 'policyProfile|action|agentGateways|authzExtensions'
gcloud beta service-extensions authz-extensions list --location="$REGION"; gcloud beta network-security authz-policies list --location="$REGION"
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "$API" | python3 -c 'import json,sys,hashlib
for e in json.load(sys.stdin).get("reasoningEngines",[]):
    s=e.get("spec",{}); d=s.get("deploymentSpec",{}); g=d.get("agentGatewayConfig") or {}
    fp=hashlib.sha256(json.dumps([s.get("packageSpec"), d.get("env")], sort_keys=True).encode()).hexdigest()[:16]
    print(e["name"].rsplit("/",1)[1], "|", e.get("displayName"), "| inbound:", g.get("clientToAgentConfig","none"), "| outbound:", g.get("agentToAnywhereConfig","none"), "| code+config", fp)' | tee "$W/agents_step4.txt"
cut -d'|' -f1,2,5 "$W/agents_before.txt" | sed 's/ *$//' > "$W/fp_before.txt"; cut -d'|' -f1,2,5 "$W/agents_step4.txt" | sed 's/ *$//' > "$W/fp_step4.txt"; diff "$W/fp_before.txt" "$W/fp_step4.txt" && echo "code+config unchanged on every agent"
python3 -c 'import json,sys; a,b=(json.load(open(f)).get("filterConfig") for f in sys.argv[1:3]); print("template filters unchanged" if a==b else "template filters CHANGED")' "$W/template_before.json" "$W/template_step4.json"
gcloud projects get-iam-policy "$PROJECT" --format=json > "$W/project_policy_step4.json"
python3 -c 'import json,sys; P=lambda f:{(b["role"],m) for b in json.load(open(f)).get("bindings",[]) for m in b["members"]}; a,b=P(sys.argv[1]),P(sys.argv[2]); [print("REMOVED",*x) for x in sorted(a-b)]; [print("ADDED",*x) for x in sorted(b-a)]; print("project policy diff done")' "$W/project_policy_before.json" "$W/project_policy_step4.json"
grep -l 'floorsettings' /config/Desktop/novasmart-evidence/m3/*.txt || echo "no floor-setting command recorded in M3"
```

- **Row 13:** the website agent `inbound: none`, the back office's outbound binding the same as in
  `agents_before.txt`.
- **Row 22:** expected diff is empty, or only a service-agent role Step 3 recorded. The platform may add
  its own network-security service agent role when a policy is created: name it as made by the platform.
  Anything naming `antigravity-sa` → row 23 shows it.
- A missing before-file (`agents_before.txt`, `template_before.json`, `project_policy_before.json`) → that
  row is `not verified`; say so.

## 6. Evidence, strongest first

`m3.md` §7: the refused call's own body first; a log entry only as corroboration; never the storefront or
the dashboard. A configuration re-read says what is set, not that anything was stopped. The customer-record
attack's reply is an observation of an agent this check does not cover — it is neither a pass nor a failure.

## 7. Read back, then the table and the coverage line

Event rows (1–7, 12, 14–18, 21) are read back, never retyped. Run this, record it as a command, and copy
each value from its output:

```
cat "$W/step1_ids.txt" "$W/step3_ids.txt" "$W/step4_ids.txt"
python3 "$W/read_reply.py" "$W/pma_attack_step1.txt" "$W/pma_normal_step1.txt"; python3 "$W/read_reply.py" --pii "$W/cpa_attack_step1.txt" "$W/cpa_normal_step1.txt"
for f in m3_step1 m3_step2 m3_step3; do echo "== $f"; awk '/^ENTRY /{b=""} {b=b $0 "\n"} END{printf "%s", b}' "/config/Desktop/novasmart-evidence/m3/$f.txt" | grep -nE 'matches:|liquidation|override|inbound:|nvst-jailbreak-template|policy-done|attach-done|^Change:|^When:|^Written '; done
bash -n "$W/undo_step3.sh" && echo "undo syntax ok"
```

All 23 rows of `m3.md` §9, in order, `# | Check | How I verified | Result`, after OUTPUTS in this turn's
entry. The before/after lives in the cells: Step 1's value and time in *How I verified*, this turn's in
*Result*. Row 16's Result is `not covered`, with the reason in one line (the website agent is reached over
A2A, which the inbound check does not read) and its reply noted as observed. **Keep every row**; a row you
could not fill is `not verified` with the command tried. On screen, `### What I checked` is one line, e.g.
*"22 of the 23 checks are evidenced live; 1 is not covered."* — counted off the rows written.

**Over-blocking is a finding.** A normal request refused by the screen: quote it, name the dial (the
manipulation filter's level), and say plainly that an agent which turns away a real customer is as broken as
one that approves a fraud. Row 17 shows it; never retune.

## 8. The scorecard — every time, pass or fail, last

```
python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/update_scorecard.py \
  --mission M3 --status <PASS or FAIL> --checks-json '[{"name":"<§9 check>","proof":"<value quoted this turn>"}]'
```

- **`--status` follows the table:** `PASS` only when every row is evidenced live showing the control holding
  and row 16 is `not covered`. **`FAIL`** when any row is `not verified`, shows the control not holding (the
  Price Match attack answered, a normal request refused), or rests on output that did not come back this
  turn — that row counts as `not verified` in the coverage line too. The status agrees with the coverage line.
- One object per row (23); each `proof` a value in this turn's OUTPUTS; no customer value; **no single quote
  inside any value**.
- **Run it directly in the shell, exactly as written** — never through a `python3`/`subprocess` wrapper or a
  script file — and record that same command line, with its real `--checks-json`, and its output.
- **PASS:** one plain line of achievement for the Price Match Agent. **FAIL:** name the failing row and the
  step to return to (rows 1–5 → Step 1; 6–7 → Step 2; 8–13 and 21 → Step 3; 14–20, 22, 23 → this step, in a
  later turn once the cause is fixed). **Always** print:
  `📊 **Live Scorecard:** [http://localhost:8088/governance_scorecard.html](http://localhost:8088/governance_scorecard.html)`

## 9. The answer and the picture

- **Bold line — the leader's question, as far as the rows go.** E.g. *"The Price Match attack was refused at
  the inbound gateway — its reply reads '<the body's words>' — and the 5% price match still got its answer;
  the customer-record attack still got an answer, because that agent is not behind this screen."* Each
  clause only if its row holds.
- `### Why this matters`: a four-row before/after table — `| Request | Before (Step 1) | After (now) |` —
  every cell a short quotation from the reader's output, `not tested before` or `not verified` (customer
  rows as count and masked row only); then the wait and its length; the refusal's words beside the
  template's block message; what the normal requests did. One line stating only what the rows show.
- `### What this does not fix`: one agent; `failOpen: true`; four cases chosen by someone who knew the
  answer; the screen looks for manipulation and harmful content, not names or emails; the outbound half not
  demonstrated.
- **The picture — REQUIRED, CALL.** This turn's four requests as arrows from *a customer* to the agent each
  went to, the inbound gateway drawn in front of the Price Match Agent only, each arrow labelled with what
  came back in plain words: *refused — "<the reply's first words>"* only if quoted; *answered*; for the
  website agent *answered — no screen in front of this agent*. No tick, cross, pass, *blocked*,
  *verified*, n of m or coverage line. Caption: the four calls and their times, and the wait. Read the image
  back; a word you did not prompt → regenerate.
- `### Where the proof is`: `m3_step4.txt`, its command count and failures, no undo clause (nothing changed).

## 10. Don't mislabel

- A missing leak, an empty answer, a `500` alone or a quiet log is not a refusal.
- The customer-record attack is never *blocked*, *failed* or *a gap in testing*: it is `not covered`.
- A plausible storefront reply is not a working agent; a dashboard "INTERCEPTED" row is not a verdict.
- A `sanitize-user-prompt` result is the template's opinion of a string, not live traffic.
- Never write a customer name, email, count or time the reader did not print.

## 11. How to close

`m3.md` §2 Close check, row 4. Write *"one attack met the screen"* only if row 15 holds a quoted refusal;
otherwise the smaller close — *"one reply was read, and it was not a refusal"* — is the honest one. Anchor
the questions in the four cases: which message would a determined customer try that none of these resembles;
how NovaSmart would learn that this screen had begun refusing real shoppers.
