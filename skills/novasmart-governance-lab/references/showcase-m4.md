# M4 Step 5 · Show what you measured — the five demos

> Read with `showcase.md`, which holds the workflow, the build bar, the check and the answer shape. This
> file holds Module 4's facts rules and one recipe per demo. In `showcase.md`, read "Step 7" as **Step 5**
> for this module: the evidence entry goes in `m4_step5.txt`, slot `M4 Step 5`. Source: the fact sheet from
> `show_facts.py 4 <demo letter>` (Steps 1–4). Save every page in `/config/Desktop/novasmart-showcase/`.

## 1. What an M4 page may say

M4 changed nothing in the estate. It measured the Price Match agent three times. These rules bind every
page.

- **Three runs, never merged.** *Step 1 · the deployed agent* (the shipped scenario set, against the agent
  serving the stores); *Step 2 · the local copy* (a tougher set the tooling wrote, against a copy of the
  agent's own code); *Step 4 · the local copy after the change* (the same set again, if the file says it
  was the same). Every number, row and quote carries its run's label.
- ⛔ **No single score.** No percentage, average, grade, pass rate, judge score (*4.2 / 5*), "X out of 10"
  or before-and-after delta, on any page, chart or slide. A run is shown as its **full partition on its
  fixed denominator**, counts exactly as recorded — *matched · did not match · near-miss · not run, of N*
  (the categories the file uses) — always all parts together, never one fraction alone.
- ⛔ **Near-misses and not-run cases stay in the denominator.** `N` is the case count the file fixed before
  the run. A case with no reply is *not run* (gray), never a pass or a fail, and never dropped. A
  *near-miss* is the right outcome reached by the wrong reasoning, shown with the agent's own words that
  make it one. A case refused before the agent saw it is a refusal, not a near-miss. If the counts in the
  file do not add up to `N`, show them as recorded and say *"the counts as recorded do not add up to N"*.
- **The judge.** Name what judged the cases, and its model, only as the file records one that ran, separate
  from the agent's own model. If the file says no judge ran, every verdict is labelled *"agy's reading — no
  judge ran"* (yellow, *inference*). Show the judge's written reason per case where the file holds it.
- ⛔ **The local copy is not production.** It is *"a local copy of the agent's own code, in a folder on this
  workstation"* — never "a project", "a test environment in the cloud" or "staging". Wherever a local
  result appears, say what differs, as the file records: **it cannot read competitor prices** (its login
  has no read on the competitor price data), **its escalation to the back office is removed**, and **no
  screen stands in front of it**. If the file does not record one of these, show it dashed: *"from
  configuration, not a test"*. A local result is never a statement about the deployed agent.
- ⛔ **The fix is not deployed.** The change was made to the local copy only. Never *"fixed"*, *"patched"*,
  *"rolled out"*, *"shipped"*, *"now live"* or *"the agent now refuses…"* about the deployed agent. The
  deployed agent's state comes only from Step 4's read of it, with how it was read (for example from the
  deployed package, or from the source) as the file says.
- **Same set, or not.** Show a case-by-case before-and-after only if Step 4's entry records replaying Step
  2's saved case file. If Step 4 wrote new cases, say *"a different set — not a case-by-case comparison"*
  and show the two runs side by side without pairing rows.
- ⛔ **Who refused: the screen or the agent, only from evidence.** A case was *refused by the screen* only
  where the file quotes the screen's reply for that case (copied character for character, with its status
  and time); *refused by the agent* only where the agent's own refusing words are quoted. Otherwise gray
  *"refused — who refused is not recorded"*. The local runs have no screen: a refusal there is never the
  screen's. A screen in front of the deployed agent is drawn only if a step read it or quoted its reply.
  A refusal by the screen says nothing about the agent: *"the agent was never asked"*.
- ⛔ **No governance scorecard for M4.** No PASS or FAIL for the module, no badge, nothing called *"the
  governance scorecard"*. The Instructions' word *scorecard* means the evaluation results table only.
- **Quotes are exact or absent.** Agent replies, the screen's message, the judge's reason and the
  instruction lines are copied from the file or left out. The one exception: the exposed discount code is
  **never** shown — in a quoted line, replace it with *[code withheld]* and say so beside the quote.
