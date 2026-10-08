# M2 Step 7 · Show what you controlled — the five demos

> Read with `showcase.md`, which holds the workflow, the build bar, the check and the answer shape. This
> file holds Module 2's facts rules and one recipe per demo. Source: the fact sheet from
> `show_facts.py 2 <demo letter>` (Steps 1–5). Save every page in `/config/Desktop/novasmart-showcase/`.

## 1. What an M2 page may say

M2 changed the estate in two steps (Step 3 and Step 5). These rules come from `m2.md` and bind every page.

- **Names.** The back office is *the Markdown Strategy agent*; the front desk is *the Price Match agent*;
  the store website is `novasmart-store-portal`; `test-agent-caller` is *the leftover test login (a service
  account — a login for a program rather than a person)*. An agent's identity is *"the Price Match agent's
  own badge"*, never a `principal://` string, an email or an ID.
- **Two lists, never merged.** Who may call the back office is decided in two places: **its own caller
  list** (a list on that one agent) and **project-wide roles that also carry the ability to call any agent
  in the project**. Permissions add up: the lock narrows only the agent's own list. BEFORE, from Step 1's
  reads: the own list's one name, and the project-wide holders as Step 1 counted them (the count and the
  number of roles exactly as recorded; the roles in plain words — *full control of the project*, *edit
  anything in the project*, *view the project*, *use and manage agents* — never role names). AFTER, from
  Step 3's re-read: the own list names one caller, the Price Match agent's own badge. **The project-wide
  holders are drawn unchanged on both sides of every before-and-after**, and the Price Match agent keeps
  its project-wide line after the lock (it is on the own list **and** still holds a project-wide role).
