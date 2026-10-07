# M3 · Protect the Content — What did we learn?

*Read this after you finish Module 3. It names what you found, so you can explain it in your own words.*

**In one sentence:** A filter NovaSmart already owned now screens what customers send to one agent, the Price Match Agent, at its inbound gateway; the customer-record attack and the other two agents are not covered, and the screen lets traffic through if it cannot run.

## What each prompt tested

<!-- FIGURE:L3_01 BEGIN -->

![The title reads: What each prompt tested. Five rows, each a white step card with a speech-bubble icon and a blue product chip, and an arrow to a finding under the heading What the Instructions say to expect. 1 · Talk them into it?, Agent Runtime, leads to Both agents broke their rules, in red. 2 · What screens today?, Model Armor, leads to Owned filter, connected to nothing, in amber. 3 · Screen the door, Agent Gateway + Model Armor, leads to Price match agent behind the screen, in green. 4 · Try it again, Agent Runtime, leads to Discount attack stopped; real requests answered, in green. 5 · What can we claim?, Agent Gateway, leads to One agent, not the estate, in amber.](images/L3_01_what_each_prompt_tested.webp)

<!-- FIGURE:L3_01 END -->

Two agents face customers, the Price Match Agent and the Customer Personalization Agent, and pass whatever a shopper types to the AI. Your own run is your evidence; this page uses what the Instructions say to expect.

