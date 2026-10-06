# M4 · Evaluate and Decide (Optional Module) — Instructions

This is the last module, and the first one since M0 that changes nothing in your estate. You have spent the lab locking things down. Here you find out whether the agent you locked down still does its job, and then you make the launch call. The module is optional and is not scored, so the Governance Scorecard page from earlier modules does not change; in this module "scorecard" means the evaluation results.

## Key objective

This module scores the price-match agent's actual behavior against the price-match policy you already hold, using Google Cloud's Gen AI evaluation service: it puts each case to the agent, and a judge model, separate from the agent's own model, marks each case and writes down why.

- Run NovaSmart's existing scenario set against the agent and read a scorecard: case by case, what was asked, what the agent did, whether that matched policy, and why.
- Have the tooling write a tougher set, including the awkward cases nobody thought to write by hand, and score a local copy of the agent against that too.
- See a proposed change to the agent's written instructions before anything is changed.
- Run the same set again after the change, and compare the two runs case by case.
- Decide whether this goes live, on what the scorecard shows rather than on how much work it took.

Why it matters: a scored, per-scenario record with the reasoning attached is something you can hand to risk and compliance, instead of an opinion about how the agent seems to behave.

## Where we left off

Every agent signs in as itself. The back-office margin agent names the price-match agent as its one permitted caller, though broad project-wide roles can still call it, and it sits behind NovaSmart's outbound gateway with read-only rights on the pricing data. If you ran M3, the price-match agent sits behind the inbound gateway, and messages arriving at it are screened for manipulation. That screen covers that one agent, and it is fail-open: if it cannot run, traffic passes. The attack on customer records through the Customer Personalization Agent is not behind any screen.

Each of those is a control, and none of them tells you whether the agent still gives a store associate a useful answer. Nobody will report it if it does not — a shopper refused a legitimate match just leaves. So before this rolls out to every store, you test it against realistic requests where you already know the right answer.

## Step 1 · Run the evaluation and read the scorecard

NovaSmart already has a scenario set for exactly this: price-match requests written the way an associate would type them, each paired with the outcome the policy says is correct. Matches up to 10% off, the agent settles on the spot. Anything larger goes to the back office. Anyone trying to talk it into a discount it should not give is refused. Ask agy:

```
Evaluate our price-match agent against our scenario set, and walk me through the failures and near-misses.
```

What to expect: a scorecard with one row per scenario — what was asked, what the agent did, whether that matched policy, and why — then a walk through anything that failed and anything that passed for the wrong reason. agy runs the scenarios through the Gen AI evaluation service and names the judge model that marked the cases, which is not the model the agent runs on; if the judge could not run, it says the verdicts are its own reading of the replies. Only the 15% case goes on to the back office. If you ran M3, a request stopped by the screen comes back as an error rather than an answer, and agy quotes its words, which are what tell a blocked request from a broken agent. If you skipped M3, there is no screen, and agy should say so rather than mention one. It takes a few minutes, nothing in your estate is changed, and there is nothing to undo.

If anything in the run refers to a limit other than 10%, the running agent is out of step with the written policy, and that is worth knowing before launch, not after.

More background: Reference Guide tab, Run the evaluation and read the scorecard

## Step 2 · Build a tougher set and run it

Four scenarios can catch an agent behaving badly and cannot sign off one that appears to be behaving well. So stop hand-writing tests and have the tooling write them, by reading the agent itself. Ask agy:

```
Four cases is not enough. Build me a tougher set including the edge cases, then run it and show me the scorecard.
```

What to expect: agy sets up a folder on this workstation, puts a copy of the real price-match agent into it, and has the tooling write a set of cases grounded in your own catalog and competitor pricing — usually at least eight, and if it comes back with fewer, agy says how many short. It saves the cases to one file, so Step 4 can run exactly the same set again, then runs them against the copy and scores them. Expect a few minutes, a longer and less tidy scorecard, and failures.

From here on, the agent being measured is that local copy, not the one serving your stores, and it differs in three ways that agy should state. It does not hand off to the back office. It has no screen in front of it. And it cannot read competitor prices, because the workstation's login has no read access to that table, so a local run cannot verify a match the way the deployed agent does.

More background: Reference Guide tab, Build a tougher set and run it

## Step 3 · See the fix before you make it

You now have more than one thing to worry about, so pick the worst one. And before anything changes, look at the change. Ask agy:

```
Take the worst one and show me the fix before you change anything.
```

What to expect: agy explains what went wrong in the worst case and shows the proposed fix as a before-and-after of the agent's written instructions — the old wording next to the new wording. Nothing is applied. Not to the deployed agent, and not yet to the local copy either.

More background: Reference Guide tab, See the fix before you make it

