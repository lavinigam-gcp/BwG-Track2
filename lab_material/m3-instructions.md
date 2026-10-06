# M3 · Protect the Content — Instructions

M2 settled who may call whom. M3 settles what may be said. As in the modules before it, agy acts directly rather than stopping to ask permission before each change, and every change it makes is recorded. Step 3 tells you which part of its change can be reversed and which cannot.

## Key objective

Put a Google Cloud Model Armor filter on the inbound gateway in front of the Price Match Agent, so manipulation attempts are stopped before that one agent ever reads them.

- Watch agy talk two of your customer-facing agents into breaking their own rules, in plain English, with no stolen credential and no technical skill.
- Ask what screens customer messages today, and find a content filter NovaSmart already owns and has never connected to anything.
- Route the Price Match Agent through the inbound gateway with that filter attached, and confirm by name which single agent it covers.
- Replay the attacks, see the discount attack stopped before the agent reads it, and check that ordinary requests still work. The customer-record attack is not covered by this screen, and agy says so.
- Finish with a plain account of what you can claim: this screen stands in front of one agent, not the estate.

Why it matters: an agent that reads whatever a shopper types, with nothing checking it first, can be talked into settling a discount it should have escalated, or into handing over customer records.

## Where we left off

The back office now names one permitted caller, the Price Match Agent, and the leftover login that used to reach it is refused. It sits behind the outbound gateway, and it can read the pricing data but no longer change it. Broad project-wide roles can still call it; that is written down as remaining work.

That controls which agent may reach which agent. It says nothing about what a person types into a chat box. Two of your agents face customers directly — the Price Match Agent on the store floor and the Customer Personalization Agent on the website — and both read whatever a shopper sends and pass it straight to the AI. A locked door does not help if you let a trap walk through it.

## Step 1 · See if the agents can be talked into breaking their rules

Start by finding out whether the problem is real in your estate, rather than real in general. Do not take it from a briefing slide. Have agy behave like a customer with bad intentions, send the messages itself, and show you exactly what the live agents did with them.

Ask agy:

```
Can a customer talk our agents into breaking their own rules? Try it and show me.
```

What to expect: agy sends attacker-style messages to the two agents that face customers and shows you the real replies. Both attacks land. The Price Match Agent goes past the 10% discount limit it is supposed to hold and says yes to a discount it should have escalated, and the Customer Personalization Agent hands over customer records to someone who simply asked for them. agy shows you how many records came back and which details they held, with the personal details masked rather than printed. It also sends two ordinary requests, so Step 4 has a before for those too. Nothing in your environment is changed — agy only sent messages.

Sit with that for a moment before you move on. The agents were not broken into. They were asked politely, in English, and they complied.

More background: Reference Guide tab, See if the agents can be talked into breaking their rules

## Step 2 · See what is screening messages today

Same discipline you practiced in M1. Before you switch anything on, ask what is already there. This step changes nothing.

Read the answer carefully. There is something in it that most estates have and almost nobody notices, and spotting it yourself is the point of the step.

Ask agy:

```
Don't change anything yet. What is screening those messages today?
```

What to expect: a plain-English readout of what inspects customer messages before they reach your agents, and what inspects the replies on the way back. The short answer is nothing. The longer answer is more interesting, and it is worth reading to the end. Your environment is unchanged.

More background: Reference Guide tab, See what is screening messages today

## Step 3 · Turn the screening on

You own the protection. It has never been switched on. The filter you saw in Step 2 exists, and nothing routes through it.

There is a project-wide version of this control, and it is the obvious thing to reach for. It is also the wrong thing here, and it is worth knowing why before you choose. Turned on across the whole project, it inspects everything an agent assembles internally — its own instructions, the tools it is allowed to call, the data those tools hand back. That traffic looks a great deal like an attack, because a set of instructions telling a system what to do is exactly what an attack is. When NovaSmart's engineers switched it on, it stopped almost every piece of real work: price checks, customer lookups, offers. The only requests that survived were ones the agent could answer without doing anything.

So you screen at the door instead, where the only thing being read is what the customer actually sent. The door is NovaSmart's inbound gateway: it stands in front of an agent and sees what clients send it. It is not the outbound gateway the back office sits behind since M2, which decides where the back office may reach.

