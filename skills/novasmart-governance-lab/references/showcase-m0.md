# M0 Step 7 · Show what you found — the five demos

> Read with `showcase.md`, which holds the workflow, the build bar, the check and the answer shape. This
> file holds Module 0's facts rules and one recipe per demo. Source: the fact sheet from
> `show_facts.py 0` (Steps 1–4). Save every page in `/config/Desktop/novasmart-showcase/`.

## 1. What an M0 page may say

M0 was a look. These rules come from `m0.md` and bind every page.

- **Readiness (Step 1)** in words, never ticks or crosses: *"Environment ready: 8 checks, all ready"* only
  if the table in the sheet says so.
- **The catalog (Step 2)** — count distinct agents, deduplicated on `agentId`: an agent listed in both
  locations counts once and is drawn once, marked as listed in both. Give the per-location counts and the
  distinct total as separate, labelled figures. Spell names as the catalog returns them.
- **Built-ins** — Google's own entries that NovaSmart did not deploy — get **one plain sentence**. Never a
  group, colour, legend, column or "(Built-in)" tag of their own: draw them exactly like the other catalog
  entries, with Step 3's verdict. Never a finding, a gap or a risk.
- **What runs (Step 3)** = the Agent Runtime agents plus the agent on Cloud Run. `novasmart-mcp` (the tool
  layer), `novasmart-store-portal` (the store website) and `remote-browser-*` (the lab workstation) are not
  agents: they stay out of every drawing and count. One footnote may say they were left out and why.
- **Matching** is on the runtime reference, as Step 3 did, never on display name or count. Each agent gets
  one of Step 3's verdicts: *matched* · *running, not in catalog* · *in catalog, nothing of ours running*.
  Runtime spellings differ from catalog spellings (*Markdown Strategy Agent* vs
  `markdown-strategy-agent`): show the match, don't merge the names.
- **The shadow** (`promo-agent-shadow`): running, no catalog entry, no owner — the module's headline, in
  red. It is unlisted because it was deployed as an ordinary service on a shared login; **never say it is
  unlisted because it runs on Cloud Run.**
- **Who signs in as what (Step 4 re-reads):** the two workloads on `novasmart-customer-sa`, and the two
  agents that each have their own badge. Nothing about what the login is *allowed* to do: M0 never read its
  permissions.
- **Reads (Step 4):** count as the shared login's reads only the rows whose principal is
  `novasmart-customer-sa`. Which runtime each came through is read from the service agent that acted for
  it: the Cloud Run robot (`serverless-robot-prod`) means *came through Cloud Run*; the Agent Runtime
  service agent (`gcp-sa-aiplatform`) means *came through Agent Runtime*. Every other row — the project's
  setup login, a person, an agent's own badge from earlier tests — is either labelled as what the file
  says it is (*"the project's setup login"*, without guessing why it ran), in a separate muted list, or
  left out. Never count it as the shared login's.
