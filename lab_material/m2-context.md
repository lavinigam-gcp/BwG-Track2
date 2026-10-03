# M2 · Control the Connections — Reference Guide

The sections below match the steps on the Instructions tab. Dip into a Step section whenever the Instructions tab points you here — but read *Working with agy in this module* first, because M2 is where you stop governing what an agent may read and start governing who it may talk to.

## Working with agy in this module

The rhythm is the one you learned in M1. You brief agy in plain English, it does the work directly at full speed, it comes back with the real evidence rather than an opinion, and it leaves a record of what changed and how to reverse it. Say "undo that" or "roll that back" at any point and it will.

Three things about this module are worth flagging before you start.

First, only one of the four steps changes anything. Step 1 reads, Step 2 reads, Step 4 tests, and only Step 3 writes. That ratio is deliberate, and it is the honest shape of most governance work: the change itself is a single sentence, and everything around it is knowing what to change and being able to show afterwards that it worked.

Second, agy still does not pause. If your next sentence is "lock it down", the lock exists a moment later. In M1 you learned to create the pause yourself, by asking a question that only reads before you ask for anything that writes. Step 2 is that pause, and here it is doing real work: cutting a caller list down to one name is exactly the kind of change that can quietly break a working part of the business.

Third, access changes do not take effect the instant they are saved. They propagate through the platform over a minute or two, so a test run immediately afterwards can still show the old behaviour and tell you nothing at all. agy waits before it tests. If you test by hand, wait too.

One framing helps throughout. M1 governed identity and access — who is acting, and what data may they touch. M2 governs connection — who may call whom. These are separate controls and neither implies the other. An agent can hold no data access whatsoever and still be able to reach an agent that holds all of it.

A word on the product you might expect to see doing this job. Agent Gateway is the Agent Platform's networking control: it sits between agents and polices which of them may reach which agent, tool or endpoint. NovaSmart has two gateways provisioned and has never attached an agent to either, so nothing is routed through them today. You will change that in Step 5. But notice what it governs. A gateway controls where an agent may go, not who may come in to see it, and not what the agent may do once it arrives. Those are three different questions, and this module answers all three with three different controls. Keeping them apart is most of the skill.

## Step 1 · See who can call the back office

### The cast

Three parties matter in this module.

The Markdown Strategy Agent is the back office. It holds NovaSmart's confidential cost and margin data — what each product actually costs the business, and how far a price can move before a sale stops being worth making — and it makes the real call on large discounts. It is the most sensitive agent in the estate, and it serves no customer directly.

The Price Match Agent is the front desk. It works the store floor alongside associates: a shopper produces a competitor's lower price, and the agent decides whether to match it. Up to 10% it settles on its own. Anything larger it does not decide alone; it escalates to the back office and asks for a ruling.

That escalation is the one agent-to-agent conversation the business genuinely needs. Both of these agents have carried their own Agent Identity from the start — identity was never the problem here. The problem is that nothing states the front desk is the only caller.

Then there is `test-agent-caller`: a service account sitting in the project with no owner, holding a grant made directly on the back-office agent. It can call it. It is otherwise unprivileged and it has no legitimate reason to be on that list at all. Treat it as the stand-in for the thing you will find in your own estate — a caller left over from a test, a migration or a favour, granted once and never taken away.

### What the list says today

| Who can reach the back office today | Should it? | Why it can |
| :---- | :---- | :---- |
| Price Match Agent, the front desk | Yes | Escalating a discount above 10% is its job, and this is the one path the business genuinely needs |
| `test-agent-caller`, an unowned service account | No | A grant made directly on the back-office agent, and never taken away |
| Identities holding broad project-wide roles | Almost never | The ability to call any agent arrives bundled inside a wide role, rather than from the back office's own list |

Only one of these sits on the back office's own list, which is the thing this module changes: the leftover test login. The others reach it by other means, and Step 3 returns to that in detail — noting it here so the picture you carry into the fix is the accurate one rather than the comfortable one.