- **Counts add up.** The project-wide figure includes the back office's own badge and the Price Match
  agent's badge; when you say who *else* can call it, use the "others" figure the file records, and subtract
  every holder you draw separately (the store website's account, the Price Match agent) from the group.
  The back office is never a caller of itself.
- ⛔ **The banned sentence.** Never *"only the front desk can call it"*, *"only the Price Match agent can
  reach it"*, *"everyone else is out"* or *"the back office is private"* — not in a heading, a caption, an
  animation's end state or a slide. In a game it is the overclaim the player must catch; on any other page
  it may appear only in quotes, in a column or panel headed *Goes too far*, never alone. The true sentence:
  *"The back office's own list now names one caller. Project-wide roles still carry the ability to call
  it."*
- **The store website's direct route** — it calls the back office directly, signed in as an account with
  full control of the project — only as Step 1 or Step 2 recorded it. It keeps working after the lock
  because its access is project-wide: draw it as a finding (red), never as a reassurance.
- **Step 1's call as the leftover login: quote what came back, honestly.** The status and what the reply
  held, as recorded. An HTTP 200 that only accepted a task (*submitted*) is *"the call was accepted"* —
  never *"the back office answered it"* or *"it read the margin data"* unless the file shows the reply.
- **Step 4's door test.** The same request replayed, refused: **HTTP 403** and the platform's own words,
  quoted from the file up to the resource — *Permission 'aiplatform.reasoningEngines.query' denied* — with
  its time. Never paste the resource path or the troubleshooter link (the check flags them). Say *"the
  same request"* (or *"byte-identical"*) only if the file says so. An audit-log row backs it up only if
  the file shows one, its method quoted as recorded; an empty result is drawn gray: *"no audit row found
  by that query"*. The refusal came from the agent's own access settings (IAM): **never call it a gateway
  refusal** — "gateway" means the Step 5 egress gateway only.
- ⛔ **Quotes are exact or absent.** A log line, method name or error message is copied character for
  character from the file, or left out. Never rename a permission, method or API to get past the check: it
  allows API identifiers such as `reasoningEngines.query` inside a quote.
- ⛔ **Nothing the files do not hold:** no time for an event that has none on record; no "before" state no
  step read; no mechanism the file does not name; no fix or recommendation (the store website's route is a
  finding, never "until its code is updated"); no action item, priority or plan for the next module.
- **Roles in plain words only.** `bigquery.admin`, `bigquery.jobUser`, `jobUser`, `READER`, `editor`,
  `owner` are role names too: *change or delete every table in the project*, *run queries*, *read the two
  pricing datasets*, *full control of the project*, *edit anything in the project*.
- **The escalation counts only if the back office's answer came back** — a margin decision in the file.
  A call to escalate with no reply, a quota error (429), or *"returned no response"* is drawn gray:
  *"not verified — the front desk asked the back office; no answer is recorded"* — even if a table in the
  file marks it as working. Show the decision in words (*approved*, *declined*); wholesale costs and
  margin floors never appear. It was a **test request** with seeded values, never "a genuine customer
  escalation", and one call is not "escalations continue to work".
- **Step 2 changed nothing.** Its impact table as recorded — who loses access, who does not, and why —
  labelled *"assessment, no change made"*.
- **Step 5 is two controls. Never conflate them, and never claim more than the files show.**
  - **Where it may reach** — the egress gateway. Drawn as attached only if a re-read in the file shows the
    attach. Its evidence is **the gateway log's verdict** on the back office's traffic, only as row 21
    records it: name exactly the methods row 21 lists (session setup such as `initialize` and
    `tools/list`, and `tools/call` when it was recorded — tied to the read or the change by its time only,
    and say so). `ALLOWED` means that traffic went through the gateway and was let through — nothing
    more. Row 21 `not verified`
    or no verdict in the file → gray, *"no gateway verdict recorded"*; attach not confirmed → gray,
    *"attach not confirmed"*. No `DENIED` in the file → never say the gateway blocks, prevents or refuses
    anything. **Wherever the gateway is described, say it is set to let traffic through if its check
    fails** (`failOpen: true`, as the file records). Never *"governs all outbound connections"*,
    *"prevents unauthorized destinations"*, *"actively authorizes"*, *"routes exclusively"*, or a
    "PROVEN" label on the gateway. *"Attached only to the back office"* means no other agent has it.
  - **What it may do** — read, not change. Its database access went from *change or delete every table in
    the project* to *run queries* plus *read the two pricing datasets*. Proven only by **the refused change
    in the audit log under the back office's badge** and **the table check that printed `UNCHANGED`**,
    both quoted. If it printed `CHANGED`, the page says the test write landed, never that it was refused. If the recorded row shows no caller, say *"the audit log shows the refusal; the row as
    recorded does not name the caller"*. Missing either → say which is missing; with neither, dashed
    *"from configuration, not a test"*.
  - ⛔ The gateway never "stopped the write"; the database access never "decided where it may go". A
    read the back office still makes is *"working"* only if its answer is in the file.
  - ⛔ **Never "the pricing data is read-only"** without *"for the back office"*: other holders of
    project-wide access can still change it.
  - A Step 5 command the file records as failed or rejected is drawn as failed, never as in place.
- **Changes** are the `Change:` lines in Steps 3 and 5; count them from the sheet's index lines and say the
  count on the caller map, the two-controls page and the board update. Each: what changed and on what, in plain words, and its `When:` time. Show *"undo on record"*
  only for what the change's `Undo:` lines cover; when one `Change:` bundles several moves and the undo
  covers only some, say which moves have no undo on record. Never the undo command.
- **The scorecard verdict and coverage line exactly as recorded**, from whichever step wrote them (Step 5 in
  the current skill; older runs wrote them at Step 4). Rows marked `not verified` are gray; configuration
  rows are dashed. If the verdict and a row disagree, show both as recorded and resolve nothing.
- **The leftover login's key** — only if `m2_other.txt` records the optional question: the account still
  exists, a usable key for it sits in the seed bucket, and who can read that bucket, as recorded.
  *"Closing a list is not retiring a credential."* Not recorded → leave it out.
- **No customer values, no margin figures.** A read of the pricing data is described by its table and
  columns.
- **Still open / next:** only these sentences from M2 Step 6, word for word, and nothing added (no
  "Action:", "priorities", "next steps") — *"Cloud permissions stack,
  and a handful of broad project-wide roles still carry the ability to call any agent in the project."* ·
  *"Closing the back office's own list did not touch those"* · *"M3 · Protect the Content is where you
  screen what customers can talk your agents into."* There is no Step 6 evidence file: never cite one.
- **Footer on every page:** *"Every change is on record with a way to undo it"* — only if every move in
  every change has an undo line; otherwise *"Every change is on record"* plus which move has no undo on
  record.

## 2. The demos

### A · Who-can-call map — `m2_caller_map.html` (the one to start with)

*"Build me a map of who can call our back-office agent, before and after."*

**Answers:** who could call the back office before this module, who can now, and through which door?

**Must show**
1. Hero band with the takeaway built from the sheet (the own list went from the leftover test login to the
   front desk; the leftover login is refused; project-wide roles are unchanged).
2. **BEFORE and AFTER side by side** (stacked on a phone). Play animates the own-list line moving from the
   leftover login to the Price Match agent's badge; the project-wide lines do not move.
3. **The graph** (SVG): callers on the left — the leftover test login, the Price Match agent, the store
   website, the project-wide holders as one labelled group with Step 1's count — the back office on the
   right. Two line styles, labelled in words: *"on its own list"* (blue) and *"through a project-wide role"*
   (yellow); after the lock the Price Match agent has both. Refused after the lock: red, *"refused — HTTP
   403"* with Step 4's time. Labels 13 px or larger.
4. **The store website's route** as a finding, as §1 says: it keeps working because its access is
   project-wide (no "completely unhindered", no fix).
5. **A marker:** *"The lock narrows the agent's own list. Project-wide roles still carry the ability to call
   it."*
6. A small **Step 5 strip**: the two controls as §1 allows (gateway, database access), each with its proof
   state. Not run yet → gray.
7. "Still open" band and footer.

**Done when:** the project-wide group is identical on both sides; nothing says or draws "only the front
desk"; every AFTER item traces to Step 3–5 lines.

### B · Door-test replay — `m2_door_test.html`

*"Build me a replay of the door test: the leftover login refused, the front desk answered."*

**Answers:** what happened when the leftover login knocked before and after the lock, and did the real
escalation still get its answer?

**Must show**
1. **A timeline** from Step 1's call to Step 4's last result: the first call (time, status as recorded) →
   the lock (`When:` from Step 3) → the replay (time, HTTP 403) → the escalation. Play, Pause and Step;
   loads showing the finished timeline.
2. **The two requests side by side**: the same request (in plain words — who sent it, to which agent,
   what it asked), with each response quoted as §1 allows. The difference is the response, not the
   request.
3. **The audit card**: the audit row if the file has one, or gray *"no audit row found by that query"*.
4. **The escalation**: the front desk's test request (item, shelf price, competitor price — test values
   from the file) → the escalation → the back office's decision. The decision only if it came back (§1);
   otherwise the last hop is gray, *"not verified"*. The prompt's *"the front desk answered"* never
   overrides the file.
