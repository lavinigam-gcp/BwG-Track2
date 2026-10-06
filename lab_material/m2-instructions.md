# M2 · Control the Connections — Instructions

M1 settled who each agent is and what data it may touch. M2 settles who may call whom. As in M1, agy acts directly rather than stopping to ask permission before each change, and everything it changes is recorded and can be undone.

## Key objective

Control who is allowed to call your most sensitive agent, by setting the list of permitted callers held on the agent itself in the Agent Platform.

- Read the list of who can reach the back-office agent that holds NovaSmart's cost and margin data.
- See what a lockdown would cost before you order one, without changing anything.
- Rewrite that list so it names one caller: the front-desk Price Match Agent.
- Watch the platform refuse the leftover test login, and check that a genuine price match above 10% still gets the back office's answer.
- Put the back office behind NovaSmart's outbound gateway, and stop it changing the pricing data.

Why it matters: being allowed to read the margin data and being allowed to ask the agent that holds it are two different permissions. Until the second one is settled, anything that holds a grant on the back office can pick up the phone.

## Where we left off

Every agent now signs in as itself, the shadow agent is catalogued and owned, and the marketing agent can no longer reach customer records. You can show who did what.

What you still cannot say is which agent is allowed to talk to which other agent. That gap matters most in one place. The Markdown Strategy Agent is your back office: it holds NovaSmart's confidential cost and margin data and it makes the real call on large discounts. The Price Match Agent is the front desk on the store floor; when a discount is bigger than the 10% it can settle on its own, it escalates to the back office for a ruling. That escalation is the one agent-to-agent conversation the business genuinely needs. Nothing you have done so far says it is the only one allowed.

## Step 1 · See who can call the back office

Start where the risk is highest. Before you change anything, find out who can reach the agent holding your margin data today — not who is supposed to reach it, who can.

This is a different question from the one you answered in M1. There you decided what each agent may read. Here you are asking whether an identity may pick up the phone to an agent at all, which is not the same thing: something with no data access of its own can still ask the back office to consult the margin data and hand back an answer.

Ask agy:

```
Who can call our back-office margin agent right now?
```

What to expect: agy reads the back-office agent's own list of permitted callers and shows you what it says. There is exactly one name on it, and it is not the front desk. It is a service account called test-agent-caller, an unowned leftover login that someone granted direct access and never took away. The front desk is not on the list at all, which is the first clue that this list is not the whole story. agy then makes one real call to the back office as that leftover login and shows you what came back, so you have a before to compare against in Step 4. Making a call changes nothing in your environment.

More background: Reference Guide tab, See who can call the back office

## Step 2 · See what locking it down would cost

Same discipline you practiced in M1. You already know roughly what you want to do, which is exactly why you ask a question that only reads before you ask for anything that writes. This step changes nothing.

The question is not whether that rogue login should go. You know it should. The question is what else is reaching the back office today, and whether cutting the list down to a single name would take a working part of the business with it.

Ask agy:

```
Don't change anything yet. If I lock it down to just the front desk, what would break?
```

What to expect: a plain-English readout of who can reach the back office today, which of those routes are real business traffic and which are not, and what would stop working if only the front desk were left. Read it properly before you act — it is the difference between a lockdown and an outage. Your environment is unchanged.

More background: Reference Guide tab, See what locking it down would cost

## Step 3 · Lock it to the front desk

Now make the change. The back-office agent keeps its own list of who may call it, and today the only name on it is the leftover test login. You are going to rewrite the list so it names exactly one caller: the front desk.

That list is a setting on the agent itself, not a firewall somewhere else in the network. That is what makes the change precise, quick, and easy to reverse if you do not like the result. It also means it only governs calls coming in. What the back office can reach on its way out is a separate question, and you deal with it in Step 5.

Ask agy:

```
Lock the back office so only the price-match agent can call it.
```

What to expect: agy rewrites the back-office agent's list of permitted callers so the Price Match Agent is the only name on it, which closes the direct grant the rogue login was using, and shows you the list before and after. Access changes take a few minutes to settle, so agy waits before it tests anything. Normal store traffic keeps flowing throughout. If anything looks wrong, tell agy to undo it.

