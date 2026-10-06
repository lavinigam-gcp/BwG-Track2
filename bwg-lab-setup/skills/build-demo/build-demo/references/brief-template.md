# `BRIEF.md` — the template, and the rules about it

**Path: `$HOME/Desktop/Session1/bwgtrack2-demo/BRIEF.md`** (`Session2` / `Session3` if that is where the
learner is working). Create the folder if it is not there. It is the same folder the app appears in, so
the brief is the first file in a tree the learner then watches fill up — in **their own words**.

⛔ Not `/tmp` (invisible, and the missions already use it as scratch). ⛔ Not the skill directory —
learner-owned output never goes inside a skill.

**Hard constraint: at most 20 lines, one screen, no nesting.** They read it back in one glance and correct
it in one sentence. Anything longer is a spec, and a spec is the builder's job, not yours.

---

## The template — copy the shape, fill every angle bracket

```markdown
# Demo brief — <two or three words>
<UTC timestamp> · project <PROJECT_ID> · seed `<xx>`
Mission     <M0|M1|M2|M3|M5>   <the mission they just finished>

Audience    <A>          <(from seed) | (swapped off seed: <original>)>
Form        <B>          <(from seed) | (swapped off seed: <original>)>
House rule  <E>

On the front, in your words:
  "<Q2 verbatim>"

What worried you:
  <Q3 verbatim>
  -> permanent place on the page

Your own ask:
  "<Q4 verbatim>"
  -> <what the estate can evidence of it | this is what the "could not attribute" panel answers>

Fixed, not yours to change: <the baseline for this Mission, copied from
bwgtrack2-demo-build/SKILL.md §1 — for M1: cause a real read · name the workload from the
audit log · say what could not be attributed>.

Tell me to change anything above. I build from this file.
```

## Filled example — what a good one looks like

```markdown
# Demo brief — Last Month
2026-08-19 14:22 UTC · project qwiklabs-gcp-02-6b4c9e8d0a · seed `0a`

Audience    the board (their CFO specifically)   (from seed)
Form        a map                                (from seed)
House rule  readable aloud in 60 seconds

On the front, in your words:
  "We know which of our systems touched customer data - and we didn't know that last month."

What worried you:
  The dataset access list had five entries and nobody had ever looked at it.
  -> permanent place on the page

Your own ask:
  "How many things can read that customer table that we've never listed?"
  -> this is what the "could not attribute" panel answers, and where it stops

Fixed, not yours to change: <the baseline for this Mission, copied from
bwgtrack2-demo-build/SKILL.md §1 — for M1: cause a real read · name the workload from the
audit log · say what could not be attributed>.

Tell me to change anything above. I build from this file.
```

## After version one — recording a change of direction

Version one is a first pass and the learner is told so at the end of the build. When they come back
wanting it different, **the brief grows; it is never rewritten.** Add this at the bottom, under whatever
`local-run.md` already appended:

```markdown
After seeing it:
  <UTC timestamp>  "<what they want changed, verbatim>"
```

- ⛔ **Append, never edit.** The lines above are what they asked for *before* they had seen anything, and
  keeping both halves is the whole point — one line per change of direction, newest at the bottom.
- **The 20-line cap is on the brief as first written**, not on this tail. A brief carrying three change
  lines is a brief that did its job.

## Four rules on the content
- **The open answers are quoted, not summarised.** Their sentence, their grammar, their dash. A
  paraphrase is your sentence, and the entire mechanism is that it is theirs.
- ⛔ **No real personal names and no real employer names.** Record the **role** — *the marketing
  director*, never a colleague's name. If they put a name in the app text themselves, say once that it
  may be published, then do what they say.
- ⛔ **No command, endpoint, panel list, function name, file layout or API.** That is the line between a
  brief and a spec: if the builder could be replaced by pasting this file, you over-wrote it.
- **A thin answer is written down as one, honestly** — *"they could not name a moment, and that is itself
  the finding"* — never dressed up, never left blank, never quietly filled with a house default.

**The name is two or three words.** Theirs if they offer one; otherwise take the most distinctive phrase
from their Q2 answer — *Last Month*, *Nothing Switched Off*.
