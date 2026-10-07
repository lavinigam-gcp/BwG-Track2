# M1 · Take Action — What did we learn?

*Read this after you finish Module 1. It names what you found, so you can explain it in your own words.*

**In one sentence:** The shadow agent now has an owner, each of the two agents signs in as itself, and the audit log shows which agent read customer data and which one was refused.

## What each prompt tested

<!-- FIGURE:L1_01 BEGIN -->

![The title reads: What each prompt tested. Five rows, each a white step card with a blue product chip and an arrow to a finding. 1 · Register it, Agent Registry, leads to Owned, not yet safe, in gray. 2 · See its power, IAM, leads to Can change or delete all data, in red. 3 · One login each, Agent Identity + Cloud Run, leads to Each signs in as itself, in green. 4 · Cut marketing's access, BigQuery access list, leads to Already closed in Step 3, in green. 5 · Prove it, Cloud Audit Logs, leads to Denial in the log is the proof, in green.](images/L1_01_what_each_prompt_tested.webp)

<!-- FIGURE:L1_01 END -->

In M0, two agents shared one login, a service account: a login for a program rather than a person — how an agent signs in. NovaSmart runs two more agents, Price Match and Markdown Strategy. They already had their own identities but still hold a project-wide admin role (a role is a bundle of permissions with a name) in BigQuery, where NovaSmart keeps its customer and business data; M2 is where they come in. The store app is an app, not an agent.

- **Step 1** registered the promo agent in the official catalog, Agent Registry, with marketing as owner. Visible and owned, not yet safe.
- **Step 2** changed nothing. IAM, the system that decides who is allowed to do what, showed the shared login's power was project-wide (granted across everything in the project, not on one database): it could change or delete every table.
- **Step 3** gave each agent its own login with only what its job needs.
- **Step 4** asked to cut the promo (marketing) agent's access to customer data. The customer dataset's access list showed Step 3 had already closed it, and agy said so.
- **Step 5** read the audit log, the platform's own record of who did what, which we cannot edit, and evidenced 16 of the 16 checks, one from configuration only.

## One shared login became one each

<!-- FIGURE:L1_02 BEGIN -->

![The title reads: One shared login became one each. Two panels. Before: Personalization agent and Promo agent, shown as gear icons in blue cards, both have amber arrows into one amber login, novasmart-customer-sa. After: the same two cards, each with a green arrow to its own green pill: Own Agent Identity under the personalization agent, promo-agent-sa under the promo agent. Below, novasmart-customer-sa sits in a gray dashed pill with no arrows, beside the words No users left.](images/L1_02_one_login_to_one_each.webp)

<!-- FIGURE:L1_02 END -->

The personalization agent runs on Agent Runtime, Google Cloud's managed service for running agents, so it moved to Agent Identity: the per-agent badge that makes every action traceable to one agent.

Agent Identity is for agents on Agent Runtime. The promo agent runs on Cloud Run, Google Cloud's service for running any container — a website, a tool, or an agent — so it got its own service account instead, `promo-agent-sa`, that can only read the bucket its code loads from. Same principle, different plumbing. The shared login has no users left.

## Re-grant before you revoke

<!-- FIGURE:L1_03 BEGIN -->

![The title reads: Re-grant before you revoke. Three blue cards joined by arrows, left to right: a badge icon, Move to its own badge, Opens nothing yet; a key icon, Grant back only what it needs, Run queries, read customer data; a padlock icon, Remove the broad access, Shared login: no users left. Under the first card, a small red tag reads Stop here: reads fail. A gray bar across the bottom reads One agent, one badge.](images/L1_03_moving_the_badge_takes_the_keys.webp)

<!-- FIGURE:L1_03 END -->

The access belonged to the shared login, not the agent. On its own badge the personalization agent inherited nothing: it would answer a greeting and fail its first read.

So agy moved the agent, granted its badge permission to run queries in the project and read-only access to the customer dataset (one database inside BigQuery), showed it reading, and only then removed the shared login's admin role.

## The proof: what the log proves now

<!-- FIGURE:L1_04 BEGIN -->

![The title reads: What the log proves now. Two log rows. A green row: 19:23:22, Read allowed, Personalization agent's own badge, Agent named in its own field. A red row: 19:23:39, Query denied, promo-agent-sa. Below, an amber box reads The app said: Launched, 0 records analyzed, and a blue box reads The log said: Denied, under its own login.](images/L1_04_the_proof.webp)

<!-- FIGURE:L1_04 END -->

In one test run on October 3, 2026 (UTC; your times will differ), agy triggered a read from each agent. The allowed read named the agent in a different field of the log; a badge has no email address.

The promo agent may not run a query, yet its app said the campaign launched, with 0 records analyzed. The log is the evidence; the app is not.

Each agent's reads show its own name, and the refusal works. That does not show nobody else reads customer data: the store app's account still can. Open `/config/Desktop/novasmart-evidence/m1/m1_step5.txt` and find `bigquery.jobs.create`, the refused permission.

## Where this shows up

<!-- FIGURE:L1_05 BEGIN -->

![The title reads: Same fix, other industries, with a tag reading Illustration. Four cards, each with an icon: Retail, Store and marketing agents, in blue; then, in gray, Healthcare, Triage and billing agents; Banking, Loan and fraud agents; and Manufacturing, Supplier and quality agents. A green bar beneath reads: One workload, one login, only what it needs.](images/L1_05_same_fix_elsewhere.webp)

<!-- FIGURE:L1_05 END -->

- **Scenario: one login on the plant floor.** A supplier-portal agent and a quality-inspection agent share one login to the plant historian. When a recipe changes, nobody can say which agent changed it.
- **Scenario: a badge, not a key.** A bank's loan agent reads account data on its own Agent Identity, with no long-lived key anyone can leak.
- **Scenario: prove it with a refusal.** Compliance asks for proof a vendor tool can't read personal data. You trigger the attempt and hand over the denied entry.

[Google documents](https://docs.cloud.google.com/iam/docs/access-change-propagation) that an access change typically takes 2 minutes, "potentially 7 minutes or longer".

## Your call: ask what the job needs

<!-- FIGURE:L1_06 BEGIN -->

![The title reads: What does this job need? Four tall cards joined by arrows, left to right. Two amber cards with question-mark icons: Who signs in as this? (One login per agent) and What does its job need? (Compare the job to the grant). Two blue cards with gear icons: Grant that, then remove the rest (Re-grant before you revoke) and Prove it with a refusal (Trigger it, then read the log).](images/L1_06_what_does_this_job_need.webp)

<!-- FIGURE:L1_06 END -->

Step 2 was the pause: a question that only reads, before anything that writes.

- **Least privilege:** giving a job only the access it needs and nothing more. The personalization agent needs to read customer records, never to change one. The promo agent needs none.
- **Blast radius:** how far the damage reaches if this is misused or stolen. Before Step 3, the whole project for both agents; now only what each job needs.

## Where your estate stands

<!-- FIGURE:L1_07 BEGIN -->

![The title reads: Where your estate stands after Module 1. A row of six tall segments, left to right: Visible, Attributable, Least privileged, Access controlled, Screened, Measured, tagged M1, M1, M1, M2, M3 and M4 · optional. Visible and Attributable are green; the other four are gray. Least privileged carries a small amber marker above it reading Two agents only.](images/L1_07_estate_progress.webp)

<!-- FIGURE:L1_07 END -->

Module 1 made the first two true. Least privileged holds only for the two agents you changed; Price Match and Markdown Strategy still hold broad data access, which this module leaves as a finding.

| Property | What it means | Where you build it |
| :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 |
| Attributable | Every action traces to one named agent | M1 |
| Least privileged | Each agent holds only the access its job needs | M1 |
| Access controlled | Only approved callers can reach a sensitive agent | M2 |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) |

Still open: which agents may talk to each other. The back-office Markdown Strategy Agent reads confidential margin data and should only be called by another agent; nothing enforces that. M2 · Control the Connections is where you decide who may call whom, starting with who is allowed to call that back-office margin agent.

## Questions to take back to your team

- Which of our agents share one login?
- For each agent, what does its job need, and what does its login hold?
- When we take access away, do we grant the replacement first?
- Can we show a refused attempt in our logs, not just a quiet log?

## Read more

| Topic | Official page |
| :-- | :-- |
| The agent catalog | [Agent Registry overview](https://docs.cloud.google.com/agent-registry/overview) · [Register agents](https://docs.cloud.google.com/agent-registry/register-agents) |
| Each agent's own badge | [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview) · [Use Agent Identity with Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity) |
| A login for a Cloud Run service | [Introduction to service identity](https://docs.cloud.google.com/run/docs/securing/service-identity) |
| Why not to share a login | [Best practices for using service accounts securely](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts) |
| Smallest role for the job | [BigQuery IAM roles and permissions](https://docs.cloud.google.com/bigquery/docs/access-control) · [Use IAM securely](https://docs.cloud.google.com/iam/docs/using-iam-securely) |
| How long a change takes | [Access change propagation](https://docs.cloud.google.com/iam/docs/access-change-propagation) |
| Who did what, and when | [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit) |

For the story behind each step, see the matching Step section on the Reference Guide tab.
