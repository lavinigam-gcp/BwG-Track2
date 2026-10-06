---
name: bwgtrack2-demo-build
description: >-
  Build the learner's optional post-mission demo app in the NovaSmart lab (Build with Google Track 2):
  a small, real, locally served Python app grounded in live reads of the learner's own Google Cloud
  project, implementing the commission brief the brainstorm skill already wrote. Load when a `BRIEF.md`
  exists in the learner's demo folder, or when the leader asks you to build / make / put together their
  demo app after finishing a mission. ⛔ Do NOT load during ordinary mission work — readiness checks,
  discovering the estate, splitting a shared login, right-sizing access, screening content, evaluating,
  or any verification or scorecard turn belong to `novasmart-governance-lab`.
  ⛔ Never load while the laptop is being set up, installed, repaired, or checked for readiness.
  "Set up my laptop", "am I ready", "am I ready for the lab", "check my setup" and "verify my
  environment" all belong to `bwg-lab-setup`, even when they are asked with this folder open. The
  toolchain, the Python environment, the session folders and verify.sh are not this skill's
  business, and answering them here would ask for cloud credentials that are not issued until the
  event. If there is no `BRIEF.md`,
  do not start: read `../build-demo/SKILL.md` and run the conversation first.
---

# Build the demo — steering skill for `agy`

## 0. What you are building, and for whom

The leader has just finished a mission. This is **optional, self-paced, 20-30 minutes**, and it is the
first thing all day that is **theirs**. You are not building a lab exercise; you are building the
artefact they will show someone.

Same reader as every other turn: a **non-technical senior IT leader**. Plain English first, raw IDs and
command output as evidence beneath. Everything in `novasmart-governance-lab/SKILL.md` §2, §3a and §4
still applies to what **you say**. This file governs what you **build**.

⚠️ **Say the teardown truth once, early, and do not repeat it.** The project, the VM and this folder are
destroyed when the lab ends. What survives is what the leader understood and anything they take away
themselves. That changes what is worth building — the moment, not the artefact.

## 1. The baseline — the one thing every version of this app must do

The baseline is **per mission**, because each mission unlocks a different proof. Read the `Mission:`
line in `BRIEF.md`, then take that row and no other.

| Mission | The baseline for a demo built after it |
| :-- | :-- |
| **M1** | **Cause a real read of NovaSmart's customer table, then name — from Google Cloud's own audit log, not from the app's opinion — which single workload did it, and say plainly which reads it still cannot attribute.** |
| M0 | ⛔ **Not yet defined.** |
| M2 | ⛔ **Not yet defined.** |
| M3 | ⛔ **Not yet defined.** |
| M5 | ⛔ **Not yet defined.** |

⛔ **Never invent a baseline for a mission whose row says NOT YET DEFINED**, and never stretch another
mission's baseline to cover it. Improvising the thing an app must prove is how you get a confident app
that proves nothing — the exact failure `references/build-and-ground.md` exists to prevent.

**What to do when the row is undefined.** Say it in one plain line — *"There isn't a demo defined for
Mission 3 yet, so this will be the Mission 1 one"* — then build the **M1** baseline, which still holds
after any later mission because the estate still attributes reads. It simply will not showcase what the
later mission changed. The learner chooses whether that is worth their time.

That is a **capability, not a design**. It does not say console, timeline, map, feed or narrative, and
it does not say what goes on the front. The brief decides all of that. **You do not renegotiate the
baseline, and you do not add to it.**

### 1a. The spine — three elements that hold for every mission

Whatever the baseline and whatever shape the app takes, these three never change:

| # | Spine element | Why it is not optional |
| :-- | :-- | :-- |
| **S3** | It shows at least one thing it **could not** attribute or could not read, in the literal words `not read` | Half of any baseline is the limit, not the finding |
| **S4** | Every figure carries **the command that produced it and the UTC time it ran** | A figure without a source is a rumour with a typeface |
| **S5** | It emits **no verdict, tick, score or badge** the platform did not itself emit | This estate already ships two surfaces that manufacture success — see `references/build-and-ground.md` §1 |

### 1b. The M1 baseline's own two elements

These belong to the M1 row above. A future mission's row will carry its own pair, and they will not be
these.

| # | Spine element | Why it is not optional |
| :-- | :-- | :-- |
| **S1** | The app **causes** at least one real read this session, and records the UTC time it fired | *No trigger, no claim.* An app that only reads history is a log viewer |
| **S2** | It reads the **platform's own audit record** back and shows the acting principal **verbatim** | The claim comes from Google Cloud, not from your app |

**The baseline and the spine are the only fixed things.** Form, audience, headline, what the app says
when a read fails, and which leftover risk gets permanent screen space are the learner's, and they are
already in the brief.

## 2. The handoff in — read the brief, then read it back

