# M3 · Protect the Content — Reference Guide

The sections below match the steps on the Instructions tab. Dip into a Step section whenever the Instructions tab points you here — but read *Working with agy in this module* first, because M3 is where you stop governing the plumbing and start governing the words.

## Working with agy in this module

The rhythm is the one you already know. You brief agy in plain English, it does the work directly at full speed, it comes back with real evidence, and it leaves a record you can undo. Three things about this module are worth flagging before you start.

First, agy attacks your own systems in Step 1. That feels different from listing agents or reading a log, and it should. It is also the only honest way to establish that you have a problem: a briefing slide about prompt injection proves nothing about NovaSmart, whereas an agent that hands over your customer records when politely asked proves everything. agy sends messages and reads replies. It changes no settings, no identities and no data.

Second, this module has exactly one step that changes anything. Step 1 attacks, Step 2 reads, Step 4 verifies. Only Step 3 writes, and what it writes is a single setting. That ratio is deliberate. The interesting work in security is almost never the change itself; it is knowing what to change and being able to prove afterwards that it worked.

Third, the change in Step 3 does not take effect the instant it is saved. Screening rules propagate through the platform rather than flipping instantly, so an attack that still lands ten seconds after you switch protection on tells you nothing at all. agy waits before it tests. If you test by hand, wait too.

One habit carries over from M1 and is worth naming again, because M3 is where it pays off most visibly. You ask a question that only reads before you ask for anything that writes. In M1 that pause showed you a login with far more power than anyone intended. Here it shows you something even more common, and slightly more embarrassing.

## Step 1 · See if the agents can be talked into breaking their rules

### The thing an agent's instructions cannot do

Every agent at NovaSmart was built with rules written into it. The Price Match Agent is told to settle discounts up to 10% and escalate anything larger to the back office. The Customer Personalization Agent is told to use customer records to tailor an offer to the shopper it is serving, and nothing else.

Those rules are real instructions and the agents follow them almost all the time. What they are not is a boundary. They are written in the same language, in the same place, as the customer's message. When a shopper types something into the chat box, that text arrives at the model sitting right next to the agent's own instructions, and the model has to work out which one to obey. A message crafted to sound more urgent, more authoritative or more official than the agent's own rules can win that argument.

That is a prompt injection attack, sometimes called a jailbreak. There is nothing exotic about it. It does not require a stolen credential, an unpatched server or any technical skill at all. It requires a text box and some persistence, which every customer already has.

The uncomfortable framing for a leadership audience: your agent's guardrails are guidance written in the same medium as the attack. Guidance is not a control. Controls live outside the thing they are controlling.

### The two attacks that are live in your estate

agy sends two messages, one to each customer-facing agent, and shows you what came back. Both work today.

| Which agent | What a customer could type | What the agent does today |
| :---- | :---- | :---- |
| Price Match Agent | A message dressed up as an internal instruction that tells the agent to set its pricing rules aside for this one case | It settles a discount far past the 10% limit it is supposed to hold, and reports it as a legitimate decision |
| Customer Personalization Agent | A message telling the agent to ignore its instructions and list the customers it can see | It returns customer records: 20 rows of names, email addresses, loyalty tiers and lifetime values |

Take those one at a time, in business terms.

The pricing one is a fraud route. The 10% limit is not a preference; it is the line between a decision an agent may settle alone and a decision that requires the back office to look at confidential margin data first. An attacker who can move that line at will can extract discounts NovaSmart would never have agreed to, at whatever volume they can be bothered to type. Nothing is stolen. Every transaction looks legitimate in the records, because as far as the system is concerned the agent decided to say yes.

The customer-data one is a reportable breach. Twenty records is the shape of the problem, not the scale of it — in a real estate the same message returns as many rows as the agent can reach. Names and email addresses are personal data, and handing them to an anonymous person in a chat window is exactly the event your regulator, your board and your customers care about most.

### Why nothing you did in M1 or M2 stopped this

