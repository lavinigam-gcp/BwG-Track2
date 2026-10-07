# M1 Step 3 — Give each agent its own login · the procedure

> Read this when the leader reaches **M1 Step 3**. `../SKILL.md` and `m1.md` still apply: commands are in
> `m1.md` §5, the allowlist and re-point rules in §6·5–§6·7, gotchas in §8. This file adds the order, the
> evidence, the disclosure list, the picture and the close.
>
> ⛔ **Two identity moves, then one removal — in that order.** Every sub-step is its own say → do → re-read
> → evidence → change record, appended to `m1/m1_step3.txt` in the order you did them. Never bundled.

## 1. The mechanism — say it this way

- **The personalization agent runs on Agent Runtime**, so it can carry an **Agent Identity**: a badge the
  platform issues to that one agent, with no service account and no key. Price Match and Markdown Strategy
  already have one. Moving the personalization agent onto its own is the heart of this step.
- **The promo agent runs on Cloud Run**, which cannot hold one. It gets **a new service account of its
  own**. Say *"same principle — one workload, one identity — different plumbing"*, and never claim the promo
  agent got an Agent Identity.

## 2. Sub-step 1 · Move the personalization agent — two moves

**(a) Flip.** Resolve the agent from the live Agent Runtime listing (match `displayName`, read `name` from the
same record). Send the PATCH in `m1.md` §5 with both fields in the update mask. It returns a long-running
operation: poll it to `done` (about 45 s), then GET the agent and read `spec.identityType` and
`spec.effectiveIdentity`. A read while the operation runs returns the old value. **Poll in the
foreground:** each poll is one short command (`sleep 10`, then one GET of the operation) run with
`WaitMsBeforeAsync` 15000, repeated until `"done": true`; no timer, no background loop. (A run that sent
the poll to the background had its raw `<SYSTEM_MESSAGE>` completion notice shown in the chat.)

- **Refused or failed?** Record the response verbatim and report it in the §6·4 shape. Do not redeploy.
  Take the **fallback** in `m1.md` §5: the agent stays on the shared login, which gets project `jobUser` and
  dataset `READER` in place of `bigquery.admin` (add `READER`, confirm a read, then remove the admin role).
  The answer says the flip failed and that this was done instead; sub-step 4 then does not apply.

**(b) Re-key — do not skip, do not defer.** The flip voids every grant the agent held through the shared
login. Prepend `principal://` to `spec.effectiveIdentity` (never assemble it), then:
1. project-level `roles/bigquery.jobUser` on that member (lets a query run; no data);
2. dataset `READER` on `customer_data` for that member, via `bq show` → edit → diff → `bq update --source`
   → re-read (`GRANT … ON SCHEMA` does not take a `principal://` member).

Those two and nothing else (§6·5 iii). The tool layer is public and the platform already gives Agent
Runtime agents model and logging access, so no tool, invoker or telemetry role is part of this.

**(c) Show a real read.** Wait 60–120 s after the grants, then make the agent use its database tool with the
A2A `message:stream` call (§5) and quote its reply in the file with the UTC time sent. A greeting is not a
read. **Do not predict what comes back** — record it. A refusal naming a permission means a grant has not
landed or is missing: wait once more and retry before you judge it. If it still fails, report what came
back; never add a role to make it pass.

## 3. Sub-step 2 · A new login for the promo agent

1. **Create** `promo-agent-sa` (§5). Refused (`iam.serviceAccounts.create` → `PERMISSION_DENIED`) → stop the
   split and take `m1.md` §6·7: report it blocked, name the permission, mark it `not verified`, carry on to
   sub-step 4 and Step 4. **Never** reuse, rename or re-point an existing account — `test-agent-caller`
   least of all.
2. **One role.** Read the seed bucket's name from the container command in the promo service's
   `describe --format=yaml` (the `gcloud storage cp gs://…/promo_agent_service.zip` line). Grant
   `promo-agent-sa` **only** `roles/storage.objectViewer` **on that bucket** (§5). That is all the container
   needs: its stdout logs need no role, its spans go to the console, the tool layer is public, and
   `/run-campaign` makes no model call. Never `aiplatform.user`, `run.invoker`, `logging.logWriter`,
   `telemetry.writer` or any project-level role — a past run mirrored five project roles from the shared
   login, including the project-wide `aiplatform.user` a later module counts.
3. **Wait 60–120 s** for the grant to propagate (refused at 20 s, allowed at 90 s here).

## 4. Sub-step 3 · Re-point the promo service

