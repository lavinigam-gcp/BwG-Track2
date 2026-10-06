# Build and ground it honestly — the contract

Rules, not advice. Every one is checkable, and every one traces to something this estate already gets
wrong. Read this **before** you write a line of the page.

## 1. Why this matters more here than anywhere else in the lab

**This estate already ships two surfaces that manufacture success.**

1. **The store portal invents an answer.** When the real backend reply is empty or under eighty
   characters, the web tier fabricates a complete, confident personalization answer — including the
   sentence *"Successfully queried `customer_data.customers`"* and the shared login's own name. A blocked
   call renders there as a success.
2. **The provisioned monitoring dashboard defaults to a pass.** Its SQL substitutes a hard-coded identity
   into rows that name nobody, invents a query string that was never run, and its classification branch
   **defaults to `SANITIZED & PASSED`** for events the screening service never touched — while naming a
   template that does not exist in this project.

**A learner-built app is the third one unless you stop it — and it is the most dangerous of the three,
because the learner will believe it.** They wrote it. It is about their own estate. Their name is on it.

Everything below exists so that the app they walk away with is the one thing in this project that does
not lie to them.

## 2. The honesty contract — seven rules, all imperative

| # | Rule |
| :-- | :-- |
| **H1** | **Every figure on the page came from a command run in this session.** ⛔ No value carried over from a reference file, an earlier answer, a config, or your own memory. A row count is quoted only if the command returned it **this run** |
| **H2** | **Every panel prints the command and the UTC time it ran**, verbatim, beside the value. No exceptions, no "obvious" panels, no header-level stamp standing in for a per-panel one |
| **H3** | **Anything unread renders as the literal words `not read`** — never blank, never `0`, never `—`, never a plausible substitute. ⛔ **Never substitute a default for an empty field.** An empty field renders empty or `unknown` |
| **H4** | **No verdicts, ticks, scores, badges or grades the platform did not itself emit.** ⛔ No pass/fail branch that defaults to a verdict — a default branch renders `not classified`. ⛔ No verdict inferred by string-matching log text |
| **H5** | **A refusal is the platform's own words, with the gate named.** Quote the permission and the resource beside the status, so the page says *which gate fired* rather than "blocked". ⛔ Never a green BLOCKED badge |
| **H6** | **An empty result is rendered as empty, with the window stated.** *"No rows in the last 60 minutes"* — never *"no reads happened"*, never *"clean"*. Silence is not evidence, these rows lag minutes, and the page says it is waiting |
| **H7** | **Every page carries a non-empty "Still open" band** — the leftover risk from the brief, permanently on screen, not a footnote and not behind a toggle. ⛔ **An empty or omitted band is a build failure**, not a tidy page |

**Two rules that decide what "still open" must say.** The band states the boundary of the claim as well
as the risk: this shows reads **in the window queried**, by principals that appear in **this** log, and
it says nothing about what one agent can ask another to do.

## 3. The fences — targets, not motives

Each of these names a **target**, because a fence worded by intent has already been satisfied in this lab
by finding a different route to the same place.

### 3.1 Read-only

- **The app reads. It never changes a cloud resource.** No IAM edit, no patch, no delete, no re-point, no
  deploy, no API enablement, no service account created.
- **The only writes are the two triggers**, and both are ordinary agent calls the lab already makes.
- **The identity check is the proof, and it is cheap:** the filtered IAM read on `antigravity-sa` before
  and after the build must be **identical**. ⛔ **Never self-grant a role** to make a panel work. A panel
  that needs a new permission is a panel that says `not read`.

### 3.2 No customer rows

- **The shape is fine: the table name, the column names, the row count, and which columns a logged read
  touched.** Column names come out of the audit entry and carry no values — that is why they are safe.
- ⛔ **A value is never fine.** No name, no email, no lifetime value, no customer ID, no row.
- **The clean route is already blocked**: this identity has `tables.get` but **not** `tables.getData`.
  Say that on the page. It is the control working, and it is the best line in the activity.
- ⛔ **The four side doors are never called, for any reason:** the seed SQL file in the bucket, the
  portal's customer API, the unauthenticated tool server that falls back to owner-level credentials, and
  the promo agent's `/query` and `/run-campaign` **bodies**.
- **If the brief's headline question cannot be answered without a customer value, the question changes —
  the app does not.** State the reason plainly: this identity cannot read those rows by design.

