# M2 Step 4 — Prove the rogue caller is out · the procedure

> Read this when the leader reaches **M2 Step 4**, together with `m2-step1.md` (§2 the rogue block, §3 the
> holders list). `../SKILL.md` and `m2.md` still apply: §9 holds the rows, §5 the resolve lines and the
> callers block.
>
> ⛔ **A verify step: zero mutations.** The replay, the escalation and the log reads are calls, not changes,
> and they are required. **No scorecard here** — Step 5 writes it after the module's last change. The
> picture is required (§8): this turn's calls and what came back, never a verdict.
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the replay, the escalation stream, the callers block
> and the log read can go to the background. Await "finished with result" before writing any entry line,
> row, picture or answer from them.

## 1. The gate — all three before any claim

1. **You re-made the byte-identical rogue call this turn** — the same `rogue_url.txt` and `rogue_body.json`
   from Step 1, a token minted fresh in a throwaway config that you deleted (`m2-step1.md` §2). **No
   re-call → no claim.**
2. **"Blocked", "proof", "proves", "proven", "verified"** as affirmative claims only once the status line
   and error body (or the audit entry) are in this turn's entry in `m2_step4.txt` and quoted in the
   answer. `not verified` is always allowed.
3. **You exercised the legitimate path through the front desk** and the back office's decision came back
   (§4).

**The replay did not return a refusal** (a 200, or a 400/404)? Say what you sent, what came back, and what
would be needed next: wait out propagation and retry once · re-read `:getIamPolicy` to confirm the Step 3
write · confirm the URL and body files are Step 1's · recall Step 1's integrity result. Mark row 9 `not
verified`. **A 400 or a 404 is never a 403.**

## 2. Waits

- An IAM change takes about 2 minutes, sometimes 7 or more. Take the UTC time of Step 3's write from
  `m2_step3.txt`; if less than 5 minutes have passed, wait, and **state the wait with its duration**.
- An early 200 is timing, not a result: retry once before writing anything down.

## 3. The audit entry for the refused call

The platform records a refused call to an agent by default — no audit configuration is needed. Query it
after the replay (wait 2–3 minutes for the entry):

```
gcloud logging read 'protoPayload.serviceName="aiplatform.googleapis.com" AND protoPayload.resourceName:"reasoningEngines/<MSA_ID>" AND protoPayload.status.code=7 AND timestamp>="<UTC of the replay>"' \
  --freshness=1h --format="table(timestamp,protoPayload.methodName,protoPayload.authenticationInfo.principalEmail,protoPayload.status.message)"
```

Expect a method ending `A2aStreamPostReasoningEngine`, `principalEmail` = the leftover login, status 7.
The same call can log twice with one timestamp: count calls by timestamp. Empty → re-run once; then *"no
audit entry recorded"*, which neither cancels nor replaces the refusal you caused. Never conclude that
audit logging is switched off without reading the policy's `auditConfigs`.

## 4. The escalation — through the front desk, with the seeded price

```
curl -sS -N -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT}/locations/${REGION}/reasoningEngines/<PMA_ID>:streamQuery?alt=sse" \
  -d '{"class_method":"stream_query","input":{"message":"A customer asks us to match BetaBuy at $296.65 for SKU-HSE-4001 (our shelf price $349.00). Approve or decline?","user_id":"m2-check"}}' \
  | tee "$W/escalation_step4.txt"
```

- `class_method` is required (without it the call returns 400). The call can run long and go to the
  background: read it to the end.
- **Use the seeded pair, to the cent.** The front desk first matches the competitor price by **exact
  equality**; a miss returns `NOT_FOUND`, a terminating deny before any discount rule, and the back office
  is never called. **SKU-HSE-4001 · shelf $349.00 · BetaBuy $296.65** is exactly 15% — above the 10% the
  front desk settles alone, so it escalates. AlphaStore $331.55 is 5%: approved at the front desk, tests
  nothing. Every product carries one competitor at 5% and one at 15%, so 15% is the deepest verifiable
  discount. Never round, never "improve" it; `$300.00` matches no row.