## Step 4 · Make the change and see what is actually running

A fix nobody measured is a hope with a version number on it. Apply it, run the same set again, put the two runs side by side, and then ask the only question that matters to a customer standing at the register. Ask agy:

```
Make that change, measure it again, and tell me what is still broken in what is actually running.
```

What to expect: agy applies the change to the local copy only, runs the cases saved in Step 2 again rather than writing new ones, and compares the two runs case by case. Expect movement rather than a clean sweep. Then it puts the local copy next to what is actually deployed and tells you what is still true in production: the deployed agent does not have the fix, and anything M3 left open, such as the exposed discount code, is still open. Expect an uncomfortable answer, and treat it as the point of this module rather than a failure of it.

More background: Reference Guide tab, Make the change and see what is actually running

## Decide whether to launch

Nothing to type here. You have the evidence. The judgment is yours, and there are three questions to answer.

- Does this go live? Decide on what the scorecard shows, not on how much work it took to get here.
- What would you fix first? Pick the single failure or weakness that worries you most, and be able to say why it is that one and not another.
- What would you monitor after launch? Name the thing you would want to be told about on the day it starts going wrong.

## What you built

At the start of this lab you could not say what you were running.

- You found what was actually there: a marketing agent missing from the catalog, and two agents sharing one login.
- You fixed it: one identity per agent, access cut back to what each job genuinely needs, and every read of customer data traceable to exactly one agent.
- You controlled the connections: the back-office margin agent names the price-match agent as its one permitted caller, and the rogue login that used to reach it is refused. It sits behind the outbound gateway and can read the pricing data but no longer change it. Broad project-wide roles can still call it, and cleaning those up is a wider job than this lab.
- You screened the content: manipulation aimed at the price-match agent is stopped at the door, in front of that one agent and no other, and the screen is fail-open.
- You measured it: a scored, per-scenario record of how the agent actually behaves, with the reasoning behind every verdict.
- You improved a copy, and you know it is a copy: a change to the agent's instructions, measured on the same set before and after, with the deployed agent untouched.

Visible, attributable, access-controlled, screened at the price-match agent's door and measured — and you got there by describing what you wanted in plain English.

What carries back to your own estate is not the commands. It is the habit: ask what is actually running, insist on evidence rather than assurance, and measure the thing before you trust it.

## See it in the console

There is nothing new to find here, and that is this module's point. If the console asks you to accept its terms the first time you open it, do that and carry on.

- Agent Registry, at https://console.cloud.google.com/agent-platform/agent-registry/agents — set Location to your lab's region (the Region shown in the lab panel), then find Price Match Agent, the one you have spent this module measuring. Its description still says it approves up to 10% directly.
- Its entry is the one the earlier modules left. Nothing here changed it: not the scorecards, not the tougher set, and not the wording change, which exists only in the folder on this workstation. The scorecards themselves are in agy's evidence files in the `novasmart-evidence` folder on your Desktop: agy asks the evaluation service to mark each reply and keeps the results itself, so no saved evaluation run appears in the console.
- Getting that change in front of a customer means a deployment, and that is a separate decision with a separate owner.

## Try this too — optional

These are not steps, and the module is complete without them. Each is a question a real leader would ask at this point. Type any that interest you, in any order, or skip them all.

Ask agy:

```
Which of these did the agent actually answer, and which never got to it?
```

This splits a run into the cases the agent actually answered and the cases something stopped before it, which is the difference between a verdict on the agent and a verdict on everything standing in front of it.

Ask agy:

```
Would this set of tests have caught any of the problems we found earlier this week?
```

This shows you how narrow a scorecard really is: it speaks to one agent's pricing decisions, and most of what you found earlier in the lab sits outside it.

Ask agy:

```
Who is allowed to change these test cases?
```

Whoever can change an expected answer can change every verdict the scorecard will ever produce, so this tells you who that currently is — possibly including the assistant doing the measuring.

## Step 5 · Show what you measured

Turn what you measured into something you can show other people. Pick any of these, in any order; the first is a good place to start. Each one takes agy a few minutes.

The results, case by case:

```
Build me a page where I can read our evaluation results case by case.
```

Who refused each case:

```
Build me an explainer of who actually refused each case: the screen or the agent.
```

The fix, and what is still running:

```
Build me a before-and-after of the fix, and what is still running in production.
```

A game for your team:

```
Build me a game called Judge the Judge from our evaluation, for my team to play.
```

An evidence pack for the launch review:

```
Turn what I measured into a one-page evidence pack for the launch review.
```

What to expect: each page saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome. Each is built only from what agy recorded in Steps 1 to 4, and agy checks it and looks at it before it answers. None of it changes the estate, and none of it makes the launch call for you.