- **Step 1** sent attacker-style messages to both agents on Agent Runtime, Google Cloud's managed service for running agents. Expect both to comply: a discount past the 10% limit approved instead of escalated, and customer records handed over, masked in agy's report.
- **Step 2** changed nothing. Expect nothing screening these messages, and a Model Armor filter (Model Armor is Google Cloud's service that screens what people send to an AI and what it sends back), `nvst-jailbreak-template`, attached to nothing.
- **Step 3** put the Price Match Agent behind the inbound gateway, which hands each message to that filter, and read the routing back. Expect one agent named.
- **Step 4** replayed both attacks and two ordinary requests. Expect the discount attack stopped, ordinary requests answered, and the customer-record attack not covered.
- **Step 5** separated proof from assumption: one agent screened, not the estate.

## Screen what the customer sent

<!-- FIGURE:L3_02 BEGIN -->

![The title reads: Where the screen stands to read. Two panels split by a vertical line, each a white box with a magnifying-glass icon. Left, Project-wide, inside the agent: three pills, Its own instructions and Its tools and their data in gray, and The customer's message in blue; beneath the box, a red box reads Real work stopped too. Right, At the inbound gateway: a line reading Instructions, tools and data not read, then one blue pill, The customer's message.](images/L3_02_where_the_screen_reads.webp)

<!-- FIGURE:L3_02 END -->

The obvious fix was a project-wide setting (applied across everything in the project, not to one agent). It reads everything an agent assembles: its instructions, its tools and their data. That looks like an attack, because instructions telling a system what to do are what an attack is. When NovaSmart's engineers switched it on, it stopped almost all real work: price checks, lookups, offers.

An inbound gateway stands in front of an agent and sees only what clients send it, which is what you wanted to read.

## One door, one agent behind it

<!-- FIGURE:L3_03 BEGIN -->

![The title reads: What the screen covers. A white box, Customer messages, with a chat icon, has a solid arrow to a blue block holding two white pills, novasmart-ingress-gateway and nvst-jailbreak-template, and a small amber note reading Fails open if it cannot run. A solid arrow runs from the blue block to a green box, Price Match Agent, tagged Screened. A dashed arrow runs from Customer messages, below everything else, to a gray box, Customer Personalization Agent, tagged Not covered. Under the blue block, a separate gray box, Back office, holds a white pill, novasmart-egress-gateway, and the line Reach control, not a screen; no arrow touches it.](images/L3_03_what_the_screen_covers.webp)

<!-- FIGURE:L3_03 END -->

The screen covers the Price Match Agent only. The other two agents are reached over A2A (Agent2Agent), an open protocol for calling agents, which this screen does not read. M2's outbound gateway, `novasmart-egress-gateway`, decides where the back office may reach and reads no content.

The screen is set to fail open: if it cannot run, traffic passes with no error. That keeps stores serving, and it is a remaining risk. Replies pass the same filter, which looks for manipulation, harmful content and malicious links, not names or email addresses; nothing in this module tested the way out.

## The proof: same requests, before and after

<!-- FIGURE:L3_04 BEGIN -->

![The title reads: Same requests, before and after. Three rows, each with an arrow from a box under Before the screen to a box under What to expect after. Discount attack: Settled past the limit, in red, to Stopped before the agent, in green. Customer-record attack: Records handed over, in red, to Not covered, in gray. Ordinary requests: Answered, in blue, to Still answered, in green.](images/L3_04_same_requests_before_after.webp)

<!-- FIGURE:L3_04 END -->

The Instructions say to expect the discount attack stopped before the agent reads it. A blocked message comes back as an error that can look like a fault; its words, quoted with the time, are the record of the block. Cloud Logging holds no verdict, because NovaSmart's filter is not set to log verdicts.

Ordinary requests, including a lookup, should still get answers; a screen that blocks the business has caused an outage. The customer-record attack is reported as not covered, which does not fail the module.

Open `/config/Desktop/novasmart-evidence/m3/m3_step4.txt` and find the quoted reply. Step 4 ends with agy updating the Governance Scorecard, the web page on your Desktop that tracks each module's checks.

## Where this shows up

<!-- FIGURE:L3_05 BEGIN -->

![The title reads: Same door, other industries, with a tag reading Illustration. Four cards, each with an icon: Retail, Price match agent screened at the door, in blue; then, in gray, Banking, Loan chatbot keeps its rate limit; Travel, Refund agent ignores fake staff orders; and Healthcare, Booking agent screens what patients type. A gray bar beneath reads: Screen what customers send, at the door.](images/L3_05_same_door_elsewhere.webp)

<!-- FIGURE:L3_05 END -->

Swap in any agent that reads what customers type and the pattern holds. Three scenarios, made up to illustrate it:

- **Scenario: the loan chatbot.** A bank's chatbot must not offer a rate below a set limit. Its screen turns away messages written to talk it past that limit.
- **Scenario: the fake staff order.** A traveler claims a staff member approved a full refund. The screen catches it before the refund agent acts.
- **Scenario: what patients type.** A clinic screens what patients send its booking agent. The filter looks for manipulation, not names, so personal details need a separate check.

[Google's Agent Runtime documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy) says "Changing an Agent Gateway binding on a Runtime agent archives every pre-existing revision of the agent. Archiving is irreversible." Taking an agent back out restores its routing, not those revisions.

## Your call: where to screen, and what it covers

<!-- FIGURE:L3_06 BEGIN -->

![The title reads: Before you screen anything. Four tall cards joined by arrows, left to right. Two amber cards with question-mark icons: What screens it today? (Look for what you own) and Where should it read? (At the door, not inside). Two blue cards with gear icons: Screen one door (Name each agent it covers) and Test attacks and real work (A block plus an answer). An amber band across the bottom, with a question-mark icon, reads What happens if the screen cannot run?](images/L3_06_before_you_screen.webp)

<!-- FIGURE:L3_06 END -->

Step 2 paused before any change and found a control already paid for. Ask the two questions before taking the two actions.

- **Screen at the door:** read what the customer sent, not everything the agent assembles.
- **Name each agent it covers:** an agent you tested is not an agent you covered.
- **PII:** personal information about a real customer — name, email, purchase history. This filter does not look for it.

If the screen cannot run, who notices? Write that owner down.

## Where your estate stands

<!-- FIGURE:L3_07 BEGIN -->

![The title reads: Where your estate stands after Module 3. A row of six tall segments, left to right: Visible, Attributable, Least privileged, Access controlled, Screened, Measured, tagged M1, M1, M1, M2, M3 and M4 · optional. Visible and Attributable are green; the other four are gray. Small amber markers sit above three segments: Three agents only above Least privileged, Back office only above Access controlled, and Price match only above Screened.](images/L3_07_estate_progress.webp)

<!-- FIGURE:L3_07 END -->

Module 3 built Screened for one agent, the Price Match Agent. Still open: the two agents this screen cannot reach, fail open, the untested way out, the storefront's exposed discount code, broad project-wide roles, and the front desk's broad database role.

| Property | What it means | Where you build it |
| :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 |
| Attributable | Every action traces to one named agent | M1 |
| Least privileged | Each agent holds only the access its job needs | M1 |
| Access controlled | Only approved callers can reach a sensitive agent | M2 |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) |

M4 · Evaluate and Decide (Optional Module) measures, against a full scenario set, whether the agent got worse at its job.

## Questions to take back to your team

- Which controls have we paid for that are not switched on?
- Which agents read what customers type, and which of them are screened today?
- If our screen stopped running, how would we find out?
- When we test a screen, do we also check that real customers still get answers?
- Who decided how suspicious our screen is, and what would changing it cost?

## Read more

| Topic | Official page |
| :-- | :-- |
| What Model Armor screens | [Model Armor overview](https://docs.cloud.google.com/model-armor/overview) |
| Screening at the gateway | [Integrate Model Armor with Agent Gateway](https://docs.cloud.google.com/model-armor/model-armor-agent-gateway-integration) · [Configure Model Armor on a gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/configure-model-armor) |
| Inbound and outbound gateways | [Agent Gateway overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview) |
| Routing an agent, and archived revisions | [Route Agent Runtime traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy) |
| A filter and its settings | [Create and manage templates](https://docs.cloud.google.com/model-armor/manage-templates) |
| Why there is no verdict in the logs | [Configure logging](https://docs.cloud.google.com/model-armor/configure-logging) |

For the story behind each step, see the matching Step section on the Reference Guide tab.
