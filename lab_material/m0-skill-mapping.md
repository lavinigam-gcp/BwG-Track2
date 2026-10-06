# M0 · See Everything — Skill Mapping

*Read this after you finish Module 0. It explains what each prompt was for, so it gives away the module's findings.*

Every number here comes from one test run on October 3, 2026 (agy 1.1.19, Gemini 3.8 Flash with low thinking): 9 prompts, 70 tool calls, about 27 minutes. No project resource or setting changed, though Step 4 sent test requests to NovaSmart's store portal, an application, and agy also called the promo agent's campaign endpoint directly (see below). Your run will differ.

## What you learned

<!-- FIGURE:S0_01 BEGIN -->

![One prompt, start to finish: a swimlane with five lanes: You, agy, Skill files, Google Cloud, Evidence file. Your plain-English question goes to agy, which sees the skill name and description, reads skill files when needed, runs fixed, tested commands on Google Cloud, and writes m0_stepN.txt first; an arrow then rises to the answer, built only from this file. A strip below reads: Model sign-in: Google account or API key; Cloud commands run as antigravity-sa.](images/S0_01_one_turn_swimlane.webp)

<!-- FIGURE:S0_01 END -->

The prompts are a leader's questions, not the technique. The technique is what the skill turned each one into: fixed, tested commands, an evidence entry holding those commands and their raw output, and an answer built only from that entry.