### 3.3 No credential, anywhere

- ⛔ **No token in the page, in the JavaScript, in the HTML, in `evidence/`, or in any file the page
  loads.** A page with a bearer token baked into it is a credential in a file, in a security lab.
- ⛔ **Never read the service-account key that sits in the seed bucket.** Not to inspect it, not to
  demonstrate it, not to prove it is there. Its existence is a finding; its contents are never yours.
- **The app authenticates by shelling out and inheriting ambient credentials.** It creates no key and
  writes no key file. The page's only credential is that the browser is talking to its own origin.
- **Write nothing you would have to scan for later.** ⛔ Never write into `app.py` or `evidence/`: a token
  string, a private key block, a lab account address, or a customer email. This is cheaper than a scan
  and it means there is nothing to rescue if this ever travels anywhere.

### 3.4 Never touch `test-agent-caller`

⛔ **Do not use, re-point, tidy, re-grant or delete it.** Do not include it in a "clean this up" panel.
Doing exactly this in a real run destroyed a later mission's before-state for the whole project. **List
it if a read returns it; act on it never.**

### 3.5 Never build on the store portal

Its chat endpoint, its buttons, its APIs — all banned as a trigger and as a source. It fabricates a
confident answer when the real reply is empty, and it runs as an owner-privileged identity, so anything
it does proves nothing about the agent. Full reasoning: `data-palette.md` §4.3.

### 3.6 This file beats the vendored design rules

If `vendor/` ships alongside this skill, its guidance governs **how the page looks** and nothing else.
**Where it and this file disagree, this file wins — every case, not just hard ones, and without asking.**
Two collisions are already known and recorded in `vendor/OVERRIDES.md`: the vendored interaction states
carry a tick and a warning glyph (banned here — a tick is a verdict), and the vendored remedy for a
missing figure is a dash or a grey block (banned here — the literal words `not read`, because a dash is
ambiguous and a grey block is a thing readers learn to skip).

⛔ **Never edit a file under `vendor/` to make it agree.** Record the divergence; leave the copy
verifiable against its upstream commit.

## 4. Grounding — how a figure gets onto the page

**One path, and only one.** A panel's value is produced by a command the app itself ran, in this session,
whose exact `argv` and UTC timestamp travel with the value from the moment it is captured.

- **Capture the command, the UTC time and the exit status at the point of the call** — not later, and
  never re-typed from what you meant to run. Retyping the command with the flag you intended is a
  fabrication even when the finding is right.
- **A read that failed is captured as its own error**, in the words the system used, and rendered that
  way. *The command errored* and *the command found nothing* are different findings, and only one of them
  is about the estate.
- **Write `evidence/` before the app exists**, one file per read. Then every failure downstream still
  leaves something real, and the page is assembling records rather than inventing them.
- **The trigger's UTC send time is recorded before the response is read**, so a slow stream cannot quietly
  become the wrong timestamp.

## 5. The starter, and diverging from it

`assets/starter_app.py` is the skeleton, not the answer. Copy it, run it once to see it work, then make
it the learner's: their panels, their ordering, their words, their failure text.

⛔ **The starter with a different project ID in it is not a build.** If you can describe the finished app
without mentioning anything in the brief, start again.

⚠️ **Keep the honesty machinery when you cut.** The command-and-timestamp capture, the `not read` state
and the "Still open" band are the parts that make it worth showing. Cut a panel instead.

## 6. The layout contract — the form is decided here, never asked about

§2 governs what the page may **claim**. This governs how it is **set**. It is the short, enforceable form
of the vendored guidance in `vendor/design-rules/`: read those files at step 4 of the build loop, and read
this section again while you are writing the CSS.

⚠️ **Never ask the learner what the page should look like.** The brief already settled who it is for, what
sentence is on the front and what stays permanently on screen. Every remaining decision is yours, and it is
taken from the rules below. Asking about taste hands the design back to somebody who came to see their own
estate, not to art-direct an assistant. (`vendor/OVERRIDES.md` O10 records this as a deliberate override of
the vendored instruction to ask.)

**The page this exists to prevent.** A real run produced a near-black background, monospace type in every
heading, an emoji on every heading, three cramped cards side by side, bright chips reading `PASS` and
`REFUSED 403`, and service-account addresses running the full width of the screen. The reader's verdict was
*"not really good looking and very confusing… not sure how to think or interpret that."* Every rule below is
one of the decisions that page got wrong.

