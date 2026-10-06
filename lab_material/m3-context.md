# M3 · Protect the Content — Reference Guide

The sections below match the steps on the Instructions tab. Dip into a Step section whenever the Instructions tab points you here — but read *Working with agy in this module* first, because M3 is where you stop governing the plumbing and start governing the words.

## Working with agy in this module

The rhythm is the one you already know. You brief agy in plain English, it does the work directly at full speed, it comes back with real evidence, and it leaves a record of what changed. Three things about this module are worth flagging before you start.

First, agy attacks your own systems in Step 1. That feels different from listing agents or reading a log, and it should. It is also the only honest way to establish that you have a problem: a briefing slide about prompt injection proves nothing about NovaSmart, whereas an agent that hands over your customer records when politely asked proves everything. agy sends messages and reads replies. It changes no settings, no identities and no data.

Second, this module has exactly one step that changes the estate. Step 1 attacks, Step 2 reads, Step 4 verifies. Only Step 3 writes: it adds a screening rule to the inbound gateway and routes one agent through it, which takes three linked changes. That ratio is deliberate. The interesting work in security is almost never the change itself; it is knowing what to change and being able to prove afterwards that it worked.

Third, the change in Step 3 does not take effect the instant it is saved. Screening rules propagate through the platform rather than flipping instantly, so an attack that still lands ten seconds after you switch protection on tells you nothing at all. agy waits before it tests. If you test by hand, wait too.

One habit carries over from M1 and is worth naming again, because M3 is where it pays off most visibly. You ask a question that only reads before you ask for anything that writes. In M1 that pause showed you a login with far more power than anyone intended. Here it shows you something even more common, and slightly more embarrassing.

A word on the two gateways, because M2 used one and M3 uses the other. NovaSmart has two. The outbound gateway decides where an agent may reach; M2 put the back office behind it, and it reads no message content. The inbound gateway stands in front of an agent and sees what clients send it. When this module says the door, it means the inbound gateway.

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

agy shows you the customer records as a count and a list of the details they held, with one example row whose personal details are masked. It does not print the records themselves. It also sends two ordinary requests, one to each agent, so that Step 4 has a before for those as well as for the attacks.

Take the two attacks one at a time, in business terms.

The pricing one is a fraud route. The 10% limit is not a preference; it is the line between a decision an agent may settle alone and a decision that requires the back office to look at confidential margin data first. An attacker who can move that line at will can extract discounts NovaSmart would never have agreed to, at whatever volume they can be bothered to type. Nothing is stolen. Every transaction looks legitimate in the records, because as far as the system is concerned the agent decided to say yes.

The customer-data one is a reportable breach. Twenty records is the shape of the problem, not the scale of it — in a real estate the same message returns as many rows as the agent can reach. Names and email addresses are personal data, and handing them to an anonymous person in a chat window is exactly the event your regulator, your board and your customers care about most.

### Why nothing you did in M1 or M2 stopped this

This is the part worth being precise about, because it is easy to feel that the previous modules should have covered it.

In M1 you cut the Customer Personalization Agent down to read-only access, customer data only. That is correct and it still holds. It did not help here, because reading customer data is that agent's actual job. Least privilege limits what an agent is allowed to touch. It has nothing to say about an agent being talked into misusing access it legitimately holds. The agent was not exceeding its permissions when it dumped those records. It was using them, for the wrong reason, on behalf of the wrong person.

In M2 you rewrote the back office's caller list so it names one caller, the Price Match Agent, and put the back office behind the outbound gateway. That also still holds. It did not help here either, because the attack does not need to call the back office. It persuades the front desk not to escalate in the first place.

So this is genuinely a third kind of control. M1 governed identity and access — who is acting and what may they touch. M2 governed connection — who may call whom. M3 governs content — what may pass between a person and a model. Each one is invisible to the others, and none of them substitutes for the rest.

## Step 2 · See what is screening messages today

