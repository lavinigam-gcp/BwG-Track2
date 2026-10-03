# M5 · Evaluate and Decide — Instructions

This is the last module, and the first one since M0 that changes nothing in your estate. You have spent the lab locking things down. Here you find out whether the agent you locked down still does its job, and then you make the launch call.

## Where we left off

Your estate is visible and owned. Every agent signs in as itself, so every read of customer data names exactly one of them. Only the price-match agent can reach the back-office margin agent. And messages arriving at the price-match agent are screened for manipulation before it sees them. That door stands in front of that one agent and no other, and you can name the ones it does not cover.

Every one of those describes a control. None of them tells you whether the price-match agent still gives a store associate a useful answer. An agent that turns away an honest customer is broken too, in a way no security check would ever catch — and the harder you tighten, the more likely that becomes.

Nobody is going to report it, either. A shopper who is refused a legitimate match does not file a ticket. They just leave.

So before this rolls out to every store, you test it against a set of realistic requests where you already know the right answer.

## Step 1 · Run the evaluation

NovaSmart has a scenario set for exactly this: a short list of price-match requests written the way a real associate would type them, each paired with the outcome the policy says should happen. Matches up to 10% off, the agent settles on the spot. Anything larger goes to the back office. Anyone trying to talk it into a discount it should not give is refused.

Nothing here touches your environment. The evaluation puts each scenario to the live agent, records what it actually did, and scores that against the policy.

Ask agy:

```
Evaluate our price-match agent against our scenario set and show me how it did.
```

What to expect: agy runs every scenario through the live agent and comes back with a scorecard — what was asked, what the agent did, whether that matched policy, and why. Running the full set takes a few minutes. Nothing in your estate is changed, and there is nothing to undo.

One thing about this run changed in M3, and it changes how you read every refusal in it. The evaluation reaches the price-match agent by the same route the screening now sits on, so a scenario that comes back refused has two possible authors: the screen turned it away before the agent ever saw it, or the agent refused it itself. The scorecard cannot tell those two apart on its own, and only one of them is evidence about the agent. The scenario written to test manipulation is exactly the sort of message that door was built to stop, so it is the likeliest one to be answered by the screen. Tell agy you want the run to name which layer refused each refused scenario, and to show you what it actually received rather than summarising it as a failure.

More background: Reference Guide tab, Run the evaluation

## Step 2 · Read the scorecard

A score is a number. What you actually need is the reasoning underneath it, one case at a time — and the cases that went wrong deserve far more of your attention than the ones that went right.

Ask agy:

```
Walk me through the failures and near-misses.
```

What to expect: agy takes you through anything that did not match policy, and anything that matched for the wrong reason. A right answer reached by faulty reasoning is a near-miss, not a pass, and it will come apart on the next case that looks slightly different.

Refusals now need one extra question. When a scenario is refused, ask which layer refused it. A message stopped by the screen comes back looking like a server error, and the words are the evidence: the reply names the screening service, in text along the lines of "Model Armor: Prompt violates content security configurations". Ask agy to quote that text rather than the status code, because a server-error status on its own reads like a broken agent. If the screen answered, that row is not evidence about the agent at all — it is your M3 control doing its job, and it should be recorded as the screen's refusal whether the run counted it as a failure or passed the screen's words on to be scored as though the agent had said them. Either way the agent was never asked.

That distinction is the same near-miss idea turned on your own security control: the right outcome, produced by something other than the thing you were measuring. It is also the honest reading of what M3 bought you. The screening put a door in front of the manipulation attempt; it did not repair the agent behind the door. This run can tell you the door held against that phrasing. It cannot tell you the agent would refuse on its own.

Two habits keep a scorecard honest, and they are worth saying out loud rather than assuming. The set has a size, that size is fixed before the run starts, and the score is read against it — a total that quietly shrinks to the cases that worked is not a score. And a scenario with no reply recorded is not run: not a pass, not a failure, and it does not migrate into either column once the summary is written. Nothing is complete while anything is still pending.

Ask who marked each case, too. If a separate judge was run, it has a name of its own, and that name is not the agent's own model handed back to you. If no judge was run, the verdicts are agy's own reading of the replies, and the scorecard should say so plainly rather than dressing them up as an independent mark.

If everything passed, hold off on the celebration. Ask agy how many scenarios it actually ran and what each verdict was based on. A clean sweep can mean the agent is good, or it can mean the scenario set is too small, too easy, or was scored against the wrong rulebook.

Watch for one specific mismatch. If anything in the run refers to a 20% limit rather than 10%, the version of the agent that is running is out of step with the policy you think you have. That is worth knowing before launch, not after.

Before you move on, make sure you can answer all of these:

- how many scenarios ran, out of how many the set holds, and whether the two numbers agree
- what the agent actually said in every case that failed
- which layer refused each scenario that was refused, in the words of the reply rather than the status code
- which cases produced no reply at all, and that they are recorded as not run rather than as passes or failures
- whether each verdict came with a reason specific to that case, and who wrote it
- whether the 10% rule is what the run was scored against

More background: Reference Guide tab, Read the scorecard

## Step 3 · Build a tougher set

Four scenarios is enough to catch an agent behaving badly and nowhere near enough to sign off one that appears to be behaving well. It is also a set somebody wrote by hand, which means it holds the cases that person thought of. The ones that catch you out in production are the ones nobody thought of.

So stop hand-writing tests and have the tooling write them, by reading the agent itself.

This is also where the module stops going anywhere near the deployed estate. agy stands up a throwaway project on the workstation, installs the real price-match agent source into it, and works on that. It is the real agent running locally, and the module says so out loud because that is the point: a stand-in that behaved differently would prove nothing. One part is deliberately left out — the hand-off to the back-office margin agent, which depends on an identity that only exists on the deployed estate. Escalation is not exercised locally. That was M2's subject and it was settled there.

Ask agy:

```
Four cases is not enough. Build me a tougher set, including the edge cases.
```

What to expect: agy sets up the local project, puts the real agent into it, and hands the case-writing tool the ground truth it needs — your actual product catalogue and the competitor pricing behind it — so that the cases it writes are about products that exist. That grounding matters more than it sounds. Left to invent, the tool produces plausible-looking product codes that match nothing, every lookup misses, every case is refused for the same dull reason, and you end up with a set that looks thorough while testing one rule out of three. Expect the writing to take a few minutes, and expect conversations rather than one-line requests: a simulated associate who pushes back, corrects a price halfway through, and asks again. The tool is marked experimental by the platform, and that label is worth taking at face value: it usually writes a sensible set rather than dependably writing one, so read the set before you run it.

Before you move on, make sure you can answer all of these:

- whether the cases name products from your own catalogue rather than codes that look plausible and match nothing
- whether the set covers the awkward cases and not four more of the easy one — just inside the limit, past it, and a price claimed that nobody is offering
- how many cases were written, and how many of them actually produced a conversation
- that agy has said plainly this is a local copy of the real agent, with escalation to the back office left out

More background: Reference Guide tab, Build a tougher set

## Step 4 · Run the new set

A bigger set proves nothing until it is scored. This runs the way Step 1 ran: every case put to the agent, every answer marked against the policy, a written reason on each verdict. One difference carries through the rest of the module — the agent being measured from here on is the local copy, not the one serving your stores.

Ask agy:

```
Run the new set and show me the scorecard.
```

What to expect: a scorecard in the same shape as the first one, longer and considerably less tidy. Expect failures. A tougher set that everything passes is a set that is not tough. Expect some cases to come back with no conversation in them at all, as well: a simulation that fails partway is still written into the set, empty. Those are not run. They are not passes and they are not failures, and they belong in their own column with the reason they are there.

The two habits from Step 2 apply to this run too, and they are worth checking rather than assuming they carried over. The set has a size, fixed before the run starts, and the score is read against that size. And nothing is described as complete while a case is still pending — a run called complete a paragraph above a table listing cases as not run is telling you two stories at once, and one of them is wrong.

Before you move on, make sure you can answer all of these:

- how many cases were scored, out of how many the set holds, with any difference named rather than absorbed
- that cases with no reply are marked not run, and stay that way in the total
- whether every verdict carries a reason specific to that case
- who marked each case: a judge that was actually run, or agy's own reading of the replies

More background: Reference Guide tab, Run the new set

## Step 5 · See the fix before you make it

You now have more than one thing to worry about, so pick the worst one. And before anything changes, look at the change. You would not let a supplier alter a production system on a verbal description of what they were about to do, and the fact that this change is written in plain English rather than code does not make it a smaller change.

Ask agy:

```
Take the worst one and show me the fix before you change anything.
```

What to expect: agy takes the worst case, explains what went wrong in it, and shows you the proposed fix as a before-and-after of the agent's written instructions — the old wording next to the new wording. Nothing is applied. Not to the deployed agent, and not yet to the local copy either. Read it the way you would read any change request: what exactly changes, what else that wording touches, and whether it addresses the cause or covers the symptom.

Before you move on, make sure you can answer all of these:

- whether you can see the actual wording that would change, rather than a description of it
- whether the change is tied to a named case and to the reason that case failed
- that nothing has been applied yet, and agy has said so
- what the change might break, as well as what it should fix

More background: Reference Guide tab, See the fix before you make it

