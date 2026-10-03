# M0 · See Everything — Reference Guide

The sections below match the steps on the Instructions tab. Read *What you're walking into* first, then dip into a Step section whenever the Instructions tab points you here.

## What you're walking into

### The company: NovaSmart

NovaSmart is a large consumer-electronics retailer — physical stores plus a website, selling espresso machines, laptops, phones, headphones and wearables.

Last year NovaSmart went "AI-first": leadership told every team to adopt AI everywhere, fast. Teams were asked to build AI *agents* — AI workers that take actions, not just chat — and ship them to production quickly.

It worked. And then it sprawled. Nobody has a clear picture of what is actually running.

<!-- FIGURE:F01 BEGIN -->

![NovaSmart transitioned to an AI-first model by deploying agents across Store Systems, Pricing and Finance, Customer Experience, and Marketing. However, rapid adoption led to agent sprawl, leaving no clear picture of what is actually running today.](images/F01_novasmart_sprawl.jpg)

<!-- FIGURE:F01 END -->

### The app everyone actually uses: the price-match co-pilot

NovaSmart's flagship AI app helps a store associate answer one question on the spot: *a customer says "Store X sells this cheaper — will you match it?" — do we say yes?*

Before AI, the associate had to guess, say no and lose the sale, or phone a manager and make the customer wait. The co-pilot gives an instant, policy-backed answer. The rule it enforces is simple:

- Up to 10% off, the associate can approve on the spot.
- Anything larger than 10% goes to the back office, which checks NovaSmart's confidential cost and margin data before answering.


<!-- FIGURE:F02 BEGIN -->

![The price-match workflow routes customer requests to the Price Match Agent. Discounts up to 10% are approved immediately, while larger discounts pass to the Markdown Strategy Agent, which uses confidential back-office data to issue a final approval or denial.](images/F02_ten_percent_rule.jpg)

<!-- FIGURE:F02 END -->
So in practice:

- A customer wants a $450 espresso machine matched to a competitor's $427 — about 5% off. The co-pilot checks and says approved. Around ten seconds, no manager.
- Same machine, but the competitor is at $382 — about 15% off, past the 10% line. The co-pilot escalates. The back office weighs the real margin and returns an approve or deny with a reason, without ever exposing those confidential numbers to the store floor.
- If the competitor is out of stock, or matching would cut too deep into margin, the answer is no, with a reason. No guesswork, no arguing with a manager.

<!-- FIGURE:F03 BEGIN -->

![Price match requests under the 10% line are set to APPROVE automatically. Discounts past the 10% line ESCALATE to the back office to review margins, while requests are set to DENY if competitors are out of stock or margins cut too deep.](images/F03_worked_examples.jpg)

<!-- FIGURE:F03 END -->

### The cast: the agents, and why each exists

Four AI workloads run at NovaSmart. Two power the price-match co-pilot, one personalizes shopper offers, and the fourth is the troublemaker.

| Agent | Who built it and why | What it does | Tools it uses | The problem | Where it runs |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Price Match Agent (the front desk) | Store Systems, to answer associates instantly | Weighs the competitor's price and stock, our own stock and margin; approves matches up to 10% on the spot, denies when the competitor is out of stock or the margin is too thin, and escalates bigger discounts to the back office | Competitor price and stock, our inventory | None. It works well and already has its own identity | Agent Runtime |
| Markdown Strategy Agent (the back office) | Pricing and Finance, to protect margin | Only consulted for discounts above 10%. Reads the confidential cost and margin data and makes the real call | Confidential cost and margin data | Only other agents should be able to call it, never customers or associates. It already has its own identity | Agent Runtime |
| Customer Personalization Agent (shopper-facing) | Customer Experience, to tailor offers and rewards to each shopper | Personalizes promotions and VIP rewards using customer records | Customer records, through the MCP doorway | Shares one login with the marketing promo agent, so their reads of customer data cannot be told apart | Agent Runtime |
| Demand and Promotion Agent, running as `promo-agent-shadow` (marketing) | Marketing, to auto-generate local promos | Writes promotional campaign copy and flash-sale bundles | One tool, and it extracts customer records: names, emails, loyalty tier and lifetime value, read straight from the customer database | The shadow. It is not in the official catalog, it shares that same login, and a marketing agent has no business reading customer records at all | Cloud Run |