5. "Still open" band and footer.

**Done when:** every time and status matches the sheet; no resource path or troubleshooter link appears;
a missing answer is gray, not green.

### C · Two-controls explainer — `m2_two_controls.html`

*"Build me an explainer of the two controls I put on the back office."*

**Answers:** what is the difference between where the back office may reach and what it may do, and what
proves each?

**Must show**
1. **Two columns**: *Where it may reach* (the egress gateway) and *What it may do* (its database access).
   Each: before (only as a step read it) → the change (`When:`) → after → **its own proof** (§1) or its
   honest state. The gateway column carries the `failOpen: true` line and no "proven" label.
2. **A request's path** (SVG, Play): the back office → the gateway (its verdict) → the pricing data → a
   read answered / a change refused. Each hop drawn solid only if the file holds its record; dashed or
   gray otherwise.
3. **"Why one cannot stand in for the other"**: the gateway decides where traffic may go; the database
   access decides what the badge may change; each is proven by its own record. No claim about what the
   gateway can or cannot see inside a request.
4. **What these do not cover**, from the files: other holders that can still change the pricing data;
   any command the file records as failed.
5. Changes with *undo on record* as §1 allows. "Still open" band and footer.

**Done when:** no sentence credits one control with the other's result; no verdict or refusal appears that
the sheet does not quote.

### D · Gatekeeper — `m2_gatekeeper.html` (a game)

*"Build me a game called Gatekeeper from what I controlled, for my team to play."*

**Answers:** can your team tell the two doors apart, sort the two controls, and catch an overclaim? Three
rounds, two to four minutes.

**Must show**
1. **Start screen**, then **Round 1 · Who gets through?**: caller cards — the leftover test login, the Price
   Match agent, the store website, a project-wide holder. For BEFORE and AFTER, the player picks *on its own
   list* · *through a project-wide role* · *both* · *refused*. **Answers are buttons or cards
   (`aria-pressed`), never a `<select>` dropdown**; every answer, right or wrong, reveals its evidence line.
2. **Round 2 · Reach or do?**: evidence cards (attached to the gateway; the gateway's verdict; run queries
   plus read two datasets; the refused change in the audit log; the table check as printed) sorted
   into the two controls. Cards the files do not hold are dropped, and an unproven card is labelled so.
3. **Round 3 · Spot the overclaim**: six to eight statements to mark *the evidence supports this* or *goes
   too far*. Goes too far: *only the front desk can call the back office*; *the gateway stopped the
   write*; *the leftover login is retired* (if the key question is recorded); *the pricing data is
   read-only for everyone*. Supported, if the files say so: *the leftover login was refused, HTTP 403*;
   *the back office's own list names one caller*; *the escalation still gets an answer* (only if it came
   back — otherwise it goes too far). Drop any statement the sheet does not settle.
4. **Score** the player, with feedback on every answer; **end screen** with their score and what they
   practised; **facilitator view** at `#answers`. "Still open" band on the start and end screens; footer.

**Done when:** every answer is settled by a line in the sheet; the banned sentence appears only as a
*goes too far* answer.

### E · Board update — `m2_board_update.html`

*"Turn what I controlled into a two-minute update I can present to the board."*

**Answers:** who can call the back office now, what is proven, what is still open? Six to seven slides.

**Must show** — one diagram per slide:
1. Title and takeaway.
2. The door before: the own list (one leftover login) and the project-wide group.
3. The lock: own list of one, project-wide group unchanged.
4. The door test: the first call's result vs HTTP 403; the escalation as recorded.
5. Two controls: reach vs do, each with its proof state.
6. What we can now say / what we still cannot — two columns, from the files.
7. Still open: the Step 6 sentences (§1) and nothing else — no "Action:" lines, no next-module plan.
Speaker notes (`N`), the timer (`T`), print layout (`showcase.md` §4). The notes follow §1 too: the
project, not "the organization"; a test request, not a customer's; no "remediation", no verdict words.

**Done when:** no slide says or implies "only the front desk"; the notes carry the detail; every slide has
a source line.

**Asked for a poster or picture instead** (run `show_facts.py 2 E`, which prints this too): build
`m2_poster.html`; the check renders it as a poster by itself — the
before-and-after caller map and the two-controls pair on one 1600 × 900 canvas, with the takeaway, the
"Still open" line and the footer.