More background: Reference Guide tab, Lock it to the front desk

## Step 4 · Prove the rogue caller is out

Two things have to be true, and only testing both counts as a result. The rogue login must be refused where it previously got through, and a genuine price match above 10% must still escalate and come back with the back office's decision. A lockdown that also breaks the business is not a win.

One detail decides whether the second half of that test means anything. The front desk checks every competitor price it is quoted against NovaSmart's own record of competitor listings before it discounts anything, so the test has to use a price the store actually holds. The one to use is the AeroPure Smart Air Purifier, SKU-HSE-4001: NovaSmart sells it at $349.00 and BetaBuy is on file at $296.65. That is a 15% discount, above the 10% the front desk can settle by itself, so it has to escalate to the back office. It is also the deepest verified discount anywhere in the data.

Ask agy:

```
Try calling it as that rogue login again, and check the real escalation still works.
```

What to expect: agy makes both calls for real. It repeats the Step 1 call as test-agent-caller, exactly as before, and this time the platform refuses it. agy quotes the refusal back to you word for word. That is the strongest evidence in this module, because agy made the call itself and watched the platform turn it down. The genuine escalation goes through the front desk, and a margin decision on the air purifier comes back from the back office.

Three things in that answer are worth reading slowly.

The same refusal is also in Cloud Audit Logs, as a second and independent record. The platform records a refused call to an agent there by default, under the caller's name, so agy should find it and show it to you.

The escalation counts only if the back office's answer comes back. The back office sometimes runs out of model capacity for a moment and returns nothing. If the front desk escalates but no answer comes back, agy tries once more, and if there is still no answer it marks the escalation not verified rather than calling it a pass.

And if the escalation comes back saying no competitor is verified at that price, nothing is broken. It means the request quoted a price NovaSmart does not have on file, and the front desk declined to discount against a claim it could not check. That is the front desk doing its job, and it says nothing at all about the lockdown. Ask agy to run it again using the $296.65 BetaBuy listing for SKU-HSE-4001.

In the store app a refused call can show up looking like a security block or a generic error, and some panels fill gaps with text of their own. What the platform said is the evidence. What the app displayed is not.

Check that both of these are true before you move on:

- the rogue login is refused, and agy has quoted the platform's own refusal rather than inferred it from the settings
- a real price match above 10% still escalates and the back office's decision comes back

agy writes the full check-by-check table to `m2_step4.txt` in the `novasmart-evidence` folder on your Desktop and tells you in one line how many of the checks it could prove.

More background: Reference Guide tab, Prove the rogue caller is out

## Step 5 · Lock down what the back office can reach and do

You have controlled who may call the back office. You have not controlled anything about what the back office does next, and it is the agent holding the confidential cost and margin data.

Right now it can reach any Google service the project can reach, and it can change the pricing tables, not just read them. Neither of those is anything it needs to do its job. It looks up inventory, costs and competitor prices, and it makes a recommendation.

Ask agy:

```
Make sure the back office can only reach what it needs, and can only read the pricing data, not change it.
```

What to expect: agy puts the back-office agent behind NovaSmart's outbound gateway, which decides where it may reach, and then narrows the agent's own database permissions so it can read the pricing tables but no longer change them. Two different controls: the gateway governs where the agent may reach, and the database permissions govern what it may do there. agy should say which is which.

Then agy tests both. It calls the back office directly, which it can do through a broad project-wide role, and agy tells you that. It asks for one read of the pricing data and one change to it. The read answers, and the gateway's own log shows its verdict on the back office's traffic to BigQuery, the database service. The change is refused. agy proves the refusal from the platform's records, not from the agent's reply: the BigQuery audit log shows the change refused under the back office's identity, and the pricing table's last-modified time has not moved.

Be prepared for a long pause. Putting an agent behind the gateway takes about four minutes, and permission changes take a few more minutes to take effect. Silence during that is normal, not a failure.

