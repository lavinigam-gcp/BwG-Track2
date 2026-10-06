# M1 Step 5 — Prove it worked · the procedure

> Read this when the leader reaches **M1 Step 5**. `../SKILL.md` and `m1.md` still apply: commands are in
> `m1.md` §5, the 16-row table in §9. This file adds the triggers, how to read the rows, the mislabels, the
> answer and the scorecard.
>
> ⛔ **A verify step: zero mutations.** No create, patch, grant, revoke or re-point. The triggers below are
> calls, not changes, and they are required.

## 1. The gate — both hold before any claim

1. **You caused a real action this session** — a legitimate read and a promo attempt. **No trigger, no
   claim:** say so and name the call you would need.
2. **"Proof", "proves", "proven", "verified" as affirmative claims** only once the log rows are written in
   this turn's entry in `m1_step5.txt` and the answer names what they show. Never "cryptographic proof",
   "100 % accountability", "fully verified". `not verified` is always allowed.

**Nothing relevant came back** (no entries, or only rows that name none of your triggers)? The only output
is **"no evidence recorded"**, plus what you triggered and when, the query you ran, and what is needed next
(wait longer and re-run · re-trigger). Mark the row `not verified`. Rows that do not name your workloads are
no evidence, not weak evidence.

## 2. The triggers — in this order, each with its UTC time

Take `date -u +%Y-%m-%dT%H:%M:%SZ` before each, and keep every reply in the file.

1. **Legitimate read** — the A2A `message:stream` call to the personalization agent (§5), with a question
   that needs customer records. **Never the store portal:** it runs as the default compute account, so its
   reads name the portal, and its personalization card is composed by the portal itself, naming the old
   login. Read the reply in `artifactUpdate.artifact.parts[].text`.
2. **The promo attempt** — `curl -sS -X POST "<PROMO_URL>/run-campaign"` (URL from `describe`). Expect HTTP
   200 with `campaign_status: launched` and `records_analyzed: 0`: the app swallows the refusal and reports
   success. That reply is a self-report; the log is the record.
3. **Price Match still answers** — one `:streamQuery` call to the Price Match Agent (§5) with a price-match
   question. Quote its reply in the file. It is §9's 16th row; Price Match never used the shared login, and
   this shows the step left it working.