This is not a retail problem. Swap the margin logic for whatever your own organisation would least like consulted without oversight — the billing engine, the patient record system, the eligibility service. The rule is the same wherever you apply it: the sensitive back end should name the callers it accepts, rather than accepting whoever happens to be holding a grant.

### Call permission is not data permission

This is the distinction the whole module turns on, and it is easy to blur.

In M1 you controlled what each agent may read. That is data permission, and you sized it to each agent's job. This step is about something different: whether one identity may pick up the phone to an agent at all. Call it call permission.

The two are independent, and the rogue login shows why that matters. `test-agent-caller` has no data access worth the name — and it can still ask the agent that holds your margin data to make a decision. It never needs to read the margin data itself. It only needs the back office to read it and answer, which is precisely what the back office is built to do.

That is why least privilege has to be applied to connections as well as to data. An agent that can be called by anything is a service that can be used by anything, whatever the caller's own permissions happen to say.

### Why leftover grants are the normal case

Nobody set out to leave a rogue caller on the most sensitive agent in the estate. Somebody needed to test the escalation path, granted a test identity access so the test would run, and moved on. The grant does not expire. Nothing reminds anyone it exists. And it never fails in a way anyone notices, because an unused grant is silent by definition.

That is the general shape of the finding, and it is not specific to agents: access accumulates, because granting is a one-minute task with an obvious benefit, and revoking is a task nobody is assigned. Reading the caller list out loud, as you just did, is the routine that turns that silence into a finding.

## Step 2 · See what locking it down would cost

### The read-only beat

You already know roughly what the fix is. That is exactly why this is the moment to ask a question that changes nothing.

The question is not whether the rogue login should go — that answer is obvious and you do not need agy to confirm it. The question is what else is reaching the back office today, and what would stop working if the list were cut to a single name. agy answers, shows you the evidence, and applies nothing.

Doing this in the other order is how governance work earns a bad reputation. A lockdown that is technically correct and takes a revenue-generating path down with it gets reversed by lunchtime, and the next proposal you bring meets a much harder conversation.

### Four routes in, and what a lockdown does to each

| Route into the back office | What locking the list to the front desk does to it |
| :---- | :---- |
| The front desk escalating a price match above 10% | Nothing. It is added to the list by this change, so the path is named and deliberate rather than incidental |
| The rogue login's direct grant | Closes it. That grant sits on the back office's own list, so rewriting the list removes it |
| The store application calling the back office directly | Nothing. That route is written into the application's code, not into an access list |
| Broad project-wide roles that include the right to call any agent | Nothing. They sit above the agent's list rather than on it |

Two of those four rows are the honest limits of this module. They are covered below and in Step 3, and neither is a reason to skip the change — closing the one route you can close is still worth doing, provided you describe it accurately afterwards.

### What matters in the readout

Two things are worth checking carefully.

The escalation path has to survive. If the front desk cannot reach the back office after the change, every discount above 10% either stalls or gets refused at the counter, and store associates discover it before you do. Confirming the escalation still works is not a formality — it is the reason this change is safe to make.

And the rogue caller's route has to be one that closing the list actually closes. It is. Its access was granted directly on the back-office agent, so rewriting that agent's list removes it. That is worth verifying rather than assuming, because access granted somewhere else would not be touched by this change at all — a point Step 3 comes back to.

### One route that will not close, and is worth knowing about

There is a second way into the back office, and it does not run through the front desk.

The NovaSmart store application calls the back-office agent directly for one of its actions, rather than routing that request through the Price Match Agent. That path is written into the application's own code, and the access it relies on comes from elsewhere in the project rather than from the back office's own list — the additive-permissions point Step 3 sets out in full. Rewriting one agent's list does not remove a line of application code, so this route survives the change.