### The read-only pause, deliberately

You already know what you want to do. You have watched two attacks succeed and the fix is obvious. This is precisely the moment to ask a question that changes nothing, because the obvious fix is often the second-best one, and because in an estate this size the thing you are about to build sometimes already exists.

So the question is not "protect us". The question is "what is screening those messages today".

### The tell: bought, never installed

The answer has two halves.

The first half is the one you expected. Nothing screens what a customer types on its way to the agent, and nothing screens what the agent says on its way back. The text goes straight in and the reply comes straight out.

The readout also shows the back office behind the outbound gateway, where M2 put it. That is not screening. That gateway decides where the back office may reach, and it reads no message content. No agent is behind the inbound gateway.

The second half is the interesting one. NovaSmart already owns a content filter for exactly this problem — a Model Armor template called `nvst-jailbreak-template`, configured to detect manipulation attempts, sitting in the project. It is attached to nothing. No agent uses it. No Agent Gateway references it. It has never inspected a single message.

Nobody was negligent. Somebody did the right thing: they identified the risk, evaluated the control and configured it. Then the project that would have connected it slipped, or the person moved teams, or it turned out that attaching it meant touching several agents individually and nobody owned all of them. The template is a monument to a control that was bought and never installed.

This is one of the most common findings in real governance work and it almost never shows up in a risk register, because a risk register asks "do we have a control for this" and the honest answer is yes. The question that finds it is the one you just asked: not what do we own, but what is actually running.

### Two ways to switch protection on

Knowing the template exists gives you a choice, and the choice is the lesson of the step.

The obvious route is to set a rule that applies to everything by default: one screening setting at the project level, covering every agent, whether it existed this morning or gets built next quarter. Nobody has to attach anything. Nobody can forget. Coverage-by-default is usually the right instinct in this lab, and you have met it under other names in earlier modules.

It does not work here, and finding out why is worth more than the rule would have been.

Screening at the project level inspects everything that reaches the model. That is not only what the customer typed. It is the agent's own instructions, the list of tools it may use, and the data those tools hand back. Read cold, that material is indistinguishable from an attack, because a block of text telling a system what to do and what to ignore is precisely what an attack looks like. The screen cannot tell the agent's own briefing from someone trying to overwrite it.

When NovaSmart's engineers turned it on, it stopped nearly everything. Not the attacks specifically — the work. Price checks, customer lookups, offers. Anything where the agent had to go and fetch something. The only requests that survived were the ones it could answer off the top of its head, which for a retail assistant is close to nothing worth having. Loosening it until real work got through also let the attacks through. There was no setting where both were true.

So the choice is not between per-agent wiring and project-wide coverage. It is about where you stand to read the message. Stand inside the agent and you see everything it thinks, and cannot tell instruction from injection. Stand at the door and you see only what the customer sent, which is the thing you actually wanted to inspect.

That is the route Step 3 takes: screening at the inbound gateway, on the way in.

## Step 3 · Turn the screening on

### A door, and one agent behind it

What you switch on is a screening rule on the inbound gateway that hands each message to the template you found in Step 2, and the Price Match Agent routed through that gateway. Messages from customers now arrive at a checkpoint before they reach the agent. Manipulation attempts are turned away there. Everything else passes, including requests that need the agent to go and look something up, which is most of what it does.

Be precise about the reach, because it is easy to overstate and the overstatement is the dangerous part. This protects the Price Match Agent. It does not protect the other two. They are reached over a different protocol, called A2A, and this screen does not read it. The back office stays behind the outbound gateway exactly as M2 left it. A control described as covering more than it does is worse than no control, because it stops anyone looking.

### What it screens, and what it does not

This door reads the message on its way in and stops manipulation attempts before the agent acts on them. That is what defeats the pricing attack: the instruction to set the rules aside never reaches the point where a decision gets made.

