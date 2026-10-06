# M4 · Evaluate and Decide (Optional Module) — Instructions

This is the last module, and the first one since M0 that changes nothing in your estate. You have spent the lab locking things down. Here you find out whether the agent you locked down still does its job, and then you make the launch call.

## Key objective

This module scores the price-match agent's actual behaviour against the price-match policy you already hold, using the Gen AI evaluation service on the Gemini Enterprise Agent Platform.

- Run NovaSmart's existing scenario set against the agent and read a scorecard: case by case, what was asked, what the agent did, whether that matched policy, and why.
- Have the tooling write a tougher set, including the awkward cases nobody thought to write by hand, and score the agent against that too.
- See a proposed change to the agent's written instructions before anything is changed.
- Measure the same set again after the change, and compare the two runs case by case.
- Decide whether this goes live, on what the scorecard shows rather than on how much work it took.

Why it matters: a scored, per-scenario record with the reasoning attached is something you can hand to risk and compliance, instead of an opinion about how the agent seems to behave.

## Where we left off

Your estate is visible and owned: every agent signs in as itself, only the price-match agent can reach the back-office margin agent, and messages arriving at the price-match agent are screened for manipulation. Every one of those is a control, and none of them tells you whether the agent still gives a store associate a useful answer. Nobody will report it if it does not — a shopper refused a legitimate match just leaves. So before this rolls out to every store, you test it against realistic requests where you already know the right answer.

## Step 1 · Run the evaluation and read the scorecard

NovaSmart already has a scenario set for exactly this: price-match requests written the way an associate would type them, each paired with the outcome the policy says is correct. Matches up to 10% off, the agent settles on the spot. Anything larger goes to the back office. Anyone trying to talk it into a discount it should not give is refused. Ask agy:

```
Evaluate our price-match agent against our scenario set, and walk me through the failures and near-misses.
```

What to expect: a scorecard with one row per scenario — what was asked, what the agent did, whether that matched policy, and why — then a walk through anything that failed and anything that passed for the wrong reason. A refusal stopped by M3's screening comes back looking like a server error, and the words name the screening service rather than a broken agent. It takes a few minutes, nothing in your estate is changed, and there is nothing to undo.

If anything in the run refers to a 20% limit rather than 10%, the version of the agent that is running is out of step with the policy you think you have, and that is worth knowing before launch, not after.

More background: Reference Guide tab, Run the evaluation and read the scorecard

## Step 2 · Build a tougher set and run it

Four scenarios can catch an agent behaving badly and cannot sign off one that appears to be behaving well. So stop hand-writing tests and have the tooling write them, by reading the agent itself. Ask agy:

```
Four cases is not enough. Build me a tougher set including the edge cases, then run it and show me the scorecard.
```

What to expect: agy stands up a throwaway project on the workstation, puts the real price-match agent into it, writes a larger set of cases grounded in your own catalogue and competitor pricing, then runs and scores them. Expect a few minutes, a longer and less tidy scorecard, and failures — and note that from here on the agent being measured is that local copy, not the one serving your stores.

More background: Reference Guide tab, Build a tougher set and run it

## Step 3 · See the fix before you make it

You now have more than one thing to worry about, so pick the worst one. And before anything changes, look at the change. Ask agy:

```
Take the worst one and show me the fix before you change anything.
```

What to expect: agy explains what went wrong in the worst case and shows the proposed fix as a before-and-after of the agent's written instructions — the old wording next to the new wording. Nothing is applied. Not to the deployed agent, and not yet to the local copy either.

More background: Reference Guide tab, See the fix before you make it

## Step 4 · Make the change and see what is actually running

A fix nobody measured is a hope with a version number on it. Apply it, run the same set again, put the two runs side by side, and then ask the only question that matters to a customer standing at a till. Ask agy:

```
Make that change, measure it again, and tell me what is still broken in what is actually running.
```

What to expect: agy applies the change to the local copy, runs the same set again, and compares the two runs case by case. Expect movement rather than a clean sweep. Then it puts the local copy next to what is actually deployed and tells you what is still true in production. Expect an uncomfortable answer, and treat it as the point of this module rather than a failure of it.

More background: Reference Guide tab, Make the change and see what is actually running

## Decide whether to launch

Nothing to type here. You have the evidence. The judgment is yours, and there are three questions to answer.

- Does this go live? Decide on what the scorecard shows, not on how much work it took to get here.
- What would you fix first? Pick the single failure or weakness that worries you most, and be able to say why it is that one and not another.
- What would you monitor after launch? Name the thing you would want to be told about on the day it starts going wrong.

## What you built

At the start of this lab you could not say what you were running.

- You found what was actually there: a marketing agent nobody had catalogued, and two agents sharing one login.
- You fixed it: one identity per agent, access cut back to what each job genuinely needs, and every read of customer data traceable to exactly one agent.
- You controlled the connections: the back-office margin agent now names the price-match agent as its one permitted caller, and the rogue login that used to reach it is refused.
- You screened the content: manipulation aimed at the price-match agent is stopped at the door, in front of that one agent and no other.
- You measured it: a scored, per-scenario record of how the agent actually behaves, with the reasoning behind every verdict.

Visible, attributable, access-controlled, screened at the price-match agent's door and measured — and you got there by describing what you wanted in plain English.

What carries back to your own estate is not the commands. It is the habit: ask what is actually running, insist on evidence rather than assurance, and measure the thing before you trust it.

## See it in the console

There is nothing new to find here, and that is this module's point.

- Open the Agent Registry at https://console.cloud.google.com/agent-platform/agent-registry/agents and find the price-match agent — the one you have spent this module measuring.
- Its entry is the one the earlier modules left. Nothing here changed it: not the scorecards, not the tougher set, and not the wording change.
- Getting that change in front of a customer means a deployment, and that is a separate decision with a separate owner.

## Try this too — optional

These are not steps, and the module is complete without them. Each is a question a real leader would ask at this point. Type any that interest you, in any order, or skip them all. Ask agy:

```
Which of these did the agent actually answer, and which never got to it?
```

This splits a run into the cases the agent actually answered and the cases something stopped before it, which is the difference between a verdict on the agent and a verdict on everything standing in front of it. Ask agy:

```
Would this set of tests have caught any of the problems we found earlier this week?
```

This shows you how narrow a scorecard really is: it speaks to one agent's pricing decisions, and most of what you found earlier in the lab sits outside it. Ask agy:

```
Who is allowed to change these test cases?
```

Whoever can change an expected answer can change every verdict the scorecard will ever produce, so this tells you who that currently is.
