# The data palette — every read this app is allowed to make

This is the operational core of the build. **Every command below was recorded as actually run in this
lab, or is marked as not yet proven.** Nothing here is invented, and you must not invent an addition.

## 0. How to read this

### 0.1 The confidence marks — carry them into the app

| Mark | Means | What the app does with it |
| :-- | :-- | :-- |
| **VERIFIED** | This exact command was run in this lab and worked, usually with a date or a measured outcome | Build a panel on it |
| **LIKELY** | The resource is provably deployed and the surface is standard, but no run of this read is recorded | Run it once first. If it fails, the panel says `not read` and names the command |
| **UNCERTAIN** | Something in the evidence is contradictory, or it turns on a permission nobody confirmed | Probe it before you promise it. Never quote a figure from a file instead |

⛔ **A confidence mark is not decoration.** If you build a panel on a LIKELY read and it 403s, the panel
renders `not read` with the error in it — it never falls back to a number you found written down.

### 0.2 Whose credentials — the one framing fact

The app shells out and inherits the VM's ambient credentials: **`antigravity-sa`**, the login `agy`
already runs as. No key is created, no key file is written, no token goes anywhere near the page.

**That identity deliberately cannot read customer rows.** Its BigQuery role withholds
`bigquery.tables.getData`. So the app can show the **shape** of customer data — table name, column
names, row count, which columns a logged read touched — and can never show a value. **The PII fence and
the authentication story are the same fact, and saying that on the page is the best line in the whole
activity.**

**The app adds nothing to that identity.** It grants no role, creates no principal, enables no API.

### 0.3 At a glance

| # | Source | Confidence |
| :-- | :-- | :-- |
| R1 | Agent registry — regional services listing | **VERIFIED** |
| R2 | Agent registry — global agents listing | **VERIFIED** |
| R3 | Registry REST fallback (v1alpha) | **VERIFIED** as the tested fallback |
| R4 | `reasoningEngines` listing — what is actually deployed | **VERIFIED** |
| R5 | One engine's identity (`spec.effectiveIdentity`, `spec.identityType`) | **VERIFIED** |
| R6 | Cloud Run services and their runtime service accounts | **VERIFIED** |
| R7 | Cloud Run revision history — the one recoverable config before-state | **LIKELY** — probe |
| R8 | Project IAM filtered to one principal | **VERIFIED** |
| R9 | Full project IAM policy | **VERIFIED** |
| R10 | Dataset access list | **VERIFIED** |
| R11 | Table shape — schema and row count | **UNCERTAIN** — probe |
| R12 | ⭐ The mandatory `tableDataRead` audit query | **VERIFIED** — exact and mandatory |
| R13 | Denied reads, `status.code=7` | **VERIFIED** |
| R14 | Pre-M1 rows, split client-side on the change time | **LIKELY** |
| R15 | The provisioning-row filter | **VERIFIED** |
| T1 | Trigger — A2A `message:stream` to the Customer Personalization Agent | **VERIFIED live** |
| T2 | Trigger — promo agent `/query`, **status code only** | **LIKELY** |
| T3 | ⛔ The store portal | **BANNED** — §4.3 |

Set `P="$(gcloud config get-value project)"` once and reuse it. Resolve every ID from a live listing.

### 0.4 Every capture is a receipt — command, time, exit status, or it is not evidence

A file in `evidence/` is not true because it is on disk and named after a source in this table. **It is
true because someone else can re-run the thing that made it.** The learner will ask whether these files
are real reads or answers you already knew — and *"the values are correct"* is not an answer to that
question. A receipt is.

**So every capture carries the payload and, beside it, four facts:**

| Field | What it holds | Why it is not optional |
| :-- | :-- | :-- |
| `source` | the palette ID this read came from — `R1`, `R12`, `T2` | Ties the file back to a command in this document, so nobody has to guess which read it was |
| `command` | the **exact** command that ran, as it ran — same flags, same order, **fully expanded**, no tidying, nothing reconstructed afterwards | It is the only thing that makes the file reproducible. ⚠️ **Expanded matters:** a command still carrying `$P` or `<ENGINE_NAME>` cannot be re-run by anyone but you, so it proves nothing |
| `ran_utc` | the UTC time it was executed, to the second — `2026-08-19T09:41:12Z` | Separates a read from this session from one carried over, and it is what pairs a trigger with the audit row it caused |
| `exit_status` | the process exit code — plus the stderr text whenever it is non-zero | It is the difference between *nothing came back* and *it never ran* |