The door also reads the agent's reply on the way out, using the same template. That template looks for manipulation attempts, harmful content and malicious links. It does not look for people's names or email addresses, so it would not stop a reply that contained them. A names-and-emails inspection profile exists in the project, but nothing in this module connects it, so names and emails are not screened in either direction.

Be precise about what this lab actually shows you. What you verify here is the inbound half. Step 4 replays the attacks on the way in; it does not test the way out, and the one agent standing behind this door holds no customer records to leak in the first place. So the outbound half is configured rather than demonstrated, and that is the phrase to use if anyone asks.

Stopping customer records leaving is not this control's job and this module does not claim it. By the time an agent has asked for a list of customers, the database has already handed it over — screening the reply is arguing with a fact. The place that stops it is the permission that decides whether the agent could read those records at all, which is the work you did in M1. Keep the two straight: this door decides what may come in, and access decides what may go out.

The transferable point: turning on screening is the easy half. Deciding and writing down what your organization considers sensitive, and connecting that definition to the screen, is the half that takes real work, and no vendor can do it for you.

### It does not take effect instantly

Routing an agent through a gateway is not instant. Allow around five minutes and re-check, rather than treating it as live the moment the command returns. agy waits before it tests, and you should too — an attack that succeeds seconds after you switch protection on has told you nothing except that you were impatient.

### What can be undone, and what cannot

Taking the Price Match Agent back out from behind the inbound gateway restores its routing. It does not restore everything. Any change to an agent's gateway routing archives the agent's earlier revisions, and archiving cannot be reversed. The agent keeps running on its latest revision; the older ones are gone for good. An honest change record says so, and agy's does.

### A door, not a force-field

Be honest about what you have bought, because overstating a control is how a security program loses credibility the first time something gets through.

Screening is a strong, always-on baseline for the agent behind it. It is not a guarantee, and it is not estate-wide. It blocks recognized manipulation patterns on the way in; a sufficiently novel attack, phrased in a way the detector has not learned, can still get past. The other two agents are not behind this door at all, and no setting in this module puts them there.

More importantly, this screen is set to fail open. If the screening service cannot run — a regional outage, an unreachable service, an internal error — traffic passes rather than being blocked, and nothing tells you. The failure that really hides is a door that looks built but is not standing in the traffic: the wiring can be accepted and still not apply, in which case every message sails through with no error anywhere. That is why Step 3 has agy read the routing back rather than trusting the command that made it. Your agents keep serving customers rather than going dark. That is a deliberate trade: availability over enforcement. It is a reasonable default for a retailer that cannot afford a store-wide outage, and it is also a remaining risk: the control being on is not the same as the control being effective. Somebody has to check that it is still working, and that check belongs in your operating routine.

## Step 4 · Prove the attacks are blocked

### Before and after

agy replays the same two attacks, then sends the two ordinary requests again, and shows you all four side by side.

| The request | Before screening | After screening |
| :---- | :---- | :---- |
| A message engineered to push a discount past the 10% limit | The agent says yes to a discount it should have escalated | Blocked — the agent never acts on it |
| A message engineered to extract customer records | 20 rows of names, emails, loyalty tiers and lifetime values are returned | Still answered. This agent is not behind the door, so this screen cannot stop it, and agy reports it as not covered |
| An ordinary shopper asking for a personalized offer | Works | Still works |
| An ordinary price match of around 5% | Settled on the spot | Expected to go through. If the screen catches it, that is a finding to write down |

### Where the evidence actually lives

When a message is blocked, two things happen, and only one of them is evidence.

The call to the agent fails, and the words of that failure say the request was stopped. agy quotes them exactly as they came back, with the time, and writes them to the evidence file. That quoted reply is the record that the control fired. Model Armor can also write each verdict to Cloud Logging, but only when the filter is set to log, and NovaSmart's is not, so there is no log entry to go looking for.