### 6.1 The tokens — paste this block, then use nothing that is not in it

Hex first so an old engine renders, `oklch()` second so a modern one renders the intended colour
(`vendor/OVERRIDES.md` O3). Every colour and every face on the page comes through one of these names; a
literal colour or font stack anywhere else in the stylesheet is a build failure
(`vendor/design-rules/slop-test.md` gate 48).

```css
:root {
  /* Faces. System stacks only - no webfont, no @import, no remote src. */
  --prose: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --mono:  ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;

  /* Type scale, ratio 1.25 from a 16px base. Five sizes, no sixth. */
  --t-note: 0.8rem;    /* 12.8px - the command line and the UTC line only */
  --t-body: 1rem;      /* 16px   - the floor for anything a person reads as prose */
  --t-panel: 1.25rem;  /* 20px   - a panel heading */
  --t-band: 1.5625rem; /* 25px   - a band heading */
  --t-page: 1.9531rem; /* 31.25px - the page title, and nothing else */

  /* Spacing, 4pt base. Gaps come from here; a raw px value is a tell. */
  --s-xs: 0.5rem; --s-sm: 0.75rem; --s-md: 1rem;
  --s-lg: 1.5rem; --s-xl: 2.5rem; --s-2xl: 4rem;

  /* Ink on warm light paper. No pure black, no pure white, every neutral
     tinted toward the anchor hue. No green token and no red token exist. */
  --paper:  #F6F4EF; --paper:  oklch(97% 0.007 89);
  --panel:  #FCFAF5; --panel:  oklch(99% 0.007 89);
  --rule:   #DFDACF; --rule:   oklch(89% 0.016 86);
  --muted:  #6B665D; --muted:  oklch(51% 0.015 82);
  --ink:    #232019; --ink:    oklch(24% 0.014 88);
  --accent: #8A5A2B; --accent: oklch(51% 0.089 63);  /* focus ring and link rule only */

  --measure: 68ch;   /* prose */
  --column:  52rem;  /* the page's single column */
}
```

Measured on this palette: ink on paper **14.8:1**, muted on paper **5.2:1**, accent on paper **5.3:1** —
all clear of the 4.5:1 body floor and the 3:1 focus-ring floor in `vendor/design-rules/color.md`. Change the
anchor hue if you want a different mood; if you change a lightness, re-check the ratio before you ship it.

### 6.2 The twelve rules

