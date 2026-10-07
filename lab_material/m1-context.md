# M1 · Take Action — Reference Guide

The sections below match the steps on the Instructions tab. Dip into a Step section whenever the Instructions tab points you here — but read *Working with agy in this module* first, because M1 is the point where agy stops looking and starts changing things.

## Working with agy in this module

M0 only looked. Every step listed, compared and reported, and nothing in your environment changed. M1 is the opposite. From here on, agy is making real changes to a real cloud project.

The rhythm is the same as before, with one difference that matters.

- You state what you want in plain English, the way you would brief a competent colleague. No commands, no syntax, no cloud jargon.
- agy tells you what it is about to do, in a line or two you can actually read.
- Then it does it. It does not stop and wait. In this lab agy runs at full speed, so the work happens as soon as you ask for it.
- It comes back with the real evidence: the actual catalog entry, the actual log line, the actual configuration. Not an opinion, and not a summary you have to take on trust.
- It leaves a record of exactly what changed and how to undo it. You can say "undo that" or "roll that back" at any point, including after the fact.
- Longer jobs run in the background and it keeps you posted. Normal store traffic keeps flowing throughout.

That combination — very capable, very fast, no pause — is worth sitting with, because it is how these assistants behave in a real organization. An assistant that can reshape your cloud from a single plain-English sentence is only as safe as your habit of looking at what it is about to do.

Which means the pause is yours to create. You create it by asking a question that only reads, before you ask for anything that writes. That is exactly what Step 2 is for, and it is the most transferable thing in this module. Everything else here is mechanics. That habit is the skill.

One last thing before you start: order matters here. The three fixes run in a deliberate sequence, and doing them out of order would break a working agent. Each Step section says why.

### The three surfaces you are working with

Three parts of Gemini Enterprise Agent Platform carry the governance you are putting in place. Agent Registry is the catalog — what you run, and who owns it. Agent Identity is the per-agent badge — who acted. Agent Gateway governs the connections — which agent may reach which agent or tool. M1 is the first two. The third is M2.

## Step 1 · Register the shadow agent

### The leadership call: own it, don't kill it

At the end of M0 you had a choice. Shut the promo agent down, or bring it under an owner.

Shutting it down is fast and feels decisive. It is also the weaker answer: it breaks a marketing team that genuinely relies on the thing, and it teaches that team to build the next one even further out of sight. Bringing it under an owner fixes the same risk in the open, without breaking the business.

So: own it, don't kill it. Step 1 is the first half of carrying that out.

### What registering actually does

Registering the promo agent writes it into the Agent Registry — the official catalog of what you run — with three things written into its entry.

| What gets written into the entry | Why it matters |
| :---- | :---- |
| A name and a description of what it is | It stops being "some service on Cloud Run" and becomes a known part of the estate |
| An owner: the marketing team, written into its description | There is now a named team that answers for what it costs and what it reaches |
| A risk tier: high, because it touches customer data, also written into its description | Risk tier drives how often it gets reviewed and how much scrutiny a change to it gets |

The catalog has no separate fields for an owner or a risk tier, so both are recorded as text in the entry's description.

Its one tool is described on the entry too, which matters more than it sounds. The promo agent has exactly one tool, and that tool extracts customer records. The tool is part of the agent's own code rather than a separate service, so it is recorded as a note on the entry, not as an entry of its own. Cataloging the agent without recording what it can reach would leave you with a tidy list and the same blind spot.

### What registering does not do

This is the part people skip, so it is worth being blunt about.

- The promo agent is still running. Registration does not stop it, pause it or throttle it.
- It still costs whatever it was costing. Nothing about a catalog entry reduces cloud spend.
- It is still signing in with the shared login it was using when you found it.
- It can still read your customer database.

Registration closes exactly one of the two gaps you identified in M0. Visibility: something is running that nobody cataloged and nobody owns. That gap is now closed. Accountability — a legitimate agent and this one sharing a single identity, so their actions are recorded under that login and never as either agent — is completely untouched, and so is the over-reach.

That is not a failure of the step; it is the honest shape of it. Cataloging a rogue workload is the first move, not the fix — and it comes first because everything after it depends on having a named, owned thing to change.

## Step 2 · See what that shared login can do

This is the judgment moment of the whole module, and it changes nothing at all.

Before you ask agy to hand out new identities, you ask it a read-only question: what can that shared login do today, and what does each agent's job actually need? agy answers, shows you the evidence, and applies nothing.

### Why you deliberately create this pause

