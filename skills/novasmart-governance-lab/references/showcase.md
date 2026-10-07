# Show step — a module's recorded work, turned into a page people want to look at

> Read this file **and the module's recipe file** — `showcase-m0.md` for **M0 Step 7 · Show what you
> found**, `showcase-m1.md` for **M1 Step 7 · Show what you changed**, `showcase-m2.md` for **M2 Step 7 ·
> Show what you controlled**, `showcase-m3.md` for **M3 Step 7 · Show what you screened**, `showcase-m4.md`
> for **M4 Step 5 · Show what you measured** (read "Step 7" below as Step 5 there) — at every Show prompt,
> before you build. `../SKILL.md` and the module's `mN.md` still apply; this file replaces the answer blocks
> with the short shape in §7. Below, `N` is the module number and "the recorded steps" are M0 Steps 1–4,
> M1-M3 Steps 1–5, or M4 Steps 1–4.
>
> ⛔ **Nothing in the estate changes, and no estate command runs** — no `gcloud`, `curl` or `bq`. Every
> page is built from what the recorded steps already wrote down.

## 1. The prompts

Each module offers five demos, typed in any order, each one building **one page**. The recipe file lists
them: the prompt, the file name, what the page must show, how the viewer uses it, and when it is done.
Match a prompt to its recipe by meaning ("dashboard", "investigation board", "game", "briefing",
"poster", "map", "replay", "proof", "update"), never by exact wording.

**Anything else** — a poster in M1, a comic, a one-pager, a quiz, or the older infographic, presentation,
storybook and game prompts — is built to the same bar from the closest recipe's facts. Name the file after
the format (`mN_comic.html`) and add *"because you asked for a comic"* to the answer's first line. **A
picture is always an HTML page rendered to PNG:** name it `mN_<format>_poster.html` or `mN_poster.html` and
the check renders it (§5); never `generate_image`.

## 2. The workflow — every Show prompt, in this order

1. **Read** this file and the module's recipe file, whole, with `view_file`.
2. **Facts and recipe.** Run the fact-sheet script with **the demo you are building** — its letter in the
   recipe file (`A`–`E`) or its file name (`m0_dashboard`) — then read the sheet it names, whole, with
   `view_file` (the script says how if it is too long for one read):

   ```bash
   python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/show_facts.py N A
   ```

   It copies the latest entry of each recorded step file into one sheet, with each line's number in its
   file, lists the values no page may contain, and **prints that demo's recipe — its Must show and Done
   when — at the end of its output.** Run it at every Show prompt: it is the re-read of both. For a format
   with no recipe of its own (§1), pass the closest demo's letter.
3. **Plan** against the recipe's *Must show* list. Find each item in the sheet. An item the sheet does not
   hold is left out, or drawn as *not run yet* (§3) — never filled in.
4. **Write the page** with `write_to_file`, in one go: the data block first (§4), then the layout, then
   the script. Never through `python3 -c` or a shell heredoc: quoting breaks on pages this size. **Never
   open, copy or edit a page already in the folder** (an earlier run's page is not a source): build from
   this turn's fact sheet only.
5. **Check and look** (§5): run `show_check.py`, fix every `FIX:` line, then open the screenshots and
   compare them with the recipe's *Done when* list. Fix what you see, run the check again, look again.
6. **Record and answer:** run `show_record.py` for the evidence entry (§6), then the short answer (§7).

## 3. Source — the fact sheet, and nothing else

- **Every name, count, time and status on the page is copied from the fact sheet.** For a detail the sheet
  lacks, `grep` the step file for it (pass the grep to `show_record.py`, §6). Figure parity (`../SKILL.md` §3g) applies to the
  page: count from the sheet's lines, never from memory or from an earlier answer's wording.
- **A step marked `NO FILE: not run yet`** is drawn as *not run yet*, and the answer says which. If no
  recorded step has a file, build nothing and say which step comes first. This is how the step gate holds
  here: a page can only show what the leader has already been shown.
- **Change records become plain words** (`Change:`, `Resource:`, `When:`). An undo command is never on a
  page: show *"undo on record"* against each change that has one.
- **Customer records never appear** — no name, email or customer ID. A read is described by its columns.
- **The leader's own words** from this session may be quoted as theirs. Nothing from the module's spoiler
  fence, from memory, or from another module.

**What any page may say**
- **Short names, glossed** in the `../SKILL.md` §3a wording: *`novasmart-customer-sa`, the shared login (a
  service account — a login for a program rather than a person)*. An agent's own identity is *"the Price
  Match agent's own badge"*, never its identifier. No role names: say what the access lets you do (*read
  the customer data*, *change or delete every table in the project*).