You are not being asked to fix it and it is not a step in this module. It is here because it is precisely the kind of thing that makes an otherwise clean governance claim wrong. If you tell your board that every request to the back office now arrives by way of the front desk, the store application makes that statement false — not because your control failed, but because a shortcut was built before the control existed. Removing it is an application change on an engineering backlog, not something you can direct from an access list.

The transferable habit: whenever you tighten a path, ask who was already using a different one.

## Step 3 · Lock it to the front desk

### What actually changes

The back-office agent keeps its own list of who may call it. Today the only name on it is the leftover test login, and the front desk is not on it at all. The change rewrites the list so it names exactly one caller: the Price Match Agent's own Agent Identity.

Nothing else is touched at this point. No agent is stopped, no data access is altered, no network is reconfigured. This is not a firewall. The control lives on the agent itself, which is what makes it precise: it states who this one sensitive agent will accept a call from, and it says nothing about anything else in the project, including anything the agent itself goes on to do.

### Name who is in, rather than chasing who is out

There are two ways to shape a control like this, and the difference is worth a minute of your time because it decides whether the control still holds in a year.

You can chase the callers you do not want, removing them one at a time as you find them. That list only ever grows. Every grant somebody makes next quarter is a new item on it, nobody is assigned to notice, and you are permanently one forgotten entry away from being wrong.

Or you can name the callers you do want and let everything else fall outside by default. That statement does not need maintaining as the estate changes, because it does not depend on knowing in advance what is coming. The change you make here is the second kind: one name on the list, and the list itself is the policy.

### It takes a minute or two to settle

Access changes propagate. For a short period after the change is saved, the old behaviour can still be observed — which means a test run immediately afterwards can show a rogue call succeeding and cause an entirely unnecessary panic. agy waits before it tests. The lesson generalises beyond this lab: with access control, "it did not work" and "it has not landed yet" look identical for the first couple of minutes.

### What this locks, and what it does not

This is the part to get exactly right, because the temptation to overstate it is strong and the overstatement is the kind an auditor will find.

What is true: the back-office agent now names exactly one permitted caller, and the rogue login that previously reached it is denied. You will see that denial for yourself in the next step. The direct grant is gone, and closing it was the specific job of this module.

What is not true is the tidier sentence you would like to write — that the front desk is now the only thing in the entire project capable of calling the back office. Cloud permissions are additive. Access can be granted in more than one place, and the widest grant wins. Several broad, project-wide roles — the kind given to administrators, to platform teams, and sometimes to service identities during a migration — carry the right to call any agent in the project as one item among the many things they allow. Nothing in this module removed those, because they do not sit on the back office's list. They sit above it.

So the honest claim is narrower, and it is still worth making: the back office's own list now names one caller, the leftover grant is closed, and the rogue is denied.

The wider work is real and it belongs on your plan. Find every project-wide role that carries the ability to call an agent, work out who genuinely needs it, and cut the rest. That is a bigger and slower job than this module — it touches people and teams rather than one agent's settings — and it is exactly the sort of cleanup that never happens unless somebody writes it down. Write it down.

Saying this out loud is not an admission of failure. It is the difference between a control you can defend under questioning and a claim that collapses the first time somebody tests it.

## Step 4 · Prove the rogue caller is out

### Both halves of the test

agy makes two real calls and shows you both results.

| The call | Before the change | After the change |
| :---- | :---- | :---- |
| The rogue login `test-agent-caller` calls the back office directly | The call goes through | Refused, in the platform's own words, quoted back to you |
| The front desk escalates a genuine price match above 10% | A margin decision comes back | A margin decision still comes back |

The first row is the security result. The second row is the business result, and it is not the lesser of the two. A control that stops the attack and also stops the work has traded one problem for a more expensive one, and it will be switched off by somebody who has had enough of the complaints.

Testing both in the same breath is the habit worth taking away, and it is also the honest way to report the change: not "we locked it down", but "we locked it down, and here is the legitimate path still working".

### Why the front desk checks the price it is quoted

The escalation half of the test has a wrinkle worth understanding, because it can look like a failure when it is nothing of the kind.

