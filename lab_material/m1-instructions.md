# M1 · Take Action — Instructions

M1 fixes what M0 found, using Agent Registry (the catalog of what you run) and Agent Identity (each agent's own badge). agy acts without asking first and records every change with a way to undo it.

> **Before you start**
> - Start a new agy conversation for M1 before Step 1. One long conversation carries every earlier module's history, which slows agy down and makes its answers less reliable.
> - If replies are slow, ask agy to skip the pictures; every step works the same without them.

## Key objective

Give the promo agent a named owner and every agent its own login, so each customer-data read is recorded under the agent that made it.

- Register the promo agent under a named owner.
- See what the shared login can do today, changing nothing.
- Give each agent its own login, with only what its job needs.
- Remove customer-data access from the agent that never needed it.
- Read the audit log back and see each read named by one agent.

Why it matters: while two agents share one login, the record never names the agent, and any access one needs, the other gets.

## Where we left off

- One agent was running that nobody had catalogued: the marketing promo agent, `promo-agent-shadow`.
- It shares one login with the Customer Personalization Agent, so the log names that login, never either agent. Price Match and Markdown Strategy already sign in as themselves.
- The leadership call: own it, don't kill it.

## Step 1 · Register the shadow agent

<!-- FIGURE:K1S1 BEGIN -->

![Map of the NovaSmart estate, M1 Step 1: agy (1) reads the running promo service on Cloud Run and (2) adds an entry for it in Agent Registry. The promo agent now shows a green 'cataloged · owner set' tag but stays amber, still on the shared login with the personalization agent.](images/K1S1_map.webp)

<!-- FIGURE:K1S1 END -->

**Goal:** Put the agent nobody knew about on the official record, under a team you can hold accountable.

Ask agy:

```
Register the promo agent in our catalog, owned by the marketing team.
```

**What to expect:**

- agy adds the running promo agent to Agent Registry with the marketing team as its owner and a risk tier, and shows you the entry.
- This closes the visibility gap only: the agent is visible and owned, but still shares a login and still reads customer records.
- One change: the new catalog entry, which can be undone.

More background: Reference Guide tab, Register the shadow agent

## Step 2 · See what that shared login can do

<!-- FIGURE:K1S2 BEGIN -->

![Map of the NovaSmart estate, M1 Step 2, read only: agy (1) reads what the shared login may do and (2) reads the customer dataset's access list. The shared login, used by the personalization and promo agents, is amber with a tag 'read · change · delete · all data', and the whole BigQuery group is outlined amber. Nothing changes.](images/K1S2_map.webp)

<!-- FIGURE:K1S2 END -->

**Goal:** See what the shared login can do today, against what each agent's job needs.

Ask agy:

```
Don't change anything yet. What can that shared login actually do today?
```

**What to expect:**

- A plain-English readout of every power attached to the shared login and, beside it, what each agent's job needs.
- Read it line by line and ask: does this agent have more power than its job needs? Something is far larger than it should be.
- Nothing in your environment changes.

More background: Reference Guide tab, See what that shared login can do

## Step 3 · Give each agent its own login

<!-- FIGURE:K1S3 BEGIN -->

![Map of the NovaSmart estate, M1 Step 3: agy (1) switches the personalization agent to its own agent identity, (2) gives the promo agent a new login of its own and (3) removes the shared login's data access. The personalization agent turns green ('own identity'), the promo agent's tag reads 'cataloged · own login', and the shared login is grey, 'unused', with no agent attached.](images/K1S3_map.webp)

<!-- FIGURE:K1S3 END -->

**Goal:** Replace the shared, oversized login with separate identities, each scoped to its job.

Ask agy:

```
Give each agent its own login, with only what its job needs.
```

**What to expect:**

- The personalization agent moves to a platform-issued agent identity: no account or key, and the audit log records its own identity.
- The promo agent runs on Cloud Run, which cannot hold one, so it gets its own service account that can only read the bucket its code is loaded from.
- Moving the personalization agent removes the access it inherited, so agy grants it back and has the agent read customer data to show it works.
- Changes: two new identities with their access, and the shared login's project-wide data power removed; it has no users left. Takes a few minutes; agy can undo it.

More background: Reference Guide tab, Give each agent its own login

## Step 4 · Cut off what shouldn't have access

<!-- FIGURE:K1S4 BEGIN -->

![Map of the NovaSmart estate, M1 Step 4: agy (1) checks the promo agent's login and (2) checks the customer dataset's access list. The promo agent's line to novasmart-mcp is now grey dashed with no arrowhead, so it has no route to customer data, and the box is green; the personalization agent's path through novasmart-mcp to customer data is green, 'read kept'.](images/K1S4_map.webp)

<!-- FIGURE:K1S4 END -->

**Goal:** Make sure the promo agent, which writes promotional copy, has no route to customer records.

Ask agy:

```
Marketing doesn't need our customer database. Take that access away, and leave the others working.
```

**What to expect:**

- agy checks the promo agent's routes to customer data, leaving the Customer Personalization Agent and the Price Match Agent working.
- If a path is still open, agy removes it. If Step 3 already closed it, agy says so rather than inventing a change. Either is a pass.
- The only possible change: removing access that remained, which can be undone.

More background: Reference Guide tab, Cut off what shouldn't have access

## Step 5 · Prove it worked

<!-- FIGURE:K1S5 BEGIN -->

![Map of the NovaSmart estate, M1 Step 5: agy (1) sends test calls through the personalization agent and the promo agent, then (2) reads Cloud Audit Logs, which is highlighted. Two dashed outcomes end at the log: (3, green) the customer-data read recorded under the personalization agent's own identity, and (4, red) the promo agent's attempt, denied. Nothing changes.](images/K1S5_map.webp)

<!-- FIGURE:K1S5 END -->

**Goal:** Check that the Cloud Audit Logs record you read in M0 can now say which agent read customer data.

Ask agy:

```
Show me the customer data log again. Can you prove who did what now?
```

**What to expect:**

- agy triggers a legitimate read and a promo agent attempt, checks Price Match answers, waits a few minutes for the log to catch up, then reads it.
- Every read names exactly one agent. The personalization agent's email column is blank, as it should be; its identity is in another field.
- The promo agent's attempt shows as denied, yet the store app reports the campaign launched with zero records: the log is the evidence, not the app.
- agy saves the table to `m1_step5.txt` (`novasmart-evidence` folder on your Desktop), says how many of 16 checks it proved, and links your Governance Scorecard; open that link in Chrome yourself. Nothing in your environment changes.

More background: Reference Guide tab, Prove it worked

## Step 6 · What's next

<!-- FIGURE:K1S6 BEGIN -->

![Map of the NovaSmart estate, M1 Step 6: what M1 put in place is green, the promo agent cataloged on its own login with no route to customer data, the personalization agent on its own identity with its read kept, and the shared login unused. The back-office Markdown Strategy Agent is outlined in amber with its two callers, the store portal and the Price Match Agent, tagged 'M2 · its callers'.](images/K1S6_map.webp)

<!-- FIGURE:K1S6 END -->

*Optional.* You can go straight to M2, or open the **What did we learn?** tab.

> **Going to M2?** Start a new agy conversation first, then ask M2's first prompt there.

- You can now see every agent you run and prove which one touched customer data.
- Still open: which agents may talk to each other. The back-office Markdown Strategy Agent reads confidential margin data and should only be called by another agent; nothing enforces that.
- M2 · Control the Connections is where you decide who may call whom, starting with who is allowed to call that back-office margin agent.

## See it in the console

- [Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents) — set Location to your lab's region; Promo Agent is now one of five rows, owner in its description.
- The same Agent Registry page — Identity shows customer-personalization-agent's own agent identity; Promo Agent shows a dash (the catalog does not display a Cloud Run login).
- [Logs Explorer](https://console.cloud.google.com/logs/query;query=logName%3A%22cloudaudit.googleapis.com%252Fdata_access%22%0A%28protoPayload.metadata.tableDataRead%3A%2A%20AND%20resource.labels.dataset_id%3D%22customer_data%22%29%0AOR%20%28protoPayload.status.code%3D7%20AND%20resource.type%3D%22bigquery_project%22%29;duration=P1D) — personalization reads show an empty email (principalSubject names the identity); promo attempts show Access Denied under promo-agent-sa.

## Try this too — optional

*Optional.* Ask any of these, in any order, or skip them.

Ask agy:

```
Show me everything you changed today. Did you touch anything I didn't ask for?
```

This shows you every change agy made today, including ones you never asked for, and how to reverse each.

Ask agy:

```
Is anyone else reading customer data, and did anything I did today change that?
```

This shows you every identity that actually reads customer records, beyond the two agents in the story.

Ask agy:

```
What would break if I just deleted that login?
```

This shows you what depended on that shared login, the question worth asking before you take any access away.

## Step 7 · Show what you changed

*Optional.* You can skip this and go to M2, or open the **What did we learn?** tab.

Pick any of these, in any order. Each takes agy a few minutes.

```
Build me a before-and-after map of how each agent got its own login.
```

Who signs in as what, before and after; a good place to start.

```
Build me a replay of every change I made in this module, in order.
```

A replay of your changes, in order.

```
Build me a page that shows an auditor the proof that this worked.
```

The proof, laid out for an auditor.

```
Build me a game called Key Master from what I changed, for my team to play.
```

A game for your team.

```
Turn what I changed into a two-minute update I can present to the board.
```

A two-minute update for your board.

Pages are saved in the novasmart-showcase folder on your Desktop, built only from what agy recorded in Steps 1 to 5. agy gives you each page's file name but cannot open a browser window in this lab: in Chrome, go to `file:///config/Desktop/novasmart-showcase/` and click the page. Nothing in your environment changes.

> **Going to M2?** Start a new agy conversation first, then ask M2's first prompt there.