4. **Wait, and state it** — data-access entries arrive a few minutes late. Wait at least 3 minutes, then
   query; empty → wait again and re-run once. **Write the wait into the answer with its duration** (*"waited
   4 minutes; re-ran at 15:57 UTC"*). A wait you did not state is a wait you did not take.

## 3. The queries — both, exactly as `m1.md` §5 gives them

- **Successful reads:** the `tableDataRead` query (`bigquery_dataset`, `customer_data`).
- **The denial:** the `bigquery_project` / `JobService.InsertJob` / `status.code=7` query filtered to the
  promo login. A denial never reaches the dataset, so it never appears in the first query.
- Use the compact view with **both** principal fields and the permission column. If you broaden a query,
  show the narrow one and its empty result first.

## 4. Reading the rows

- **Which field names the actor.** An Agent Identity read carries the badge in
  `protoPayload.authenticationInfo.principalSubject` (the full `principal://…`), and **`principalEmail` is
  blank on that row — the expected post-flip shape**, not a missing entry or an anonymous read; do not
  re-trigger for a "proper" one. A plain service account (the promo login) is in `principalEmail`.
- **`effectiveIdentity`** is not a log field: it lives on the Agent Runtime resource, without the scheme.
  The registry record carries the same identity in its `RuntimeIdentity` attribute, with `principal://`.
  If you tie them together, label where each came from.
- **Name the gate the denial came from:** `authorizationInfo[].permission` = `bigquery.jobs.create`,
  `resourceName` = a job in the project. The promo login holds no right to run a query here, so it was
  stopped at job creation and the customer dataset's access list was never consulted. Say *"refused
  permission to run a query in this project"*, never *"the read of the customer table was refused"*.
- **Match by time.** The promo container tries a read about 15 s after every boot, so a denial under the
  new login already sits right after the Step 3 re-point. The row that answers this step is the one just
  after **your** trigger's UTC time. If times cannot separate them, say so.
- **A post-change read that still succeeds:** check who acted. The default compute account means a caller
  sent no token and the tool layer used its own owner-level account — a finding to report
  (*"a caller that sends no token bypasses per-agent access"*), never something to fix here.

## 5. Don't mislabel

- The app's "launched, 0 records" is not a 403, and not a success; the log entry is the record.
- A missing log entry is not a denial: wait, re-run once, then `not verified`.
- A `PredictionService.GenerateContent` entry is a model call, not a database read.
- An app's own stdout is a self-report, not the platform's record.
- The store portal's personalization card is never evidence that personalization works.
- Never write a customer name, ID, count or timestamp your output did not contain.
- Price Match and Markdown Strategy hold broad data access of their own; never say they have none.

## 6. The answer

- **Bold line first**, answering *who did what* in the leader's words; no progress messages before it.
- `### Why this matters`: what the rows show, in plain words. On screen, a principal is whose badge it is
  (*the personalization agent's own badge*, *the promo agent's new login*); no `principal://`, email or
  `roles/` (`m1.md` §2 Close check 5). Verbatim values are in the file.
- **The picture** (REQUIRED, `../SKILL.md` §3b) draws only what this turn's log rows show: the
  personalization agent's own badge reading customer data, labelled with the read's UTC time; the promo
  agent's new login with an arrow labelled *refused* and the denial's UTC time (you caused and observed it
  this turn); Price Match *answered* only if its reply is in the file. Never a pass, tick, "verified", a
  count of checks or the coverage line: the verdict lives in the table.
- `### What I checked`: **one coverage line, never a table** — *"15 of the 16 checks are evidenced live; 1 is
  not verified."* Both numbers counted off the rows you wrote in the file, and both present there.
- **The table** (§9 order, all 16 rows, `Check | How I verified | Result`) goes into this turn's entry in
  `m1_step5.txt` after OUTPUTS. A table with gaps is the step working; never drop a row.
- `### Where the proof is` names `/config/Desktop/novasmart-evidence/m1/m1_step5.txt`, its command count and
  failures, in the `../SKILL.md` §3g form.

## 7. The scorecard — every time, pass or fail

Run the `../SKILL.md` §4 command with its absolute path:

```bash
python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/update_scorecard.py \
  --mission M1 --status <PASS or FAIL> --checks-json '[{"name":"<§9 check>","proof":"<value quoted this turn>"}]'
```

- `--status` is the **measured verdict**: `PASS` only when all 16 rows are evidenced live and every one
  shows the control holding; `FAIL` when any row shows it not holding or stands `not verified`. It must agree
  with the coverage line. Never a constant.
- `--checks-json`: one object per §9 row, `name` = the check, `proof` = the value from the file.
- It writes `governance_scorecard.html` under `/config/Desktop/novasmart-scorecard/`. Record the command and
  its output in the entry; running it is not an estate mutation.
- **PASS:** one plain line of achievement in the prose (each workload signs in as itself, and the promo
  agent's access to customer data is gone). **FAIL:** no achievement line; name the failing row and the step
  to return to — identity or dataset scope → Step 3, a remaining promo path → Step 4, an entry that never
  arrived → wait and re-run this step. Do not re-run the fix here to turn a row green.
- **Always** print: `📊 **Live Scorecard:** [http://localhost:8088/governance_scorecard.html](http://localhost:8088/governance_scorecard.html)`

## 8. How to close

Shape: every read of customer data now names one agent, and that can go in front of anyone who asks — but it
covers what each agent did itself and says nothing about what one agent can ask another to do on its behalf.
`Worth sitting with` asks what the leader would want an auditor to reconstruct, or what would have to be
true before this estate carried something that mattered more than promotional copy. **If the denial was not
observed, the close says so**, alongside the reads that were. Name the category still uncovered, never the
next module's finding. Run the Close check (`m1.md` §2).
