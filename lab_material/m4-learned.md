# M4 · Evaluate and Decide (Optional Module) — What did we learn?

*Read this after you finish Module 4. It names what you found, so you can explain it in your own words.*

**In one sentence:** A control tells you what cannot happen; only a scored test against known right answers tells you the agent still does its job, and a fix measured on a copy is not a fix in production.

## What each prompt tested

<!-- FIGURE:L4_01 BEGIN -->

![The title reads: What each prompt tested. Four rows, each a white step card with a speech-bubble icon and a blue chip, and an arrow to a finding. 1 · Score the four cases, Deployed agent, leads to Judge's verdict and reason, per case, in gray. 2 · Build a tougher set, Local copy, leads to One saved case file, in gray. 3 · See the fix first, Instructions, leads to Old and new wording, not applied, in amber. 4 · Change, measure again, Same case file, leads to Fix on the copy, not production, in red.](images/L4_01_what_each_prompt_tested.webp)

<!-- FIGURE:L4_01 END -->

M4 changed nothing in your estate. It measured the front desk (the Price Match Agent) against NovaSmart's written policy: settle up to 10% on the spot, send larger matches to the back office, refuse manipulation. Your own run is your evidence; this page uses what the Instructions say to expect.

- **Step 1** put NovaSmart's four cases to the deployed agent through Google Cloud's Gen AI evaluation service. A judge, a second AI model separate from the agent's own, marks each answer and writes down why. If the judge could not run, agy says the verdicts are its own reading.
- **Step 2** had the tooling write a tougher set, usually at least eight cases grounded in your catalog, saved to one file and run on a local copy of the agent in a folder on this workstation.
- **Step 3** showed the fix for the worst case as the old and new wording of the agent's instructions. Nothing was applied.
- **Step 4** applied it to the copy only, ran the same file again, compared the runs case by case, then said what still holds for the deployed agent.

## Read the rows, not the total

<!-- FIGURE:L4_02 BEGIN -->

![The title reads: Every case stays in the count. Four cards side by side, each with an icon. A blue card: Matched, Right outcome, right reason. An amber card: Near-miss, Right outcome, wrong reason. A red card: Did not match, Wrong outcome. A gray card: Not run, No reply came back. A gray bar bracketing all four reads One case count, fixed before the run.](images/L4_02_every_case_counted.webp)

<!-- FIGURE:L4_02 END -->

Each verdict carries the judge's reason, the part you can audit. The judge is not infallible, so check an odd verdict against the agent's actual reply.

Fix the number of cases before the run and report against it. A case with no reply is not run: not a pass, not a failure, still counted. A near-miss is the right outcome reached by the wrong reasoning: the judge may mark it matched, so read the reply. If anything cites a limit other than 10%, the running agent and the written policy have drifted apart.

## Two authors of one refusal

<!-- FIGURE:L4_03 BEGIN -->

![The title reads: Two authors of one refusal. A gray card with a speech-bubble icon, A manipulation attempt, points to an amber diamond, Who refused it? The diamond branches to two blue cards: The screen, with a shield icon, Comes back as an error; and The agent, with a gear icon, Answers in its own words. A gray band beneath reads Quote the message, not the status code.](images/L4_03_two_authors_of_a_refusal.webp)

<!-- FIGURE:L4_03 END -->

If you ran M3, the evaluation reaches the deployed agent through the screen in front of it, the way a customer does. So a refused manipulation case has two possible authors: the screen turned the message away, or the agent read it and declined. A screened refusal arrives as an error rather than an answer, and its words are the tell. NovaSmart's screen is not set to log its verdicts, so the quoted reply is the record. If you skipped M3, every refusal is the agent's own.

A screen in front of a problem is not a repair of it. You can say the screen held against the wording tried, that day. You cannot say the agent was fixed.

## The proof: same set twice, on a copy

<!-- FIGURE:L4_04 BEGIN -->

![The title reads: Same set twice, on a copy. Two panels. A large blue panel, Folder on this workstation, holds a row joined by arrows: a gray card with a document icon, Saved case file; Run 1; an amber card with a pencil icon, Fix applied; and Run 2. A gray band beneath the row reads Compared case by case. A white panel on the right, What your stores run, holds a blue card with a gear icon, Deployed agent, and two tags below it: a red tag, Fix not deployed, and an amber tag, Screen in front, if M3 ran.](images/L4_04_same_set_twice.webp)

<!-- FIGURE:L4_04 END -->

Step 4 is the smallest honest unit of evidence for a change: the same cases, the same policy, the same judge, one thing different. A regenerated set is a different set.

What it proves: which cases moved, and in which direction, on a local copy, measured once. What it does not prove: anything about the deployed agent, or by how much. The judge is a model, so two runs can disagree on a case nothing changed. Expect movement, not a clean sweep.

The copy is the real agent's code with three differences: no hand-off to the back office, no screen in front of it, and no read access to competitor prices, so it cannot verify a match.

Open `/config/Desktop/novasmart-evidence/m4/m4_step4.txt` and find row 17, the same cases replayed, and row 20, nothing in the estate changed or deployed.

## Where this shows up

<!-- FIGURE:L4_05 BEGIN -->

![The title reads: Same test, other industries, with a tag reading Illustration. Three gray cards, each with an icon: Banking, with a bank building, Loan assistant scored against known decisions; Insurance, with an umbrella, Claims fix measured on a test copy; and Healthcare, with a cross, Who refused: the filter or the bot?](images/L4_05_same_test_elsewhere.webp)

<!-- FIGURE:L4_05 END -->

Three made-up scenarios:

- **Scenario: the loan desk.** A bank scores its loan assistant against past applications with known decisions. The near-misses get read first.
- **Scenario: the measured fix.** An insurer improves its claims bot's wording and measures it on a test copy. Production runs the old wording until someone deploys.
- **Scenario: who said no.** A clinic's chatbot refuses a risky request. The team checks whether the filter or the bot refused before calling the bot safe.

[Google's Gen AI evaluation service overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview) says "Evaluation rubrics are similar to unit tests in software development." Treat a scenario set the same way: it grows every time production surprises you.

## Your call: launch on evidence

<!-- FIGURE:L4_06 BEGIN -->

![The title reads: Launch on evidence, not effort. Four amber cards with question-mark icons, side by side: Go live today? (Decide on Step 1's rows); Ship the local fix? (Separate decision, separate owner); What to fix first? (Name one, and say why); and What to watch? (The day it goes wrong). A gray band across the bottom reads Your call, with risk and compliance.](images/L4_06_launch_on_evidence.webp)

<!-- FIGURE:L4_06 END -->

The call has two halves. Whether today's agent goes live rests on Step 1, the only measurement of the deployed agent. Whether the local fix goes anywhere is a separate decision with a separate owner. The launch call is yours together with risk and compliance, not agy's.

- **Evaluation:** running an agent against many known cases at once and scoring each answer, instead of trying one and forming an impression.
- **Configured is not running:** a measured improvement on a copy is not in production until somebody deploys it.

## Where your estate stands

<!-- FIGURE:L4_07 BEGIN -->

![The title reads: Where your estate stands after Module 4. A row of six tall segments, left to right: Visible, Attributable, Least privileged, Access controlled, Screened, Measured, tagged M1, M1, M1, M2, M3 and M4 · optional. Visible and Attributable are green; the other four are gray. Small amber markers sit above the four gray segments: Least privileged reads Three agents only, Access controlled reads Back office only, Screened reads One agent only, and Measured reads Fix on a copy.](images/L4_07_estate_progress.webp)

<!-- FIGURE:L4_07 END -->

Module 4 left your estate as Module 3 left it. It added a record: the deployed agent scored on known cases, and a fix measured on a copy that is not in production. Measured covers one agent, as Screened does if you ran M3.

| Property | What it means | Where you build it |
| :-- | :-- | :-- |
| Visible | Every agent that runs is in the catalog, with an owner | M1 |
| Attributable | Every action traces to one named agent | M1 |
| Least privileged | Each agent holds only the access its job needs | M1 |
| Access controlled | Only approved callers can reach a sensitive agent | M2 |
| Screened | Attempts to talk an agent out of its rules are stopped at the door | M3 |
| Measured | The agent's answers are tested against known cases before you trust it | M4 (optional) |

This is the last module. The habit to take home: ask what is running, insist on evidence, measure before you trust.

## Questions to take back to your team

- Who tests our agents against cases with known right answers, and how often?
- Do our test totals keep the cases that never ran?
- When an agent refuses, can we show whether a filter or the agent said no?
- Which measured fixes are not in production, and who owns deploying them?
- Who can change an expected answer in our test cases?

## Read more

| Topic | Official page |
| :-- | :-- |
| What the evaluation service does | [Gen AI evaluation service overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview) |
| Writing the cases | [Prepare your evaluation dataset](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-dataset) |
| Scoring against your own policy | [Define your evaluation metrics](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/determine-eval) |
| The judge model | [Configure a judge model](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/configure-judge-model) |
| Evaluating an agent, not only a model | [Evaluate Gen AI agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents) |
| The screen in front of the agent | [Model Armor overview](https://docs.cloud.google.com/model-armor/overview) |

For the story behind each step, see the matching Step section on the Reference Guide tab.