A price match begins with a claim. A shopper says a competitor is selling the same product for less, and asks the store to match it. The front desk does not take that claim on trust. Before it discounts anything — and before it works out whether the discount is large enough to need the back office — it looks the claimed price up in NovaSmart's own record of competitor listings. If that price is not on file, the request stops right there and the answer says no competitor is verified at that price.

That is a governance control, not an obstacle. It is the same principle as everything else in this lab, applied to money rather than to access. A shopper who invents a competitor price should not be able to talk an agent into a discount, and an agent that discounts against an unverified claim is a margin leak that runs at machine speed and never gets tired. The check is what makes the front desk's decisions defensible after the fact.

It matters in this step for a practical reason. If the test quotes a price the store does not hold, what comes back is a refusal about the price, arriving before any escalation happens at all. Read quickly, that looks like the lockdown having broken the business. It is not related to the lockdown in any way.

The listing to use is the AeroPure Smart Air Purifier, SKU-HSE-4001. NovaSmart's shelf price is $349.00 and BetaBuy is on file at $296.65 — a 15% discount, above the 10% the front desk can settle by itself, so the request has to go to the back office for a ruling. That is precisely the path this module needs to see still working. It is also the deepest verified discount in the data, so a request built on anything larger is refused for the same reason, and again it says nothing about the lock.

### Where the evidence actually lives

When the rogue call is refused, several things happen at once, and they are not equally good evidence. Knowing which one to put in front of an auditor is most of the skill.

The strongest by a distance is the call agy made itself. It sent the request as the rogue login, the platform turned it down, and agy can quote the platform's own answer back to you with the time it happened. That is first-hand: agy caused the event and read the refusal directly. Nothing else in this module beats it, and you should expect agy to lead with it.

The rewritten caller list is the second record, and it is a different kind of thing altogether. It shows what you intended — the back office now names one caller — but a settings page cannot tell you that anybody was actually stopped. It is evidence of the rule, not of the rule firing.

Cloud Audit Logs can supply a third record, independent of both: this identity attempted this call at this time, and it was refused. Where it exists it is genuinely useful, because it is system-generated, timestamped, exportable to your compliance team, and it comes from somewhere other than the tool that made the call. But it may simply not be there. Detailed access logging is switched off unless an administrator turns it on, and not every operation on this surface is captured even then. A missing entry does not mean the call succeeded and it does not mean the control failed. It means that particular record was never written. The honest response is for agy to say which records it has and which it does not, rather than to paper over the gap or to keep hunting for an entry that was never going to exist.

Whatever made the call, meanwhile, simply receives an error, and in the store app that error looks like any other failure. An error could be a bug, a timeout, a bad address, or a service that happens to be down — and worse, the app fills a thin response with plausible-sounding text of its own. It is a symptom at best, and it is not proof in either direction.

So look at what the platform said, not at what the app displayed. This is the same lesson as M1's denied log entry arriving from a different direction, and it is the one that matters when somebody asks you to demonstrate that a control works rather than assert it.

### Why triggering the denial deliberately matters

A control nobody has exercised is a control nobody can vouch for. It might be working perfectly, or it might have been switched off last quarter, and from the outside those two look identical. Causing the refused call on purpose and reading the platform's answer to it is the difference between believing a control works and knowing it does.

That holds whether or not an audit entry turns up beside it. Because you produced the event yourself, your evidence does not depend on a log somebody else had to have enabled first — which is exactly why it is the record to rely on.

### The checks worth making

- The rogue login is refused where it previously got through, and agy quoted the platform's own refusal rather than inferring it from the settings.
- A genuine price match above 10% still escalates to the back office and comes back with a decision.
- Ordinary store traffic is unaffected: associates on the floor see no change in price matches under 10%.
- An audit-log entry for the refusal is corroboration where it appears. If agy reports that no audit entry was recorded, that is an honest result and not a failed check.

## Step 5 · Lock down what the back office can reach and do

