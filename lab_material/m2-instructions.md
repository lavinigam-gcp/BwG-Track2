# M2 · Control the Connections — Instructions

M2 settles who may call your most sensitive agent, and what that agent may reach and change.

> **Before you start**
> - Start a new agy conversation for M2 before Step 1. One long conversation carries every earlier module's history, which slows agy down and makes its answers less reliable.
> - If replies are slow, ask agy to skip the pictures; every step works the same without them.

## Key objective

Control who may call the back-office agent, using the caller list held on the agent itself.

- Read who can reach the back-office agent holding NovaSmart's cost and margin data.
- See what a lockdown would cost before you order one.
- Rewrite the agent's caller list so it names one caller: the Price Match Agent.
- Watch the platform refuse the leftover test login; check the real escalation still works.
- Put the back office behind the outbound gateway and stop it changing the pricing data.

Why it matters: reading the margin data and asking the agent that holds it are two different permissions.

## Where we left off

- Every agent signs in as itself, the shadow agent has an owner, and the marketing agent can no longer reach customer records.
- Still open: which agent may call which. The Price Match Agent (the front desk) escalates discounts above 10% to the Markdown Strategy Agent (the back office), which holds the margin data.

## Step 1 · See who can call the back office

<!-- FIGURE:K2S1 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 1. 1: agy reads the Markdown Strategy Agent's own caller list. 2: the one login on it, test-agent-caller, a leftover test login marked amber, calls the back office and gets in. The project-wide roles, which reach any agent, are drawn alongside. No setting changes.](images/K2S1_map.webp)

<!-- FIGURE:K2S1 END -->

**Goal:** Find out who can reach the agent holding your margin data today.

Ask agy:

```
Who can call our back-office margin agent right now?
```

**What to expect:**

- agy reads the back office's own list of permitted callers. It holds one name: test-agent-caller, an unowned leftover test login.
- The front desk is not on that list, a first clue that the list is not the whole story.
- agy makes one real call as that login and shows what came back, a before for Step 4.
- Nothing in your environment changes.

More background: Reference Guide tab, See who can call the back office

## Step 2 · See what locking it down would cost

<!-- FIGURE:K2S2 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 2: the routes into the Markdown Strategy Agent today. 1: test-agent-caller's route, in amber, is the one a lock to the front desk would stop. 2: the store portal's direct route would stay. 3: the Price Match Agent's A2A route would stay. The project-wide roles still reach any agent. No setting changes.](images/K2S2_map.webp)

<!-- FIGURE:K2S2 END -->

**Goal:** Check what a lockdown would break before you act.

Ask agy:

```
Don't change anything yet. If I lock it down to just the front desk, what would break?
```

**What to expect:**

- A plain-English readout of who reaches the back office today, and which routes are real business traffic.
- What would stop working if only the front desk were left. Read it before you act.
- Nothing in your environment changes.

More background: Reference Guide tab, See what locking it down would cost

## Step 3 · Lock it to the front desk

<!-- FIGURE:K2S3 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 3. 1: agy rewrites the Markdown Strategy Agent's caller list. 2: the Price Match Agent's A2A route, in green, is now the listed caller. 3: test-agent-caller, greyed out with a dashed line, is off the list. The project-wide roles are unchanged.](images/K2S3_map.webp)

<!-- FIGURE:K2S3 END -->

**Goal:** Rewrite the back office's own caller list so it names one caller, the front desk.

Ask agy:

```
Lock the back office so only the price-match agent can call it.
```

**What to expect:**

- agy shows the list before and after: the Price Match Agent is now the one name on it, and the leftover login's direct grant is gone.
- The list governs only calls coming in; Step 5 handles what the back office reaches on its way out.
- Access changes take a few minutes to settle. Store traffic keeps flowing.
- One change: the back office's caller list. Tell agy to undo it if anything looks wrong.

More background: Reference Guide tab, Lock it to the front desk

## Step 4 · Prove the rogue caller is out

<!-- FIGURE:K2S4 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 4. 1: test-agent-caller's replayed call is refused at the back office, in red. 2: agy sends a price match to the Price Match Agent, which escalates. 3: its A2A call to the Markdown Strategy Agent is answered, in green. The project-wide roles are unchanged and not exercised.](images/K2S4_map.webp)

<!-- FIGURE:K2S4 END -->

**Goal:** Show the leftover login is refused and a genuine price match above 10% still gets the back office's answer.

Ask agy:

```
Try calling it as that rogue login again, and check the real escalation still works.
```

**What to expect:**