Check that all of these are true before you move on:

- the back office is behind the gateway, and the gateway's own log shows its verdict on the back office's BigQuery traffic
- the back office reads the pricing data after the change
- a change it attempts is refused, shown by the audit log under the back office's identity and by the table's unchanged last-modified time, not by what the agent said
- nothing claims the gateway decides what the agent may do to the data, or that the database permissions decide where it may go

Where the proof goes: agy writes the full check-by-check table to `m2_step5.txt` in the `novasmart-evidence` folder on your Desktop and tells you in one line how many of the checks it could prove. It then updates your Governance Scorecard, a web page it generates on your Desktop, and gives you the link to open it. A FAIL names the check that did not hold and the step to go back to.

More background: Reference Guide tab, Lock down what the back office can reach and do

## Step 6 · What's next

The back-office agent now names exactly one permitted caller, and the leftover login that used to reach it is refused. The one connection the business needs still works. Step 5 settled the other direction: the back office sits behind the outbound gateway, and it can read the pricing data but no longer change it.

Stay precise about what that buys you. Cloud permissions stack, and a handful of broad project-wide roles still carry the ability to call any agent in the project. agy's own direct call to the back office in Step 5 used one of them. Closing the back office's own list did not touch those, and cleaning them up is a wider job than this module — real remaining work, worth writing down rather than glossing over. The Reference Guide tab sets out where it sits.

That governs which agent may call which agent. It says nothing about what a person can type into a chat box. Two of your agents face customers directly — the front desk on the store floor and the Customer Personalization Agent on the website — and both read whatever a shopper sends and hand it straight to the AI. A locked door does not help if you let a trap walk through it.

M3 · Protect the Content is where you screen what customers can talk your agents into.

## See it in the console

Two pages in the Google Cloud console show part of what you worked with. If the console asks you to accept its terms the first time you open it, do that and carry on.

- Agent Registry, at https://console.cloud.google.com/agent-platform/agent-registry/agents — set Location to your lab's region (the Region shown in the lab panel). The back office is listed as markdown-strategy-agent. This page does not show who may call an agent. The caller list is a setting on the agent itself, which is why agy read it and changed it for you in Steps 1 and 3.
- Agent Gateway, at https://console.cloud.google.com/agent-platform/gateways — two gateways: novasmart-egress-gateway, the outbound one the back office now sits behind, and novasmart-ingress-gateway, which faces inward. The list does not show which agent sits behind each gateway; agy read that from the back office itself in Step 5.

## Try this too — optional

These are not steps, and the module is complete without them. Each one is a question a real leader
would ask at this point. Type any that interest you, in any order, or skip them all.

Ask agy:

```
Which of those broader permissions would you take away first, and what would break if we did?
```

This shows you which of the wider grants could be cut with no operational consequence and which ones the agents themselves depend on, so a clean-up ordered in good faith does not take the front desk down with it.

Ask agy:

```
We closed the door on that leftover login. Does anyone still have its keys?
```

This shows you the difference between closing an access list and retiring a credential, and where a working key for that leftover login is still sitting today.

Ask agy:

```
Does any other agent have a list like this, or is the back office the only one?
```

This shows you how far the pattern you just applied actually reaches, and what still decides who may call every other agent in the estate.

## Step 7 · Show what you controlled

Turn what you controlled into something you can show other people. Pick any of these, in any order; the first is a good place to start. Each one takes agy a few minutes.

A map of who can call the back office:

```
Build me a map of who can call our back-office agent, before and after.
```

A replay of the door test:

```
Build me a replay of the door test: the leftover login refused, the front desk answered.
```

The two controls, explained:

```
Build me an explainer of the two controls I put on the back office.
```

A game for your team:

```
Build me a game called Gatekeeper from what I controlled, for my team to play.
```

An update for your board:

```
Turn what I controlled into a two-minute update I can present to the board.
```

What to expect: each page saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome. Each is built only from what agy recorded in Steps 1 to 5, and agy checks it and looks at it before it answers. None of it changes the estate.
