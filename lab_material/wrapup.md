# Wrap-up

You took NovaSmart's AI estate from unmapped to governed, one module at a time, by asking agy in plain English.

## Before and after

| | When you started | When you finished |
| :-- | :-- | :-- |
| The catalog | Missing the promo agent, which had no owner | Lists every running agent, each with an owner |
| Logins | Two agents shared one login that could reach the whole customer table | Each agent signs in as itself |
| Customer-data reads | The audit log named only the shared login | The audit log names the one agent that read |
| The back-office agent | A leftover test login could call it, and it could change pricing data | Its caller list names one caller, the Price Match Agent; it reads pricing data but cannot change it |
| Customer messages | Reached the agents unscreened | Screened before the Price Match Agent reads them |
| Agent quality | Never measured | Scored case by case, with reasons (M4, optional) |

## Your path

| Module | What you did | Products | Concepts |
| :-- | :-- | :-- | :-- |
| **M0 · See Everything** | Compared the catalog with what really runs, and checked who read customer data. Changed nothing. | Agent Registry, Agent Runtime, Cloud Run, Cloud Audit Logs | Shadow AI; a shared login hides which agent acted |
| **M1 · Take Action** | Registered the hidden agent under an owner, gave each agent its own login, and cut customer-data access back | Agent Registry, Agent Identity, IAM | One agent, one identity; least privilege; blast radius |
| **M2 · Control the Connections** | Named one caller for the back-office agent, put it behind the outbound gateway, and made pricing data read-only for it | Agent Gateway, IAM, BigQuery | Name who may call an agent; see what a lockdown costs before you order one |
| **M3 · Protect the Content** | Watched agy talk two agents out of their rules, then screened one at the inbound gateway and replayed the attacks | Model Armor, Agent Gateway | Screen at the door; know which agents a screen covers; fail open |
| **M4 · Evaluate and Decide** *(optional)* | Scored the agent against its policy, had the tooling write a tougher set, and measured a fix on a local copy | Gen AI evaluation service, agents-cli | Evaluation; read the rows, not the total; a fix on a copy is not in production |

## Six properties of a governed estate

| Property | What it means | Built in | Covers now |
| :-- | :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 | Every running agent |
| Attributable | Every action traces to one named agent | M1 | Every customer-data read |
| Least privileged | Each agent holds only the access its job needs | M1, M2 | Three agents; not yet the Price Match Agent |
| Access controlled | Only approved callers can reach a sensitive agent | M2 | The back-office agent |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 | The Price Match Agent |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) | The Price Match Agent |

## Still open

- The screen covers one agent, and lets traffic through if it cannot run.
- Broad project-wide roles can still call any agent.
- The Price Match Agent still holds broad database rights.
- The M4 fix is on a local copy, not deployed.

## How you worked

- You described what you wanted in plain English; agy ran every command.
- Every claim agy made is backed by a saved record: the `novasmart-evidence` folder on your Desktop, one file per step.

## The habit to take home

Find out what is running, make every action traceable to one actor, decide who may reach what, screen what flows through, then measure before you trust it.

## Take it with you

- [Skills and lab materials on GitHub](https://github.com/lavinigam-gcp/BwG-Track2): the skill, and every module's instructions and guides.
- Questions about the lab: the **Ask agy** button under the left nav.

## Glossary

### Products

Agent Registry, Agent Runtime, Agent Identity and Agent Gateway are part of Gemini Enterprise Agent Platform.

| Product | What it is | Learn more |
| :-- | :-- | :-- |
| Antigravity (agy) | The AI agent you worked with; it ran every command and saved the evidence | [Antigravity CLI](https://antigravity.google/docs/cli/install/) |
| Agent skills | Instructions that steer agy; this lab's skill is in the repo | [Agent skills](https://antigravity.google/docs/skills) |
| Agent Registry | The official catalog of the agents you run, with their owners | [Agent Registry overview](https://docs.cloud.google.com/agent-registry/overview) |
| Agent Runtime | Google Cloud's managed service for running agents | [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) |
| Agent Identity | The per-agent badge that makes every action traceable to one agent | [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview) |
| Agent Gateway | Decides which agent may reach which agent or tool, inbound and outbound | [Agent Gateway overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview) |
| Model Armor | Screens what is sent to an agent for attempts to talk it out of its rules | [Model Armor overview](https://docs.cloud.google.com/model-armor/overview) |
| Gen AI evaluation service | Scores an agent's answers case by case, using a separate judge model | [Gen AI evaluation service overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview) |
| agents-cli | Command-line tool for building and evaluating agents; it wrote M4's tougher test set | [Agents CLI](https://google.github.io/agents-cli/) |
| IAM | The system that decides who is allowed to do what | [IAM overview](https://docs.cloud.google.com/iam/docs/overview) |
| Service accounts | A login for a program rather than a person; how an agent signs in | [Service accounts overview](https://docs.cloud.google.com/iam/docs/service-account-overview) |
| Cloud Run | Google Cloud's service for running any container: a website, a tool, or an agent | [What is Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run) |
| BigQuery | Google Cloud's data warehouse, where NovaSmart keeps its customer and business data | [BigQuery overview](https://docs.cloud.google.com/bigquery/docs/introduction) |
| Cloud Audit Logs | The platform's own record of who did what, which you cannot edit | [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit) |

### Concepts

| Concept | In plain words | Module |
| :-- | :-- | :-- |
| Shadow AI | An agent running in the business that no central list knows about | M0 |
| Shared login | One login used by several agents, so the log cannot tell them apart | M0 |
| Attribution | Tying every action to the one agent that took it | M1 |
| Least privilege | Giving a job only the access it needs and nothing more | M1, M2 |
| Blast radius | How far the damage reaches if a login is misused or stolen | M1 |
| Re-grant before you revoke | Give the new login what it needs before removing the old access, so the agent keeps working | M1 |
| Caller list | Who may call an agent; name the callers you want instead of accepting whoever holds a grant | M2 |
| Project-wide role | Access granted across everything in the project, not on one resource | M2 |
| Prompt injection | Wording meant to talk an agent out of its rules | M3 |
| Screen at the door | Check what a customer sent before the agent reads it | M3 |
| Fail open | If the screen cannot run, traffic goes through unscreened | M3 |
| Evaluation | Running an agent against many known cases and scoring each answer | M4 |
| Judge model | A second model that scores each answer, separate from the agent's own | M4 |
| Configured is not running | A fix measured on a copy is not in production until someone deploys it | M4 |