| # | Rule | It fails if |
| :-- | :-- | :-- |
| **L1** | **Light paper by default.** `--paper` is the page background. A dark page is built only when the brief asks for one **in words**, and then every surface under 50% lightness sets its own light `color` in the same rule | The background is near-black, or a dark surface inherits dark ink (`color.md` dark-mode recipe; `slop-test.md` gate 41) |
| **L2** | **Two faces, and monospace is not the prose one.** `--prose` sets `body` and every heading. `--mono` is permitted on exactly four things: the command block, a resource path / principal / service-account address / dataset or table id, a UTC timestamp, and an error string quoted from the platform | `monospace` appears on `body`, `h1`–`h3`, a button or a panel title. A monospace-everywhere page is the terminal aesthetic, which `typography.md` allows only when the terminal **is** the design — and the reader here is a senior IT leader |
| **L3** | **Five type sizes, one ratio, and a floor.** Use the five tokens and no sixth. Prose never below `--t-body`; nothing on the page below `--t-note`. Line-height 1.5–1.6 on prose, 1.15–1.25 on headings | A sixth size appears, or prose renders below 16px (`typography.md` § Scale, § Body text rules) |
| **L4** | **One column, and it has a stated width.** `--column` (52rem) caps the page; prose blocks additionally cap at `--measure` (68ch). Gutter of at least `--s-md` at every viewport | Any block runs the full width of a wide screen, or a prose measure lands outside 45–75ch (`slop-test.md` gate 25) |
| **L5** | **Panels stack.** One panel per row is the default. If two genuinely belong side by side, use `repeat(auto-fit, minmax(22rem, 1fr))` so they collapse on a narrow screen | Three fixed equal columns of cards appear — the single most recognised generated-page shape (`anti-patterns.md` § The 3-column feature grid; `slop-test.md` gate 3) |
| **L6** | **Spacing comes from the scale, and it varies.** Panel padding `--s-lg`, gap between panels `--s-lg`, space above a band `--s-xl`, page margin `--s-xl` top | A raw value like `padding: 17px` appears, or every gap on the page is the same number (`layout-and-space.md` § The spacing scale; `slop-test.md` gate 24) |
| **L7** | **One accent, on the focus ring and the link rule, nowhere else.** It covers 3% of the viewport or less | The accent fills a surface, **or any green or red appears at all** — there is no green token and no red token, by name or by value. That is stricter than the vendored rule and it is deliberate (`OVERRIDES.md` O4) |
| **L8** | **A long identifier wraps or truncates; it never runs the width.** Every element that can hold a path, a principal, a service-account address or a command carries `overflow-wrap: anywhere; word-break: break-word; min-width: 0`. The command block is a `<pre>` with `white-space: pre-wrap`. `html` and `body` carry `overflow-x: clip`. An identifier quoted mid-sentence is shortened to its last segment, with the full value on its own line in the evidence block beneath | A horizontal scrollbar appears at any width from 320px to 1920px, or one identifier sets the width of the page (`slop-test.md` gates 34, 50, 51) |
| **L9** | **Headings are roman, sentence case, and carry no glyph.** No emoji anywhere on the page — not in a heading, not as an icon, not as a bullet. No italic heading | An emoji or a glyph stands in for an icon (`anti-patterns.md` § Generic emoji as feature icon; `slop-test.md` gates 30, 38a, 45) |
| **L10** | **Depth is weight and rule, not shadow.** One hairline `1px solid var(--rule)` per panel. No shadow. No bordered box inside a bordered box | A card sits inside a card, or a shadow is stacked (`layout-and-space.md` § Depth; `slop-test.md` gate 4) |
| **L11** | **Do not redraw chrome the reader already has.** No fake terminal, no `$` prompt, no window dots, no browser bar, no IDE frame. A command is a `<pre>` under a worded label | Any of them is hand-built in HTML or CSS (`anti-patterns.md` § Re-drawn UI chrome; `slop-test.md` gate 47) |
| **L12** | **Every control has four states and an instant focus ring.** `:hover`, `:focus-visible`, `:active`, `:disabled`; `outline: 2px solid var(--accent); outline-offset: 2px`, never transitioned. Control labels do not wrap to two lines | A control has hover only, the ring fades in, or a button label wraps (`slop-test.md` gates 15, 26, 49) |

### 6.3 The three checks that settle it

Run these on the page **as served**, not on the source you meant to write.

1. **Squint at it from two metres.** You should see a light page, one column, a title, and a stack of
   panels with headings in a proportional face. If you see a dark terminal, L1 or L2 failed.
2. **Drag the window from 1920px down to 320px.** No horizontal scrollbar, no identifier setting the
   width, no control on two lines. If a scrollbar appears, L8 failed.
3. **Grep the stylesheet for a colour or a font stack that is not in the `:root` block.** One hit is a
   build failure — lift it into a token or delete it.

## 7. Gamified is a form. It is not a licence to emit a verdict.

A learner may ask for the demo to be a game, and that ask **wins** — it arrives through the brief's own
"your own ask" line, which trumps every seeded slot. Build the game. The line to hold is narrow and it is
not about tone:

> **The learner chooses the game. The platform still writes the result — and it wrote none, so the page
> shows none.**

### 7.1 What a gamified page may do

| # | Allowed | Why it stays honest |
| :-- | :-- | :-- |
| **P1** | **Levels, rounds, stages, chapters** as the page's structure, numbered and ordered | A heading is a place, not a claim. *"Level 3 — which login each workload signs in as"* still names what was read |
| **P2** | **Progression the reader moves through** — a next control, a reveal in order, a "you are here" marker | Sequence is layout. It says nothing about the estate |
| **P3** | **Playful headings and playful control labels** — *"Make a noise the log will hear"* on the trigger button | The wording is free; what the button does is a real call, and the panel beneath still prints the command and the UTC time |
| **P4** | **A count of the page's own work** — *"4 of 7 panels have run"*, *"3 panels came back `not read`"* | It counts this page's reads, not the estate's condition |
| **P5** | **Counts the platform emitted** — principals seen, columns touched, rows in the window | These are readings with a command beside them, not scores. They are never summed into a total and never compared with a target |

