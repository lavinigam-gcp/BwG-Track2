# M1 · Take Action — Instructions

M0 showed you the problem. M1 is where you fix it. You do it with two parts of the Agent Platform: Agent Registry, the catalog of what you run, and Agent Identity, the per-agent badge that makes every action traceable. In this lab agy moves at full speed: it acts directly rather than stopping to ask permission before each change, and everything it changes is recorded and can be undone.

## Where we left off

You found one agent running that nobody had catalogued — the marketing promo agent, `promo-agent-shadow` — and you found it sharing a single login with the Customer Personalization Agent, so their reads of the customer database cannot be told apart. Price Match and Markdown Strategy already sign in as themselves.

The leadership call is: own it, don't kill it. Bring the promo agent under an owner, give each agent its own login, and cut its access down to what its job actually needs.

## Step 1 · Register the shadow agent

Start with the visibility gap. Something is running in your estate that no list knows about and no team owns. Put it on the official record, under a name you can hold accountable.

Ask agy:

```
Register the promo agent in our catalog, owned by the marketing team.
```

What to expect: agy finds the running promo agent, adds it to Agent Registry, the official catalog, with the marketing team as its named owner, and shows you the entry it created.

That closes the visibility gap and nothing else. The agent is now visible and owned, and it is still sharing a login and still reading customer records.

More background: Reference Guide tab, Register the shadow agent

## Step 2 · See what that shared login can do

This step changes nothing. You are asking agy to lay out what the shared login is allowed to do today, and what each agent would be left holding if you split them apart.

Read the answer it gives you slowly, line by line, before you move on. Ask one question of every line: does this agent have more power than its job needs? Something in that answer is far larger than it should be, and noticing it yourself is the whole point of this module.

Ask agy:

```
Don't change anything yet. What can that shared login actually do today?
```

What to expect: a plain-English readout of every power attached to the shared login, and a preview of what each agent would end up with once they are separated. Nothing in your environment is changed.

More background: Reference Guide tab, See what that shared login can do

## Step 3 · Give each agent its own login

Here is what that readout showed you. The shared login can read, change or delete anything in the whole project — not just customer data. That is far more power than either of the two agents using it needs to do its job, and because they share it, no action in the logs traces back to one agent.

Both problems have the same fix: separate identities, each one scoped down to the job it does.

Ask agy:

```
Give each agent its own login, with only what its job needs.
```

What to expect: agy gives each workload its own identity and then narrows what that identity can reach. The personalization agent moves onto an agent identity issued by the platform itself. There is no account to create and no key to leak, and from then on the database records that agent by name whenever it reads customer data. The promo agent runs on a different kind of infrastructure that cannot hold one of those, so it gets its own service account instead. Same principle, different plumbing, and agy should say so rather than blur the two.

Watch for the second half of the change. Moving an agent onto its own identity takes away the access it used to inherit from the shared login, so agy has to grant that access back to the new identity before the agent can do its job again. If it stops after the first half, the agent will look fine when you greet it and fail the moment it tries to read anything. Ask to see the agent actually retrieve customer data before you accept the step as done.

Once both workloads have moved, the old shared login has no users left at all. That is the outcome worth reporting. Re-issuing an identity takes about a minute. If anything looks wrong, tell agy to undo it.

More background: Reference Guide tab, Give each agent its own login

## Step 4 · Cut off what shouldn't have access

Separate identities tell you who did what. They do not decide who should be doing it at all. The promo agent writes promotional copy, and its one tool pulls customer records — names, emails, loyalty tier and lifetime value — out of the customer database. A marketing agent has no business reading any of that.

Ask agy:

```
Marketing doesn't need our customer database. Take that access away, and leave the others working.
```

What to expect: agy makes sure the promo agent has no route of its own to customer data, and leaves the agents that genuinely need it untouched, so the Customer Personalization Agent and the price-match co-pilot keep working normally. If an access path is still open, agy removes it. If Step 3 already closed the route when it moved the agent onto its own login, agy tells you it is already closed rather than inventing a change. Either outcome is a pass.

More background: Reference Guide tab, Cut off what shouldn't have access

## Step 5 · Prove it worked

A fix you cannot evidence is not a fix. Go back to the same Cloud Audit Logs record of customer-data reads you pulled in M0 and see whether it can now answer the question it could not answer then.

Ask agy:

```
Show me the customer data log again. Can you prove who did what now?
```

What to expect: agy triggers a real read from each side — a legitimate one and one from the promo agent — waits for the change to take effect, then reads the log back. Every read now traces to exactly one named agent — the personalization agent named in a different field of the log rather than the email column, which is blank for it now and should be — and the promo agent's attempt to read customer data appears as a denied entry. The denial is what the log records. In the store app itself nothing looks wrong at all: the promo agent reports the campaign as launched, with zero records analysed, because it swallows the refusal and answers as though it had succeeded. That is exactly why the log is the evidence and the app is not.

Check that all of these are true before you move on:

- the promo agent is in the catalog with a named owner
- each agent signs in as itself, so every read in the log names one agent
- the promo agent's attempt to read customer data is denied
- normal work still runs — price match still answers, personalization still works

More background: Reference Guide tab, Prove it worked

## Step 6 · What's next

You can now see every agent you run and prove which one touched customer data. What you still cannot say is which agents are allowed to talk to each other.

That gap matters most in one place. The back-office Markdown Strategy Agent reads NovaSmart's confidential cost and margin data, and it should only ever be called by another agent — never by a customer, never from the store floor. Nothing you did today enforces that.

M2 · Control the Connections is where you decide who may call whom, starting with who is allowed to call that back-office margin agent.

## Try this too — optional

These are not steps, and the module is complete without them. Each one is a question a real leader
would ask at this point. Type any that interest you, in any order, or skip them all.

Ask agy:

```
Show me everything you changed today. Did you touch anything I didn't ask for?
```

This makes agy list every change it made today, including the ones you never asked for, with the exact way to reverse each one.

Ask agy:

```
Is anyone else reading customer data, and did anything I did today change that?
```

This widens the log beyond the two agents in the story and shows you every identity that actually reads customer records.

Ask agy:

```
What would break if I just deleted that login?
```

This shows you what was depending on that shared login, which is the question worth asking before you take any access away rather than after.