Two supporting pieces sit behind all of this: the customer database, and a controlled doorway the agents use to reach it. You will hear that doorway called an MCP.

The customer database is small and very sensitive. It holds 20 customer records, each with a name, an email address, a loyalty tier, a lifetime value and similar details. Twenty records is exactly the point: this is the shape of the problem, not the scale of it. In your real estate it would be millions.

Plain-English translations: *Agent Runtime* and *Cloud Run* are two different places Google Cloud runs software. Think of Agent Runtime as the official managed home for agents, and Cloud Run as a box someone can spin up on the side. An *MCP* is a controlled doorway an agent uses to reach data. You do not need the internals — agy handles those.

<!-- FIGURE:F04 BEGIN -->

![Two of four workloads share the login novasmart-customer-sa: Customer Personalization Agent, which reaches the customer database through an MCP doorway, and Cloud Run shadow agent promo-agent-shadow, which reaches it directly. Price Match and Markdown Strategy Agents hold their own identity.](images/F04_estate_map.jpg)

<!-- FIGURE:F04 END -->

### Why this sprawl is dangerous

The marketing agent was stood up off to the side. That is classic shadow IT: technology running without sign-off. Because nobody catalogued it, it has been quietly running up cloud costs and reaching into customer data with no owner and no oversight.

Worse, that promo agent and a completely legitimate agent, Customer Personalization, were set up sharing one login — a service account named `novasmart-customer-sa`. Their reads of customer data are therefore impossible to tell apart. When something goes wrong, nobody can say which one did it.

Nobody here was malicious. Marketing just needed to ship a promo fast, so they stood up a service on the side, which made it a shadow. They reused an existing shared login to save time, which removed accountability. That login already had broad power over the database, which made it over-privileged. Every one of those is a normal speed-versus-governance shortcut, and every one of them is why you now have a problem.

This is not only a retail story. Swap "customer database" for your own world: patient records in healthcare, citizen data in the public sector, wholesale margins in finance. The pattern is identical everywhere. Shadow IT plus a shared login means nobody can see or prove who touched sensitive data. That is a reportable incident waiting to happen.

<!-- FIGURE:F05 BEGIN -->

![Three common speed shortcuts create governance failures: deploying on Cloud Run without onboarding leads to Shadow IT, reusing shared logins causes No Accountability, and leaving broad access results in Over-Privilege.](images/F05_sprawl_anatomy.jpg)

<!-- FIGURE:F05 END -->

### Your role

You are the new Head of AI Platform and Security. You did not build any of this — it was already running when you walked in. Your job is to make the estate, meaning every AI agent and tool you run, safe, governed and accountable.

You do that through Antigravity, an AI assistant wired into NovaSmart's cloud, which you will call agy. You state your intent in plain English and it does the hands-on work.

The skill this lab builds is judgment: knowing what to ask, reading the evidence that comes back, and catching a risky change before it ships.

## Working with agy

You lead in plain English. agy does the hands-on work and reports back.

- You ask a question the way you would ask a competent colleague. No commands, no syntax, no cloud jargon required.
- agy goes and does the work directly. In this lab it moves at full speed and does not stop to ask permission before each action, so expect answers rather than approval prompts.
- Every answer comes with the real evidence behind it: the actual catalog entry, the actual audit log line, the actual configuration. Not an opinion, and not a summary you have to take on trust.
- Everything it does is recorded, and anything it changes can be undone.
- Long jobs run in the background and it keeps you posted.

You can always follow up with "explain that", "show me the evidence" or "undo that".

One thing to know about this module: M0 only looks. Every step here reads, lists, compares and reports. Nothing in your environment is changed. The fixing happens in M1, once you have decided what should be fixed.

<!-- FIGURE:F06 BEGIN -->

![In read-only M0, you ask questions in plain English, agy executes hands-on tasks and returns evidence, and you decide what it means before any fixing occurs in M1.](images/F06_working_with_agy.jpg)

<!-- FIGURE:F06 END -->

## Words you'll hear today