This is the part worth being precise about, because it is easy to feel that the previous modules should have covered it.

In M1 you cut the Customer Personalization Agent down to read-only access, customer data only. That is correct and it still holds. It did not help here, because reading customer data is that agent's actual job. Least privilege limits what an agent is allowed to touch. It has nothing to say about an agent being talked into misusing access it legitimately holds. The agent was not exceeding its permissions when it dumped those records. It was using them, for the wrong reason, on behalf of the wrong person.

In M2 you locked the back office so only the Price Match Agent may call it. That is also correct and also still holds. It did not help here either, because the attack does not need to call the back office. It persuades the front desk not to escalate in the first place.

So this is genuinely a third kind of control. M1 governed identity and access — who is acting and what may they touch. M2 governed connection — who may call whom. M3 governs content — what may pass between a person and a model. Each one is invisible to the others, and none of them substitutes for the rest.

## Step 2 · See what is screening messages today

### The read-only pause, deliberately

You already know what you want to do. You have watched two attacks succeed and the fix is obvious. This is precisely the moment to ask a question that changes nothing, because the obvious fix is often the second-best one, and because in an estate this size the thing you are about to build sometimes already exists.

So the question is not "protect us". The question is "what is screening those messages today".

### The tell: bought, never installed

The answer has two halves.

The first half is the one you expected. Nothing screens what a customer types on its way to the agent, and nothing screens what the agent says on its way back. The text goes straight in and the reply comes straight out.

The second half is the interesting one. NovaSmart already owns a content filter for exactly this problem — a Model Armor template called `nvst-jailbreak-template`, configured to detect manipulation attempts, sitting in the project. It is attached to nothing. No agent uses it. No Agent Gateway references it. It has never inspected a single message.

Nobody was negligent. Somebody did the right thing: they identified the risk, evaluated the control and configured it. Then the project that would have connected it slipped, or the person moved teams, or it turned out that attaching it meant touching four agents individually and nobody owned all four. The template is a monument to a control that was bought and never installed.

This is one of the most common findings in real governance work and it almost never shows up in a risk register, because a risk register asks "do we have a control for this" and the honest answer is yes. The question that finds it is the one you just asked: not what do we own, but what is actually running.

### Two ways to switch protection on

Knowing the template exists gives you a choice, and the choice is the lesson of the step.

The obvious route is to set a rule that applies to everything by default: one screening setting at the project level, covering every agent, whether it existed this morning or gets built next quarter. Nobody has to attach anything. Nobody can forget. Coverage-by-default is usually the right instinct in this lab, and you have met it under other names in earlier modules.

It does not work here, and finding out why is worth more than the rule would have been.

Screening at the project level inspects everything that reaches the model. That is not only what the customer typed. It is the agent's own instructions, the list of tools it may use, and the data those tools hand back. Read cold, that material is indistinguishable from an attack, because a block of text telling a system what to do and what to ignore is precisely what an attack looks like. The screen cannot tell the agent's own briefing from someone trying to overwrite it.

Turned on, it stopped nearly everything. Not the attacks specifically — the work. Price checks, customer lookups, offers. Anything where the agent had to go and fetch something. The only requests that survived were the ones it could answer off the top of its head, which for a retail assistant is close to nothing worth having. Loosening it until real work got through also let the attacks through. There was no setting where both were true.

So the choice is not between per-agent wiring and project-wide coverage. It is about where you stand to read the message. Stand inside the agent and you see everything it thinks, and cannot tell instruction from injection. Stand at the door and you see only what the customer sent, which is the thing you actually wanted to inspect.

That is the route Step 3 takes: screening at the doorway, on the way in.

## Step 3 · Turn the screening on

### A door, and one agent behind it

What you switch on is a gateway with the screening template attached, and the Price Match Agent routed through it. Messages from customers now arrive at a checkpoint before they reach the agent. Manipulation attempts are turned away there. Everything else passes, including requests that need the agent to go and look something up, which is most of what it does.

