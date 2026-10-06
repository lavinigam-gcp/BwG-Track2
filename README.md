# Build with Google — Track 2: Govern Your AI Estate (NovaSmart Lab)

Take-home lab materials, agent steering skills, architecture guides, and local no-VM environment setup for **Build with Google — Track 2: Govern Your AI Estate**.

In this lab, you step into the role of **Head of AI Platform and Security** at **NovaSmart**, a consumer-electronics retailer whose rapid "AI-first" push left behind unmanaged agent sprawl. Working alongside **Antigravity (`agy`)**, you take an unmapped, over-privileged multi-agent estate on Google Cloud and make it **visible, attributable, least-privileged, access-controlled, content-screened, and measured**—without writing application code by hand, and with every finding and change backed by verifiable platform evidence.

---

## Table of Contents

1. [What This Lab Is About](#what-this-lab-is-about)
2. [The 5-Module Governance Journey (M0–M4)](#the-5-module-governance-journey-m0m4)
3. [Repository Structure](#repository-structure)
4. [How to Use This Take-Home Repository](#how-to-use-this-take-home-repository)
   - [1. Read the Interactive Lab Portal & Module Guides](#1-read-the-interactive-lab-portal--module-guides)
   - [2. Inspect or Reuse the `novasmart-governance-lab` Agent Skill](#2-inspect-or-reuse-the-novasmart-governance-lab-agent-skill)
   - [3. Run the Lab Locally Without a Cloud VM (`bwg-lab-setup`)](#3-run-the-lab-locally-without-a-cloud-vm-bwg-lab-setup)
5. [Applying These Patterns to Your Own Google Cloud Estate](#applying-these-patterns-to-your-own-google-cloud-estate)
6. [Google Cloud & Agent Platform Surfaces Reference](#google-cloud--agent-platform-surfaces-reference)

---

## What This Lab Is About

When organizations ask every team to ship AI agents quickly, three governance shortcuts almost always appear together:
1. **Shadow AI (No Visibility):** Workloads are deployed on general-purpose compute without being registered in a central catalog or assigned an owner.
2. **Shared Credentials (No Accountability):** Multiple workloads reuse a single service account, making Cloud Audit Logs incapable of proving which agent accessed sensitive data.
3. **Over-Privilege & Unchecked Boundaries (High Blast Radius):** Agents inherit project-wide admin roles, accept calls from leftover test accounts, pass unscreened customer text straight to models, and ship without systematic policy evaluation.

### The NovaSmart AI Estate

NovaSmart runs four AI workloads across **Gemini Enterprise Agent Platform** (**Agent Runtime**) and **Cloud Run**, backed by **BigQuery** (`customer_data` and pricing datasets) and an **MCP** tool layer (`novasmart-mcp`):

| Workload | Where It Runs | Role in the Business | Initial Governance Gap |
| :--- | :--- | :--- | :--- |
| **Price Match Agent** (`AdkApp`) | Agent Runtime | Storefront co-pilot. Approves competitor price matches up to 10% on the spot; escalates >10% discounts to the back office. | Holds broad project-wide data access; accepts raw user input with no prompt-injection screening; running version may drift from written policy. |
| **Markdown Strategy Agent** (`A2A`) | Agent Runtime | Back-office authority for discounts >10%. Evaluates confidential cost and margin tables. | Resource IAM policy permits an unowned leftover account (`test-agent-caller`); lacks outbound gateway constraints; holds write access to pricing tables. |
| **Customer Personalization Agent** (`A2A`) | Agent Runtime | Tailors shopper promotions and VIP rewards using customer records via `novasmart-mcp`. | Shares a single service account (`novasmart-customer-sa`) with a shadow agent; vulnerable to data-exfiltration prompt injection. |
| **Demand and Promotion Agent** (`promo-agent-shadow`) | Cloud Run | Marketing service that generates promotional copy and flash-sale bundles. | **Shadow AI.** Unregistered in Agent Registry, has no owner, shares `novasmart-customer-sa` (which holds `roles/bigquery.admin` project-wide), and extracts customer PII it never needed. |

### Six Properties of a Governed Estate

Across five modules, you progressively establish six security and governance properties:

| Property | Meaning | Built In |
| :--- | :--- | :--- |
| **1. Visible** | Every running agent is registered in **Agent Registry** with a named owner. | **M0 → M1** |
| **2. Attributable** | Every action in **Cloud Audit Logs** traces to one specific agent via **Agent Identity** or a dedicated login. | **M0 → M1** |
| **3. Least Privileged** | Each agent holds only the minimum permissions required for its job—and nothing more. | **M1 & M2** |
| **4. Access Controlled** | Sensitive agents enforce explicit inbound caller lists and outbound **Agent Gateway** boundaries. | **M2** |
| **5. Screened** | Prompt injections and jailbreaks are intercepted at the door by **Model Armor** before reaching the model. | **M3** |
| **6. Measured** | Agent behavior is scored against a scenario set using the **Gen AI evaluation service** before launch. | **M4** *(Optional)* |

---

## The 5-Module Governance Journey (M0–M4)

### M0 · See Everything (Shadow AI Discovery & Audit Attribution)
* **Mode:** Strictly read-only (`Changes made: 0`).
* **What You Do:**
  1. Verify your workstation and cloud environment readiness across an 8-point checklist.
  2. Query **Agent Registry** across regional and `global` locations, separating NovaSmart's 3 registered agents from 3 Google built-in agents (*Workspace Agent*, *Gemini Enterprise Core Assistant*, *Deep Research*).
  3. Sweep live deployments across **Agent Runtime** and **Cloud Run** to uncover `promo-agent-shadow`, an unowned marketing agent missing from the catalog.
  4. Query **Cloud Audit Logs** (`cloudaudit.googleapis.com/data_access`) on `customer_data` and discover that customer PII reads are logged under a shared login (`novasmart-customer-sa`), requiring hosting inference (`serviceAccountDelegationInfo`) rather than direct agent attribution.
  5. Make the executive call (*"Own it or kill it?"*) and generate interactive HTML showcase artifacts (`Desktop/novasmart-showcase/`) from your evidence files.

### M1 · Take Action (Identity Split & Least Privilege)
* **Mode:** Mutating (7 ordered changes, each with a verified live re-read and recorded undo command).
* **What You Do:**
  1. Register `promo-agent-shadow` in **Agent Registry** with marketing ownership and a high risk tier recorded in its description.
  2. Inspect `novasmart-customer-sa` (read-only pause) and uncover project-wide `roles/bigquery.admin` and `roles/storage.objectViewer` permissions.
  3. Execute a zero-downtime identity split (*re-grant before you revoke*):
     - Flip `customer-personalization-agent` on Agent Runtime to **Agent Identity** (`principal://...`), grant it project-level `roles/bigquery.jobUser` and dataset-level `READER` on `customer_data`, and verify a live read.
     - Create a dedicated `promo-agent-sa` service account with bucket-only `roles/storage.objectViewer` on the code seed bucket, re-point `promo-agent-shadow` on Cloud Run, and vacate `roles/bigquery.admin` from `novasmart-customer-sa`.
  4. Confirm the marketing agent has zero access to customer records while personalization and price-match services stay healthy.
  5. Trigger live requests and prove in **Cloud Audit Logs** that personalization reads carry the agent's `principalSubject` badge while the promo agent's query job is actively denied (`PERMISSION_DENIED` on `bigquery.jobs.create`, even though the app itself returns HTTP 200 with `0 records analyzed`). Generate the 16-check **Governance Scorecard** and M1 showcase pages.

### M2 · Control the Connections (Inbound Caller Lists & Outbound Perimeters)
* **Mode:** Read-before-write + targeted resource IAM and gateway attachment.
* **What You Do:**
  1. Inspect the back-office **Markdown Strategy Agent**'s resource IAM policy (`reasoningEngines/{id}:getIamPolicy`) and identify an unowned leftover caller (`test-agent-caller`).
  2. Assess the blast radius of locking down the caller list, accounting for additive project-wide IAM roles and direct storefront routes.
  3. Rewrite the back-office agent's resource IAM policy (`:setIamPolicy`) so only the front-desk **Price Match Agent**'s Agent Identity is listed.
  4. Prove `test-agent-caller` flips from HTTP 200 to HTTP 403 while a genuine >10% escalation (*AeroPure Smart Air Purifier*, `SKU-HSE-4001` at BetaBuy's `$296.65`, 15% off) still succeeds.
  5. Place the back-office agent behind an **Agent Gateway** to govern outbound destinations and narrow its BigQuery permissions from `roles/bigquery.admin` to read-only on pricing data, confirming via direct database reads that writes are refused.

### M3 · Protect the Content (Runtime Guardrails & Model Armor)
* **Mode:** Adversarial red-teaming + gateway-attached content screening.
* **What You Do:**
  1. Send live prompt-injection attacks to both customer-facing agents—tricking the Price Match Agent into approving a >10% discount without escalating, and tricking the Customer Personalization Agent into dumping all 20 customer PII rows.
  2. Audit existing content filters and discover a provisioned but unattached **Model Armor** template (`nvst-jailbreak-template`), while learning why a project-wide Model Armor floor setting breaks legitimate tool-calling agents by flagging their internal system prompts and tool schemas.
  3. Attach `nvst-jailbreak-template` (plus the Sensitive Data Protection inspection profile) to the **Agent Gateway** in front of the **Price Match Agent** (`AdkApp` on `streamQuery`).
  4. Replay both the attacks and legitimate 5% price-match lookups, verifying the platform's block message (`Model Armor: Prompt violates content security configurations`) alongside healthy business traffic.
  5. Document what is covered and what remains open (fail-open availability trade-offs, single-agent `streamQuery` ingress coverage vs. A2A `message:stream` workloads).

### M4 · Evaluate and Decide (Optional Module — Batch Evaluation & Launch Readiness)
* **Mode:** Read-only on production; local sandbox iteration and batch scoring via the **Gen AI evaluation service**.
* **What You Do:**
  1. Score the deployed Price Match Agent against NovaSmart's 4-case baseline scenario set (5% approve, 15% escalate, unverified $150 refuse, 90% jailbreak refuse). Inspect judge reasoning, near-misses, 10%-vs-20% policy drift, and whether refusals came from the M3 gateway or the agent itself.
  2. Stand up a local workstation copy of the real Price Match Agent code, generate a tougher multi-turn synthetic test set grounded in NovaSmart's product catalog and competitor prices, and score it.
  3. Review a proposed before-and-after diff to the agent's system instructions prior to applying any change.
  4. Apply the instruction fix to the local copy, re-run the exact same scenario set to measure case-by-case movement, and contrast the local improvement against the unchanged production agent (*"configured is not running"*).
  5. Make an evidence-backed launch decision and define post-launch monitoring priorities.

---

## Repository Structure

```text
BwG-Track2/
├── README.md                                 # This take-home guide
├── lab_material/                             # Full lab instructions, reference guides, takeaways & HTML portal
│   ├── lab_instructions.html                 # Self-contained offline 3-column interactive reader (English)
│   ├── lab_instructions_ja.html              # Self-contained offline 3-column interactive reader (Japanese)
│   ├── images/                               # Architecture, swimlane, and concept diagrams (.webp)
│   ├── m0-instructions.md                    # M0 step-by-step prompts and expected outcomes
│   ├── m0-context.md                         # M0 Reference Guide (NovaSmart backstory, cast of agents, deep dive)
│   ├── m0-learned.md                         # M0 "What did we learn?" post-module visual summary & team questions
│   ├── m0-skill-mapping.md                   # M0 "Skill Mapping" (exact CLI commands, audit analysis & DIY guide)
│   ├── m1-instructions.md                    # M1 step-by-step prompts and expected outcomes
│   ├── m1-context.md                         # M1 Reference Guide (Agent Registry, Agent Identity, least privilege)
│   ├── m1-learned.md                         # M1 "What did we learn?" post-module visual summary & team questions
│   ├── m1-skill-mapping.md                   # M1 "Skill Mapping" (7-change sequence, undo table, 16 checks & DIY guide)
│   ├── m2-instructions.md                    # M2 step-by-step prompts and expected outcomes
│   ├── m2-context.md                         # M2 Reference Guide (Resource IAM, additive permissions, Agent Gateway)
│   ├── m3-instructions.md                    # M3 step-by-step prompts and expected outcomes
│   ├── m3-context.md                         # M3 Reference Guide (Prompt injection, Model Armor gateway vs floor)
│   ├── m4-instructions.md                    # M4 step-by-step prompts and expected outcomes (Optional Module)
│   └── m4-context.md                         # M4 Reference Guide (Gen AI evaluation service, judges, near-misses)
├── skills/
│   └── novasmart-governance-lab/             # The steering skill loaded by Antigravity (agy) during the lab
│       ├── SKILL.md                          # Core rules, 10 non-negotiables, output blocks, glossary & evidence spec
│       ├── references/
│       │   ├── m0.md                         # M0 agent playbook: readiness table, step gate, CLI/REST commands
│       │   ├── m1.md                         # M1 agent playbook: registration, IAM inspection, scope fence
│       │   ├── m1-step3.md                   # M1 Step 3 playbook: 7-step identity split & re-keying sequence
│       │   ├── m1-step5.md                   # M1 Step 5 playbook: live triggers, audit log queries & 16-row table
│       │   ├── m2.md                         # M2 agent playbook: resource IAM lockdown, 200->403 proof & gateway
│       │   ├── m3.md                         # M3 agent playbook: red-team prompts, Model Armor gateway wiring
│       │   ├── m4.md                         # M4 agent playbook: batch evaluation, synthetic cases & local diff loop
│       │   ├── showcase.md                   # Shared build bar & verification workflow for Step 7 HTML demos
│       │   ├── showcase-m0.md                # M0 Step 7 recipes (dashboard, investigation board, game, briefing, poster)
│       │   └── showcase-m1.md                # M1 Step 7 recipes (before/after map, change replay, auditor proof, game)
│       └── scripts/
│           ├── update_scorecard.py           # Generates cumulative HTML Governance Scorecard for M1, M2, M3
│           ├── show_facts.py                 # Compiles line-numbered fact sheets & PII blocklists from evidence files
│           └── show_check.py                 # Validates & screenshots Step 7 HTML pages via headless Chromium
└── bwg-lab-setup/                            # Local no-VM setup toolkit (macOS / Linux / WSL2)
    ├── README.md                             # Detailed setup guide & OS support matrix
    ├── manual_setup.md                       # Step-by-step manual installation reference
    ├── TROUBLESHOOTING.md                    # Per-OS diagnostic & remediation guide
    ├── .agents/skills/bwg-lab-setup/         # Setup assistant skill for agent-driven laptop configuration
    └── setup/
        ├── preflight.sh                      # Read-only hardware, OS, network, and identity check
        ├── install.sh                        # Idempotent environment & session workspace installer
        ├── verify.sh                         # 12-point environment parity and readiness verifier
        ├── lab-phase.sh                      # Pre-event vs. day-of phase detection helper
        └── requirements-lock.txt             # 120 pinned Python packages for local parity
```

---

## How to Use This Take-Home Repository

### 1. Read the Interactive Lab Portal & Module Guides

You can explore the entire curriculum offline without a live Google Cloud project:

* **Interactive Browser View (Recommended):** Open `lab_material/lab_instructions.html` (or `lab_material/lab_instructions_ja.html` for Japanese) directly in any browser (`file://`). It requires no build step, server, or internet connection and provides:
  * A **Mission Switcher** across **M0** through **M4**.
  * Four tabs per module:
    1. **Instructions:** The exact plain-English prompts you give `agy` and what to check in each reply.
    2. **What did we learn?:** Visual diagrams, mental models, industry scenarios, and questions to take back to your engineering and security teams.
    3. **Skill Mapping (Optional):** Behind-the-scenes breakdown of how the `novasmart-governance-lab` skill translated your plain-English prompts into `gcloud`, `bq`, and REST calls, what was captured in the audit trail, where model execution can slip, and how to set up the same workflow in your own company.
    4. **Reference Guide (Optional):** Deep narrative context on the architecture, trade-offs, and security principles behind every step.
* **Markdown Reading Order:** If reading the `.md` files directly in an editor or on GitHub, follow this order for each module `N`:
  1. `lab_material/mN-instructions.md` alongside `lab_material/mN-context.md`
  2. `lab_material/mN-learned.md` (available for M0 and M1)
  3. `lab_material/mN-skill-mapping.md` (available for M0 and M1)

---

### 2. Inspect or Reuse the `novasmart-governance-lab` Agent Skill

The `skills/novasmart-governance-lab/` directory is a production-grade example of an **Antigravity Agent Skill** designed to steer an autonomous CLI/IDE agent through high-stakes cloud security operations safely and honestly.

#### How to Install the Skill in Your Workspace
Copy `skills/novasmart-governance-lab` so that `SKILL.md` sits one level inside `.agents/skills/`:

```bash
# For a single project workspace (start your IDE/agent from <workspace-root>):
mkdir -p <workspace-root>/.agents/skills
cp -r skills/novasmart-governance-lab <workspace-root>/.agents/skills/

# Or globally for all Antigravity CLI sessions:
mkdir -p ~/.gemini/antigravity-cli/skills
cp -r skills/novasmart-governance-lab ~/.gemini/antigravity-cli/skills/
```

> **Important:** The skill loader scans only direct children of `.agents/skills/`. Ensure `.agents/skills/novasmart-governance-lab/SKILL.md` exists at the top of its folder. Additionally, each file in `SKILL.md` and `references/*.md` is intentionally kept under **44 KB** so the agent's file viewer reads the complete file in a single call without truncating tail sections.

#### Key Engineering Patterns Inside the Skill
* **Evidence-First Architecture (`SKILL.md` §3g):** Before the agent writes a single word of its user-facing answer, it appends an entry to `Desktop/novasmart-evidence/m<N>/m<N>_step<K>.txt` containing three mandatory sections:
  * `-- COMMANDS --` (runnable commands only, indexed `# 1`, `# 2`, ...)
  * `-- OUTPUTS --` (verbatim system output with exit codes `[1] exit 0`, `[2] exit 0`)
  * `-- CHANGE RECORD --` (what changed, resource, UTC timestamp, and the exact runnable `Undo:` command)
* **Strict Figure Parity:** Every count, resource ID, status code, timestamp, role name, or principal shown to the user—or drawn in an architectural diagram—must appear character-for-character in the `OUTPUTS` section of that turn's evidence entry.
* **Spoiler Fence & Step Gate (`references/m0.md`–`m4.md`):** Each reference file gives the agent orientation on the estate so it knows which APIs to query, but strictly forbids reciting expected findings before the step's live command produces them. If live cloud output differs from the reference map, **the live result always wins**.
* **Verification & Showcase Scripts (`scripts/`):**
  * `update_scorecard.py`: Generates a self-contained HTML **Governance Scorecard** (`governance_scorecard.html`) after verification steps in M1, M2, and M3. Set `export NOVASMART_SCORECARD_HOME="$HOME"` when running outside the `/config` container path.
  * `show_facts.py` & `show_check.py`: Powers the Step 7 *Show what you found / changed* prompts. `show_facts.py` distills multi-kilobyte evidence files into a line-numbered fact sheet while stripping PII/project IDs into `.build/mN_private.txt`. `show_check.py` runs static leak checks and headless Chromium rendering checks (at `1440px` desktop and `390px` mobile viewports) before the agent returns the page.

---

### 3. Run the Lab Locally Without a Cloud VM (`bwg-lab-setup`)

While the cloud-hosted lab workstation VM is the default environment during live sessions, experienced developers can configure their own **macOS**, **Linux**, or **Windows (WSL2)** machine using the **`bwg-lab-setup/`** folder included directly in this repository (synced from [`lavinigam-gcp/bwg-lab-setup`](https://github.com/lavinigam-gcp/bwg-lab-setup)).

> **Disclaimer & Safety Note:** Running `bwg-lab-setup` modifies your local machine (installing system packages, Python 3.14, Node.js 24, Google Cloud CLI, and a 120-package locked Python virtual environment). Review `bash setup/install.sh --dry-run` or follow `bwg-lab-setup/manual_setup.md` before executing.

#### Prerequisites
* **OS:** macOS 13+ (Apple Silicon or Intel), Linux with glibc 2.28+ (Ubuntu 20.04+ / Debian 10+), or Windows 10 build 19044+ with **WSL2 and WSLg** (native Windows is not supported because `uvloop` does not publish Windows wheels).
* **Hardware:** 8 GB RAM minimum (16 GB recommended), 15 GB free disk space, 4+ CPU cores recommended.
* **Antigravity IDE:** Install from [https://antigravity.google/download](https://antigravity.google/download).
* **Account Isolation (Critical):** Sign in to both Antigravity IDE and `gcloud` using **only the lab account issued for your lab project**—never your personal or corporate Google account. Isolate your `gcloud` config first:
  ```bash
  gcloud config configurations create lab
  gcloud auth login
  gcloud auth application-default login
  gcloud config set project YOUR_LAB_PROJECT_ID
  gcloud auth application-default set-quota-project YOUR_LAB_PROJECT_ID
  ```
  *(Do not skip `set-quota-project`; without it, several APIs return `403` errors complaining about `x-goog-user-project`.)*

#### Three Ways to Set Up Your Laptop

All three paths produce the exact same environment and are verified by `bash setup/verify.sh --readiness`.

##### Path A — Ask the Assistant (Agent-Driven in Antigravity IDE)
1. Open the `bwg-lab-setup/` folder from this repository in **Antigravity IDE**.
2. In the Antigravity prompt, enter:
   ```text
   Set up my laptop for the lab.
   ```
3. The assistant runs the read-only preflight check, displays your machine's report card, lists every change it plans to make, and waits for your confirmation before installing.

##### Path B — Run the Automated Scripts
```bash
# 1. Enter bwg-lab-setup and run read-only preflight (changes nothing; exits GO / GO WITH CAVEATS / NO-GO)
cd bwg-lab-setup
bash setup/preflight.sh

# 2. Preview commands (optional) and run the idempotent installer
bash setup/install.sh --dry-run
bash setup/install.sh               # add --with-extras for ffmpeg, VS Code, and Playwright Chromium

# 3. Verify all checks pass and check cloud readiness
bash setup/verify.sh --readiness
```

##### Path C — Manual Step-by-Step Setup (`bwg-lab-setup/manual_setup.md`)
See [`bwg-lab-setup/manual_setup.md`](bwg-lab-setup/manual_setup.md) for the complete command-by-command walkthrough, and [`bwg-lab-setup/TROUBLESHOOTING.md`](bwg-lab-setup/TROUBLESHOOTING.md) for per-operating-system diagnostics.

---

## Applying These Patterns to Your Own Google Cloud Estate

The `m0-skill-mapping.md` and `m1-skill-mapping.md` guides include blueprints for adapting this lab's governance workflow to your own organization:

1. **Use a Dedicated Service Account with Split Read/Write Roles:**
   * **For Discovery (M0-style audits):** Grant only read-only roles (`roles/agentregistry.viewer`, `roles/aiplatform.viewer`, `roles/run.viewer`, `roles/logging.privateLogViewer`, `roles/serviceusage.serviceUsageViewer`, and dataset-level `roles/bigquery.metadataViewer`).
   * **For Remediation (M1–M3 changes):** Keep write roles separate and test in a non-production project first.
2. **Lock Down Agent Command Permissions (`.gemini/antigravity-cli/settings.json`):**
   * Never use unrestricted auto-approve (`Turbo`) in production. Use the `Default` or `Request Review` permission preset, allow-list read commands, and require interactive confirmation (`ask`) for every mutating command:
     ```json
     {
       "permissions": {
         "allow": [
           "command(gcloud agent-registry agents list)",
           "command(gcloud agent-registry services list)",
           "command(gcloud run services list)",
           "command(gcloud run services describe)",
           "command(gcloud projects get-iam-policy)",
           "command(gcloud logging read)",
           "command(bq show)"
         ],
         "ask": [
           "command(gcloud agent-registry services create)",
           "command(gcloud agent-registry services update)",
           "command(gcloud iam service-accounts create)",
           "command(gcloud projects add-iam-policy-binding)",
           "command(gcloud projects remove-iam-policy-binding)",
           "command(gcloud run services update)",
           "command(bq update)"
         ]
       }
     }
     ```
3. **Capture an Independent Audit Record:**
   * Run read-only discovery prompts in headless mode (`agy -p "..." --output-format stream-json > step.ndjson`) and compare the independent tool-call capture against the agent's self-reported evidence file and **Cloud Audit Logs**.
4. **Update SIEM / Log Alerts for Agent Identity:**
   * When an agent on **Agent Runtime** moves from a service account to **Agent Identity**, its `principalEmail` field in Cloud Audit Logs becomes blank and its identity is recorded in `protoPayload.authenticationInfo.principalSubject` (`principal://...`). Update monitoring and alerting queries to inspect both fields.

---

## Google Cloud & Agent Platform Surfaces Reference

| Governance Capability | Google Cloud Product / Surface | Key CLI / API Surface Used in Lab |
| :--- | :--- | :--- |
| **Agent Inventory & Ownership** | **Agent Registry** | `gcloud agent-registry agents list --location=<REGION\|global>`<br>`gcloud agent-registry services create / update` |
| **Managed Agent Hosting** | **Agent Runtime** *(Gemini Enterprise Agent Platform)* | `GET / PATCH https://<REGION>-aiplatform.googleapis.com/v1beta1/projects/<PROJECT>/locations/<REGION>/reasoningEngines` |
| **Per-Agent Traceable Badge** | **Agent Identity** | `spec.identityType = "AGENT_IDENTITY"` → `spec.effectiveIdentity` (`principal://...`) |
| **Container Hosting & Service Identity** | **Cloud Run** & **IAM Service Accounts** | `gcloud run services list / describe / update --service-account=...` |
| **Data Access Audit Trail** | **Cloud Audit Logs** *(BigQuery Data Access)* | `gcloud logging read 'logName=".../cloudaudit.googleapis.com%2Fdata_access" AND ...'` |
| **Agent-to-Agent Caller Control** | **Agent Runtime Resource IAM** | `POST .../reasoningEngines/<ID>:getIamPolicy` & `:setIamPolicy` |
| **Outbound Egress & Ingress Screening** | **Agent Gateway** + **Model Armor** | Gateway attachment + `nvst-jailbreak-template` + Sensitive Data Protection profile |
| **Pre-Launch Policy Scoring** | **Gen AI Evaluation Service** | `agents-cli eval` / batch scenario evaluation with LLM-as-judge reasoning |