- agy repeats the Step 1 call as test-agent-caller and quotes the platform's refusal word for word, and looks for it in Cloud Audit Logs.
- The escalation uses SKU-HSE-4001, the air purifier: $349.00 at NovaSmart, $296.65 at BetaBuy, 15% off. It counts only if the back office's decision comes back; otherwise agy retries once, then marks it not verified.
- If the answer says no competitor is verified at that price, the request used the wrong price; agy reruns it with the $296.65 BetaBuy listing.
- Nothing changes. The checks go to `m2_step4.txt` in the `novasmart-evidence` folder on your Desktop.

More background: Reference Guide tab, Prove the rogue caller is out

## Step 5 · Lock down what the back office can reach and do

<!-- FIGURE:K2S5 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 5, with the M1 fixes in green and test-agent-caller still refused. 1: the outbound gateway is attached to the Markdown Strategy Agent, so its traffic to BigQuery MCP runs through it. 2: the back office's BigQuery access is narrowed to read. 3: reads of the pricing and competitor data are allowed, in green. 4: a change is refused by BigQuery, in red, and recorded in Cloud Audit Logs.](images/K2S5_map.webp)

<!-- FIGURE:K2S5 END -->

**Goal:** Limit where the back office can reach and stop it changing the pricing data. This is the longest step.

Ask agy:

```
Make sure the back office can only reach what it needs, and can only read the pricing data, not change it.
```

**What to expect:**

- Two controls: the outbound gateway decides where the back office may reach; its database permissions now let it read the pricing tables, not change them.
- Expect pauses: about four minutes for the gateway attach, three for permissions, three more before agy reads the records.
- agy calls the back office directly through a broad project-wide role. A read answers; a change is refused, shown by the BigQuery audit log and the table's unchanged last-modified time, not by the gateway's allow.
- The pricing data is read-only for the back office only; other accounts can still change it. agy writes `m2_step5.txt` and updates your Governance Scorecard (open its link in Chrome yourself); a FAIL names the step to revisit.

More background: Reference Guide tab, Lock down what the back office can reach and do

## Step 6 · What's next

<!-- FIGURE:K2S6 BEGIN -->

![Map of the NovaSmart agent estate, M2 Step 6. In place: the Price Match Agent is the listed caller, the outbound gateway is attached to the back office, which reads the pricing and competitor data while its changes are refused, and test-agent-caller is refused. Still open, in amber: the project-wide roles that reach any agent. Outlined in amber as M3's target: Model Armor and the inbound gateway, for screening what customers send the front desk.](images/K2S6_map.webp)

<!-- FIGURE:K2S6 END -->

*Optional.* You can go straight to M3, or open the **What did we learn?** tab.

> **Going to M3?** Start a new agy conversation first, then ask M3's first prompt there.

- The back office's list names one caller, the leftover login is refused, the escalation gets the back office's answer if Step 4 recorded one, and the back office reads but cannot change the pricing data.
- Still open: broad project-wide roles can still call any agent; agy's Step 5 call used one.
- M3 · Protect the Content is where you screen what customers can talk your agents into.

## See it in the console

- [Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents) — set Location to your lab's region; the back office is markdown-strategy-agent. Its caller list is not shown.
- [Agent Gateway](https://console.cloud.google.com/agent-platform/gateways) — novasmart-egress-gateway, the outbound one the back office now sits behind.

## Try this too — optional

*Optional.* Ask any of these, in any order, or skip them.

Ask agy:

```
Which of those broader permissions would you take away first, and what would break if we did?
```

This shows you which wider grants could be cut safely and which the agents depend on.

Ask agy:

```
We closed the door on that leftover login. Does anyone still have its keys?
```

This shows you the difference between closing an access list and retiring a credential.

Ask agy:

```
Does any other agent have a list like this, or is the back office the only one?
```

This shows you how far the pattern reaches, and what governs calls to other agents.

## Step 7 · Show what you controlled

*Optional.* You can skip this and go to M3, or open the **What did we learn?** tab.

Pick any of these, in any order. Each takes agy a few minutes.

```
Build me a map of who can call our back-office agent, before and after.
```

Who could call the back office, before and after.

```
Build me a replay of the door test: the leftover login refused, the front desk answered.
```

The Step 4 door test, replayed.

```
Build me an explainer of the two controls I put on the back office.
```

The gateway and the read-only permissions, explained.

```
Build me a game called Gatekeeper from what I controlled, for my team to play.
```

A game built from your results.

```
Turn what I controlled into a two-minute update I can present to the board.
```

A short board update.

Pages are saved in the novasmart-showcase folder on your Desktop, built only from what agy recorded in Steps 1 to 5. agy gives you each page's file name but cannot open a browser window in this lab: in Chrome, go to `file:///config/Desktop/novasmart-showcase/` and click the page. Nothing in your environment changes.

> **Going to M3?** Start a new agy conversation first, then ask M3's first prompt there.
