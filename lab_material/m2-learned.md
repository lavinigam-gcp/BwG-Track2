# M2 · Control the Connections — What did we learn?

*Read this after you finish Module 2. It names what you found, so you can explain it in your own words.*

**In one sentence:** The back-office agent's own list now names one caller, the front desk; the leftover login is refused; and the back office can read the pricing data but no longer change it, though broad project-wide roles can still call it.

## What each prompt tested

<!-- FIGURE:L2_01 BEGIN -->

![The title reads: What each prompt tested. Five rows, each a white step card with a blue product chip and an arrow to a finding. 1 · Who can call it?, Agent Runtime IAM, leads to Leftover login got an answer, in red. 2 · What would break?, IAM, leads to Safe, but partial, in amber. 3 · Lock it, Agent Runtime IAM, leads to One name on its own list, in green. 4 · Try it again, Cloud Audit Logs, leads to Refused; business call answered, in green. 5 · Reach and rights, Agent Gateway + BigQuery, leads to Reads; a change is refused, in green.](images/L2_01_what_each_prompt_tested.webp)

<!-- FIGURE:L2_01 END -->

M2 settles who may call whom. The back office (the Markdown Strategy Agent) holds NovaSmart's cost and margin data; the front desk (the Price Match Agent) escalates discounts above 10% to it.

- **Step 1** read the back office's own list of callers. It named one unowned leftover login, `test-agent-caller`, not the front desk. A real call as that login got an answer.
- **Step 2** changed nothing. It found four routes in: the leftover login on the list, the front desk's business calls, the store website's direct route, and project-wide roles. The lock would close only the leftover's: safe, but partial.
- **Step 3** rewrote the list to name one caller: the front desk's own Agent Identity, the per-agent badge that makes every action traceable to one agent.
- **Step 4** repeated Step 1's call. It was refused; the business call still worked.
- **Step 5** put the back office behind the outbound gateway and narrowed it to reading the pricing data. The module's check table passed, and agy wrote that result to the lab's scorecard.

## Two lists decide who can call

<!-- FIGURE:L2_02 BEGIN -->

![The title reads: Two lists decide who can call. Two panels, Before and After, each holding the same two boxes. Before: a white box, Back office's own list, holds a red pill, test-agent-caller; below it, an amber box reads Project-wide roles, Can call any agent. After: the same white box now holds a green pill, Front desk's own badge; the amber box below sits in the same place with the same words and carries a gray tag reading Unchanged.](images/L2_02_two_lists.webp)

<!-- FIGURE:L2_02 END -->

Two places decide who may call the back office: its own list, a setting on that agent, and project-wide roles (granted across everything in the project, not on one database). A role is a bundle of permissions with a name; in this run, 8 roles held by 15 identities could call any agent. Permissions add up, so the widest grant wins. Step 3 changed the list, not the roles.

Call permission is not data permission. `test-agent-caller`, a service account (a login for a program rather than a person — how an agent signs in), could read no data, yet could ask the back office to read the margin data for it.

## The proof: same call, before and after

<!-- FIGURE:L2_03 BEGIN -->

