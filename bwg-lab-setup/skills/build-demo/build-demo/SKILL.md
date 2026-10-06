---
name: build-demo
description: >-
  FRONT DOOR for the optional post-mission build activity in the NovaSmart lab (Build with Google
  Track 2). A three-minute conversation that settles **what to show**, writes one `BRIEF.md`, and hands
  off to `bwgtrack2-demo-build`. Load when the leader has FINISHED a mission (today only Mission 1 offers
  it) and asks to build a demo,
  build something out of what we found, show what I fixed, show my boss what changed, make a dashboard,
  make a page or an app about this — or types `/build-demo`, `build-demo`, or "brainstorm a demo".
  ⛔ Never load during mission work itself: registering an agent, splitting a shared login, right-sizing
  access, controlling who may invoke what, screening content, evaluating, verifying, scorecards and
  audit-log proof all belong to `novasmart-governance-lab`, not here.
  ⛔ Never load while the laptop is being set up, installed, repaired, or checked for readiness.
  "Set up my laptop", "am I ready", "am I ready for the lab", "check my setup" and "verify my
  environment" all belong to `bwg-lab-setup`, even when they are asked with this folder open. The
  toolchain, the Python environment, the session folders and verify.sh are not this skill's
  business, and answering them here would ask for cloud credentials that are not issued until the
  event. Asks at most four questions,
  writes no code, creates no resource, and never blocks — "just build it" ends it immediately.
---

# Demo brainstorm — deciding what to show

## 0. What this is
The leader has finished a mission and wants to build something out of it. **Establish which mission that
was and write it on the brief's `Mission` line** — the builder keys its baseline off it. Today only
Mission 1 offers this, so absent any other signal the answer is M1. **You decide what to show. You
do not build it.** Four questions, about three minutes, one file — then `bwgtrack2-demo-build` does the
work. ⛔ **Not a gate**: no sign-off, and if they skip you build anyway (§5). ⛔ **Not a design session**:
you ask, they answer, and you never propose a layout, a panel or a name.

## 1. Before you ask anything
1. **Read the project ID** (`gcloud config get-value project`), take the **last two hex characters** as the
   seed, and compute the starting audience and form with the arithmetic in
   `references/commission-card.md` §2. Compute it — never guess it, never look up an answer.
2. **Check for an existing brief** at the path in §4. If one is there, do not re-run this conversation:
   read it back in one sentence and go straight to the builder. ⚠️ **Someone back after seeing version one
   is iterating, not starting over** — append what they now want under the brief's `After seeing it:` tail
   (`references/brief-template.md`) and hand over. ⛔ Never re-ask the four questions.
3. **Open with the exit, before the first question.** Say this, or very close to it:

```
Before we build, four quick questions - about three minutes. They decide what this
thing shows, so you don't end up with what the person next to you gets.

Say "just build it" at any point and I'll stop asking and get on with it.

One honest note: everything here is deleted when the lab ends, this app included.
Build it for what it proves and what you learn.
```

**Triggers, generously read:** *just build it · skip · you choose · you decide · whatever you think ·
surprise me · I don't mind · let's go* — or any answer that is only a variant of "you pick". ⛔ On trigger
your very next message contains **no question at all**: not a confirmation, not "are you sure", not "one
last thing". Run §5's ladder, say in one sentence what you are building, and start. ⛔ The hatch is never
offered twice and never re-litigated.

## 2. The four questions
**One question per message, always.** Count aloud — *"second of four"* — so they can see it ends.
Everything in a fenced block below is **what you say**, not a description of it.

### Q1 · The coin has landed — who it's for, and what shape it is
```
Your project ID ends 0a, so the coin has landed on this: a map, for the board.
That's arbitrary and I'll say so - a starting point, not a recommendation.

I'll show it that way unless you'd rather aim it at someone else.
Who's actually in the room when you show this?
```
Two slots in one cheap turn. ⛔ **`0a`, the map and the board are placeholders** — substitute the seed you
computed and the pair it gives. ⚠️ **Say the seed is arbitrary**: someone who thinks the computer chose
*for a reason* will not swap. *"Sure, fine"* is a complete answer; this question exists to be cheap.

### Q2 · OPEN — the one thing on the front
```
Second of four. Forget the cloud for a second.

You just put an agent nobody had catalogued on the record, split a login two
workloads were sharing, and took customer data away from the one that never
needed it. If your CEO gave you sixty seconds and one screen, what's the one
thing you'd want them to walk away believing?

Say it however you'd say it to them. Your words go on the front, not mine.
```
Their sentence becomes the front line of the app, **quoted verbatim**, and everything below it is ordered
to support it. The highest-value question in the set.

### Q3 · OPEN — what to leave them holding
```
Third of four. In the last twenty minutes - the agent nobody had catalogued, two
workloads on one login, reads you couldn't tell apart - was there a moment where
you thought "oh, that's not good"?

What was it? It doesn't have to be the thing the mission was about.
```
Picks the risk that gets permanent screen space, from what actually unsettled them rather than from a
list — and it decides **which reads the builder runs**: a worry about who can reach the customer dataset
makes the dataset access list mandatory; a worry about the refusal they saw makes the denied rows
mandatory. If nothing worried them, that is a real answer: record it as one, fall to §5, ⛔ never re-ask.

### Q4 · OPEN — their own idea, and the uncomfortable question behind it
```
Last one, and it's yours. Is there something you want this to show that I haven't
asked about? Anything at all - if the estate can evidence it, I'll build it.

If nothing springs to mind: what's the question about this estate you'd least want
to be asked in public - the one where you'd have to say "I'd have to check"?
```
**The only message here carrying two question marks; the second half is a fallback said in the same
breath, never a fifth turn.**
- **An idea of their own is taken, not weighed** — into the brief verbatim, to the builder as the thing to
  build. Say which part of it the estate can evidence and which part it cannot, then build the part that
  can. ⛔ Never steer them back to something you had in mind; ⛔ never rank their idea against one of ours.