- **Product names as `../SKILL.md` §3a gives them:** *Agent Runtime*, never "reasoning engine", "Agent
  Engine", "Vertex AI" or "managed agent runtime" (the check flags them).
- **No recommendation, plan, owner or deadline of your own.** The next module is described only as the
  Instructions tab already describes it at this module's What's next step.
- **No verdict on the estate** — no "secure", "compliant", "healthy", "fully governed", "critical"
  (or "critically"), "violates", "in production", "all clear" — on the page, in its speaker notes or in
  its script, unless a recorded check says exactly that, and then it is quoted as the check's. The check
  flags each one the fact sheet does not hold.
- **Quoted wording stays word for word.** Where the recipe file quotes the module's own words (the
  next-module sentence, the leader's decision questions), copy them exactly: no paraphrase, and no
  "least privilege", "remediate" or owner of your own added to them.
- **A quoted log line or error stays exactly as recorded.** Never reword one to get past the check: keep
  it (API identifiers like `reasoningEngines.query` are allowed) or drop the quote.
- **Every `from` cites what the fact sheet shows:** a step file and `L<n>` line numbers that appear in the
  sheet. Never cite a file, step or line the sheet does not hold (the check tests the line numbers).

## 4. The build bar — every page

**Data first.** The first element inside `<body>` is
`<script type="application/json" id="evidence">`, holding every fact the page shows, each with where it
came from: `{"label": "Agents running", "value": 4, "from": "m0_step3.txt L1331-L2086"}`. The page's
script draws from this block; no figure exists only in the markup.

**One file that works offline.** Inline CSS, JavaScript and SVG. No CDN, web font, image URL or fetch.
There is no chart library offline: **hand-write charts and diagrams as inline SVG** — boxes, arrows with
labels, rings, bars, timelines. Draw simple SVG icons; emoji are not icons.

**How it looks.** It should look designed, not like a document.
- **White page, edge to edge** — presentations and games too; never a dark background or slide frame.
  Text `#202124`, secondary text `#5F6368`, hairlines `#DADCE0`, panel fill `#F8F9FA`.
- **Color means the same thing on every page:** blue `#4285F4` listed, known, normal · green `#34A853`
  changed for the better, confirmed in a re-read · yellow `#FBBC05` an inference, a caution, something
  shared · red `#EA4335` a gap: unlisted, shared, refused · gray `#9AA0A6` not run yet, not read,
  unknown. For text in those colors use `#1A73E8`, `#188038`, `#B06000`, `#C5221F`. Color is never the
  only signal: every colored thing also carries a word.
- Type: `font-family: "Google Sans", Roboto, Arial, sans-serif`; identifiers in monospace. Hero title
  40–48 px, panel headings 22–26 px, body 16 px, nothing under 13 px.
- **A hero band** first: the module tag (*Module 0 · See Everything*), a title, the one-sentence takeaway,
  and *"Built from the evidence agy recorded on <date of the latest entry>"*. Then panels on a 12-column
  grid, max width 1200 px, with generous space. **Each panel answers one question** in its heading and
  ends with a source line (*From Step 3 · m0_step3.txt*).
- **Phone:** at 390 px the panels stack and the page never scrolls sideways. A wide diagram keeps a
  legible size (about 640 px wide) and scrolls inside its own panel (`overflow-x: auto`); it is never shrunk
  until its labels cannot be read.
- **Motion with a purpose.** Transitions of 200–600 ms. Anything that plays a sequence has Play, Pause and
  Step buttons, and **the page loads showing the finished picture**, so a viewer who never presses Play,
  and a screenshot, still see everything. Honour `prefers-reduced-motion`.
- **Accessible:** everything clickable is a `<button>` with a text label (never a clickable `<div>`), so
  it works from the keyboard; every SVG has `role="img"` and a `<title>`.
- **Depth:** a page that does the recipe justice is usually 25–80 KB. Under 15 KB is almost always too
  thin.

**Honest states, each drawn differently:** read from a file (solid) · *not run yet* (gray, dashed
outline, the words "not run yet") · *not read* — the file holds no such read (gray, the words "not read")
· an inference (yellow, labelled *"inference — most likely, not proven"*) · *from configuration, not a
test* (dashed border, those words). A blank never stands for unknown.

**Every page also carries:**
- A **"Still open"** band that is always visible: what the files show is not fixed, and the next module
  only as the Instructions tab's What's next step describes it.
- The **module's footer line** (recipe file).
- A short **"How this page was built"** note: the step files it draws on, and *"Nothing in the estate was
  changed to make this page."*