⛔ **A capture missing `command`, `ran_utc` or `exit_status` is not evidence, and no panel may be built
on it.** Run the read again rather than patching the file. A panel whose capture has no receipt renders
`not read`, exactly like a read that failed — from the outside the two are indistinguishable, and that is
the point.

*(Use those four names. If your app already labels them differently, that is fine — but use **one** set
of names across every capture in the folder, so a learner checking two files does not have to learn two
formats. What is banned is a capture that is missing one of the four facts.)*

**Empty is a result, and it gets a file.** A source that returned nothing is written out as an empty
payload **with its command, its time and its exit status beside it**, like any other capture. ⛔ **Never
omit the file.** An absent file and an empty result look identical on disk and mean opposite things: one
says *we looked and there was nothing there*, the other says *nobody looked*. They read differently on
the page too — an empty capture says *"no rows in this window"* (§3, R12); a source with no file at all
says `not read`.

**A read that FAILED is captured with its real error.** Non-zero exit status, and the message the command
actually printed — the 403, the `PERMISSION_DENIED`, the quota message — verbatim, not summarised. ⛔
**Never write a failed read out as an empty list.** That silently converts a permission problem into a
finding about the estate, and it is the most misleading thing this pipeline is capable of: *"no denied
reads recorded"* and *"I was not allowed to look"* are opposite claims, and one empty array can be read
as either.

⛔ **No sample data, no seed data, no placeholder, no fixture, no fallback — anywhere in the pipeline.**
Not in the sweep, not in `app.py`, not in a file kept beside it, not "just so the panel renders while I
finish the layout". **If a read did not happen, the panel says `not read` and names the command that
would settle it.** That is the entire fallback, and there is no other.

⚠️ **A file you wrote from memory is a fabrication even when every value in it is correct.** The values
are not what is being tested — the connection is. A capture that was typed rather than executed has no
command that produced it and no time it ran, so there is nothing to re-run and nothing to compare
against, and the page standing on it is narrating. **Run the command; keep what it printed.** The learner
can check this for themselves in one paste — `local-run.md` §4.1, and you hand them that check yourself.

---

## 1. Inventory and identity

### R1 · R2 — the registry, **both locations** · VERIFIED

```
gcloud agent-registry services list --location=us-central1 --format=json
gcloud agent-registry agents   list --location=global      --format=json
```

**Returns.** Catalog entries with display name, owner and risk tier; the global listing also carries
platform built-ins.

**What the app does with it.** The "catalogued" column, with **each row labelled with which listing it
came from**.

- ⚠️ `--location` is **mandatory**, and **two locations are in play**. A single-location listing is not
  the estate, and **empty from one location is not evidence of absence**.
- ⚠️ **There is no registered/unregistered field.** The diff is computed client-side by joining the
  registry listings against R4 and R6 **by display name**. ⛔ **Never diff by count** — six and six hides
  the finding.
- ⛔ **Platform built-ins are not findings.** Name them plainly, never as shadow agents.
- ⛔ **Re-read the listing; never render a create response as the catalog state.**
- The registry API may ship disabled in a fresh project.

### R3 — registry REST fallback · VERIFIED as the tested fallback

```
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://agentregistry.googleapis.com/v1alpha/projects/$P/locations/$LOC/agents"
```

Use it **only** if the CLI 403s after the API is confirmed on.

### R4 — what is actually deployed · VERIFIED

```
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-central1-aiplatform.googleapis.com/v1beta1/projects/$P/locations/us-central1/reasoningEngines"
```

**Returns.** `reasoningEngines[]` with `name`, `displayName`, `spec`.

**What the app does with it.** The "what is actually running" column, and the source for every engine ID
the app later uses — matched on `displayName`, read out of the same record.

⛔ **There is no `gcloud ai reasoning-engines` group** in GA, beta or alpha. REST is the only surface.

### R5 — a managed agent's own identity · VERIFIED

```
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-central1-aiplatform.googleapis.com/v1beta1/<ENGINE_NAME>"
```

Read `spec.effectiveIdentity` (the SPIFFE value, stored **without** the `principal://` scheme) and
`spec.identityType`.

⛔ **Never construct a principal.** Read it, then match it against what the audit log prints.

### R6 — Cloud Run workloads and their runtime identities · VERIFIED

```
gcloud run services list \
  --format="table(metadata.name, spec.template.spec.serviceAccountName)"
gcloud run services describe promo-agent-shadow --region=us-central1 --format=yaml
```

**Returns.** Service names, `spec.template.spec.serviceAccountName`, `status.url`, traffic split.