Go back to the way agy behaves in this module. It moves at full speed. If your next sentence is "give each agent its own identity", the identities exist a moment later, with whatever access agy inferred they needed.

Most of the time that is fine, and it is why these assistants are so useful. But it means that if you never ask a question that reads before you ask one that writes, there is no gap in which a bad outcome could have been caught. Reading what is about to happen, and being willing to say "not that, something smaller", is the whole discipline — and it transfers straight back to your own estate.

### The tell

What comes back is uncomfortable. The shared login, a service account called `novasmart-customer-sa`, can read, change or delete the data in any database in the entire project. Not the customer database specifically — every database the project holds. It can also read every file stored in the project. It cannot delete those files, but it can read all of them, which for anything confidential is bad enough.

Now hold that against what the two agents on that login actually do.

| Agent | What its job genuinely needs | What the shared login gives it |
| :---- | :---- | :---- |
| Customer Personalization Agent | Read customer records, so it can tailor offers and VIP rewards | Read, change and delete the data in every database in the project, and read every stored file |
| Demand and Promotion Agent, running as `promo-agent-shadow` | Write promotional copy and flash-sale bundles | Read, change and delete the data in every database in the project, and read every stored file |

Neither of those jobs needs to change a customer record. Neither needs to delete anything. And one of them has no business reading customer records at all — a marketing copy generator does not need names, emails, loyalty tiers and lifetime values to write a flash-sale headline.

### Blast radius, in plain terms

Blast radius is how much can go wrong if one agent is later tricked, misconfigured or breached. Access granted to a login is inherited by everything running under it, so today the blast radius of either agent is identical: every database and every stored file in the project. A prompt-injection attack on the promo agent, or an ordinary bug in the personalization agent, reaches as far as the login does — and the login reaches all of that.

Nobody did this maliciously. A broad grant is the fastest way to make something work, and it never fails in testing. It is the same speed-over-governance shortcut that produced the shadow agent, which is why the two problems showed up together.

### What "sized to the job" looks like

Least privilege means each agent gets only the access its job needs, and nothing more. Applied here, that is two sentences:

- The Customer Personalization Agent gets read-only access to customer data, and only to customer data. It genuinely needs to read those records. It never needs to change or delete one.
- The promo agent gets no access to customer data at all.

You did not guess at that. You worked it out by comparing the job to the grant, which is exactly what this step exists to let you do. Now you can tell agy the shape you want, instead of letting it infer one.

## Step 3 · Give each agent its own login

### Identity and permissions are two different questions

Identity is *who is acting*. Permissions are *what they are allowed to do*. The two get confused constantly, and keeping them apart is what makes this module work: Step 3 fixes identity, Step 4 fixes permissions, and you cannot sensibly do the second first — until each agent signs in as itself, there is no way to give one of them less access than the other.

### Only two agents are affected

Be precise about the scope here, because it is easy to over-state. Four agents run at NovaSmart, and two of them are already fine: the Price Match Agent and the Markdown Strategy Agent each have their own identity and always did. Nothing in this step touches them.

The problem is the other two — the Customer Personalization Agent and the promo agent — sharing `novasmart-customer-sa` between them.

### Two agents, two different mechanisms

They also sit in different places, so the fix looks slightly different for each.

The Customer Personalization Agent runs on Agent Runtime, Google Cloud's managed service for running agents. The platform can issue it a per-agent Agent Identity directly: a unique badge issued by the platform to that one agent.

The promo agent runs on Cloud Run, which is a general-purpose place to run software rather than a managed home for agents. It cannot be handed a platform-issued agent identity, so the equivalent is its own dedicated service account — its own login, used by nothing else. That login gets only read access to the storage bucket its own code is loaded from. Different plumbing, same outcome: one badge per worker, shared with nobody.

You do not need the internals, but the distinction is worth noticing: it is a small, concrete example of why running things off the official platform costs you something later.

### Moving the badge takes the keys with it

There is a second half to this step that is easy to miss and expensive to skip.

The personalization agent's access to customer data was never granted to the agent. It was granted to the shared login, and the agent inherited it by signing in as that login. The moment it stops using the shared login, it stops inheriting anything. It keeps running, it will still answer a greeting, and it will fail the first time it tries to read a customer record.

So agy has to do two things, not one: move the agent onto its own identity, then grant that new identity the narrow access the agent needs to do its job. Identity and permissions are two different questions, and here you can watch the difference happen.

It is worth insisting on proof, because the failure is quiet: the agent still answers a greeting and only fails when it tries to read, so a half-finished migration can look like an unrelated outage. Ask to see the agent actually retrieve customer data after the change, not just a confirmation that the identity was updated.