- Agent Registry — the official catalog of the agents you run. It answers "what do we have?" Note that it is a record of what got registered, not a live scan of what is running.
- Agent Identity — a unique, tamper-proof ID badge for a single agent, so every action can be traced to exactly one of them. It answers "who did it?"
- Service account — a login used by software rather than a person. When several agents share one, every action they take looks identical in the logs.
- MCP — the controlled doorway an agent uses to reach data, instead of reaching into the database directly.

In one line, the fix you are heading towards: replace one shared service account with a per-agent Agent Identity, so every action ties to exactly one agent and each agent gets only the access its job needs. But first you have to see the problem clearly, which is what M0 is for.

<!-- FIGURE:F07 BEGIN -->

![Four enterprise agent concepts are defined: Agent Registry catalogs registered agents, Agent Identity uniquely identifies an agent to trace actions, Service account provides software logins, and MCP serves as a controlled doorway to reach data.](images/F07_glossary.jpg)

<!-- FIGURE:F07 END -->

## Step 2 · Meet your estate

The natural first move is to ask the platform what you own. The official catalog answers, and it comes back with six entries.

That number looks reassuring. It is not.

| What the catalog lists | What it actually is |
| :---- | :---- |
| Price Match Agent | Yours. The front desk of the price-match co-pilot |
| `markdown-strategy-agent` | Yours. The back office that handles discounts above 10% |
| `customer-personalization-agent` | Yours. Shopper offers and VIP rewards |
| Workspace Agent | Not yours. A platform built-in that ships with the environment. Nobody at NovaSmart deployed it |
| Gemini Enterprise Core Assistant | Not yours. Another platform built-in, listed only in the `global` location |
| Deep Research | Not yours. Another platform built-in, listed only in the `global` location |

Do not be thrown by the names you do not recognise. The platform contributes a few built-in entries of its own, and they sit in your catalog alongside the agents your teams actually deployed — nobody at NovaSmart deployed them, and nothing of yours is running them. Two of them, Gemini Enterprise Core Assistant and Deep Research, are only listed in the `global` location, so the count you get back depends on where you look. The regional listing returns four entries and the `global` one returns three, with Workspace Agent appearing in both — only putting the two together gives you the full six. The number is not the thing to hold on to. Which entries are yours is.

Notice that two of your own three are listed in lowercase with hyphens rather than as the readable names your teams use for them. That is not a mistake in the catalog. It is what whoever deployed them typed, and nothing has ever made it consistent. Small as it looks, it is the same problem as the rest of this module: the catalog reflects what was done, not what anyone intended, and you cannot match a list against your own understanding of the estate until you can see both.

Read that list against the cast above and the inversion jumps out. The catalog names things you never deployed, and it is missing something you did: the marketing promo agent, `promo-agent-shadow`, is nowhere in it.

This is the lesson of the step, and it is worth sitting with:

- A catalog is a record of what was registered. It is not a scan of what is running.
- So "six entries" does not mean "six of our agents", and it certainly does not mean "all of our agents".
- A clean-looking list is the most comfortable place for a blind spot to hide.

Cataloguing still matters enormously. The registry is your single list of every agent and tool, with an owner against each. It is the basis for visibility, governance, cost ownership and attribution. If something is not catalogued, nobody is accountable for what it costs or what it can reach. That is exactly why the gap you just found is a problem, and exactly why you cannot stop at the catalog.

<!-- FIGURE:F08 BEGIN -->

![Out of six catalog entries across regional and global listings, only Price Match Agent, Markdown Strategy Agent, and Customer Personalization Agent are yours. The remaining three entries are platform built-ins, including Workspace Agent, Gemini Enterprise Core Assistant, and Deep Research.](images/F08_catalog_breakdown.jpg)

<!-- FIGURE:F08 END -->

## Step 3 · Widen the net

The catalog only knows about things that registered themselves. To find everything else, you stop asking the catalog and start asking the cloud: list everything actually running, then compare the two lists.

That comparison is where the shadow surfaces.