⛔ **The MCP tool service, the store portal and any browser or VM service are infrastructure, not
agents.** They may appear labelled as infrastructure; rendering them as unregistered agents is the
cheapest way for this app to invent four false positives.

### R7 — Cloud Run revision history · LIKELY, probe it

```
gcloud run revisions list --service=promo-agent-shadow --region=us-central1 --format=json
gcloud run revisions describe <OLDEST_REVISION> --region=us-central1 --format=yaml
```

If the pre-mission revision survives with its old `serviceAccountName`, this is a genuine platform-side
"before" for half of M1. **If it 403s or the revision is gone, the panel renders `not recorded`** — it
never falls back to prose.

---

## 2. Reach — who can get to the data

### R8 — project IAM, filtered to one principal · VERIFIED

```
gcloud projects get-iam-policy "$P" --flatten="bindings[].members" \
  --filter="bindings.members:novasmart-customer-sa" --format="table(bindings.role)"
```

Run the same read for the promo agent's own service account and for the personalization agent's
`principal://…` value from R5. **This is the "what the shared login can still do" panel.**

### R9 — the full project IAM policy · VERIFIED

```
gcloud projects get-iam-policy "$P" --flatten="bindings[].members" \
  --format="value(bindings.role,bindings.members)"
```

Only if the brief needs the wider picture. ⚠️ **Dedupe before describing roles** — describing one role
per binding rather than per unique role runs long enough to be killed.

### R10 — the dataset access list · VERIFIED

```
bq show --format=prettyjson "${P}:customer_data"
```

**Returns.** The `access[]` array — five or more entries, including the project-level special groups.

⛔ **Never write "only X" over this array.** Enumerate it, or say exactly what you skipped. Writing "only
the personalization agent can reach it" over a five-entry array happened three times in one real run.

### R11 — the table's shape · UNCERTAIN, probe it

```
bq show --format=prettyjson "${P}:customer_data.customers"
```

Schema and row count. **The safest PII-free headline number in the lab, if it resolves.**

⛔ **If it 403s the panel says `not read` and names the command.** It never falls back to a figure quoted
in a reference file, however confidently that file states it.

---

## 3. The spine — the audit log

### R12 — the mandatory `tableDataRead` query · VERIFIED, exact and mandatory

This is **one exact query, not a family**. Use it as written.

```
gcloud logging read '
  logName="projects/'"$P"'/logs/cloudaudit.googleapis.com%2Fdata_access"
  AND resource.type="bigquery_dataset"
  AND resource.labels.dataset_id="customer_data"
  AND protoPayload.metadata.tableDataRead:*
' --limit=50 --freshness=1d --format=json
```

**Fields inside an entry:** `timestamp` · `protoPayload.authenticationInfo.principalEmail` ·
`protoPayload.authenticationInfo.principalSubject` · `protoPayload.resourceName` ·
`protoPayload.metadata.tableDataRead.fields` (**column names only, never values — safe to render**).

**What the app does with it.** Everything. This is S1 and S2. Split the rows at the identity-change time:
rows before it name the shared login, rows after name one workload each.

- ⚠️ **A blank `principalEmail` beside a populated `principalSubject` is the EXPECTED shape after the
  identity flip** — measured 5/5. Read the subject. ⛔ Never render that row as anonymous.
- ⚠️ **These entries lag minutes.** The panel states its window and its "as of" time and says it is
  waiting. ⛔ An empty result is *"no rows in the last 60 minutes"*, never *"no reads happened"*.
- ⛔ **Known-bad recipe: `resource.type="bigquery_resource"` with a table-scoped `resourceName` returns
  zero rows here** — BigQuery records the job, not the table, on that resource type.
- ⛔ **A `PredictionService.GenerateContent` entry is a model-inference event and must never be coloured
  as a database read.** An app that paints all `aiplatform` entries as data access commits exactly the
  sin it was built to expose.

### R13 — the denial variant · VERIFIED

Same query, **one clause apart**: `protoPayload.metadata.tableDataRead:*` **out**,
`protoPayload.status.code=7` **in**.

```
gcloud logging read '
  logName="projects/'"$P"'/logs/cloudaudit.googleapis.com%2Fdata_access"
  AND resource.type="bigquery_dataset"
  AND resource.labels.dataset_id="customer_data"
  AND protoPayload.status.code=7
' --limit=50 --freshness=1d --format=json
```

`status.code=7` is `PERMISSION_DENIED`. **Quote `authorizationInfo[].permission` and `resourceName`
beside it**, so the page names *which gate fired* rather than saying "blocked".