### Where the estate lands

| Agent | How it signed in before | How it signs in now | Customer data access |
| :---- | :---- | :---- | :---- |
| Price Match Agent | Its own agent identity | Unchanged | Not changed in this module |
| Markdown Strategy Agent | Its own agent identity | Unchanged | Not changed in this module |
| Customer Personalization Agent | Shared `novasmart-customer-sa` | Its own agent identity | Read-only, customer data only |
| Demand and Promotion Agent | Shared `novasmart-customer-sa` | Its own dedicated service account | None from the moment it moved (confirmed in Step 4) |

Price Match and Markdown Strategy still hold broad data access of their own. That is reviewed later, not here.

Re-issuing identities takes a few minutes, including the time for new access to take effect. agy keeps you posted while it runs, and the work from Step 1 holds. If anything looks wrong, tell agy to roll it back.

Notice what happens to the shared login itself. Only once both workloads have moved off it does agy remove its broad database role, and it adds nothing in its place. Its few other roles stay, and it is left with no users at all: vacated, not deleted.

The payoff is quiet but real: from here on, every read by the two agents names exactly one of them. In M0 you had to work out who did what by hand, cross-referencing the log against the running services. That inference is now far narrower: the personalization agent is named directly, and the promo agent's login is used by nothing else.

## Step 4 · Cut off what shouldn't have access

### Why this step could not have come first

In M0 the two agents shared one identity. Any permission you removed from that shared login, you removed from both. Cutting the promo agent's access would have taken the personalization agent down with it, and personalization is a legitimate service that shoppers see.

Now that each agent signs in as itself, you can act on one without touching the other. That is the practical value of Step 3, and why identity precedes permissions.

### What gets removed

The promo agent has one tool, and that tool pulls customer records out of the database: names, email addresses, loyalty tiers, lifetime values. It does not read inventory data. It has no other tool. Removing its access to customer data therefore closes its own route to sensitive information.

There are two ways this step can land, and both are correct. If an access path is still open, agy removes just that access, leaves the agents that genuinely need customer data alone, and shows you the before and after. If Step 3 already closed the route when it moved the agent onto its own login, there is nothing left to take away, and agy tells you that plainly rather than manufacturing a change so the step looks busy.

The lesson is the same either way, and it is worth stating in those terms. What matters is not that a removal happened in this particular step. What matters is that the promo agent ends the module with no route of its own to customer records, and that you can see which action closed it.

### What keeps working

- The promo agent keeps running. It keeps writing promotional copy and flash-sale bundles, which is what marketing actually wanted from it. What it can no longer do is reach customer records under its own name.
- The Customer Personalization Agent keeps working, on read-only access to customer data — enough for its job, not enough to change or delete a record.
- The price-match co-pilot is entirely unaffected. Store associates notice nothing.

Be clear about what this step did and did not achieve. It did not shut the promo agent down, and it does not reduce your cloud bill. What changed is that the agent is owned, named, and its own identity no longer opens the door to data it never needed. That is the claim that will hold up when somebody asks — that precise claim, and not a broader one.

Say what is still open, too. The two agents that read customer data do not reach the database on their own; they go through a shared tool layer. That layer accepts calls from anyone and holds broad access of its own. It passes on the caller's own login when the caller sends one, but a caller that sends none gets the layer's broad access instead, so narrowing one agent's identity does not narrow the layer underneath. This module does not close that. Deciding who may call what is a different control; the next module applies it to the back-office agent.

## Step 5 · Prove it worked

You have agy's word for all of this. That is not evidence. So you go back to the same access log you pulled in M0 and read it again, this time narrowed to reads of the customer records.

### What the log looks like now

The log has the same shape it always had — when it happened, what was accessed, and the login that did it — plus whether the request succeeded. Your timestamps will differ.

| Time | What happened | Who the log names | Outcome |
| :---- | :---- | :---- | :---- |
| 14:02:11 | Read customer records to answer a question about a customer | Customer Personalization Agent's own agent identity | Allowed |
| 14:03:35 | Attempted to read customer records for a promo campaign | Demand and Promotion Agent's own service account | Denied: not allowed to run a query in this project |

Compare that to the log in M0. There, two entirely different workloads — a legitimate personalization request and a marketing bulk extract — signed in with the same login, so the record named that login and never an agent. You could work out which one it was only from where each happens to run. Here they are the same two workloads, and every row names exactly one agent's own login.