| What's running | In the catalog? | What that means |
| :---- | :---- | :---- |
| Price Match Agent | Yes | Known, and it has its own identity |
| Markdown Strategy Agent | Yes | Known, and it has its own identity |
| Customer Personalization Agent | Yes | Known, but it shares a login, so its reads cannot be told apart |
| `promo-agent-shadow` (the Demand and Promotion Agent) | No | Uncatalogued. Running on Cloud Run, off the official platform, and sharing that same login |

The scan will also show ordinary plumbing alongside these: the store website and the data doorway the agents call. Those are supporting services, not agents, and they are expected. There is exactly one uncatalogued agent workload in your estate, and it is the promo agent.

Workspace Agent does not appear in this list at all, which is the other half of the same lesson. It sits in the catalog because the platform provides it, not because anything of yours is running it. The two lists were never going to line up on their own, and only comparing them tells you where they differ.

Why does a shadow agent happen at all? Build an agent the official way and the platform registers it in the catalog for you, automatically. This promo agent skipped that path — it was spun up as a plain web service off to the side, so nothing ever recorded it. It has been running unseen simply because no one knew to look.

Two separate problems are now on the table, and it matters that you keep them separate:

- Visibility. One workload is running that nobody catalogued and nobody owns.
- Accountability. A legitimate agent and that shadow agent share one identity, so their actions cannot be told apart.

Fixing the first does not fix the second. Registering the promo agent would make it visible and owned, and it would still be sharing a login and still be reading customer records.

<!-- FIGURE:F09 BEGIN -->

![Comparing a catalog record against a cloud scan reveals that Price Match Agent, Markdown Strategy Agent, and Customer Personalization Agent are both listed and running, Workspace Agent is listed but not running, and promo-agent-shadow is running unlisted on Cloud Run.](images/F09_catalog_vs_running.jpg)

<!-- FIGURE:F09 END -->

## Step 4 · Who's reading customer data

Security emails you: they are seeing heavy reads against customer records, and the reads they are worried about all sign in with the same generic account, so they cannot tell which agent actually did it.

You ask for the evidence. What comes back is Cloud Audit Logs, the platform's own record of data access — immutable and system-generated, not agy's opinion, and exportable for your compliance team.

Here is the shape of what that log gives you. Your timestamps will differ.

| Time | What happened | Login that did it |
| :---- | :---- | :---- |
| 09:12:04 | Read a customer profile, touching all seven fields, including last purchase date and preferred category | `novasmart-customer-sa` |
| 09:12:37 | Bulk read across the customer table for a promo campaign, touching five fields: customer id, name, email, loyalty tier and lifetime value | `novasmart-customer-sa` |
| 09:12:51 | Read a customer profile for the storefront | the project's default compute account |
| 09:13:15 | Checked a competitor price and our stock for a match request | Price Match Agent's own agent identity |
| 09:13:52 | Read confidential cost and margin data for an escalated discount | Markdown Strategy Agent's own agent identity |

The first three rows are reads of the customer database. The third is the one people miss: the store portal itself runs as the project's default compute account, which holds Owner-level rights over everything in the project, so a shopper browsing the site reads customer records under a login that could do anything at all. The last two rows are reads of pricing and competitor data, shown here so you can see the contrast. A question scoped to customer records returns the customer-data rows and leaves the pricing ones out.

One line in your own result will not match anything in that table: the lab's own setup account, which loaded these sample customer records into the database when your project was built. Its login is named after the project itself rather than after any workload. It is not one of the agents, it is not the shared login, and it is not what this step is asking about — it is housekeeping. Recognising a line like that and setting it aside is part of reading an audit trail.

Look carefully at what the log does and does not contain. Three things in it matter here: when it happened, what was accessed, and the login that did it. The raw record carries other technical detail as well. What it has nowhere is a field where an agent announces its own name, and there should not be one — a name a caller supplies about itself is not evidence.

So the only identifier you get is the login, and the bottom two rows show what a good one looks like. Price Match and Markdown Strategy each sign in as themselves, so each of those lines names exactly one agent. You could hand either row to an auditor as it stands.

The top two rows cannot do that. Two entirely different workloads — a legitimate personalization request and a marketing bulk extract of customer records — arrive wearing the same badge, thirty-three seconds apart in the sample above, and the platform genuinely cannot distinguish them. The identity in those rows is a shared service account, not an agent, and the real agent identity for those two was never in the record to begin with. That holds however many such lines your own log turns out to hold: one read under a shared login already tells you a read happened and refuses to tell you which agent made it.