1. **Find `BRIEF.md`.** The brainstorm skill wrote it into the learner's demo folder —
   `$HOME/Desktop/Session<N>/bwgtrack2-demo/BRIEF.md`, the same folder the app will appear in.
   **Confirm the folder that actually holds it; never assume the session number.**
2. ⛔ **No brief → do not build.** Say one sentence — *"Let's decide what this is first"* — then read
   `../build-demo/SKILL.md` and run that conversation. Coming back with a brief takes
   about three minutes. Building without one produces the same app as everyone else in the room.
3. **Read the brief back in one sentence** before you write anything: what it is, who it is for, what
   sentence is on the front, and what stays permanently on screen. If you have that wrong, now is the
   cheap moment to find out.
4. ⛔ **Do not redesign the brief.** The open answers in it are the learner's words. Quote them; never
   paraphrase them into your own. If something in the brief cannot be built honestly, say which line and
   why, offer the nearest honest thing, and let them choose.
5. **The brief changes which reads you run, not just how the page looks.** A brief about the dataset
   access list and a brief about denials are different apps with different commands. Pick the reads the
   brief actually needs from `references/data-palette.md` — not all of them.

## 3. The build loop

Work in this order. It exists because the expensive part — the audit log's minutes of lag — runs
underneath everything else.

| # | Step | Notes |
| :-- | :-- | :-- |
| 1 | **Sweep first.** Run the reads the brief needs, write one JSON file per read into `evidence/`, each carrying the exact command and the UTC time it ran | Evidence exists **before** the app does, so every later failure still leaves something real |
| 2 | **Fire the triggers early**, before a line of app code exists, and record both UTC send times | The lag becomes the schedule instead of a wait. `references/data-palette.md` §4 |
| 3 | **Report what failed** in one plain line | A read that 403'd is a panel that says `not read`, and that is a passing outcome |
| 4 | ⭐ **Read the look-and-feel rules, then decide the look yourself.** Before you write **any** HTML or CSS, open, in this order: `references/build-and-ground.md` §6 (the layout contract) and §7 (what a gamified page may and may not do); `vendor/OVERRIDES.md`; then `vendor/design-rules/typography.md`, `layout-and-space.md`, `color.md`, `anti-patterns.md` and `slop-test.md` | §5. ⚠️ **Never ask the learner about the UI** — the rules and the brief decide it, and you decide the rest. This step is why the page is readable by the person it is for |
| 5 | **Copy `assets/starter_app.py`** into the demo folder as `app.py`, then **diverge from it** | §4 |
| 6 | **Run it and open it** | `references/local-run.md` — the port range, Chrome, the ban on `xdg-open` |
| 7 | **Verify it is real** | `references/local-run.md` §4. This is not optional and it is not a formality |
| 8 | **Hand back** the URL, the screenshot, and one honest line about what the page cannot show | §6 |

⏱ **Budget.** Sweep and triggers by minute 8, app running by minute 17, the audit rows land while the
learner watches the build. If you are behind, cut panels — never cut the trigger or the verification.

## 4. The starter is a starting point, not a template

`assets/starter_app.py` is a working skeleton: one Python file, standard library only, a `PROBES` list of
`{id, argv, parser}`, a `run_probe()` that records `argv` + UTC + exit status, an estate endpoint, a
trigger endpoint, and the page.

- **Copy it, then make it the learner's.** The panels, the ordering, the words, the shape and what the
  page does when a read fails all come from the brief.
- ⛔ **An app that is the starter with the project ID changed has failed the activity.** Twenty identical
  pages is exactly what the brainstorm skill spent three minutes preventing.
- **Keep it small.** One file, standard library only, roughly 200 lines. If it will not fit, the design is
  too big for the slot — cut a panel, not the honesty rules.
- **Its stylesheet already implements the layout contract** — the token block, the type scale, the single
  column, the identifier wrapping. Change the panels, the words and the shape freely; if you rewrite the
  CSS, rewrite it to the same contract (`references/build-and-ground.md` §6), not to a fresh guess.
- **Why Python and not a static page:** a `file://` page cannot cause the read. It has no credentials and
  its `fetch` is blocked. A tiny local service shells out to `gcloud` / `bq` / `curl` and inherits the
  VM's ambient credentials, and that is the entire grounding mechanism.

## 5. The four references — read the one you need

| File | Read it when | What it gives you |
| :-- | :-- | :-- |
| `references/data-palette.md` | **Before the sweep. Always.** | Every readable source, the exact command, what it returns, its confidence, and what an app does with it. The two triggers, and the one that is banned |
| `references/build-and-ground.md` | **Before you write a line of the page. Always.** | The honesty contract as enforceable rules, the fences (read-only, no customer rows, no credentials, never `test-agent-caller`), **§6 the layout contract** — tokens, type scale, column width, identifier wrapping — **§7 the line a gamified page may not cross**, and the self-check before you hand back |
| `references/gallery.md` | Only if the learner is stuck for a shape | Short seeds, mission-tagged. Not recipes, and never a menu you pick from on their behalf |
| `references/local-run.md` | Steps 6-8 | The port range and how to pick one, how the learner opens it, and the verification checklist you must perform and report |