Ask agy:

```
Put the price match agent behind the inbound gateway and screen what clients send it.
```

What to expect: agy adds a screening rule to the inbound gateway that hands each message to the filter you found in Step 2, routes the Price Match Agent through that gateway, then reads the routing back from the agent to confirm it took. Ask which agent this covers, and expect a single name — this protects the Price Match Agent, not the estate. The other two agents are reached over a different protocol that this screen does not read, and the back office's outbound gateway from M2 is left as it is. The routing takes around five minutes to take effect, and agy waits before testing, so an early "it still got through" does not mislead you.

If you want it gone, agy can take the Price Match Agent back out from behind the inbound gateway. One thing does not come back: any change to an agent's gateway routing archives the agent's earlier revisions, and archiving cannot be reversed. agy notes that in its record of the change.

More background: Reference Guide tab, Turn the screening on

## Step 4 · Prove the attacks are blocked

A control you have not tested is a control you are hoping for. Send the same two attacks again, and — just as important — send two ordinary requests, because a screen that stops real customers is its own kind of outage.

Ask agy:

```
Run those attacks again. Are they blocked now, and do normal requests still work?
```

What to expect: the manipulation attempt on the Price Match Agent is stopped before the agent sees it, and ordinary requests go through untouched, including ones that need the agent to look something up. The customer-record attack still gets an answer: that agent is not behind the inbound gateway, and agy reports it as not covered rather than as a failure.

One detail matters more than it should. A blocked message comes back as an error, not as an answer, and it can look like something broke. It did not. The words of that reply are the evidence, and agy quotes them exactly as they came back, with the time. Be suspicious of any report that says "it failed" without showing you what the failure said — a broken agent and a blocked attack look identical until you read the words. That quoted reply is the record of the block. Do not expect a matching verdict in Cloud Logging: NovaSmart's filter is not set to log its verdicts.

Check that all of these are true before you move on:

- the attempt to force a discount past the 10% limit is stopped, and agy quotes the reply exactly as it came back
- an ordinary price match of around 5% goes through and gets an answer
- a request that needs the agent to look something up still works, rather than failing at the lookup
- the customer-record attack is reported as not covered, with the reason, and not as blocked
- agy says which agent it tested, and does not claim more coverage than it checked

The lookup check is the one worth dwelling on. A screen that blocks attacks and also blocks your business is not a security control, it is an outage with good intentions. You are confirming you did not buy safety by switching the agent off.

Where the proof goes: agy writes the full check-by-check table to `m3_step4.txt` in the `novasmart-evidence` folder on your Desktop and tells you in one line how many of the checks it could prove. It then updates your Governance Scorecard, a web page it generates on your Desktop, and gives you the link to open it. The customer-record attack counts as not covered, which does not fail the module. A FAIL names the check that did not hold and the step to go back to.

More background: Reference Guide tab, Prove the attacks are blocked

## Step 5 · Sum up what you can actually claim

Set against the modules before it, here is what you can say. Everything running is catalogued and owned, every agent signs in as itself, and customer records are limited to the agents that need them. The back office names one permitted caller, and it can read the pricing data but not change it. Content screening is the narrower one: it covers the Price Match Agent, the one agent behind the inbound gateway, and not the other two. None of it was written in code, and every change is on the record.

Before you tell anyone that, it is worth separating what you proved from what you assume. That distinction is the whole value of the last four steps, and it is the first thing a regulator or an incident review will ask for.

Ask agy:

```
Sum it up. What are we actually protected against now, and what are we not?
```

What to expect: a short account of what is now true and backed by a record you can point at, and a plain list of what is not. Expect it to name limits rather than skip them. Screening is a baseline, not a force-field, and it is set to fail open: if the screen cannot run, the traffic passes with no error, which is a remaining risk rather than a footnote. It stands in front of one agent rather than the estate, and the two agents reached over the other protocol cannot be screened by it. The inbound gateway also reads the agent's replies, but with the same filter, which looks for manipulation and harmful content, not names or email addresses, and nothing in this module tested the way out. The filter NovaSmart already owned is now doing a job, which is the one thing that genuinely changed. Anything the tests could not confirm should be described as unconfirmed rather than quietly counted as a pass.