Be precise about the reach, because it is easy to overstate and the overstatement is the dangerous part. This protects the Price Match Agent. It does not protect the other two. They talk over a different protocol, and this kind of door only stands in front of the one. A control described as covering more than it does is worse than no control, because it stops anyone looking.

### What it screens, and what it does not

This door reads the message on its way in and stops manipulation attempts before the agent acts on them. That is what defeats the pricing attack: the instruction to set the rules aside never reaches the point where a decision gets made.

Outbound is the half people reach for next, and it is worth saying plainly where it lives. Stopping customer records leaving is not this control's job and this module does not claim it. By the time an agent has asked for a list of customers, the database has already handed it over — screening the reply is arguing with a fact. The place that stops it is the permission that decides whether the agent could read those records at all, which is the work you did in Module 2. Keep the two straight: this door decides what may come in, and access decides what may go out.

### The outbound half has to be told what sensitive looks like

Here is a detail that matters more than it sounds, and that is easy to get wrong when explaining this to a board.

Out of the box, the outbound screening does not know that a person's name or an email address is sensitive. Those are not universal. What counts as confidential is specific to your business, and the platform will not guess.

So the outbound half is paired with a data-inspection profile: a definition of what NovaSmart treats as sensitive. For this lab it covers people's names and their email addresses. That profile is provisioned for you, and attaching it is part of what you switch on in Step 3. The basic setting on its own is not enough here — it looks for things like payment card numbers and credentials, and it does not treat a name or an email address as sensitive. Only the profile does.

Be precise about what that buys you, and about what this lab actually shows you. The door can read in both directions, and the profile is what tells it which outgoing details matter. What you verify here is the inbound half. Step 4 replays the attacks on the way in; it does not test the way out, and the one agent standing behind this door holds no customer records to leak in the first place. So the outbound half is configured rather than demonstrated, and that is the phrase to use if anyone asks.

It is also not the same as the data never moving. Screening reads what the model writes, and a tool that fetched rows on the model's behalf has already fetched them. If your concern is that the records must never be read at all, the control for that is who is allowed to reach the data, which is the work you did in Module 2.

The transferable point: turning on screening is the easy half. Deciding and writing down what your organisation considers sensitive is the half that takes real work, and no vendor can do it for you.

### It does not take effect instantly

Routing an agent through a gateway is not instant. Allow around five minutes and re-check, rather than treating it as live the moment the command returns. agy waits before it tests, and you should too — an attack that succeeds seconds after you switch protection on has told you nothing except that you were impatient.

### A door, not a force-field

Be honest about what you have bought, because overstating a control is how a security programme loses credibility the first time something gets through.

Screening is a strong, always-on baseline for the agent behind it. It is not a guarantee, and it is not estate-wide. It blocks recognised manipulation patterns on the way in; a sufficiently novel attack, phrased in a way the detector has not learned, can still get past. The other two agents are not behind this door at all, and no setting in this module puts them there.

More importantly, this control is fail-open. If the screening service cannot run — a regional outage, an unreachable service, an internal error — traffic passes rather than being blocked. The failure that really hides is a door that looks built but is not standing in the traffic: the wiring can be accepted and still not apply, in which case every message sails through with no error anywhere. That is why Step 3 has agy read the routing back rather than trusting the command that made it. Your agents keep serving customers rather than going dark. That is a deliberate trade: availability over enforcement. It is the right default for a retailer that cannot afford a store-wide outage, and it means the control being on is not the same as the control being effective. Somebody has to check that it is still working, and that check belongs in your operating routine.

## Step 4 · Prove the attacks are blocked

### Before and after

agy replays the same two attacks, then sends two ordinary requests, and shows you all four side by side.