**Games** look like games, not forms: an illustrated start screen, a round strip or progress bar, motion
on a right or wrong answer. They score the player, never the estate: points for right answers about the
evidence, feedback on every answer with the evidence line behind it, and an end screen with the player's
score and what they just practised. No timer pressure. The "Still open" line is on the start screen and the
end screen. A **facilitator view** opens at `#answers` (and from a button): every round's answers with their
evidence lines. The start button's label begins with *Start*.

**Presentations** (briefings, updates): white around the slide as well as on it; one idea and one diagram
per slide, at most about 30 words on
screen; arrow keys, on-screen buttons and a progress bar; **speaker notes** per slide, toggled with `N`,
built from the same facts and hidden until `N`; a **two-minute timer** toggled with `T`; `@media print`
puts one slide on each page. The check presses the right arrow, `N` and `T` and fails a page where nothing
changes, and fails one with no `@media print`.

## 5. Check and look

```bash
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright /opt/venv/bin/python3 \
  /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/show_check.py \
  /config/Desktop/novasmart-showcase/<file>.html
```

- It checks the file (offline, the data block parses, no identifier, project id or number, email address,
  customer value or role name), then renders it in Chromium at 1440 px and 390 px, presses each button
  once, and saves screenshots in `/config/Desktop/novasmart-showcase/.build/previews/`.
- **Fix every `FIX:` line** and run it again until it ends `RESULT: clean`.
- **Then look.** Open each screenshot it lists with `view_file`: `<name>_1440.png`, `<name>_390.png`, and
  `<name>_play.png` + `<name>_answers.png` for a game or `<name>_next.png` for a presentation. Look for:
  clipped or overlapping text; an empty or lopsided panel; a chart without labels; a wall of text where a
  diagram should be; the module's main finding not standing out; anything on the recipe's *Done when* list
  that is missing. Fix it once, run the check again, look again.
- **A poster or picture:** the same command. For a file whose name ends `_poster.html` the check turns
  poster mode on by itself (its first line says `poster mode: on`): it saves the 1600 × 900 picture next
  to the page as `<name>.png` and fails if the content does not fit. Nothing else is needed: do not read
  the script.
- `RESULT: … could not be rendered` (exit 2): finish, and say in one line that the preview could not be
  made, so the page was not looked at.

## 6. The evidence entry — run it, never compose it

`show_facts.py` and `show_check.py` save every run, failed ones included, word for word, in
`.build/mN_runs.log`. After the last check, and after you have looked at the screenshots, run:

```bash
python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/show_record.py \
  N /config/Desktop/novasmart-showcase/<file>.html "<the leader's words, verbatim>"
```

- It appends one entry in the `../SKILL.md` §3g shape to `mN_step7.txt` (`m4_step5.txt` in Module 4):
  this turn's `show_facts.py` run, **every** `show_check.py` run with its exit code and full output, a
  `#` line for the `write_to_file`, and `ls -l` of the page (and its `.png`). CHANGE RECORD:
  `(nothing changed in the estate)`. It reads the entry count before and after and prints both.
- **A `grep` of a step file** for a detail the sheet lacks: pass it as
  `--grep "grep -n '<pattern>' /config/Desktop/novasmart-evidence/mN/mN_stepK.txt"` (repeat for each); the
  script runs it and records it.
- **Do not write a Show entry by hand**, edit the run log, or re-run the A–D sequence: the script is the
  sequence. If it prints `WARNING`, say so on screen in that answer.
- Its last line is the `### Where the proof is` sentence, with the command count and how many failed: use it
  as printed. If it says the last check did not end `RESULT: clean`, say so in the answer.
- **Never write into the evidence files of other steps, or the scorecard folder.** Write the page this turn
  even if one is already there; a repeat overwrites only its own file.

## 7. The short answer — this shape, none of the `../SKILL.md` §3 blocks

1. A **bold** line naming what you made and its full path, then *"This is Step 7 of Module N, <step
   title>."*
2. A `file://` link to it, e.g. `file:///config/Desktop/novasmart-showcase/m0_dashboard.html` — plus the
   `.png` link for a poster — and the line *"To open it, paste that link into Chrome's address bar."*
   ⛔ **You cannot open it yourself**: no browser opens from your shell (`xdg-open` here only logs the
   URL). Never say you opened, launched or displayed it. Asked to open it (*"open the dashboard"*), say you
   cannot open a browser window in this lab and give the file name and link again. (A run answered *"I
   have launched the executive dashboard in your desktop browser"*; nothing opened.)
3. One short paragraph: what it shows, **how to use it** (Play, arrow keys, `N` for notes, the answers
   view), which steps' files it draws on, and anything shown as not run yet.
4. `### Where the proof is`, in the `../SKILL.md` §3g form.
5. `### What this does not fix` — one line: this step changed nothing in the estate; what is still open is
   what the Instructions tab names at this module's What's next step.