![The title reads: Same call, before and after. Two log rows, each with a document icon and the same pill, test-agent-caller. A red row: 03:03:31, HTTP 200, answered. A green row: 03:20:30, HTTP 403, refused. Below, a blue box reads Audit log: Same refusal, under the leftover login, and a green box reads Business call: Back office's decision came back.](images/L2_03_same_call_before_after.webp)

<!-- FIGURE:L2_03 END -->

In one test run on October 6, 2026 (UTC; your times will differ), agy sent the same request twice as `test-agent-caller`. At 03:03:31, before the lock, it got HTTP 200 and an answer. At 03:20:30, about five and a half minutes after the lock was written at 03:14:53, it got `"status": "PERMISSION_DENIED"`, `HTTP 403`. The audit log, the platform's own record of who did what, which we cannot edit, shows the same refusal under the leftover login. A real request for 15% off still came back with the back office's decision.

The leftover's route is closed and the business path works; project-wide roles and the store website's direct route were untouched. Open `/config/Desktop/novasmart-evidence/m2/m2_step4.txt` and find `PERMISSION_DENIED`.

## Two controls on the way out

<!-- FIGURE:L2_04 BEGIN -->

![The title reads: Two controls, two questions. Two cards side by side. A blue card with a route icon: Where it may reach, a white pill reading novasmart-egress-gateway, and Gateway log records its decision. A green card with a database icon: What it may do, then three lines: Read pricing data, not change it; Change refused in BigQuery's log; Table's last change did not move. Under the blue card, an amber note reads Slow check? Request goes through.](images/L2_04_two_controls.webp)

<!-- FIGURE:L2_04 END -->

Step 5 handled the other direction. agy put the back office behind NovaSmart's outbound gateway, an Agent Gateway that decides where it may reach, then cut its BigQuery role (BigQuery is where NovaSmart keeps its customer and business data) from full control to running queries and reading the pricing data.

The proof comes from records the agent cannot write. The gateway's log shows its decision on the back office's traffic to BigQuery, though not who called. BigQuery's audit log shows a change refused under the back office's Agent Identity, and the table's last-modified time did not move. The database permissions refused the change, not the gateway. One gateway setting matters: if its access check fails or cannot answer within a second, the request goes through.

## Where this shows up

<!-- FIGURE:L2_05 BEGIN -->

![The title reads: Same lock, other industries, with a tag reading Illustration. Four cards, each with an icon: Retail, Margin agent names one caller, in blue; then, in gray, Banking, Eligibility service names the loan app; Healthcare, Records agent names the clinic app; and Utilities, Billing engine names the invoicing agent. A gray bar beneath reads: The back end names who may call.](images/L2_05_same_lock_elsewhere.webp)

<!-- FIGURE:L2_05 END -->

Three scenarios, made up to illustrate the pattern:

- **Scenario: the eligibility service.** A bank's loan-eligibility agent names the loan app as its caller, not a test login left from a migration.
- **Scenario: the shortcut nobody mentioned.** A billing engine names the invoicing agent, but a reporting app was wired straight to it years ago.
- **Scenario: reads, not writes.** A clinic's records agent reads patient charts but cannot change them; the database's refusal record proves it.

[Google's IAM documentation](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control) says "The effective allow policy for a resource is the union of the allow policy set at that resource and the allow policy inherited from its parent." So a project-wide grant reaches every agent.

## Your call: lockdown or outage

<!-- FIGURE:L2_06 BEGIN -->

![The title reads: Lockdown or outage? Four tall cards joined by arrows, left to right. Two amber cards with question-mark icons: Who reaches it today? (Read both lists) and What breaks if we lock it? (Ask before you lock). Two blue cards with gear icons: Lock the list on the agent (Name who is in) and Test the door and the business (A refusal plus a real answer). An amber band across the bottom, with a question-mark icon, reads Is a list on the agent enough?](images/L2_06_lockdown_or_outage.webp)

<!-- FIGURE:L2_06 END -->

Step 2 was the pause before any change. The lock closed one route of four; the front desk's business call still worked, and the store website's direct route and project-wide roles were untouched.

- **Least privilege:** giving a job only the access it needs and nothing more, including who may call an agent.
- **Name who is in:** list the callers you want on the agent, rather than accepting whoever holds a grant.

Is a list on the agent enough while project-wide roles bypass it? Write that cleanup down.

## Where your estate stands

<!-- FIGURE:L2_07 BEGIN -->

![The title reads: Where your estate stands after Module 2. A row of six tall segments, left to right: Visible, Attributable, Least privileged, Access controlled, Screened, Measured, tagged M1, M1, M1, M2, M3 and M4 · optional. Visible and Attributable are green; the other four are gray. Least privileged carries a small amber marker above it reading Three agents only, and Access controlled one reading Back office only.](images/L2_07_estate_progress.webp)

<!-- FIGURE:L2_07 END -->

Module 2 built Access controlled for one agent, the back office. Still open: project-wide roles that can call any agent, the store website's direct route, and every other agent. Least privileged now covers three agents; the front desk still holds broad database rights.

| Property | What it means | Where you build it |
| :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 |
| Attributable | Every action traces to one named agent | M1 |
| Least privileged | Each agent holds only the access its job needs | M1 |
| Access controlled | Only approved callers can reach a sensitive agent | M2 |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) |

Two agents face customers and hand whatever a shopper types to the AI. M3 · Protect the Content is where you screen what customers can talk your agents into.

## Questions to take back to your team

- Who can call our most sensitive agents today, not who should?
- Which callers are named on the agent, and which come through broad roles?
- Before we lock something down, who checks what would break?
- Can we show a refusal we caused and a business call that still worked?
- Who owns removing broad roles that can call any agent?

## Read more

| Topic | Official page |
| :-- | :-- |
| Who may call an agent | [Share an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/share-agent) |
| Each agent's own badge | [Use Agent Identity with Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity) |
| The outbound gateway | [Agent Gateway overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview) · [Route Agent Runtime traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy) |
| The gateway's access check | [Delegate authorization with Service Extensions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/delegate-authorization) |
| Why project-wide grants reach every agent | [Using resource hierarchy for access control](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control) |
| A role that only calls | [Create and manage custom roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) |
| Read, not change, in BigQuery | [BigQuery IAM roles and permissions](https://docs.cloud.google.com/bigquery/docs/access-control) |
| How long a change takes | [Access change propagation](https://docs.cloud.google.com/iam/docs/access-change-propagation) |
| Who did what, and when | [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit) · [BigQuery audit logs overview](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs) |

For the story behind each step, see the matching Step section on the Reference Guide tab.