Price Match and Markdown Strategy do not appear in these rows. They work from competitor prices, our own stock and the margin data, and never had a reason to read customer records. These rows cover every read by the two agents in the story. Other readers, such as the store app's own account, can still appear in the full log; the second optional prompt on the Instructions tab looks at them.

Note what is still not in the log, because it never was and never should be: there is no field where an agent announces its own name. A name a caller supplies about itself is a claim, not evidence. The login is the identifier — which is precisely why giving each agent its own was the fix.

### Why the familiar column goes blank

One thing in the raw log will look wrong at first glance, so it is worth knowing before you see it. The column that used to name the shared login is empty for the personalization agent's reads. That is the fix working, not a fault.

The reason goes back to the two mechanisms in Step 3. The personalization agent no longer signs in with an account that has an email address. It now carries a machine identity issued by the platform and belonging to that one agent alone, so there is nothing to put in a column built for email addresses. Its name has moved to a different field of the same log entry, and that field is where the proof now lives. The promo agent is the exception, and for a reason you already know: it runs on Cloud Run and got its own dedicated service account rather than a platform-issued identity, so it still has an email address and still shows up in the familiar column.

Two mechanisms, two ways of being named, one outcome — every read by the two agents traces to exactly one of them. So read the blank for what it is. It is the shared account being gone, not attribution getting worse. If agy shows you only the email column, ask it for the field that carries the per-agent identity and read the proof there.

### The denial is the proof

The last row is the interesting one. The promo agent tried to read customer records and was refused at the first gate it reached: it is not allowed to run a query in this project at all, so it never got as far as the customer table.

Two things happen when that occurs, and only one of them is evidence.

- The application does not even return an error. The promo agent reports the campaign as launched, with zero records analyzed, so a caller reading only that reply would conclude nothing had gone wrong. An application's own account of itself is not evidence, and here it is not even accurate.
- The platform writes a denied entry into the access log. That entry is written by the platform, not the app, and can be exported to your compliance team. It is the authoritative record that the control fired.

So the thing to look at is the log, not the app. A denial sitting in an audit trail is a good outcome: it is your policy working, in the open, where an auditor can see it.

It also matters that this denial was triggered deliberately. An empty log proves nothing: it might mean your controls work, or that nobody tested them. Causing the blocked action on purpose and then finding it in the record is the difference between believing a control works and knowing it does.

### The checks worth making

- The promo agent is now in the catalog with the marketing team named against it, so the uncataloged agent M0 found is on the record.
- Each agent signs in as itself, and each log line names exactly one of them.
- The promo agent's attempt to read customer data appears in the log as denied.
- The personalization agent and the price-match co-pilot are still doing their jobs. For personalization, the evidence is the agent's own read in the log, not the store app's card.

agy does not leave these to your eye. It writes the full check-by-check table, all 16 checks, to `m1_step5.txt` in the `novasmart-evidence` folder on your Desktop, and its answer tells you in one line how many of them it could prove. It then updates your Governance Scorecard, a web page it generates on your Desktop, and gives you the link. A FAIL names the check that did not hold and the step to go back to, so the file, not the summary, is where to look when anything is in doubt.

## What you just did

Three fixes, in an order that mattered.

You registered a hidden workload in the catalog, so it has a name and an owner. You gave the two agents that were sharing a login one identity each, so every action traces to exactly one of them. And you cut access back to what each job actually needs — read-only on customer data for the agent that genuinely uses it, none for the agent that never should have had it.

Put together, the estate is now visible, attributable and, for the two agents you changed, least-privileged. The agent nobody owned has a named owner, every grant you changed is sized to a job you can describe, and for those two agents Security and Compliance can answer the first question anyone asks after an incident — who read the customer data — with an agent's name rather than a shared login.

Be careful what you claim beyond that. The promo agent was not shut down, it is still running, and none of this reduced your cloud spend. You removed the risk, not the workload. Claiming more than you did is how governance work loses credibility.

The skill you just practiced is not typing commands. It is knowing what to ask, and reading what comes back before it becomes permanent — and, when the assistant does not pause on its own, deliberately creating the moment where you look.

One thing you still cannot answer. You know which agent did something and what data each may touch. You do not yet control which agent may call which other agent. The Markdown Strategy Agent, sitting on NovaSmart's confidential cost and margin data, should only ever be reachable by another agent — never by a customer, never directly by a store associate. Nothing you have done so far enforces that.

Controlling who may call whom is M2 · Control the Connections, and it is where Agent Gateway comes into the picture.
