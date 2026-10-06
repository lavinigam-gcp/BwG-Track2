# M1 Step 7 · Show what you changed — the five demos

> Read with `showcase.md`, which holds the workflow, the build bar, the check and the answer shape. This
> file holds Module 1's facts rules and one recipe per demo. Source: the fact sheet from
> `show_facts.py 1` (Steps 1–5). Save every page in `/config/Desktop/novasmart-showcase/`.

## 1. What an M1 page may say

M1 changed the estate. These rules come from `m1.md` and bind every page.

- **BEFORE comes from recorded reads:** Step 1's first catalog read, and Step 2's reads (each workload's
  login, the shared login's project-wide access, the customer dataset's access list). **AFTER comes from
  the re-reads in Steps 3–5.** Never draw an AFTER the sheet does not show.
- BEFORE never calls the log "anonymous": it named the shared login, never an agent. The promo agent's
  owner and risk tier belong to AFTER: they were written in Step 1.
- **Changes** are the `Change:` lines across the step files. Count them and say the count (the
  registration in Step 1 is one of them). Each change: what changed and on what, in plain words, and its
  `When:` time. Show *"undo on record"*, never the undo command.
- **Grant first, remove last:** show that order only as the times prove it — the personalization agent's
  badge reading customer data at its logged time, before the shared login's project-wide access was
  removed at its `When:` time.
- **Step 4 as recorded** — usually *"nothing left to remove: already closed by Step 3"*, with the re-reads
  that showed it. Never say Step 4 removed access unless its change record says so.
- **Step 5's proof as recorded:** the personalization agent's read under its own badge (the log's email
  field is blank; its badge is named in another field, `principalSubject`); the promo agent's attempt
  **refused in the log** (time, its login, what it tried — *start a query job* — and the refusal); Price
  Match still answering. The promo agent's own reply ("launched", 0 records) is the app talking, not proof.
- **The Step 5 checklist** — show its rows, the coverage line and the scorecard verdict exactly as
  recorded. A row evidenced from configuration only is drawn dashed: *"from configuration, not a test"*.
  A row marked `not verified` is drawn gray.
- **Do not widen the claim.** Least privilege covers the two workloads M1 changed, as the files show them
  — never the estate. Never *"only the badge can read customer data"*: other entries on the customer
  dataset's access list remain, and are drawn as listed. Any broad access the files record elsewhere stays
  visible.
- **The promo agent got its own service account** (`promo-agent-sa`), not Agent Identity: Agent Identity
  is for agents on Agent Runtime. Same principle, different plumbing.
- **The shared login was vacated, not deleted.** It keeps the permissions its re-read lists, in plain
  words.
- **Plain words for access**, never role names: *change or delete every table in the project* (project-wide
  BigQuery admin) · *run queries* · *read the customer dataset* · *read the seed files* · and so on.
- **No customer values.** The legitimate read returned a customer record: show *"returned 1 record (values
  not shown)"*.
- **Still open / next:** Module 2 only as M1 Step 6 says it, word for word: *who may call whom, starting
  with who is allowed to call that back-office margin agent.* There is no Step 6 evidence file: never cite
  one.
- **Footer on every page:** *"Every change is on record with a way to undo it"* — only if every change in
  the files has an undo line; otherwise say which does not.

## 2. The demos

### A · Before-and-after map — `m1_identity_map.html` (the one to start with)

*"Build me a before-and-after map of how each agent got its own login."*

**Answers:** who signs in as what, and what can each reach — before M1 and now?

**Must show**
1. Hero band with the takeaway built from the sheet (each of the two workloads now signs in as its own
   login; the promo agent can no longer reach customer data; reads now name the personalization agent's
   badge).
2. **BEFORE and AFTER side by side** on a wide screen (stacked on a phone). Play animates BEFORE into
   AFTER: the login lines move, access appears and disappears.
3. **The graph** (SVG): Customer Personalization Agent (Agent Runtime) and the promo agent (Cloud Run) →
   the login each signs in as → what that login can reach, each target scoped in plain words (*everything
   in the project*, *one dataset, read only*, *the seed files only*). Price Match and Markdown Strategy as
   context, each on its own badge.
4. **The catalog chip:** BEFORE *not in the catalog* → AFTER *Promo Agent — Owner: marketing team · Risk
   tier: high*, as written in Step 1.
5. **The shared login:** BEFORE two workloads on it with project-wide access to change or delete every
   table; AFTER nobody on it, that access gone, its remaining permissions listed in plain words —
   *vacated, not deleted*.
6. **What each could reach**, before and after, as paired bars or chips — words, not scores.
7. **The log card:** after the change, the personalization agent's reads show a blank email and its badge
   in another field; an alert that matches only on email would miss them.
8. A marker: *"Least privilege — these two workloads only."* "Still open" band and footer.