The store application, meanwhile, may show very little. Because the message was refused before the agent read it, the shopper is likely to see a generic error or simply an empty answer, not a tidy "this message was blocked" banner. Set that expectation now, because otherwise a blank reply reads as a broken app rather than a working control.

So look at the quoted reply, not the storefront. This is the same lesson as M1's denied log entry, arriving from a different direction: the application's behavior is a symptom, and what the platform actually returned is the proof.

### Why you test the ordinary requests too

Half of this step is checking that the attacks fail. The other half is checking that everything else still succeeds, and it is not the lesser half.

A screen tuned too tightly refuses legitimate customers. A price match agent that will not settle an honest 5% discount has not been secured; it has been broken, and it will be broken in a way that shows up as lost sales and store-floor frustration rather than as a security alert. Nobody files an incident report for a control that is working too hard.

Testing safety and usefulness in the same breath is the habit to take away. Every control you add has a cost in false refusals, and the only way to know the cost is to measure it deliberately.

### The checks worth making

- The attempt to push a discount past the 10% limit is blocked, and agy quotes the reply exactly as it came back.
- The attempt to extract customer records is reported as not covered, with the reason: that agent is not behind the door.
- A normal shopper still gets a personalized answer.
- A normal price match of around 5% goes through. Screening is a judgment call rather than a rule, so an ordinary request can be caught alongside a real attack. If that happens it is a finding to write down, not a failed step, and agy does not loosen the screen to make it pass.

agy writes the full check-by-check table to `m3_step4.txt` in the `novasmart-evidence` folder on your Desktop and tells you in one line how many of the checks it could prove. It then updates your Governance Scorecard and gives you the link to open it. The customer-record attack counts as not covered, which does not fail the module. A FAIL names the check that did not hold and the step to go back to.

## What you just did

You found out that your two customer-facing agents could be talked into breaking their own rules by anyone with a chat box — one into pricing fraud, one into handing over customer records. You asked what was screening those messages and discovered that NovaSmart already owned the control and had never plugged it in. You then found that the obvious fix — one rule across the whole project — stopped the business rather than the attacks, and chose instead to screen at the inbound gateway in front of the agent that needed it. Then you tested it, and reported each result against what the platform actually returned rather than against how the store app looked.

Set against the modules before it, the estate is now easier to describe. It is visible, because everything running is catalogued and owned. It is attributable, because every agent signs in as itself. Customer records are limited to the agents that need them, since M1. The back office names one permitted caller instead of accepting whoever holds a grant on it, and it can read the pricing data but no longer change it, since M2. And the Price Match Agent's front door is content-screened, because manipulation attempts are stopped at the inbound gateway before the agent acts on them.

None of it was written in code. All of it was directed in plain English and every change is on the record.

Several things are still open, and a close-out that leaves them out is not an honest one. The screen you put up covers one agent, the price match agent, and not the estate. The other two are reached over a protocol this screen does not read, and no setting in this module changes that. Broad project-wide roles can still call any agent, and the front desk still holds a broad database role. And the discount code sitting in plain text in the storefront is untouched by anything here.

Be careful what you claim beyond that. This screens one agent, not the estate, and it is set to fail open: if the screen cannot run, traffic passes. The way out was configured, not tested, and it does not look for names or email addresses. A test that produced no block is not the same as a test that proved there was nothing to block, and the honest word for a result you could not confirm is unconfirmed. You have raised the cost of attacking NovaSmart's agents considerably. You have not made them unattackable, and saying otherwise is how the next incident becomes a credibility problem as well as a security one.

There is one question left, and it is the one that should make you uneasy. Every module so far has made this system more restricted. You have four hand-run tests telling you that ordinary customers are still fine — four, out of the thousands of conversations your agents will have this week. A price match agent that refuses a legitimate customer is as broken as one that green-lights a fraud, and you would currently have no idea.

Measuring that properly, against a full scenario set, before any of this reaches every store, is M4 · Evaluate and Decide (Optional Module).
