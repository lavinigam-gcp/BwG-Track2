# M4 · Evaluate and Decide (Optional Module) — Instructions

You test whether the price-match agent still does its job, then make the launch call. This module changes nothing in your estate and is not scored; "scorecard" here means the evaluation results.

## Key objective

Score the price-match agent against its policy with the Gen AI evaluation service, using a judge model separate from the agent's own.

- Run the existing scenario set and read the scorecard, case by case.
- Have the tooling write a tougher set and score a local copy against it.
- See a proposed change to the agent's instructions before anything changes.
- Run the same set again after the change and compare both runs.

Why it matters: a per-scenario record with reasons is evidence you can hand to risk and compliance, not an opinion.

## Where we left off

- Every agent signs in as itself. The back-office margin agent names the price-match agent as its one permitted caller (project-wide roles aside) and can read but not change pricing data.
- If you ran M3, a fail-open screen sits in front of the price-match agent only; the customer-record attack is not screened.
- None of this shows whether the agent still gives associates useful answers.

## Step 1 · Run the evaluation and read the scorecard

<!-- FIGURE:K4S1 BEGIN -->

![Map of the NovaSmart agent estate, M4 Step 1. 1: the Gen AI evaluation service sends the scenario set through the Inbound gateway, with Model Armor in front, to the deployed Price Match Agent. 2: a judge model in that service, separate from the agent's own model, scores each reply. Nothing in the estate changes. Architecture-and-workflow map.](images/K4S1_map.webp)

<!-- FIGURE:K4S1 END -->

**Goal:** Score the deployed agent on NovaSmart's scenarios: up to 10% settled on the spot, more goes to the back office, manipulation refused.

Ask agy:

```
Evaluate our price-match agent against our scenario set, and walk me through the failures and near-misses.
```

**What to expect:**

- One row per scenario: what was asked, what the agent did, whether it matched policy, and why; then failures and right-for-the-wrong-reason passes.
- agy names the judge model and the agent's model, which differ; if no judge ran, it says the verdicts are its own reading. Under the policy, only the 15% case should go to the back office.
- If a screen is attached and stops a request, agy quotes its message and says the agent was never asked; with no screen, it says so. Any limit other than 10% means drift.
- It takes a few minutes. Nothing in your estate changes.

More background: Reference Guide tab, Run the evaluation and read the scorecard

## Step 2 · Build a tougher set and run it

<!-- FIGURE:K4S2 BEGIN -->

![Map of the NovaSmart agent estate, M4 Step 2. 1: agy has a tougher set of cases written into one saved case file. 2: the cases run on the local copy of the Price Match Agent in a folder on your workstation. 3: the Gen AI evaluation service's judge model scores the replies. A dashed grey line marks that the local copy cannot read the competitor data. The deployed agent is not touched. Architecture-and-workflow map.](images/K4S2_map.webp)

<!-- FIGURE:K4S2 END -->

**Goal:** Have the tooling write a bigger set than four hand-written cases.

Ask agy:

```
Four cases is not enough. Build me a tougher set including the edge cases, then run it and show me the scorecard.
```

**What to expect:**

- agy copies the real agent into a folder on this workstation; the tooling writes cases from your catalog and competitor pricing: at least eight, or agy says how many short.
- The cases go to one file so Step 4 runs the same set. Expect a few minutes, a longer scorecard, and likely failures.
- The local copy differs in three ways agy states: no hand-off to the back office, no screen, and it cannot read competitor prices.
- Nothing in your estate changes; the copy is not deployed.

More background: Reference Guide tab, Build a tougher set and run it

## Step 3 · See the fix before you make it

<!-- FIGURE:K4S3 BEGIN -->

![Map of the NovaSmart agent estate, M4 Step 3. 1: agy takes the worst case from the saved case file's run on the local copy. 2: it reads the rule in the local copy and drafts a one-line change, shown in amber with a dashed outline because nothing is applied. The deployed estate is untouched.](images/K4S3_map.webp)

<!-- FIGURE:K4S3 END -->

**Goal:** Pick the worst failure and review the proposed change before anything is applied.

Ask agy:

```
Take the worst one and show me the fix before you change anything.
```

**What to expect:**

- agy explains what went wrong in the worst case.
- It shows the fix as the old instruction wording next to the new.
- Nothing is applied, not to the deployed agent and not yet to the local copy.

More background: Reference Guide tab, See the fix before you make it

## Step 4 · Make the change and see what is actually running

<!-- FIGURE:K4S4 BEGIN -->

![Map of the NovaSmart agent estate, M4 Step 4. 1: agy applies the one-line change to the local copy, now green. 2: the same case file is replayed on it. 3: the Gen AI evaluation service's judge model scores the replies. 4: the two runs are compared. The deployed Price Match Agent is unchanged and carries a red 'no fix' marker.](images/K4S4_map.webp)

<!-- FIGURE:K4S4 END -->

**Goal:** Apply the fix to the local copy, measure it on the same set, and compare with what your stores run.

Ask agy:

```
Make that change, measure it again, and tell me what is still broken in what is actually running.
```

**What to expect:**

- agy changes the local copy only, reruns the cases saved in Step 2, and compares the two runs case by case. Expect movement, not a clean sweep.
- Then what is still true in production: the deployed agent lacks the fix, and the rule that reveals the discount code is still in its source.
- Expect an uncomfortable answer; that is the point. Nothing in your estate changes or is deployed.

More background: Reference Guide tab, Make the change and see what is actually running

## Decide whether to launch

**Goal:** Make the launch call yourself; agy gives input but does not decide.

- Does this go live? Decide on what the scorecard shows, not on how much work it took.
- What would you fix first, and why that one?
- What would you monitor after launch, so you hear the day it starts going wrong?

## What you built

- Found: a marketing agent missing from the catalog, two agents sharing one login.
- Fixed: one identity per agent, least access, every customer-data read traceable to one agent.
- Controlled: the back-office margin agent names the price-match agent as its one permitted caller (project-wide roles aside), sits behind the outbound gateway, and reads but cannot change pricing data.
- Screened (if you ran M3): a fail-open screen in front of the price-match agent only.
- Measured: a per-scenario record with reasons, and a fix measured on a local copy, the deployed agent untouched.

The habit to take home: ask what is running, insist on evidence, measure before you trust.

## See it in the console

- Agent Registry, at https://console.cloud.google.com/agent-platform/agent-registry/agents — set Location to your lab's region; Price Match Agent is unchanged, and its description still says it approves up to 10% directly.
- Scorecards live in the `novasmart-evidence` folder on your Desktop, not the console; the wording change exists only in the folder on this workstation. Deploying it is a separate decision.

## Try this too — optional

*Optional.* Ask any of these, in any order, or skip them.

Ask agy:

```
Which of these did the agent actually answer, and which never got to it?
```

This shows you which verdicts are on the agent and which are on something standing in front of it.

Ask agy:

```
Would this set of tests have caught any of the problems we found earlier this week?
```

This shows you how narrow a scorecard is: one agent's pricing decisions.

Ask agy:

```
Who is allowed to change these test cases?
```

This shows you who can change every verdict by changing an expected answer, including agy itself.

## Step 5 · Show what you measured

*Optional.* You can skip this, or open the **What did we learn?** tab.

Pick any of these, in any order. Each takes agy a few minutes.

```
Build me a page where I can read our evaluation results case by case.
```

The results, case by case.

```
Build me an explainer of who actually refused each case: the screen or the agent.
```

Who refused each case: the screen or the agent.

```
Build me a before-and-after of the fix, and what is still running in production.
```

The fix, and what is still running.

```
Build me a game called Judge the Judge from our evaluation, for my team to play.
```

A game for your team.

```
Turn what I measured into a one-page evidence pack for the launch review.
```

An evidence pack for the launch review.

Each page is saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome, built only from what agy recorded in Steps 1 to 4. Nothing in your estate changes, and no page makes the launch call for you.