**agy** is the Antigravity CLI, an agent you run in a terminal. An **agent skill** is a folder with a `SKILL.md` file of instructions ([Agent skills](https://antigravity.google/docs/skills)). When a conversation starts, agy sees only each skill's name and description; when a question matches, it reads the full file. In the test run, agy's first two tool calls opened `SKILL.md` and `references/m0.md`, the Module 0 map that `SKILL.md` points to.

Both files are kept under about 44 KB. In the lab team's testing, agy's file reader returned at most about 46 KB or 800 lines per call, and larger versions were cut off before the Step 4 section.

## Does the skill know the answers? Yes.

<!-- FIGURE:S0_02 BEGIN -->

![When each fact may be said: four columns. Step 1, Ready?: tools and APIs. Step 2, Catalog: Agent Registry; may now say 6 distinct agents (gray card). Step 3, Running: Agent Runtime and Cloud Run; may now say shadow agent found (red card). Step 4, Who read: Cloud Audit Logs; may now say shared login found (amber card). Each fact card has an open padlock. An amber bar under Steps 2 and 3 reads: Shared login: already in the data, held back, and points up into Step 4. A band below reads: The live result wins.](images/S0_02_when_each_fact_unlocks.webp)

<!-- FIGURE:S0_02 END -->

`references/m0.md` lists what the module expects to find, so agy knows where to look and can sanity-check what a command returns. In the picture, gray is a plain fact, red is the visibility gap and amber is the shared login. That section of the file opens like this:

> **DO NOT RECITE.** Orientation, to know where to look and sanity-check what a command returns. NONE of it may be stated before the step whose own command reveals it […]. The live result wins.

Three rules keep the map from becoming a script:

- **Each fact waits for its step.** A table in the same file says what agy may report at each prompt and what it must not say yet. The shared login is already in the Step 2 catalog data; agy held it back until Step 4's own commands found it.
- **The live result wins.** If a command disagrees with the map, agy reports what the command returned.
- **Every value on screen must be in the evidence file**, so you can check the answer against raw output and rerun the commands.

The evidence file is still agy's own account. The section "What slipped", below, shows where it fell short.

## One step demonstrated: Step 4

<!-- FIGURE:S0_03 BEGIN -->

![Step 4: proving who read. Mark the time, trigger a real read, run the fixed log query, then a decision: row after the mark? Yes leads to Report: my request added a read. No leads to Resend promo once, fresh mark, then a second decision: row now? Yes leads to the same report box; No leads to Report earlier reads as earlier. Both report boxes lead to the amber box Who read = inference from hosting. Two red notes: No shared-login row: stop, say so; Portal reply is not proof. A gray tag joined to the earlier-reads box: This run: no new row.](images/S0_03_step4_flowchart.webp)

<!-- FIGURE:S0_03 END -->

For "Who's been reading our customer database?", the skill makes agy take a UTC time mark, send two requests to the store portal so the agents read customer data now, and run one log query exactly as written:

```bash
gcloud logging read '
  logName="projects/<PROJECT>/logs/cloudaudit.googleapis.com%2Fdata_access"
  AND resource.type="bigquery_dataset"
  AND resource.labels.dataset_id="customer_data"
  AND protoPayload.metadata.tableDataRead:*
' --limit=20 --freshness=1d --format=json
```

Only rows after the mark count as reads agy caused. agy then re-reads which login the promo agent and the Customer Personalization Agent sign in as, and names the reader only as an inference from where each one runs. A trimmed excerpt of the entry it saved in `m0_step4.txt`, showing one earlier log row:

```text
ENTRY 4 - M0 Step 4 - Who's reading customer data
[1] target: promo, status: HTTP 200
    target: customer, status: HTTP 200
    post-mark rows: 0
[2] "principalEmail": "novasmart-customer-sa@<PROJECT>.iam.gserviceaccount.com",
      "principalEmail": "service-<PROJECT_NUMBER>@serverless-robot-prod.iam.gserviceaccount.com"
    "fields": ["customer_id", "email", "lifetime_value", "loyalty_tier", "name"],
    "timestamp": "2026-10-02T22:34:10.839048Z"
(nothing changed in this step)
```

The first `principalEmail` is the shared login. The second, under `serviceAccountDelegationInfo`, is Cloud Run's service agent (Google's own account that acts for a login; in a log it names the runtime, not the agent), so this read came through Cloud Run. A shared-login row like this names a login and a runtime, never an agent.

agy's headline: "Customer data reads are recorded under a shared login (`novasmart-customer-sa`), which names no individual agent." It said its own requests added no new entry and that the reads it showed were earlier ones.

Why the rules mattered: the older `bigquery_resource` filter returns zero rows here, and a portal body keyed `message` instead of `prompt` gets HTTP 400 and causes no read. The portal's reply is not proof either: the promo reply claimed 20 customer profiles, but the mark showed no new row. The skill's explanation is BigQuery's cache, which writes no new read entry for a cached result.

## Key commands from the run

These and the rest are in your evidence files under COMMANDS, so you can paste and rerun them.

| Step | What it asks | Command |
|---|---|---|
| 1 | Region, from where NovaSmart runs | `gcloud run services list --filter="metadata.name:novasmart" --format="value(region)"` |
| 2 | Catalog, per location (then `global`; 4 + 3 entries made 6 distinct agents) | `gcloud agent-registry agents list --location=<REGION> --format=json` |
| 3 | Agent Runtime deployments (no `gcloud` commands) | `curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://<REGION>-aiplatform.googleapis.com/v1/projects/<PROJECT>/locations/<REGION>/reasoningEngines"` |
| 3 | Cloud Run services | `gcloud run services list` |
| 4 | Which login a workload uses | `gcloud run services describe <SERVICE> --region=<REGION> --format="value(spec.template.spec.serviceAccountName)"` |
| 7 | Show what you found (no cloud commands): the facts, then the page check | `python3 .agents/skills/novasmart-governance-lab/scripts/show_facts.py 0`, then `scripts/show_check.py <page>` |

## Who agy is, and which record to trust

<!-- FIGURE:S0_04 BEGIN -->

![Three records, three authors. m0_stepN.txt: written by the model; holds the commands and output agy chose to list; misses the direct promo call. Headless capture: holds every tool call, though output may be cut; misses what Google Cloud logged. Cloud Audit Logs: written by Google Cloud; holds changes always and reads if enabled; misses agy's M0 reads, by default, and which agent used the login.](images/S0_04_three_records.webp)

<!-- FIGURE:S0_04 END -->

**Two sign-ins.** agy signs in to Antigravity with a Google account or a Gemini API key ([Installation and auth](https://antigravity.google/docs/cli/install/)). The `gcloud`, `bq` and `curl` commands it runs use the machine's Google Cloud credentials: on the lab workstation, `antigravity-sa`, the service account (a login for a program rather than a person) attached to the workstation.

**The guardrails are instructions, not IAM.** The lab runs agy with every action auto-approved (the capture records the permission mode `always-proceed`). The skill calls this Turbo, the name of the [Permissions](https://antigravity.google/docs/permissions/) preset that runs terminal commands unrestricted. `antigravity-sa` holds broad roles because later modules make changes, among them project IAM admin, Cloud Run admin and Agent Platform admin. So in Module 0, "read-only" and "never grant yourself a role" are rules the model follows, not limits anything enforces.

**Three records.** [Cloud Audit Logs](https://docs.cloud.google.com/logging/docs/audit) always record changes, but reads only where Data Access logging is on, which by default covers [only some BigQuery services](https://docs.cloud.google.com/logging/docs/audit/configure-data-access). So agy's Module 0 reads leave no audit entry by default. The evidence file is written by the model. A [headless](https://antigravity.google/docs/cli/headless/) capture records every tool call with its arguments and output, though long output and file reads are shortened; the lab team captured this run that way. In the lab, agy's own working files, including its conversation logs, are under `/config/.gemini/antigravity-cli/brain/<conversation-id>/`.

Why that matters: the portal's reply put customer names and emails into agy's context. Beyond the recipe, agy also called the promo agent's campaign endpoint directly with its own credentials; that reply held customer names and emails too, and said a campaign had launched. The direct call is not in the evidence file; only the capture shows it.

## What slipped, and what it teaches

A skill is guidance that a model follows most of the time. Each item was checked against the capture.

| What slipped | Lesson |
|---|---|
| Step 4's entry left out two earlier rounds of portal requests (the skill allows one retry), extra log queries and the direct promo call, and listed as separate commands what ran inside one Python script. | An agent's own log is useful; check it against an independent capture. |
| The skill requires the number of log rows in the Step 4 answer. The answer gave none. | Required details slip. Check answers against a short list. |
| The Step 4 query also returned rows from earlier test runs, written under the Customer Personalization Agent's own identity rather than the shared login. agy did not mention them. | "The live result wins" works only if the model reports it. Read the raw output, not just the answer. |
| Step 2 printed full `urn:agent:projects-…` IDs. The skill's draft check searches for `projects/`, so it missed them. | Text checks are brittle. Test them on real output. |
| Step 3's close mentioned "what credentials it operates under", Step 4's topic. A closing question in Step 4's answer called one read "the promotional workload", stating the inference as fact. | Holding facts back leaks at the edges. |
| agy opened old entries and an M1 evidence file left by earlier test runs. Its new entries still came from live commands. | Start each review in a clean folder. |

## Use this at your company

| Situation | What you reuse | Basis |
|---|---|---|
| Quarterly agent inventory review | List both catalog locations, sweep both runtimes, match on `agentId` or runtime reference, and file the evidence entries as the review record | Grounded: Steps 2 and 3 |
| Incident: "who read this table?" | Swap the dataset in the Step 4 query. It only works if Data Access logging was already on, and a shared login gives you a login, not an agent | Grounded: Step 4 and the Data Access docs |
| Gate before a new agent ships | Check that it is in the catalog, read its login (`serviceAccountName` or `effectiveIdentity`), and confirm no other workload shares it | Scenario |
| Audit your own coding agent | Run it headless, keep the capture, and compare it with the agent's own report | Grounded: how this run was checked |

## Do it yourself

<!-- FIGURE:S0_05 BEGIN -->

![Do it yourself in six steps: install agy; read-only service account; skill folder in your workspace; allow-list only read commands; run headless, keep the capture; compare capture with evidence file. A band below reads: Turn on Data Access logs for key data.](images/S0_05_diy_setup_flow.webp)

<!-- FIGURE:S0_05 END -->

**Install** agy from [Installation and auth](https://antigravity.google/docs/cli/install/), plus the Google Cloud CLI (recent enough that `gcloud agent-registry --help` responds), `curl` and `jq`.

**A read-only login.** agy's commands act as whatever `gcloud` is signed in as. Create a service account with only these roles, point `gcloud` at it (for example with the `auth/impersonate_service_account` property of [`gcloud config set`](https://docs.cloud.google.com/sdk/gcloud/reference/config/set)), and check that a write fails before you start.

| Role | Covers |
|---|---|
| `roles/agentregistry.viewer` (Beta) | Listing catalog entries |
| `roles/aiplatform.viewer` | Reading Agent Runtime deployments; it also allows querying them, so not strictly read-only |
| `roles/run.viewer` | Listing services and the login each uses |
| `roles/logging.privateLogViewer` | Reading Data Access audit logs; basic Logs Viewer is not enough |
| `roles/serviceusage.serviceUsageViewer` | Listing enabled APIs |
| `roles/bigquery.metadataViewer` | `bq show`, granted on the dataset |

Step 4's portal trigger is an action, not a read; leave it out unless you own the application.

**The skill folder** goes in `<workspace-root>/.agents/skills/<skill-name>/`, or `~/.gemini/antigravity-cli/skills/<skill-name>/` for every workspace. Start agy from the workspace root.

**Permissions.** Use the Default or Request Review preset, never Turbo or `--dangerously-skip-permissions`. Under Default, commands run in a sandbox with no network, so a cloud command runs outside it and asks first unless a command rule allows it; Request Review asks before every command. Allow only the read commands the skill needs, in `~/.gemini/antigravity-cli/settings.json`. A command rule matches the command's first words literally, and a command containing `$(...)`, like the Agent Runtime call, must match a rule exactly.

```json
{
  "permissions": {
    "allow": [
      "command(gcloud agent-registry agents list)",
      "command(gcloud run services list)",
      "command(gcloud run services describe)",
      "command(gcloud logging read)",
      "command(bq show)"
    ]
  }
}
```

**An independent record.** Run each question headless, keep the capture next to the evidence file, and add `--continue` for follow-ups. In headless mode nobody can answer a prompt, so a command that would ask is skipped and the run prints a notice. With the allow-list above, Step 3's Agent Runtime call would be skipped unless you add an exact rule for it.

```bash
agy -p "What AI agents do we officially have?" --output-format stream-json > step2.ndjson
```

**Logging.** Turn on Data Access logs for data you must answer for, and for the services agy reads if you want its reads recorded too.

<!-- FIGURE:S0_06 BEGIN -->

![What to take from this skill. A blue panel, Reusable anywhere: evidence entry before answer; every value traceable to output; verified read-only commands; an error is never an empty result; never grant yourself a role. A gray panel, NovaSmart only: leader persona and layout; expected findings, held back per step; portal trigger and Step 7 formats.](images/S0_06_generic_vs_novasmart.webp)

<!-- FIGURE:S0_06 END -->

A starting `SKILL.md`, not a finished one:

```text
---
name: agent-estate-review
description: >-
  Read-only review of AI agents in one Google Cloud project: compare the Agent
  Registry catalog with Agent Runtime and Cloud Run, and report which logins read
  a BigQuery dataset. Use when asked what agents exist, what runs, or who read data.
---
# Agent estate review
1. Read-only: list, describe and log reads only. Never change IAM, even your own.
2. Write the evidence entry (COMMANDS, OUTPUTS, CHANGE RECORD) first; answer from it.
3. An error is reported as an error, never as an empty result.
4. Who read data comes only from Data Access log entries; configuration shows who could.
## Commands
Read references/commands.md: catalog lists, Agent Runtime list, the Data Access query.
```

In the lab, open `/config/Desktop/novasmart-evidence/m0/m0_step4.txt` and find each `tableDataRead` entry, its `principalEmail` and the service agent under `serviceAccountDelegationInfo`. Then compare the Step 4 section of `references/m0.md` with what your agy did.

## Read more

- [Agent skills](https://antigravity.google/docs/skills)
- [Installation and auth](https://antigravity.google/docs/cli/install/)
- [Permissions](https://antigravity.google/docs/permissions/)
- [Headless mode](https://antigravity.google/docs/cli/headless/)
- [Agent Registry overview](https://docs.cloud.google.com/agent-registry/overview)
- [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)
- [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit)
- [Enable Data Access audit logs](https://docs.cloud.google.com/logging/docs/audit/configure-data-access)
