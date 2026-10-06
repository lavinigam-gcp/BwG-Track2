# M3 · Protect the Content — Instructions

M2 settled who may call whom. M3 settles what may be said. As in the modules before it, agy acts directly rather than stopping to ask permission before each change, and everything it changes is recorded and can be undone.

## Where we left off

The back office is locked down. Its list of permitted callers now names the Price Match Agent and nothing else, and the rogue login that used to reach it is refused.

That controls which agent may reach which agent. It says nothing about what a person types into a chat box. Two of your agents face customers directly — the Price Match Agent on the store floor and the Customer Personalization Agent on the website — and both read whatever a shopper sends and pass it straight to the AI. A locked door does not help if you let a trap walk through it.

## Step 1 · See if the agents can be talked into breaking their rules

Start by finding out whether the problem is real in your estate, rather than real in general. Do not take it from a briefing slide. Have agy behave like a customer with bad intentions, send the messages itself, and show you exactly what the live agents did with them.

Ask agy:

```
Can a customer talk our agents into breaking their own rules? Try it and show me.
```

What to expect: agy sends attacker-style messages to the two agents that face customers and shows you the real replies. Both attacks land. The Price Match Agent goes past the 10% discount limit it is supposed to hold and says yes to a discount it should have escalated, and the Customer Personalization Agent hands over customer records to someone who simply asked for them. Nothing in your environment is changed — agy only sent messages.

Sit with that for a moment before you move on. The agents were not broken into. They were asked politely, in English, and they complied.

More background: Reference Guide tab, See if the agents can be talked into breaking their rules

## Step 2 · See what is screening messages today

Same discipline you practised in M1. Before you switch anything on, ask what is already there. This step changes nothing.

Read the answer carefully. There is something in it that most estates have and almost nobody notices, and spotting it yourself is the point of the step.

Ask agy:

```
Don't change anything yet. What is screening those messages today?
```

What to expect: a plain-English readout of what inspects customer messages before they reach your agents, and what inspects the replies on the way back. The short answer is nothing. The longer answer is more interesting: NovaSmart already owns a Model Armor content filter, `nvst-jailbreak-template`, built for exactly this and connected to nothing at all. Your environment is unchanged.

More background: Reference Guide tab, See what is screening messages today

## Step 3 · Turn the screening on

You own the protection. It has never been switched on. The screening rule you saw in Step 2 exists, and nothing routes through it.

There is a project-wide version of this control, and it is the obvious thing to reach for. It is also the wrong thing here, and it is worth knowing why before you choose. Turned on across the whole project, it inspects everything an agent assembles internally — its own instructions, the tools it is allowed to call, the data those tools hand back. That traffic looks a great deal like an attack, because a set of instructions telling a system what to do is exactly what an attack is. Switched on, it stopped almost every piece of real work: price checks, customer lookups, offers. The only requests that survived were ones the agent could answer without doing anything.

So you screen at the door instead, where the only thing being read is what the customer actually sent.

Ask agy:

```
Put the price match agent behind the gateway and screen what clients send it.
```

What to expect: agy wires the screening template to the gateway and routes the Price Match Agent through it, then confirms the routing. Ask which agent this covers, and expect a single name — this protects the Price Match Agent, not the estate. The other two agents talk over a different protocol that this door does not sit in front of. The routing takes around five minutes to take effect, and agy waits before testing, so an early "it still got through" does not mislead you. If anything looks wrong, tell agy to undo it.

More background: Reference Guide tab, Turn the screening on

## Step 4 · Prove the attacks are blocked

A control you have not tested is a control you are hoping for. Send the same two attacks again, and — just as important — send two ordinary requests, because a screen that stops real customers is its own kind of outage.

Ask agy:

```
Run those attacks again. Are they blocked now, and do normal requests still work?
```

What to expect: the manipulation attempt is stopped before the agent sees it, and ordinary requests go through untouched, including ones that need the agent to look something up.

One detail matters more than it should. A blocked message comes back looking like a server error, because that is the status code the platform returns. It is not a server error. The text of the reply names the screening service, and that text is the evidence. Ask agy to quote the message rather than the code, and be suspicious of any report that says "it failed" without showing you what the failure said — a broken agent and a blocked attack look identical until you read the words.

Check that all of these are true before you move on:

- the attempt to force a discount past the 10% limit is stopped, and the reply names the screening service
- an ordinary price match of around 5% goes through and gets an answer
- a request that needs the agent to look something up still works, rather than failing at the lookup
- agy says which agent it tested, and does not claim more coverage than it checked

That third check is the one worth dwelling on. A screen that blocks attacks and also blocks your business is not a security control, it is an outage with good intentions. You are confirming you did not buy safety by switching the agent off.

More background: Reference Guide tab, Prove the attacks are blocked

## Step 5 · Sum up what you can actually claim

Your estate is now visible, attributable, least-privileged and access-controlled. Content screening is the narrower one: it covers the Price Match Agent, the single agent now behind the gateway, and not the other two. None of it was written in code, and every change is on the record.

Before you tell anyone that, it is worth separating what you proved from what you assume. That distinction is the whole value of the last four steps, and it is the first thing a regulator or an incident review will ask for.

Ask agy:

```
Sum it up. What are we actually protected against now, and what are we not?
```

What to expect: a short account of what is now true and backed by a record you can point at, and a plain list of what is not. Expect it to name limits rather than skip them. Screening is a floor, not a force-field, and it is fail-open, so if it cannot run the traffic passes. It stands in front of one agent rather than the estate, and the two agents that talk over the other protocol cannot be put behind it. The filter NovaSmart already owned is now doing a job, which is the one thing that genuinely changed. Anything the tests could not confirm should be described as unconfirmed rather than quietly counted as a pass.

Check that all of these are true before you move on:

- every claim of a block points at a record, and anything unproven is named as unproven
- the limits are stated plainly, including fail-open and what the outbound screening does not cover
- the two agents this screen cannot reach, and the exposed discount code, are both still listed as open
- there is no all-clear, and no claim that the agents are now safe

More background: Reference Guide tab, What you just did

Which raises the question you should be nervous about. You have made this system harder to abuse. Have you also made it worse at its job? A price match agent that refuses a legitimate customer is broken just as surely as one that green-lights a fraud, and you would not find that out from four hand-run tests.

M4 · Evaluate and Decide (Optional Module) is where you stop spot-checking and start measuring: run the agent against a full scenario set — the deals it should settle, the ones it should escalate, the ones it should refuse, and the traps it should catch — and read the score before you roll it out to every store.

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

This shows you which agents the door actually stands in front of, and why an agent you tested is not the same as an agent you covered.

Ask agy:

```
What level is this screen set to, and who decided that?
```

This shows you that somebody chose how suspicious this screen is, and what moving that choice in either direction would cost you.