- **Never label a read with the test request that may have caused it** ("promo extract", "loyalty
  check"): the log does not link a read to a request.
- **Whether agy's test request landed:** quote `post-mark rows`. When it is 0, every read shown is an
  *earlier read found in the log*, never one agy caused.
- **Columns:** each read shows its column names (from `tableDataRead.fields`). Two different column lists
  prove two different queries, not two different agents.
- **Which agent read?** The log names the login and the runtime, never the agent, and never the customer.
  Pointing at an agent from where each one runs is an **inference** — yellow, *"most likely, not proven"*.
- **What the log can and cannot tell** is exactly this, and nothing added: it **can** tell the login, the
  time, the runtime it came through, the table and the columns; it **cannot** tell which agent, or which
  customer. No extra rows of your own (tickets, exports, owners, intent).
- **Nothing is fixed.** Step 5's decision belongs to the leader: show it open, with its three questions
  word for word — *"Own it or kill it? Do you shut the promo agent down, or bring it under a named owner —
  and why?"* · *"Does a marketing agent need the whole customer database, or any of it?"* · *"What is the
  blast radius if you over-grant access now, just to be safe, and the agent is later tricked or
  breached?"* — unless they stated their call this session, then quote it as theirs. There is no Step 5
  or Step 6 evidence file: never cite one.
- **Still open / next:** Module 1 only as M0 Step 6 says it, word for word: *register the shadow agent,
  give each agent its own identity, and scope its access down to what its job actually needs.*
- **No scorecard, no verdict** ("healthy", "all clear", "compliant"). M0 is not scored.
- **Footer on every page:** *"Nothing was changed — this was a look."*

## 2. The demos

### A · Executive dashboard — `m0_dashboard.html` (the one to start with)

*"Build me an executive dashboard of the agent estate I found in this module."*

**Answers:** what do we run, and can we account for it? For an executive with two minutes.

**Must show**
1. Hero band with the one-sentence takeaway built from the sheet (one agent runs with no catalog entry;
   two agents share one login, so the log cannot say which of them read customer data).
2. **KPI tiles**, each with its step tag and a hover or tap note naming the source lines: distinct agents
   in the catalog · agents running · running with no catalog entry (red) · agents on one shared login ·
   reads of the customer table under that login.
3. **Catalog vs what runs** (SVG): the catalog's agents on the left, the running agents on the right,
   matched pairs joined by labelled lines (*matched on runtime reference*). The shadow, in red, faces an
   **empty dashed slot** in the catalog column, labelled *no catalog entry* — never a line to another
   entry. Catalog-only entries carry their verdict. A toggle shows each location's listing.
4. **Who signs in as what** (SVG): the two workloads → `novasmart-customer-sa` (yellow, *shared*) → the
   customer table, with the arrow labelled *read, from the log*; the other two agents → *own badge*.
5. **Reads under the shared login** — a time strip of those rows: time, *came through Cloud Run / Agent
   Runtime*, number of columns. Tap a read to see its column names and source line. Play replays them in
   order. The *post-mark rows* result is stated beside it.
6. **What the log can tell / cannot tell** — the two lists in §1, nothing added.
7. Readiness, collapsed (`<details>`), in words.
8. "Still open" band and footer (`showcase.md` §4).

**Done when:** every tile has a source; the shadow is red in the tiles and the diagram; nothing in §1's
"not agents" list is drawn as an agent; built-ins are one sentence; no permission or fix appears.

### B · Investigation board — `m0_investigation.html`

*"Build me an investigation board that answers: who touched our customer data?"*

**Answers:** what can we prove about who read customer data, and what can't we? Framed as a case file.

**Must show**
1. **The evidence** — a timeline of the shared login's reads, each card with time, runtime and columns;
   Play walks through them, lighting the runtime each came through and the login it used.
2. **The two on that login** — the two workloads that sign in as `novasmart-customer-sa`, each with where
   it runs, from the Step 4 re-reads.
3. **The lead** — for each read, the inference from where it came through, in yellow: *"most likely
   <agent>, by where it runs — not proven"*.
4. **Proven / not provable** — the two lists in §1, nothing added.
5. **Regulator mode** (a button): five questions — which login? when? which columns? which agent? which
   customer? Each opens with *the log answers*, *partly* or *cannot answer*, and the line behind it.
6. Other rows from the same log, muted and labelled (setup login, a person, an agent's own badge), or a
   note that they were left out.
7. Whether agy's test request added a row. "Still open" band and footer.

**Done when:** no card names an agent as the reader except in a yellow inference; no customer value
appears; the regulator answers match the sheet.

### C · Shadow Hunt — `m0_shadow_hunt.html` (a game)

*"Build me a game called Shadow Hunt from what I found, for my team to play."*

**Answers:** can your team spot the gaps M0 found? Three rounds, two to four minutes.

**Must show**
1. **Start screen** that looks like a game: an SVG illustration of the estate (the catalog on one side,
   what runs on the other), the three rounds as a strip, Start, and the "Still open" line.
2. **Round 1 · Catalog vs reality** — two columns side by side, spelled as the sources spell them: the
   catalog's entries, and what the runtimes report running. The player taps a running agent, then the
   catalog entry it matches (the spellings differ, so they have to read), and finds the one running agent
   left with no match. Every pair and every catalog-only entry reveals its verdict and evidence line.
3. **Round 2 · One badge, two workers** — show a read from the log (time, login, runtime, columns). The
   player picks who did it: either workload, or *the log can't say*. The right answer is *the log can't
   say*; the follow-up shows the yellow *most likely, not proven* lead.
4. **Round 3 · The regulator calls** — four or five questions to sort into *the log can answer* / *the log
   cannot answer*.
5. **Score** the player (for example 100 for a first-try answer, 50 for a second), with feedback on every
   answer. **End screen**: their score, the three things they practised, Play again.
6. **Facilitator view** at `#answers` and from a button. "Still open" band on the end screen; footer.

**Done when:** every card and answer comes from the sheet; the score is the player's, never the estate's;
the answers view lists every round.

### D · Board briefing — `m0_briefing.html`

*"Turn what I found into a two-minute briefing I can present to the board."*

**Answers:** what does the board need to know, in two minutes? Six to eight slides.

**Must show** — one diagram per slide, not bullet lists:
1. Title and the takeaway.
2. The three questions M0 asked (what do we have? what runs? who read customer data?) as three icons.
3. Catalog vs what runs — the shadow highlighted.
4. One login, two agents.
5. What the log can and cannot tell — the reads strip and the two lists.
6. The decision in front of the board: Step 5's three questions, open (§1).
7. Still open, and Module 1 as Step 6 describes it.
Speaker notes on every slide (`N`), the timer (`T`), print layout (`showcase.md` §4).

**Done when:** the notes carry the detail and the slides stay sparse; every slide has a source line.

### E · Poster — `m0_poster.html` → `m0_poster.png`

*"Make a one-page poster of what I found that I can share."*

**Answers:** the whole module on one shareable picture. Run the check with `--poster`.

**Must show** on one 1600 × 900 canvas (fixed size, no scrolling): the title and takeaway; three panels —
catalog vs what runs, one login and two agents, what the log can and cannot tell — each a diagram with at
most three short lines; readiness in one line of words; the "Still open" line; the footer.

**Done when:** the check saves `m0_poster.png` with no overflow; the text is large enough to read when the
picture is shrunk to half size.