- **The 10% limit.** Mention a limit other than 10% only if the file records the agent stating one.
- **Escalations.** Only the cases the file shows escalating. A back-office decision appears only if it came
  back in the file; no costs or margin floors.
- **Product names.** *Agent Runtime* for where the deployed agent runs; the evaluation tooling as the file
  names it. Never "reasoning engine" or "Vertex AI" in prose.
- ⛔ **Nothing the files do not hold:** no time for an event with none on record; no case the file does not
  hold; no recommendation, launch verdict, owner, monitoring plan or deadline of your own. Never *"ready to
  launch"*, *"safe"*, *"secure"*, *"production-ready"*.
- **The leader's decision.** The three questions from the Instructions, word for word, are the leader's to
  answer: *"Does this go live? Decide on what the scorecard shows, not on how much work it took to get
  here."* · *"What would you fix first? Pick the single failure or weakness that worries you most, and be
  able to say why it is that one and not another."* · *"What would you monitor after launch? Name the thing
  you would want to be told about on the day it starts going wrong."* Leave them unanswered unless the
  leader answered in this session; then quote the leader.
- **Still open:** only the sentences `show_facts.py 4` prints as *Still open*, word for word, and nothing
  added. M4 is the last module: there is no next module to name.
- **Footer on every page:** *"Nothing in the estate was changed in this module."* — plus, if Step 4 ran,
  *"The one edit was to a local copy on this workstation, and it is not deployed."*

## 2. The demos

### A · Case explorer — `m4_case_explorer.html` (the one to start with)

*"Build me a page where I can read our evaluation results case by case."*

**Answers:** for each case, what was asked, what did the agent say, what was the verdict, and why?

**Must show**
1. Hero band: the runs recorded and each run's `N`, with the takeaway *"read the rows, not the total"*.
2. **Run buttons** (`aria-pressed`): Step 1 · deployed agent · Step 2 · local copy · Step 4 · local copy
   after the change. Each labelled with where it ran and whether a screen stood in front (§1). A run with
   no file is gray, *not run yet*.
3. **The partition bar** per run: every category on that run's `N`, counts as recorded, each segment with a
   word. No percentage.
4. **One card per case**: what was asked (quoted or in plain words), what the policy expects, the agent's
   own words, the verdict, the judge's reason (or *"agy's reading — no judge ran"*), and who refused, as §1
   allows. Filter buttons: *all* · *did not match* · *near-miss* · *not run* · *refused*. *All* is the
   default, and not-run cards stay visible in it.
5. **The judge card**: what judged, as §1 allows.
6. **What these runs do not cover**, from the files: a case count short of what was asked for; the local
   copy's three differences; anything marked not run.
7. "Still open" band and footer.

**Done when:** each run's counts add up to its `N` (or the page says they do not); no score appears; every
quote is in the sheet.

### B · Who refused — `m4_who_refused.html`

*"Build me an explainer of who actually refused each case: the screen or the agent."*

**Answers:** when a case was refused, did the screen stop it before the agent saw it, or did the agent
refuse it itself?

**Must show**
1. Hero: *a refusal has two possible authors*.
2. **The two layers** (SVG): request → the screen (drawn only for the deployed run, and only as §1 allows)
   → the agent. Each refused case is a marker placed at the layer that refused it, with its quote: the
   screen's message, or the agent's words. Not settled → gray marker *"who refused is not recorded"*.
3. **Deployed vs local, side by side**: Step 1's refusals beside the local runs' refusals. The local side
   carries *"no screen in front of this copy"*.
4. **"Refused by the screen is not a near-miss"**: the agent was never asked, so the case says nothing
   about the agent's own rules.
5. Play, Pause and Step walk one refused case through the layers; loads showing every marker placed.
6. "Still open" band and footer.

**Done when:** no refusal is attributed without its quote; no screen appears on a local run; no screened
case is counted as the agent's pass.

### C · Fix vs production — `m4_fix_vs_production.html`

*"Build me a before-and-after of the fix, and what is still running in production."*

