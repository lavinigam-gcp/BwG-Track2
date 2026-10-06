# M0 · See Everything — Instructions

In this module you find out what your AI estate actually looks like — what NovaSmart says it runs, what is really running, and who has been reading customer data. Every step here is read-only: you change nothing, and you fix nothing. Fixing is M1.

This tab is what you do — the prompt to type and a one-line check that it worked. The story, the background and the sample results live on the Reference Guide tab.

<!-- FIGURE:I01 BEGIN -->

![As Head of AI Platform and Security at NovaSmart, a read-only monitoring module observes official catalog records, actual running workloads, and customer data audit trails while maintaining Changes made: 0.](images/I01_objective.jpg)

<!-- FIGURE:I01 END -->

## Step 1 · Check your environment

Before you look at anything, make sure the machine you are working on is ready.

Ask agy:

```
Check my environment is ready.
```

What to expect: agy checks its own toolkit and your cloud project. It opens by telling you plainly whether you are ready to start, then shows a short table — one row per check, how it verified it, the result, and anything it safely fixed along the way.

If anything comes back not ready, ask agy to fix it before you move on.

## Step 2 · Meet your estate

Start with the official record — the catalog of agents NovaSmart says it has.

Ask agy:

```
What AI agents do we officially have?
```

What to expect: a catalog of six entries across two locations. Three are NovaSmart's own, though only one is listed under a readable name: Price Match Agent, and then markdown-strategy-agent and customer-personalization-agent in lowercase, the names those two give themselves on their self-description cards. The other three are Google's own built-in agents, which the catalog lists automatically: Workspace Agent, which Google publishes, and Gemini Enterprise Core Assistant and Deep Research, which come with the Gemini Enterprise app set up in this project. None of those three is a NovaSmart workload. Nothing in it looks wrong.

More background: Reference Guide tab, Meet your estate

## Step 3 · Widen the net

A catalog only lists what someone remembered to register. Ask what is actually running.

Ask agy:

```
Now show me everything that's actually running. Is anything running that isn't on that list?
```

What to expect: everything running across both Agent Runtime (Google Cloud's managed service for running agents) and Cloud Run, including exactly one workload the catalog has never heard of — the marketing team's promo agent, `promo-agent-shadow`, with no owner and no record. The running list uses the readable names, and agy matches them to the lowercase catalog entries. The list also holds the store's own services and `remote-browser-vm1`, the workstation this lab runs on. Those are infrastructure, not agents.

More background: Reference Guide tab, Widen the net

## Step 4 · Who's reading customer data

Your customer database holds 20 customer records — names, emails, loyalty tier, lifetime value and purchase history. Find out who has been reading it.

Ask agy:

```
Who's been reading our customer database?
```

What to expect: a Cloud Audit Logs record of who has read the customer table — a list of logins, not a list of agents. One line is the lab's own setup account, which loaded the sample records when your project was built; that is housekeeping, not a finding. What matters is a read under the login the promo agent and the Customer Personalization Agent share. It names the login, not an agent. The entry also records which Google service used that login — Cloud Run or Agent Runtime — and here each runtime hosts only one of the two agents, so you can work out which one it was. That is where they happen to be deployed, not who they are: the record names neither agent, and that stops working the day a second workload on either runtime picks up the same login. If more than one read shows up under that login, compare which fields of the customer table each one touched. The project's default compute account may appear too, because the store portal runs as it. Price Match and Markdown Strategy do not appear here at all; they work from pricing and competitor data and never touch customer records.

More background: Reference Guide tab, Who's reading customer data

## Step 5 · Decide

No prompt for this step. This is the leadership call, and it is yours to make before you go on. Three questions:

- Own it or kill it? Do you shut the promo agent down, or bring it under a named owner — and why?
- Does a marketing agent need the whole customer database, or any of it?
- What is the blast radius if you over-grant access now, just to be safe, and the agent is later tricked or breached?

More background: Reference Guide tab, Decide

## Step 6 · What's next

You now know three things you did not know an hour ago: what is officially registered, what is really running, and who is reading customer data under a shared login. None of it is fixed.

M1 · Take Action is where you fix it — register the shadow agent, give each agent its own identity, and scope its access down to what its job actually needs. You will also find out whether your answer to the first question above matches the leadership call.

<!-- FIGURE:I02 BEGIN -->

![Audit findings: six official catalog entries, one unrecorded workload named promo-agent-shadow, and two agents sharing the novasmart-customer-sa login, so their reads are recorded under that login and never as either agent. Changes made: zero. The decision to own it or shut it down remains open.](images/I02_accomplished.jpg)

<!-- FIGURE:I02 END -->

## Try this too — optional

These are not steps, and the module is complete without them. Each one is a question a real leader
would ask at this point. Type any that interest you, in any order, or skip them all.

Ask agy:

```
Could something be running somewhere we didn't look?
```

This shows you which places were actually searched and which were not, so you can judge how much a clean comparison of two lists is really worth.

Ask agy:

```
Would anything have told us about that agent if we hadn't gone looking?
```

This shows you whether anything in your estate would have raised its hand on its own, or whether finding that agent depended entirely on someone deciding to look.

Ask agy:

```
If a regulator asked who read a particular customer's record, what could we actually give them?
```

This shows you which half of that question your audit trail can answer and which half it cannot, which is a far better thing to learn now than during an incident.

## Step 7 · Show what you found

Turn what you found into something you can show other people. Pick any of these, in any order; the first is a good place to start. Each one takes agy a few minutes.

An executive dashboard of your estate:

```
Build me an executive dashboard of the agent estate I found in this module.
```

An investigation board on the shared login:

```
Build me an investigation board that answers: who touched our customer data?
```

A game for your team:

```
Build me a game called Shadow Hunt from what I found, for my team to play.
```

A briefing for your board:

```
Turn what I found into a two-minute briefing I can present to the board.
```

A poster to share:

```
Make a one-page poster of what I found that I can share.
```

What to expect: each page saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome. Each is built only from what agy recorded in Steps 1 to 4, and agy checks it and looks at it before it answers. None of it changes the estate, and none of it fixes anything: that is still M1.