**Done when:** every AFTER item traces to a Step 3–5 re-read; no role names; the promo agent is shown with
its own service account, not Agent Identity.

### B · Change replay — `m1_change_replay.html`

*"Build me a replay of every change I made in this module, in order."*

**Answers:** what exactly did we change, when, and in what order? The flight recorder.

**Must show**
1. **A timeline** from the first `When:` to the last, with every change as a card: what, on what, the time,
   *undo on record*. The count of changes in the header.
2. **Play, Pause, Step and a speed switch.** As each change lands, a miniature estate map beside the
   timeline updates: the login moves, access appears, access disappears.
3. **Grant first, remove last**, highlighted on the timeline with both times (§1), only if the times show
   that order.
4. Log events inside the same window, if Step 3's or Step 5's log rows hold them: the badge's successful
   read, the promo agent's refusals after it moved — each labelled *from the log*.
5. **Step 4** as a marker: what its re-reads showed and what it changed (usually nothing).
6. "Still open" band and footer.

**Done when:** the card count equals the number of `Change:` lines; every time matches the sheet; no undo
command text appears.

### C · Proof for an auditor — `m1_proof.html`

*"Build me a page that shows an auditor the proof that this worked."*

**Answers:** what does the platform's own record show, beyond what the apps say?

**Must show**
1. **"What the app said" vs "what the log shows"**: the promo agent's own reply on the left, the log's
   refusal on the right (time, `promo-agent-sa`, *start a query job*, refused). Play runs request → app
   reply → log row.
2. **The legitimate read**: its time, the personalization agent's own badge, the blank email field,
   *returned 1 record (values not shown)*.
3. **Price Match still answers**, as recorded.
4. **The checklist wall**: one tile per Step 5 checklist row — the check, then on tap how it was verified
   and the result in plain words. Configuration-only rows dashed, `not verified` rows gray. The coverage
   line, verbatim. The scorecard verdict as recorded, with its `http://localhost:8088/…` link if the sheet
   shows one.
5. **What this does not prove** — only as the files show: a configuration-only check; least privilege for
   two workloads only; the other entries still on the customer dataset's access list.
6. "Still open" band and footer.

**Done when:** every tile maps to one checklist row; no customer value or identifier appears; nothing the
files call configuration is called a test.

### D · Key Master — `m1_key_master.html` (a game)

*"Build me a game called Key Master from what I changed, for my team to play."*

**Answers:** can your team give every agent the right key, in the right order, and catch an overclaim?
Three rounds, two to four minutes.

**Must show**
1. **Start screen**, then **Round 1 · Give each agent its own key**: the workloads, and the keys the
   re-reads show them holding now, plus the old shared login as a decoy nobody holds. Match each workload
   to its key; every answer shows the re-read line behind it.
2. **Round 2 · Grant first, remove last**: four cards taken from the change records (the personalization
   agent moves to its own badge; the badge may read the customer data; the promo agent moves to its own
   login; the shared login loses project-wide access). The player orders them. Removing access before the
   badge can read plays an outage (*reads fail*); then the real order replays with its times.
3. **Round 3 · Spot the overclaim**: six to eight statements to mark *the evidence supports this* or *goes
   too far*. Use only statements the sheet settles — for example, supported: *the promo agent's attempt
   was refused, in the log*; goes too far: *only the badge can read customer data*, *every agent is now
   least-privileged*, *deleting tables was tested and blocked* (if that row is configuration only), *the
   promo agent now uses Agent Identity*, *the campaign ran successfully*. Drop any statement the sheet does
   not settle.
4. **Score** the player, with feedback on every answer; **end screen** with their score and what they
   practised; **facilitator view** at `#answers`. "Still open" band on the end screen; footer.

**Done when:** every answer is settled by a line in the sheet; the answers view lists all three rounds.

### E · Board update — `m1_board_update.html`

*"Turn what I changed into a two-minute update I can present to the board."*

**Answers:** what changed, what is proven, what is still open? Six to seven slides.

**Must show** — one diagram per slide:
1. Title and takeaway.
2. What we changed: three moves (registered and owned · one login each · access cut), with the change
   count.
3. Before and after, as a miniature map.
4. Grant first, remove last: the timeline strip with its two times.
5. The proof: what the app said vs what the log shows.
6. What we can now say / what we still cannot — two columns, from the files.
7. Still open: Module 2 as Step 6 describes it.
Speaker notes (`N`), the timer (`T`), print layout (`showcase.md` §4).

**Done when:** the slides stay sparse and the notes carry the detail; every slide has a source line.

**Asked for a poster or picture instead:** build `m1_poster.html` and run the check with `--poster` — the
before-and-after map and the app-vs-log pair on one 1600 × 900 canvas, with the takeaway, the "Still open"
line and the footer.