Now look once more at those top two rows. What was accessed is recorded more finely than it first appears: the record also lists which fields of the customer table each read actually touched, and on that the two do not match. The personalization read took all seven fields, including last purchase date and preferred category. The promo campaign's bulk read took five, asking for neither of those two.

Be exact about how far that carries you, because this is the kind of inference it is easy to overstate. Two different field lists tell you there were two different questions asked of the table. They do not, on their own, tell you there were two different pieces of software asking: one workload can perfectly well ask two different questions. It is a lead worth pulling on, not a proof. It also names nobody. Nothing in the record ties the five-field read to marketing rather than to anything else you run, and whether you see the comparison at all depends on both reads having happened while you were looking.

What it does show you is the shape of the problem. Two different questions were put to your customer table, and the trail offers you one identity for both of them. Everything you would now want to know, starting with whether that was one workload or two, has to come from somewhere other than the audit trail.

Notice how you worked out which was which: not from the log, but from Step 3. You know `promo-agent-shadow` runs under that login because you inspected the running service. That is an inference you had to assemble by hand. It is not something the audit trail proves, and it is not something you could produce at speed, under pressure, for thousands of records.

Why this is bad, in the terms your board will use:

- You cannot stop the bad reads without also breaking the good agent, because you have no way to target one and not the other.
- You cannot answer the first question any auditor, regulator or breach report asks: who accessed this data? Right now the honest answer is "we don't know."
- Full access has been granted to a login rather than to an agent, so anything running under that login inherits everything it can do.

<!-- FIGURE:F10 BEGIN -->

![The Customer Personalization Agent and promo-agent-shadow both authenticate using the shared service account novasmart-customer-sa. The sample audit rows below them carry that one identity for two different workloads thirty-three seconds apart, so the platform cannot show which agent did it.](images/F10_shared_identity.jpg)

<!-- FIGURE:F10 END -->

## Step 5 · Decide

You have now seen it all: one uncatalogued agent, one shared login, and a customer database being read by something that has no business reading it. This step is the leadership part. You decide what should happen before anyone touches anything, and M1 is where the decision gets carried out.

Three ideas worth having straight in your head first.

### Own it or kill it

Shutting the promo agent down is fast and feels decisive, but it hides the problem rather than solving it, and it breaks a team that is genuinely relying on the thing. Bringing it under an owner, giving it its own identity and cutting its access down to what it actually needs fixes the same risk in the open, without breaking the business. Neither answer is free. Decide which one you would defend, and why, before you read on.

<!-- FIGURE:F11 BEGIN -->

![When discovering an unowned service like promo-agent-shadow reading customer records, leaving it unchanged is not an option. You must decide whether to Own it by formalizing ownership and access, or Kill it by shutting it down immediately.](images/F11_own_it_or_kill_it.jpg)

<!-- FIGURE:F11 END -->

### Least privilege

Least privilege means giving each agent only the access its job needs, and nothing more. Less access means less damage when something is tricked, buggy or breached.

Apply it to the case in front of you. A marketing agent writes promotional copy. Ask what it truly needs to do that job, and then ask why its one tool pulls names, emails, loyalty tiers and lifetime values out of the customer database. The gap between those two answers is the over-privilege.

### Blast radius

Blast radius is how much can go wrong if a single agent is later tricked, misconfigured or breached. Today, anything running under the shared login inherits that login's full power over the customer database, so the blast radius of any one of them is the whole table.

The tempting shortcut is to over-grant "just to be safe" so nothing breaks. That is precisely the shortcut marketing took, and it is how you end up back here. Be clear with yourself about what breaks if you take it now.

<!-- FIGURE:F12 BEGIN -->

![Least privilege contrasts necessary access with over-privilege in agents like promo-agent-shadow. Blast radius illustrates how narrowly scoped identities limit potential damage compared to full-access shared logins like novasmart-customer-sa.](images/F12_privilege_blast_radius.jpg)

<!-- FIGURE:F12 END -->
