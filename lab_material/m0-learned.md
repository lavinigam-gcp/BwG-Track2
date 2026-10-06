# M0 · See Everything — What did we learn?

*Read this after you finish Module 0. It names what you found, so you can explain it in your own words.*

**In one sentence:** NovaSmart's official list of AI agents was incomplete, and its logs could not say which agent read customer data.

In this lab, your **estate** means every AI agent and tool NovaSmart runs.

## What each prompt tested

<!-- FIGURE:L0_01 BEGIN -->

![The title reads: What each prompt tested. Three rows, each read left to right with arrows: question, product, finding. What do we have? leads to Agent Registry, which found 6 agents, 3 are ours. What is running? leads to Agent Runtime + Cloud Run, which found Running, not listed, with promo-agent-shadow in a red box. Who read customer data? leads to Audit logs + agent settings, which found One login, two agents, with novasmart-customer-sa in an amber box.](images/L0_01_what_each_prompt_tested.webp)

<!-- FIGURE:L0_01 END -->

Step 1 confirmed your environment was ready. After that, each prompt asked one question of Google Cloud.

- **Step 2** asked the official catalog, Agent Registry. It lists what was registered: agents on Agent Runtime and Google's built-in agents are added automatically, but an agent on Cloud Run is added only if its team opts in. Three of the six agents listed are Google's built-ins.
- **Step 3** asked what is actually running, on Agent Runtime (Google Cloud's managed service for running agents) and Cloud Run (Google Cloud's service for running any container — a website, a tool, or an agent). One agent was running that no central list knows about: a shadow agent.
- **Step 4** asked the audit log, the platform's own record of who did what, which we cannot edit. It named one login: a service account, which is a login for a program rather than a person. Re-reading each agent's settings showed that two agents use that login.

## Two gaps: seeing versus proving

<!-- FIGURE:L0_02 BEGIN -->

![The title reads: Visibility vs accountability. Two panels side by side. Left, Visibility gap: a Catalog list and a Running list share three matching entries, and the Running list has one more item, promo-agent-shadow, with an empty dashed slot opposite it in the Catalog list. Right, Accountability gap: Customer Personalization Agent and promo-agent-shadow both point to one login, novasmart-customer-sa, which reads Customer data: names, emails. A dashed arrow leads down to an Audit log that reads: Records the login, not the agent. A bar across the bottom reads: Fixing one gap does not fix the other.](images/L0_02_visibility_vs_accountability.webp)

<!-- FIGURE:L0_02 END -->

**Visibility** means knowing what is running. **Accountability** means being able to say which agent did something. Module 0 found one gap of each kind.

Fixing one does not fix the other. Registering the promo agent would make it visible, and could give it an owner, but it would still share a login and still read customer records.

## Why the log can't name the agent

<!-- FIGURE:L0_04 BEGIN -->

![The title reads: Two workers, one badge, with a tag reading Analogy. Worker A and Worker B, shown as gear icons, both point to one amber card, One shared badge. From the badge, arrows lead to two blue buildings: Building A: Cloud Run and Building B: Agent Runtime. A dashed arrow leads down to a Door log that records Badge, building, time, with a red tag reading No name. A bar across the bottom reads: Guess by building, not proof.](images/L0_04_shared_badge_analogy.webp)

<!-- FIGURE:L0_04 END -->

`promo-agent-shadow` and the Customer Personalization Agent share one login, `novasmart-customer-sa`, so the log shows the same name for both. Like a door log with a shared badge, it records the badge, not the worker.