⛔ **Absent after one retry → `not verified`.** Never a tick. Check the `activity` log before concluding.

### R14 — the pre-mission rows · LIKELY

R12 with a `timestamp < "<CHANGE_UTC>"` clause, or split R12's output client-side on the change time.
This is the **only honest before/after available at this point in the lab**, and it happens to be the
exact one the mission was about.

⛔ **If it comes back empty the panel says "no pre-split reads recorded in this window"** — it does not
imply there were none.

### R15 — the provisioning-row filter · VERIFIED

Client-side on R12's output. The lab's own setup account appears in **every** run:

- principal shaped `qwiklabs-gcp-<id>@qwiklabs-gcp-<id>.iam.gserviceaccount.com`
- `reason: JOB`, and a `jobName` containing `script_job_`

**Filter it out, or label it `lab setup, housekeeping, not a finding`.** Rendering it as a finding is the
cheapest false positive in this lab.

---

## 4. Causing a real read — the triggers

*No trigger, no claim.* The app must own the read, not borrow one from history.

### T1 — the legitimate read, over A2A · VERIFIED live

```
ENGINE=projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<CPA_ID>
curl -sS -N -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1beta1/${ENGINE}/a2a/v1/message:stream" \
  -d '{"request":{"messageId":"demo-'"$(date +%s)"'","role":"ROLE_USER",
       "content":[{"text":"<ask for something that needs customer records>"}]}}'
```

- **Resolve `<CPA_ID>` from R4 by `displayName`.** ⛔ Never hardcode an engine ID.
- **The answer is only in `artifactUpdate.artifact.parts[].text`.** `status` and `history` carry your own
  request back at you.
- ⛔ **`message:send` echoes your input; `tasks/get` returns 501.** Use `message:stream`, with `-N`.
- **Record the UTC send time.** That is what makes the audit row yours.
- ⛔ **Do not decide in advance what comes back.** A genuine read and a fluent invention read identically.
  The audit row settles it, never the sentence the agent hands you.

### T2 — the attempt that should now be refused · LIKELY

```
curl -sS -o /dev/null -w '%{http_code}' -X POST "<PROMO_URL>/query" \
  -H 'Content-Type: application/json' -d '{"prompt":"<a campaign ask>"}'
```

URL from R6. 🔴 **The status code is the ONLY thing you may keep.**

⛔ **Discard the body. Never render it, never log it, never write it to `evidence/`.** That endpoint
embeds real customer personal data in its reply. `-o /dev/null` is not decoration; it is the fence.

The verdict comes from **R13**, the audit log — never from the HTTP status alone.

⚠️ **The warmup over-count.** The promo service runs the same customer query about fifteen seconds after
any container boot. A cold trigger can produce **two** indistinguishable events, only one of which the
learner caused. ⛔ **The app must never print "reads I triggered: N."** It prints rows with timestamps and
lets the learner match them against the recorded send times.

### T3 — ⛔ BANNED: the shipped store portal

**Do not build any trigger, panel or verification on the store portal — its chat endpoint, its buttons,
or any of its APIs.** Two independent reasons, both measured:

1. **It fabricates.** When the real backend reply is empty or shorter than eighty characters, the web
   tier **invents** a complete, confident personalization answer — including the sentence *"Successfully
   queried `customer_data.customers`"* and the shared login's own name. **A blocked call renders there as
   a success.** An app that verifies anything against that response body is measuring a lie.
2. **It runs as the project's default compute account, which this project binds to owner.** A read it
   causes is attributed to the portal, so it proves nothing about the agent's own permissions.

Anything built on the portal measures the web tier, not the estate.

---

## 5. Do not promise what this project does not have

| Tempting | Why not |
| :-- | :-- |
| Which customer's record was read | No field in a `tableDataRead` entry names a row. The question cannot be answered from this log |
| Customer rows, anywhere | Blocked by design, and the four side doors — the seed SQL in the bucket, the portal's customer API, the unauthenticated tool server that falls back to owner credentials, and the promo agent's reply bodies — are all banned outright |
| A Model Armor verdict read from Cloud Logging | Measured absent on a confirmed block. An empty panel reads as *no attacks*, which is the exact false all-clear this lab teaches against |
| The deployed monitoring dashboard | Very likely unreadable by this identity — and it is the anti-pattern, not a source |
| Alerting | Nothing is configured anywhere in this estate. *Recorded* and *someone was told* are different things, and that gap is worth a panel — building an alert is not |
