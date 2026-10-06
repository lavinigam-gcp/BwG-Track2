# `build-demo` — the optional post-M1 demo suite

A **catalog directory**, not a skill. It holds the sub-skills for the off-script activity a leader can
choose *after* Mission 1: turn what they just proved about their agent estate into something they can
show. The activity is **optional**, **never graded**, **read-only on the estate**, and it is offered
**only once M1 is finished** — never mid-step. The mission skill's section 5 router points at the
front door and nothing else.

## ⛔ NEVER put a `SKILL.md` at this level

**There must be no `build-demo/SKILL.md`, now or ever.** A `SKILL.md` at the shallower level
**shadows every sub-skill below it** — the enumerator stops at the first one it finds, so all four
sub-skills go invisible while the directory still looks perfect on disk. Nothing else in the system
reports this. Gate **G11a** in `.lavi-working/cutest_02_08/tools/check_skill_contract.py` is the only
thing that catches it.

If you are here to "tidy up" by adding a wrapper skill: that layout was considered and rejected. Add a
sub-skill directory instead.

## Sub-skills

Stage 1 — ships first and is complete on its own:

- **`build-demo/`** — the **front door**. The conversation that produces `BRIEF.md`. No code.
- **`bwgtrack2-demo-build/`** — implements the brief as one stdlib Python app on a free port in `8901-8940`, grounded
  in real reads. Carries `vendor/` (third-party design rules, MIT; see `vendor/NOTICE.md` for attribution).

Stage 2 — offered afterwards, only to a learner happy with their app:

- **`bwgtrack2-demo-record/`** — a short clip of the running app, written into the tree before any push.
- **`bwgtrack2-demo-publish/`** — `gh` device flow, content secret-scan, repo + topic. The only thing that
  survives lab teardown.

Both stage-2 names are already declared in `terraform/scripts/startup.sh`, so shipping them later is a
directory drop plus a zip rebuild — **no shell edit**. Their absence today is a silent skip, by design.

## This file is not installed

`startup.sh` flattens the suite by copying **named sub-skill directories only**. This README rides the
zip onto the VM but is never copied into any session's `.agents/skills/`, so a learner never sees it.
The same is true of anything else left at this level. Write for the next author, not the learner.

## Adding a demo for another mission

The baseline is **per mission**, in `bwgtrack2-demo-build/SKILL.md` §1. Today only **M1** has a real
one; M0, M2, M3 and M5 carry rows reading NOT YET DEFINED, and gate **G18** fails if a mission has no
row at all — a row is required, a filled row is not.

To add one, three edits and nothing else:

1. Fill that mission's row in §1 with the proof that mission unlocks, and add its own pair of spine
   elements alongside §1b's. §1a's three (a stated limit, provenance on every figure, no verdicts) are
   universal and never change.
2. Drop the NOT YET DEFINED marker from that mission's section in `references/gallery.md`.
3. Add the `/build-demo` invitation to that mission's optional section in `lab_material`, the way M1
   does — which needs an HTML rebuild.

The rest of the suite is already mission-agnostic: the brainstorm conversation, the grounding rules,
the port scheme, the variation mechanism and the file layout do not know which mission they came from.
The brief's `Mission` line is what the builder keys off.