Check that all of these are true before you move on:

- every claim of a block points at a quoted reply, and anything unproven is named as unproven
- the limits are stated plainly, including that the screen fails open and that the way out was not tested
- the two agents this screen cannot reach, and the exposed discount code, are both still listed as open
- there is no all-clear, and no claim that the agents are now safe

More background: Reference Guide tab, What you just did

## Step 6 · What's next

The Price Match Agent now sits behind the inbound gateway, and the message that talked it past its discount limit is turned away before the agent reads it. Ordinary requests still get answers. The filter NovaSmart owned and never switched on is finally doing a job.

Stay precise about what that buys you. The customer-record attack still works, because that agent is not behind the door and this screen cannot reach it. The screen is set to fail open, so a screen that cannot run lets everything through without a sound. And the discount code sitting in plain text in the storefront is untouched. Those are real remaining work, worth writing down rather than glossing over.

Which raises the question you should be nervous about. You have made this system harder to abuse. Have you also made it worse at its job? A price match agent that refuses a legitimate customer is broken just as surely as one that green-lights a fraud, and you would not find that out from four hand-run tests.

M4 · Evaluate and Decide (Optional Module) is where you stop spot-checking and start measuring: run the agent against a full scenario set — the deals it should settle, the ones it should escalate, the ones it should refuse, and the traps it should catch — and read the score before you roll it out to every store.

## See it in the console

Three pages in the Google Cloud console show part of what you worked with. If the console asks you to accept its terms the first time you open it, do that and carry on.

- Model Armor, at https://console.cloud.google.com/security/modelarmor/templates — the Templates tab lists nvst-jailbreak-template, created when your lab was set up; nothing you did created it. The page lists filters, not where they are used, so it cannot tell you which agent is behind the screen.
- Agent Gateway, at https://console.cloud.google.com/agent-platform/gateways — two gateways: novasmart-ingress-gateway, the inbound one the Price Match Agent now sits behind, and novasmart-egress-gateway, the outbound one the back office has sat behind since M2. The list does not show which agent sits behind each gateway; agy read that from the Price Match Agent itself in Step 3.
- Agent Registry, at https://console.cloud.google.com/agent-platform/agent-registry/agents — set Location to your lab's region (the Region shown in the lab panel). The Agent Type column shows the Price Match Agent as Non A2A and the other two NovaSmart agents as A2A. That is the protocol difference that keeps them out of reach of this screen.

## Try this too — optional

These are not steps, and the module is complete without them. Each one is a question a real leader
would ask at this point. Type any that interest you, in any order, or skip them all.

Ask agy:

```
We owned that filter and never switched it on. What else have we paid for and never switched on?
```

This shows you the gap between the controls your estate owns and the controls that are actually in force, which are almost never the same list.

Ask agy:

```
How would we know if this screening quietly stopped working?
```

This shows you how a screen like this fails, and why silence coming back from it is not the same thing as safety.

Ask agy:

```
Does this cover every agent, or only the two we just tested?
```

This shows you which agents the inbound gateway actually stands in front of, and why an agent you tested is not the same as an agent you covered.

Ask agy:

```
What level is this screen set to, and who decided that?
```

This shows you that somebody chose how suspicious this screen is, and what moving that choice in either direction would cost you.

## Step 7 · Show what you screened

Turn what you screened into something you can show other people. Pick any of these, in any order; the first is a good place to start. Each one takes agy a few minutes.

A replay of the two attacks:

```
Build me a replay of the two attacks, before and after the screen.
```

A map of what the screen covers:

```
Build me a map of which agents the screen covers and which it does not.
```

The filter you owned, explained:

```
Build me an explainer of the filter we owned and never switched on.
```

A game for your team:

```
Build me a game called Trap or Customer from what I screened, for my team to play.
```

An update for your board:

```
Turn what I screened into a two-minute update I can present to the board.
```

What to expect: each page saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome. Each is built only from what agy recorded in Steps 1 to 5, and agy checks it and looks at it before it answers. None of it changes the estate.