### The question the first three steps never asked

Steps 1 to 4 were all about calls coming in. They ended with a back office that accepts a call from exactly one caller, and you proved it. That is worth having, and it is half a control.

The other half is everything the back office does after it picks up. It holds the confidential cost and margin data, it reaches out to Google's BigQuery service to read pricing tables, and today it can also change them. Nobody asked it to. Its job is to look at inventory, costs and competitor prices and make a recommendation. Writing to the pricing tables is not part of that, and the ability to do it is left over rather than intended.

### Why this takes two controls and not one

The natural instinct is to look for a single setting. There isn't one, and the reason is worth understanding because it comes up constantly.

The gateway sits on the network path. It can see that the back office is trying to reach a particular service and it can allow or refuse that. What it cannot see is what the request says once it gets there, because the contents are sealed. So the gateway can answer where may this agent go, and it genuinely cannot answer what may it do when it arrives.

The database can answer the second question, because by the time the request lands there it has been opened and read. So the two controls sit at different points on the same path and see different things. Together they cover the route and the action. Either alone leaves a real gap, and describing one as if it did the other's job is the kind of claim that falls apart the first time somebody tests it.

### What agy actually changes

It puts the back-office agent behind the gateway NovaSmart already owns, and gives that gateway a rule about which destinations are permitted. Then it narrows the agent's own database permissions from full control down to reading the two datasets it uses.

Both changes are reversible, and neither touches the front desk or the storefront.

### What counts as proof, and what does not

This is the part to hold firm on, because the obvious evidence is the misleading kind.

When one of these controls refuses something, the agent does not return an error. It answers anyway, in confident prose, using what it already knows from its own instructions. A refused database read produces a plausible-looking list of tables that came from the agent's memory rather than the database. If you accept that as a successful read you will conclude the control is not working when it is, or that it is working when it is not.

So the proof lives outside the conversation. The gateway keeps its own record of each decision, allowed or refused, against a named destination. The database can be asked directly what a value is. Ask for both. The useful pairing is a read that succeeds and a change that fails, in the same minute, with the failure confirmed by looking at the data rather than by asking the agent what happened.

### What this locks, and what it does not

The back office can now reach only the destinations the gateway permits, and it can read the pricing data without being able to change it.

What is not true is that every agent in the estate is now constrained this way. Only the back office was put behind the gateway. The others are unchanged, and doing the same for them is a larger piece of work that belongs on the plan rather than in this module.

It is also worth saying plainly that the gateway cannot distinguish one kind of database request from another. It permitted the route; the database permissions did the rest. If somebody later asks you whether the gateway stopped the write, the honest answer is no, and the reason is a useful thing to know.

## What you just did

You read the list of callers on the most sensitive agent in the estate, found an unowned leftover login sitting on it, checked what a lockdown would cost before you ordered one, rewrote the list so it names a single caller, and then proved both halves of the outcome — the rogue refused, the legitimate escalation still working.

Set against M1, the estate has gained a third property. It was already visible, because everything running is catalogued and owned. It was already attributable and least-privileged, because every agent signs in as itself and holds only the data access its job needs. Now the connection between your two most important agents is governed as well: the back office names one permitted caller instead of accepting whoever happens to hold a grant on it.

None of that was written in code. It was directed in plain English, and every change is on the record.

Be careful what you claim beyond it. Cloud permissions are additive, so broad project-wide roles still carry the ability to call any agent, and the store application still has its own direct route into the back office. Neither of those is a failure of this module, and neither is a reason to soften the result. They are the next items on the list, and naming them is what makes the part you did finish believable.

There is one thing this control cannot do at all. It decides who may call whom. It has nothing to say about what is said. Your two customer-facing agents — the front desk on the store floor and the Customer Personalization Agent on the website — read whatever a shopper types and hand it straight to the AI. A locked door does not help if you let a trap walk through it.

Screening what customers can talk your agents into is M3 · Protect the Content.