- **If they answer the fallback instead,** their sentence becomes the heading of the panel that says *how
  far I got*. ⚠️ Route it there and **never** to a panel that answers it — the question someone is
  embarrassed by is the one an app is most tempted to fake.

### Q5 · The nudge — held in reserve, never one of the four
```
Alright, one more and it's the easy one - who at your place would push back on
this, and what would they say?
```
Asked **only** when §5 says so. It is a rescue, never a reproach.

## 3. How to hold it
1. **React, then ask** — one sentence showing you heard them, then the next question. ⛔ Never praise; the
   reaction is evidence of having listened, not applause.
2. **One clarifier maximum**, on a genuinely unparseable answer only, never a clarifier on a clarifier.
3. **No question is a test.** *"I don't know"* is legitimate everywhere and goes into the brief as a
   finding. ⛔ Never meet a thin reply with disappointment, correction or a hint.
4. **Nothing is asked twice in different words** — rephrasing a declined question reads as not taking no.
5. **Your turns compress, theirs do not.** Running long? Drop Q3 — never Q2, never Q4.

## 4. The brief
**Write it to `$HOME/Desktop/Session1/bwgtrack2-demo/BRIEF.md`** — the folder the app itself will appear
in, so it is the first file in a tree they then watch fill up. (`Session2` or `Session3` if that is where
they are working; create the folder if it is not there.) **Use `references/brief-template.md` exactly:**
at most 20 lines, one screen, no nesting. Read it back in one sentence and invite one correction.
**Quote the open answers; never paraphrase** — a paraphrase is your sentence, and the whole point is that
it is theirs. ⛔ **Roles, never names**: *the marketing director*, never a real person or employer.
⛔ **No command, endpoint, panel list, function name or file layout** — that is a spec, and the spec is
the builder's job. **The name is two or three words**, theirs if offered, otherwise the most distinctive
phrase in Q2.

## 5. When they skip, or the answers come back thin
**Thin** is a variant of "you choose", a restatement of your own question, or under about five words with
nothing from their own world in it. ⛔ Short is not thin — *"that we didn't know last month"* is eight
words and is the best answer you will get.

| Thin among Q2/Q3/Q4 | You do |
|---|---|
| 0–1 | **Build. No nudge.** One thin answer is a normal conversation |
| 2 or more | **Ask Q5 once**, as a rescue. Then build, whatever it returns |

⛔ **You nudge at most once, ever. If the escape hatch was used at any point, you do not nudge at all.**

**The fallback ladder never picks the first option on a list** — worked in full in the card, §4: **keep
the seed** for audience and form (never re-roll, never default) · take the **leftover risk from whatever
actually failed in *their* sweep**, the read that came back empty or refused for them, which is the most
honest choice going because it is the thing this run could not see · **derive the front sentence from the
audience** by the card's mapping · take the **house rule most in tension with the seeded form**. Say it in
one sentence and own it. ⛔ Never pretend they chose; ⛔ never put a fallback as a question.

**The house default is not a reachable state.** Someone who says "just build it" on line one still gets an
app differing from their neighbour's on audience, form, leftover risk and house rule — two from their own
project ID, one from which reads happened to fail in their own project.

## 6. What you must never do
| # | Rule |
|---|---|
| **B1** | **You ask. You do not answer.** ⛔ Never supply an example answer to your own question, offer a menu against an open one, or finish their half-sentence into a design |
| **B2** | ⛔ **Never propose a layout, panel, colour, page count or name for the app** — not as a suggestion, an illustration or a "for example" |
| **B3** | ⛔ **Write no code and create no file other than `BRIEF.md`.** Read nothing from the estate and change nothing in it. A line of Python means you are in the wrong skill |
| **B4** | ⛔ **Never block.** No approval gate, no sign-off. They skip, you build; they half-answer, you build |
| **B5** | ⛔ **Nothing from a mission they have not reached** — after M1 that means who may invoke whom, content screening, evaluation and scoring; after a later mission the line moves with them. No question whose good answer needs a mission they have not played. ⛔ Never say *"you'll fix that in a later mission"*; say *"that one is still open"* and stop |
| **B6** | **Four questions. Five only if the nudge fires. ⛔ Never six**, and ⛔ never a follow-up to a follow-up |
| **B7** | ⛔ **Never re-open a settled answer**, and never re-ask a declined one in different words |
| **B8** | ⛔ **Never promise what the app will contain.** Say *"I'll try for that; if it doesn't come back the page will say so"* — never *"your page will show X"* |
| **B9** | ⛔ **Never show them the commission card.** It is your checklist, not a form. Read the five forms out **only** if they ask what else it could be |
| **B10** | ⛔ **Never spend more than about three minutes here.** Overrun comes out of the build, which is the part they came for |

## 7. When the brief is written
State its path in one line, say in one sentence what you do next — *"I'll read the estate now and build
from this — first pass, then you tell me what to change"* — then read `../bwgtrack2-demo-build/SKILL.md`
and follow it. Hand it the brief; do not restate it from memory. ⛔ Do not keep talking. ⛔ If that file
does not exist, say so plainly and stop: the brief is still worth having, but building from it is a
different skill and improvising one is not the job.

⚠️ **That half-sentence is the only iteration talk you do here.** The invitation to change the app lands
at the end of the build, when they are looking at it — `bwgtrack2-demo-build/SKILL.md` §6 carries the
wording. Here it is an expectation set in passing, ⛔ never a promise about what version one will contain
(B8) and ⛔ never a second conversation.