## Step 6 · Make the change and measure it

A fix nobody measured is a hope with a version number on it. Apply it, run the same set again, and put the two runs side by side. The change goes to the local copy and nowhere else, which is the only reason it is sensible to make it in the middle of a meeting.

Ask agy:

```
Make that change and measure it again.
```

What to expect: agy applies the change to the local copy, runs the same set again, and compares the two runs case by case. Expect movement rather than a clean sweep. Some cases should improve, and it is normal — healthier, even — for others to still fail. One wording change that takes everything to full marks is the shape of a demonstration rather than the shape of a measurement, and it usually means the set was too easy or the second run was not the same set. The comparison is only worth reading if both runs scored the same cases, so confirm that before you read anything else.

Before you move on, make sure you can answer all of these:

- that both runs used the same set, with the same number of cases behind both totals
- that the comparison is case by case, rather than one total against another
- whether anything got worse, not only what got better
- that agy has stated the change went to the local copy and nowhere else

More background: Reference Guide tab, Make the change and measure it

## Step 7 · Check what is actually running

You have a fix, and you have evidence that it helps. Now ask the only question that matters to a customer standing at a till: is any of that true of the agent serving them right now?

Ask agy:

```
What is still broken in what is actually running?
```

What to expect: agy puts the local copy next to what is actually deployed and tells you what is still true in production. Expect an uncomfortable answer, and treat it as the point of the module rather than a failure of it. The improvement is real and it is local. It was measured on a copy on this workstation, and it has not been shipped anywhere — nothing in this module deployed anything. What is running in your stores is the agent you put behind a screen in M3, and a screen stands in front of a flaw rather than repairing it. The local copy is the real agent's own source, which is why it carried the same weakness until you changed it here, and why changing it here changes nothing for a customer.

So what you are looking at is a gap between what is configured and what is running. It is the same gap you have been hunting all day, except that this time you opened it deliberately and can see both sides of it. Closing it means a deployment, which is owned by the team that owns the agent, and it is not something this module does.

Before you move on, make sure you can answer all of these:

- that agy separates what was measured on the local copy from what is true of the deployed agent
- that agy states plainly nothing was deployed in this module
- that the protection on the deployed agent is described as a screen in front of it, not as a repair of it
- what would have to happen, in one sentence, for this improvement to reach a customer

More background: Reference Guide tab, Check what is actually running

## Step 8 · Decide whether to launch

No prompt for this step. You have the evidence. The judgment is yours, and there are three questions to answer.

- Does this go live? Decide on what the scorecard shows, not on how much work it took to get here.
- What would you fix first? Pick the single failure or weakness that worries you most, and be able to say why it is that one and not another.
- What would you monitor after launch? Name the thing you would want to be told about on the day it starts going wrong.

A scorecard is a photograph, not a guarantee. It says the agent behaved this way today, on these scenarios. Real shoppers ask things nobody wrote down, and people trying to manipulate an agent keep changing their wording. Whichever way you decide, the scenario set needs to grow and the agent needs watching once it is live.

The call is also not yours alone to make. Take the scored, per-scenario record to risk and compliance and decide together. That record is the reason the conversation will be a short one.

## Step 9 · What you built

At the start of this lab you could not say what you were running.

- You found what was actually there: a marketing agent nobody had catalogued, and two agents sharing one login, so their reads of customer data could not be told apart.
- You fixed it: the hidden agent registered under a named owner, one identity per agent, and access cut back to what each job genuinely needs. Every read of customer data now traces to exactly one agent.
- You controlled the connections: the back-office margin agent now names the price-match agent as its one permitted caller, and the rogue login that used to reach it is refused.
- You screened the content: manipulation attempts aimed at the price-match agent are stopped at the door before the agent sees them. That door stands in front of that one agent and no other — a narrower claim than saying the estate is screened, and a more useful one, because it names exactly where the gap is.
- You measured it: a scored, per-scenario record of how the agent actually behaves, with the reasoning behind every verdict.

Visible, attributable, access-controlled, screened at the price-match agent's door and measured — and you got there by describing what you wanted in plain English.

Be honest about the edges, because that is what makes the rest credible. The agent is not perfect and this lab did not make it so. Risk was reduced, not removed. Nothing here lowered your cloud bill, and a small scenario set is a starting point rather than a warranty.

What carries back to your own estate is not the commands. It is the habit: ask what is actually running, insist on evidence rather than assurance, and measure the thing before you trust it.

## Try this too — optional

These are not steps, and the module is complete without them. Each one is a question a real leader
would ask at this point. Type any that interest you, in any order, or skip them all.

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

Whoever can change an expected answer can change every verdict the scorecard will ever produce, so this tells you who that currently is.