1. `gcloud run services update … --service-account=promo-agent-sa@…` (§5) — the only Cloud Run re-point M1
   permits (§6·6). It needs `actAs` on the new account, which your project-level `iam.serviceAccountUser`
   already covers. ⛔ **Never grant yourself anything on the new account** (no `serviceAccountUser`, no
   `add-iam-policy-binding` naming `antigravity-sa`) — that is a self-grant, before or after a refusal.
   Refused → wait 60–120 s (a new account propagates), retry once, then §6.
2. **Re-read `describe`:** `serviceAccountName` is the new login, the latest revision is ready, and
   `status.traffic` shows **100%** on it. A revision at 0% changed nothing.
3. **Make it answer:** `curl -sS -X POST "<PROMO_URL>/run-campaign"`. Expect HTTP 200 with
   `campaign_status` in the body; `records_analyzed: 0` is the expected result now that it has no data path.
   Record it; say nothing yet about a refusal — that is Step 5's.
4. **If the revision fails to start:** inside the first minutes after the grant it is propagation — wait,
   retry once. Still failing → open the revision's logs (`gcloud logging read` on that revision), quote what
   failed, add **the single missing role** on the narrowest resource, and disclose it as an addition beyond
   the plan. Never cite logs you did not open; never grant anything else to "fix" it.

**Note:** about 15 s after the new revision boots, the container tries a customer read itself, and BigQuery
refuses it. That entry is not Step 5's evidence; leave it for Step 5 to tell apart by time.

## 5. Sub-step 4 · Right-size the shared login — last

Only after **both** moves are re-read — the personalization agent on its own badge with a real read behind
it, the promo service on `promo-agent-sa` at 100% — nothing signs in as `novasmart-customer-sa`. Then:

1. Remove its project-level `roles/bigquery.admin` (§5).
2. **Add nothing to it.** No `jobUser`, no dataset entry: a grant to an account nobody uses is a change with
   no job, and customer-data read now lives only on the personalization agent's own badge.
3. Re-read the project policy filtered to it, and write the before and after role lists in the file. Its
   other roles stay (§3); they are not this step's.

Say it plainly: the shared login has not been narrowed, it has been **vacated** — no workload signs in with
it, and it no longer holds anything on customer data.

If a move did not land (flip refused, account create blocked), the shared login still has a user: do not
remove `bigquery.admin` from under a live workload unless the fallback in §2 gave that workload its
replacement read first. Say what you did and what you left.

## 6. Disclosure — every grant and removal, in the answer, one line each

The file holds the full change record (what · resource · when (UTC) · undo), and every command, JSON reply
and polling line — none of that goes in the answer. **The answer still carries one
plain line per binding added or removed**, whoever the principal is, in plain words (no `roles/`, no
`principal://`, no email). Expected, and nothing else:

- the personalization agent's own badge: allowed to run queries in the project;
- the personalization agent's own badge: read-only on the customer dataset;
- the new promo login: read-only on the stored files in the seed bucket;
- the shared login: its power to read, change and delete every dataset in the project, removed.

Plus the identity flip and the re-point as changes of identity, and **anything you granted to get past a
failure**, flagged as beyond the plan. A grant outside §6·5 is a finding about your own run: say it was out
of scope and give the undo in the file.

## 7. The picture — IDENTITY, before and after

The AFTER half exists only once you have re-read both workloads live this turn.

- **BEFORE** (read at the start of this step): the two workloads converging on the one shared login.
- **AFTER** (re-read just now): the personalization agent against *its own badge*, the promo agent against
  *its own new login*, and the shared login with **nobody** on it — that third statement is the finding.
- A line on the image: *"who signs in as what — identity only, not access"*. Reach is Step 4's picture.
- Caption: both workloads' runtime identity, re-read just now.
- Labels say whose badge it is, never the raw identity string. Price Match and Markdown Strategy are absent:
  not touched, not re-read. If the account create was blocked, show BEFORE alone and say why in one line.

## 8. Don't mislabel

- Removing `bigquery.admin` from the shared login is not the promo agent's cut-off; Step 4 shows that.
- The re-key is not a new privilege: it restores what the flip removed, narrowed to one dataset, read-only.
- Never say the promo agent is "blocked" or "denied" — nothing has been refused that you caused and read.
- Never touch Price Match, Markdown Strategy, `test-agent-caller`, `antigravity-sa` or the tool layer.
- Never claim the personalization agent "works" from a greeting, or from the store portal's card.

## 9. How to close

Shape: what you have bought is **attribution**, and attribution is not approval — from here every read
names one agent, which is the first time anyone can see what each holds, and tracing an access does not
make it appropriate. `Worth sitting with` asks what NovaSmart's standing rule should be for access that is
now visible, or what an auditor should be able to see. Then run the Close check (`m1.md` §2): no
*marketing*, *customer database*, *take away*, *revoke*, *remove* or *cut off*.