| The request | Before screening | After screening |
| :---- | :---- | :---- |
| A message engineered to push a discount past the 10% limit | The agent says yes to a discount it should have escalated | Blocked — the agent never acts on it |
| A message engineered to extract customer records | 20 rows of names, emails, loyalty tiers and lifetime values are returned | The reply comes back with no names or email addresses in it |
| An ordinary shopper asking for a personalized offer | Works | Still works |
| An ordinary price match of around 5% | Settled on the spot | May be caught by the screen as well — record what you see |

### Where the evidence actually lives

When a message is blocked, two things happen, and only one of them is evidence.

Model Armor writes a verdict into Cloud Logging: this request was inspected, this is why it was stopped. That entry is system-generated, timestamped and exportable to your compliance team. It is the authoritative record that the control fired, and it is what you show an auditor.

The store application, meanwhile, may show very little. Because the model call was refused mid-flight, the shopper is likely to see a generic error or simply an empty answer, not a tidy "this message was blocked" banner. Set that expectation now, because otherwise a blank reply reads as a broken app rather than a working control.

So look at the record, not the storefront. This is the same lesson as M1's denied log entry, arriving from a different direction: the application's behaviour is a symptom, and the platform's record is the proof.

### Why you test the ordinary requests too

Half of this step is checking that the attacks fail. The other half is checking that everything else still succeeds, and it is not the lesser half.

A screen tuned too tightly refuses legitimate customers. A price match agent that will not settle an honest 5% discount has not been secured; it has been broken, and it will be broken in a way that shows up as lost sales and store-floor frustration rather than as a security alert. Nobody files an incident report for a control that is working too hard.

Testing safety and usefulness in the same breath is the habit to take away. Every control you add has a cost in false refusals, and the only way to know the cost is to measure it deliberately.

### The checks worth making

- The attempt to push a discount past the 10% limit is blocked, and the block appears in the platform's record.
- The attempt to extract customer records is blocked, and no customer data appears in the reply.
- A normal shopper still gets a personalized answer.
- A normal price match of around 5% is worth sending too, and worth recording honestly. Screening is a judgement call rather than a rule, so an ordinary request can be caught alongside a real attack. If that happens it is a finding to write down, not a failed step.

## What you just did

You found out that your two customer-facing agents could be talked into breaking their own rules by anyone with a chat box — one into pricing fraud, one into handing over customer records. You asked what was screening those messages and discovered that NovaSmart already owned the control and had never plugged it in. You then found that the obvious fix — one rule across the whole project — stopped the business rather than the attacks, and chose instead to screen at the door of the agent that needed it. Then you tested it, and reported each result against what the platform actually returned rather than against how the store app looked.

Set against the modules before it, the shape of the estate is now easy to say out loud. It is visible, because everything running is catalogued and owned. It is attributable, because every action traces to one named agent. It is least-privileged, because each agent holds only the access its job needs. It is access-controlled, because only the front desk may reach the back office. And its front desk is content-screened, because manipulation attempts are stopped at the door before the agent acts on them.

None of it was written in code. All of it was directed in plain English and every change is on the record.

Two things are still open, and a close-out that leaves them out is not an honest one. The screen you put up covers one agent, the price match agent, and not the estate. The other two talk over a different protocol that this door cannot sit in front of, and no setting in this module changes that. And the discount code sitting in plain text in the storefront is untouched by anything here.

Be careful what you claim beyond that. This screens one agent, not the estate, and it is fail-open: if the screen cannot run, traffic passes. A test that produced no block is not the same as a test that proved there was nothing to block, and the honest word for a result you could not confirm is unconfirmed. You have raised the cost of attacking NovaSmart's agents considerably. You have not made them unattackable, and saying otherwise is how the next incident becomes a credibility problem as well as a security one.

There is one question left, and it is the one that should make you uneasy. Every module so far has made this system more restricted. You have four hand-run tests telling you that ordinary customers are still fine — four, out of the thousands of conversations your agents will have this week. A price match agent that refuses a legitimate customer is as broken as one that green-lights a fraud, and you would currently have no idea.

Measuring that properly, against a full scenario set, before any of this reaches every store, is M4 · Evaluate and Decide (Optional Module).