### 7.2 What it may never do

| # | Banned | Why |
| :-- | :-- | :-- |
| **P6** | **A chip, pill, badge or tag whose word or colour states an outcome** — `PASS`, `FAIL`, `OK`, `SECURE`, `BLOCKED`, `REFUSED 403` | This is H4 and H5 with a rounded corner on it. A refusal is quoted as the platform's own sentence with the gate named, inside the evidence block |
| **P7** | **Points, XP, stars, streaks, medals, trophies, ranks, percentages, totals** | Every one is a number the platform did not emit — a fabricated metric (`slop-test.md` gate 46) |
| **P8** | **Green and red** — as a level state, a lane, a chip, a border, anything | L7. There is no green token and no red token |
| **P9** | **A level that can be completed, cleared, passed or won**, and any losing condition, judging timer or "you scored X of Y" | Completion is a verdict on the estate wearing a game's clothes. A level that ends says what it read and what it could not |
| **P10** | **A band the game can hide.** The "Still open" content shows on every level, or once in a place no level can cover | H7 does not have a level 5 exemption |

### 7.3 The four tests, so this is not a matter of taste

1. **The chip test.** In the served HTML, find every element whose entire visible text is 16 characters or
   fewer **and** which carries a background fill, a border, a border-radius, or a colour other than
   `--ink` or `--muted`. Subtract the controls the reader can activate (`button`, `a`). **The count must be
   zero.** A verdict needs a container to live in; deny it the container.
2. **The word test.** No heading, label, tag, chip or button whose text **is** an outcome word, or an
   outcome word plus a code: pass, passed, fail, failed, success, secure, protected, compliant, safe,
   clean, blocked, denied, win, won, lost, complete, cleared, score. Those words are permitted in exactly
   one place — inside the evidence block, as the platform's own string, beside the command that produced it.
3. **The colour test.** Grep the served page and the stylesheet for `green`, `red`, `lime`, `crimson`,
   `#0f0`, `#00ff00`, `#008000`, `#f00`, `#ff0000`. Zero hits.
4. **The noun-swap test.** Take every progress or tally line and replace its noun with the word *panels*.
   *"4 of 7 panels have run"* survives — it was always about the page. *"4 of 7 controls in place"* does
   not survive, because it was a verdict on the estate. **If the swap changes the meaning, delete the line.**

## 8. Self-check before you hand anything back

Run this over the app file **and** over the page as served. Report the result; do not narrate the check.

| # | Check | Fails if |
| :-- | :-- | :-- |
| 1 | Every panel shows a command and a UTC time | Any panel does not |
| 2 | At least one panel says the literal words `not read` | None does, and every read happened to succeed — then say so explicitly and name what was not attempted |
| 3 | The "Still open" band exists and is non-empty | It is empty, absent, or behind a toggle |
| 4 | No tick, cross, score, percentage, grade, badge or the word `PASSED` anywhere on the page | Any is present |
| 5 | No customer value anywhere in the app file, the page, or `evidence/` | Any is present |
| 6 | No token, key or lab account address anywhere in the app file, the page, or `evidence/` | Any is present |
| 7 | No default-substituted value: every empty field renders empty, `unknown` or `not read` | Any empty field renders as something plausible |
| 8 | The trigger's recorded UTC time is on the page, and the audit rows are shown with their own timestamps | The page prints a count of triggered reads instead |
| 9 | The filtered IAM read on this app's own identity is unchanged from before the build | It changed |
| 10 | The page is light, single-column, and set in a proportional face, with monospace only on commands, identifiers, timestamps and quoted errors | §6 L1, L2 or L4 fails when you squint at it from two metres |
| 11 | No horizontal scrollbar between 320px and 1920px, and no identifier sets the width of the page | §6 L8 fails on the width drag |
| 12 | Every colour and every font stack in the stylesheet comes from the `:root` token block, and no green or red appears anywhere | Any literal value survives outside the block, or the colour test finds a hit |
| 13 | The chip test returns zero, and every outcome word on the page sits inside an evidence block beside its command | §7·3 test 1 or test 2 finds one. This row applies whether or not the page is a game |

⛔ **A confident sentence with nothing above it is the failure, and rewriting the sentence does not fix
it.** If a check did not run, its row says `not verified` and names the command that would settle it.