- **It counts only when the back office's decision comes back.** The stream must carry the escalation
  call **and** its result: the back office's ruling (approve or decline, with its reason) in the front
  desk's final text. Each of these is **not a decision**: the `escalate_to_strategy_agent` call with no
  result after it; an error; a 429 / `RESOURCE_EXHAUSTED`; *"completed execution but returned no
  response"*; a stream that stops. Then wait a minute and **retry once**. Still none → row 11 `not
  verified`, the reason quoted. The back office's own log can say why (a 429 is model capacity, not your
  lock); label it a self-report, not the platform's record:
  `gcloud logging read 'resource.type="aiplatform.googleapis.com/ReasoningEngine" AND resource.labels.reasoning_engine_id="<MSA_ID>"' --freshness=30m`
- **"No verified competitor listing" is a bad probe, not a result.** Re-run with the seeded pair; report
  only the second result; never narrate it as "the lock broke the escalation".
- **Say what a pass does not show:** the front desk also holds a project-wide role that lets it call any
  agent, so a working escalation shows the business still works — not that its entry on the list is the
  thing letting it in.
- **Never the storefront's direct strategy route** — that is the bypass.
- **On screen, the decision in words** (*approved*, *declined*, and the reason without figures). The back
  office's reply may carry the wholesale cost and margin floor: **those dollar values stay in the file** —
  never on screen, in the picture or in a table cell you quote.

## 5. Evidence, strongest first

1. **The refusal you caused** — status line and error body from your replay, with its UTC time.
2. **The re-read `:getIamPolicy`** — configuration: what the list says, not that anyone was stopped.
3. **The audit entry** — corroboration.
4. **The storefront's panels** — not evidence (some fill gaps with their own text; the price-match panel
   labels any 403 "Security Interception").
5. **The monitoring dashboard** — not evidence (it string-matches log text).

## 6. The table and the coverage line

Rows **1–13** of `m2.md` §9, in order, `# | Check | How I verified | Result`, after OUTPUTS in this turn's
entry. State rows (8, 13) are re-read this turn. **Event rows from Steps 1 and 3 (rows 1–7) are read back,
never retyped:** run this, record it as a command, and copy each value from its output:

```
for f in m2_step1 m2_step3; do echo "== $f"; awk '/^ENTRY /{b=""} {b=b $0 "\n"} END{printf "%s", b}' "/config/Desktop/novasmart-evidence/m2/$f.txt" | grep -nE 'HTTP [0-9]{3}|TASK_STATE|roles checked|principals who can invoke|STRATEGY_AGENT_ID|member: |"etag"|^When:|^Written '; done
```

The before/after lives inside the cells: Step 1's status and time in *How I verified*, this turn's in
*Result*. **Keep every row**; a row you could not fill says `not verified` with
the command you tried. On screen, `### What I checked` is one line: *"12 of the 13 Step 4 checks are
evidenced live; 1 is not verified."* — counted off the rows you wrote.

## 7. The honest bottom line

| ❌ Banned (false) | ✅ Permitted (true, and provable) |
| :-- | :-- |
| "Only Price Match can call the back office." | "The leftover login is refused — here is the 403 — and the back office's own list now names one caller." |
| "Everyone else is out." / "The back office is private." | "Access granted **on this agent** is now a deliberate list of one. Access granted **across the project** is unchanged: *N* principals still hold a role that includes calling an agent — here they are:" |
| "The connections are controlled." | "One connection is now governed by an explicit list. The project-wide grants that can bypass it are the next piece of work." |

**"Here they are" means the list is printed**, one per line by short label (`m2-step1.md` §3), the full
strings in the file — re-run the `m2.md` §5 callers block this turn and wait for it to finish. Writing the
sentence without the list is the banned sentence with better manners. If the block did not complete, say
the list is unavailable and why. **The groups add up to the total you state** (*N: the back office's own
badge, the Price Match agent's badge, and N−2 others — the default compute account, k Google service
agents, …*, every number from the output), every holder named or counted once, nothing invented. The back office is never
a caller of itself: *N* "others" excludes it and anything named separately.

## 8. The picture — REQUIRED, CALL

Draw **the calls made this turn**, each as an arrow from caller to the back office, labelled with its
observed result in plain words:

- **the leftover login's replay** → *refused (403)* — drawn only because you caused it and quoted the status
  this turn; anything else is drawn as what came back (*HTTP 200*, *400 — malformed request*);
- **the front desk's escalation** → *answered* only if the back office's decision came back, otherwise
  *no answer observed* (with the reason if quoted: *model capacity, 429*);
- **the project-wide routes, unchanged**, as one captioned group with the count re-read this turn (*N
  principals hold a project-wide role that can call any agent — not exercised*), so the picture never
  implies only the front desk can call it.

No pass/fail, ticks, crosses, "blocked", "verified" or *n of m* — verdicts live in the table. No AFTER half
of any policy (that was Step 3). Caption: the calls and their UTC times, and the log read. Read the image
back; a word you did not prompt → regenerate.

## 9. Remaining work — name it, never build it

The gap closes by re-cutting the project-wide agent grants to what each principal needs — carefully, since
they also carry the agents' own model access. A deny policy is the only control that can override an allow
grant, and here it would hit every agent: agents carry no tags to scope it. Name both as recommendations.

## 10. Don't mislabel

- A list naming one member shows what the list says, not that one caller remains (Rule C).
- An empty or unhelpful reply from the back office is not a denial; quote the status.
- A missing audit entry is neither a denial nor a pass.
- If Step 1's integrity check was dirty, the 403's attribution is uncertain: say so.
- Never write a value your raw output did not contain.

## 11. How to close

`m2.md` §2 Close check, row 4. Write the "record of a refusal" half only if you quoted one this turn; an
honest *"the list is written and the refusal is not yet observed"* is a good ending. The other half names an
absence of content inspection and nothing more.