Today you can still tell them apart, because the log notes which service used the login: Cloud Run for one, Agent Runtime for the other. That is a guess by location, not proof. [Google's own guidance](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts) says the same: "Cloud Audit Logs include the name of the service account that performed a change or accessed data, but they don't show the name of the application that used the service account."

## The proof, and the regulator question

<!-- FIGURE:L0_05 BEGIN -->

![The title reads: What the log can tell. Two log rows: 22:34:10, Cloud Run, 5 columns, names and emails; and 22:34:23, Agent Runtime, 7 columns. Both rows connect to one amber login, novasmart-customer-sa. Below, a blue box reads Log can tell: Login, time, service, columns. A red box reads Log cannot tell: Which agent, which customer.](images/L0_05_what_the_log_can_tell.webp)

<!-- FIGURE:L0_05 END -->

These are two earlier reads of the customer table, recorded on October 2, 2026 (UTC) and found by our October 3 test run. Your times will differ. The 22:34:10 read came through Cloud Run, where, by the lab's setup, the promo agent is the only service on that login. So the most likely reader of those names and emails is the agent with no owner. Most likely, not proven.

Could you answer a regulator who asked who read a particular customer's record? Only partly. You could hand over the login, the time, the service and the columns. You could not name the agent or the customer, because no field in those log rows names either.

Check it yourself: open `/config/Desktop/novasmart-evidence/m0/m0_step4.txt` and find `novasmart-customer-sa`.

## Where this shows up

<!-- FIGURE:L0_07 BEGIN -->

![The title reads: Same gaps, other industries, with a tag reading Illustration. Four panels, each with an icon: Retail with customer records, in blue; then, in gray, Healthcare with patient records, Banking with account data, and Manufacturing with supplier data. An amber bar beneath reads: Unlisted agent + shared login, with an arrow to: No one can prove who touched it.](images/L0_07_same_gaps_other_industries.webp)

<!-- FIGURE:L0_07 END -->

Swap "customer records" for your own sensitive data and the pattern holds. Three scenarios, made up to illustrate it:

- **Scenario: the auditor's list.** An auditor asks for every AI agent you run, with an owner. You export the catalog, and the agent a team shipped on the side is not on it.
- **Scenario: the 2 a.m. call.** Security sees a bulk read of customer names and emails under one shared login. You can't switch off the bad reader without also breaking the good agent.
- **Scenario: Friday ship, Monday shadow.** A team ships an agent on Friday as an ordinary Cloud Run web service, reusing an existing login to make a deadline. By Monday it is reading customer emails and is on no list.

One more fact: most Google Cloud services record reads of data only if someone switches that on. BigQuery, where NovaSmart keeps its data, records them by default, which is why these reads were in the log.

## Your call: own it or kill it

<!-- FIGURE:L0_06 BEGIN -->

![The title reads: Own it or kill it. At the top, promo-agent-shadow in red, which reads customer records. An arrow leads down to a box, First, ask, with two questions: What does its job need? and What can it reach if misused? The second question carries a red answer: Today: at least the whole customer table. From that box, two amber arrows lead to two equal amber boxes: Kill it (Fast, hides the problem, breaks a team) and Own it (Named owner, access cut to the job).](images/L0_06_own_it_or_kill_it_flow.webp)

<!-- FIGURE:L0_06 END -->

Step 5 was your decision, with no prompt. M1 tells you what NovaSmart's leaders chose, so you can compare. Two ideas frame it:

- **Least privilege:** giving a job only the access it needs and nothing more. A marketing agent's job may not need every customer's name and email; that is the question Step 5 asked.
- **Blast radius:** how far the damage reaches if this is misused or stolen. By the lab's setup, anything running under the shared login can reach at least the whole customer table.

## Where your estate stands

<!-- FIGURE:L0_03 BEGIN -->

![The title reads: Where your estate stands after Module 0. A row of six tall gray segments, left to right: Visible, Attributable, Least privileged, Access controlled, Screened, Measured, tagged M1, M1, M1, M2, M3 and M4 · optional. Visible and Attributable each carry a small red marker above them reading Gap found in M0.](images/L0_03_estate_progress.webp)

<!-- FIGURE:L0_03 END -->

The lab builds toward six properties for your estate. None of them is true yet. Module 0 found the gaps behind the first two and raised the question behind the third.

| Property | What it means | Where you build it |
| :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 |
| Attributable | Every action traces to one named agent | M1 |
| Least privileged | Each agent holds only the access its job needs | M1 |
| Access controlled | Only approved callers can reach a sensitive agent | M2 |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) |

M1 · Take Action is where you fix it: register the shadow agent, give each agent its own identity, and scope its access down to what its job actually needs.

## Questions to take back to your team

- Do we have one list of every AI agent we run, with a named owner against each? Who keeps it current?
- When did we last check that list against what is actually running, including systems vendors run for us?
- Do any of our agents share a login? If one misbehaved, could our logs say which one?
- If a regulator asked who read a particular customer's record, what could we hand over today?
- Which agent could do the most damage if it were misused, and does it need that much access?

## Read more

| Topic | Official page |
| :-- | :-- |
| The agent catalog | [Agent Registry overview](https://docs.cloud.google.com/agent-registry/overview) |
| How agents get into the catalog | [Use automatic registration](https://docs.cloud.google.com/agent-registry/automatic-registration) |
| Where agents run | [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) · [What is Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run) |
| Logins for programs | [Service accounts overview](https://docs.cloud.google.com/iam/docs/service-account-overview) |
| Why not to share a login | [Best practices for using service accounts securely](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts) |
| Who did what, and when | [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit) · [Enable Data Access audit logs](https://docs.cloud.google.com/logging/docs/audit/configure-data-access) |
| Least privilege | [Use IAM securely](https://docs.cloud.google.com/iam/docs/using-iam-securely) |
| Each agent's own badge (M1) | [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview) |

For the story behind each step, see the matching Step section on the Reference Guide tab.