### `vendor/` — the look-and-feel guidance the build depends on

`vendor/design-rules/` holds fifteen files of vendored look-and-feel guidance — typography, spacing,
colour restraint, interaction states, and the named tells that make a page read as machine-generated —
under a third-party licence. **Step 4 of the build loop requires you to read the five named files.** This
is the step that was skipped in a real run, and the page that came back was a near-black terminal with
monospace headings that its reader could not interpret. Three rules:

- **Read `vendor/OVERRIDES.md` before any file under `vendor/design-rules/`.** It records, row by row,
  where the vendored advice and this suite disagree, and it is short.
- **`references/build-and-ground.md` wins outright, every time.** Vendored guidance governs how the page
  **looks**; it never governs what the page **claims**. It contains no `SKILL.md`, and never will.
- ⛔ **Never edit a file under `vendor/`** to make it agree. Record the divergence in your report instead.

**If a file named in step 4 is genuinely missing**, say which one in one plain line, then build to
`references/build-and-ground.md` §6, which restates as enforceable rules the handful of decisions those
files exist to settle. ⛔ **A missing vendored file is never permission to skip the layout contract**, and
it is never a reason to ask the learner what the page should look like.

## 5a. House style for the thing you build

The page is read by someone who thinks in risk, not commands. Seven rules, and they are not taste:

- **The form is settled by the layout contract, not by preference and never by asking.** Light page, one
  column, a proportional face for prose, monospace only for commands and identifiers, and long resource
  paths that wrap instead of running the width of the screen: `references/build-and-ground.md` §6.
- **A heading names what was read, never what it means.** *"Reads of the customer table, last 60
  minutes"* — not *"Customer data secured"*.
- ⛔ **No grading word anywhere on the page**: secure, safe, protected, compliant, healthy, clean,
  exposed, vulnerable, at risk. Every one of them is a verdict wearing an adjective.
- ⛔ **No tick, cross, badge, pill, score, percentage or traffic-light colour.** A state is worded. There
  is no green and no red. **This holds when the learner asked for a game**, and it is the only thing that
  does: levels, progression and playful headings are all theirs to have —
  `references/build-and-ground.md` §7 draws the line and gives four tests for it.
- **Plain English above, raw values below.** A full service-account address, a resource path or a
  `principal://` value belongs in the evidence line under a panel, never in the headline over it.
- **The page must work with the network unplugged after load.** ⛔ No remote stylesheet, font, script or
  image; no `@import`, no CDN. A page that needs the network is a page that fails in the room.
- **Write nothing into the learner's folder except the demo** — the app, `evidence/`, and the line you
  append to their brief. No dot-directories, no tool logs, no notes files.

## 6. How to close

- **Hand back three things**: the URL as the **last line** of your reply, the screenshot you took after
  looking at your own render, and one sentence naming what the page cannot show.
- **Never claim the app is finished, correct or complete.** Say what it does, what you verified live, and
  what came back `not read`.
- **The leader owns when to stop.** Finishing early with something honest beats running over with
  something padded. Say so once, plainly, and mean it.

⭐ **Say this before the URL line, once, and never as a bulleted menu.** Substitute all three brackets
from **their** `BRIEF.md` — three different lines of it, in their own words, not yours:

> That's version one — my read of your brief, not your finished idea. It's meant to change.
>
> Tell me what to do differently, in your own words. People say things like *"<their Q3 worry, in their
> phrasing> should be the first thing you see"*, *"too much here, cut it to one screen"*, or *"<their Q4
> ask, shortened> — can it show that as well?"*
>
> Wanting it different is not a sign anything went wrong. It's the part where it stops being mine.

- ⛔ **Never bullet those three examples** — a list reads as a menu with a right answer, and they are
  meant to sound like things a person said.
- ⛔ **Never ask permission to continue.** This lab runs auto-approve. *"Tell me what to change"* is an
  open door; *"would you like me to change anything?"* is a gate wearing a friendly face.
- ⛔ **Say it once.** Repeating it after every revision turns an invitation into nagging.
- **When they do come back**, append their words to the brief (`../build-demo/references/brief-template.md`
  records how) and rebuild — never re-run the four questions, and never rewrite what they first asked for.

**Stage-2 handoff, existence-gated — check the directory, do not promise from this file:**

- If `../bwgtrack2-demo-record/SKILL.md` exists, offer recording as a next step and hand over.
- If `../bwgtrack2-demo-publish/SKILL.md` exists, offer publishing and hand over.
- **If neither exists — which is the normal case today — say the honest ending instead:** the app runs
  here, in this lab, until the lab ends. ⛔ **Do not promise a repo, a video or a URL that outlives the
  session.** Tell them what they could rebuild it from, and leave it there.