**Answers:** what changed in the local copy, did it move the cases, and what is the deployed agent still
running?

**Must show**
1. Hero: *measured on a copy; not deployed*.
2. **Three columns**: *local copy, before* | *local copy, after* | *deployed agent, now*. The instruction
   line in each, quoted exactly as Steps 3 and 4 recorded it (code withheld, §1). The deployed column comes
   from Step 4's read only, with its time and how it was read; not read → gray *"not read"*.
3. **Per-case movement**: Step 2's verdict beside Step 4's for the same cases (*moved* · *unchanged* · *not
   run*), on the same `N` — only if §1's same-set condition holds; otherwise the banner *"a different set —
   not a case-by-case comparison"*.
4. **What is still true in production**, from Step 4's lines only: the deployed agent does not carry the
   change; a screen in front only as recorded; the exposed discount code only as recorded, never its value.
5. **The gap as a diagram**: local copy → (no deploy) → deployed agent, the break drawn and labelled *"not
   deployed"*.
6. "Still open" band and footer.

**Done when:** nothing says or implies the deployed agent is fixed; every deployed-side fact traces to a
Step 4 line; no delta or score.

### D · Judge the Judge — `m4_judge_the_judge.html` (a game)

*"Build me a game called Judge the Judge from our evaluation, for my team to play."*

**Answers:** can your team call a verdict from the reply, tell who refused, and keep the denominator
honest? Three rounds, two to four minutes.

**Must show**
1. **Start screen**, then **Round 1 · Call it**: a case card (what was asked, what the policy expects, the
   agent's own words). The player picks *matched* · *did not match* · *near-miss* · *not run*, then sees
   the recorded verdict and the judge's reason (or *"agy's reading — no judge ran"*). Four to six cases
   from the files, including a near-miss and a not-run case if the files hold them. **Answers are buttons
   or cards (`aria-pressed`), never a `<select>` dropdown**; every answer reveals its evidence line.
2. **Round 2 · Who refused?**: refused cases; the player picks *the screen* · *the agent* · *not recorded*,
   settled by §1.
3. **Round 3 · Keep the denominator**: six to eight statements to mark *the evidence supports this* or
   *goes too far*. Goes too far: a total that leaves out a not-run case; *the agent is fixed*; *production
   now has the fix*; a single score for the run; *the screen's refusal shows the agent refuses overrides*;
   *the local copy checked competitor prices*. Supported, if the files say so: the run's full partition on
   its `N`; *the change was made to a local copy only*. Drop any statement the sheet does not settle.
4. **Score** the player (the player's score, never the agent's), feedback on every answer; **end screen**
   with their score and what they practised; **facilitator view** at `#answers`. "Still open" band on the
   start and end screens; footer.

**Done when:** every answer is settled by a line in the sheet; no not-run case is scored as a pass or a
fail.

### E · Evidence pack — `m4_evidence_pack.html`

*"Turn what I measured into a one-page evidence pack for the launch review."*

**Answers:** what was measured, what does the evidence support, what does it not cover, and what is left
for the leader to decide?

**Must show** — one page that prints on one sheet (`@media print`, A4 and Letter), white, no slides:
1. **Header**: module tag, title, *"Built from the evidence agy recorded on <date>"*.
2. **What was measured**: each run — where it ran, the set, `N`, its full partition, the judge (§1).
3. **What the evidence supports**: short statements, each with its step file and line.
4. **What it does not cover**: the local copy's differences, not-run cases, the case count, anything not
   read, and the screen's limits only as recorded.
5. **Two separate decisions**: *the deployed agent as it runs now* and *the local change, not deployed* —
   each with the facts behind it and no verdict.
6. **The leader's three questions**, word for word (§1), each with blank lines, or the leader's own answer
   quoted.
7. "Still open" band, sources and footer.

**Done when:** it fits one printed page; nothing recommends launching or not; no score; the three questions
are verbatim.

**Asked for a poster or picture instead** (run `show_facts.py 4 E`, which prints this too): build
`m4_poster.html`; the check renders it as a poster by itself — the
three runs' partitions and the fix-vs-production columns on one 1600 × 900 canvas, with the takeaway, the
"Still open" line and the footer.
