# M3 Step 7 · Show what you screened — the five demos

> Read with `showcase.md`, which holds the workflow, the build bar, the check and the answer shape. This
> file holds Module 3's facts rules and one recipe per demo. Source: the fact sheet from
> `show_facts.py 3` (Steps 1–5; Step 6 · What's next has no evidence file). Save every page in
> `/config/Desktop/novasmart-showcase/`.

## 1. What an M3 page may say

M3 changed the estate in one step (Step 3). These rules bind every page.

- **Names.** *The Price Match agent* (the front desk, on the store floor); *the Customer Personalization
  agent* (on the website); *the Markdown Strategy agent* (the back office). The content filter NovaSmart
  already owned is *"the content filter"*, and its name `nvst-jailbreak-template` may appear once,
  glossed. *The inbound gateway* is the door Step 3 put in front of the Price Match agent; *the outbound
  gateway* is M2's control on the back office. Never a `projects/…` path, an agent ID or a badge string.
- **Two attacks, two agents.** The *discount attack* went to the Price Match agent (talk it past its 10%
  limit). The *customer-record attack* went to the Customer Personalization agent (ask it for customer
  records). Never merge them into "the attacks were blocked".
- ⛔ **One agent is screened: the Price Match agent.** Draw exactly one agent behind the inbound gateway,
  and only if Step 3's re-read in the sheet shows the attach. Never *"the agents are protected"*, *"the
  estate is screened"*, *"customer-facing agents are covered"*.
- ⛔ **The customer-record attack is not covered — never shown as blocked.** Its agent is not behind the
  inbound gateway. After Step 3 it is *"not covered — no inbound gateway in front of this agent"*, in red,
  never green, never "stopped", "refused", "prevented" or "mitigated". If Step 4 re-sent it, show what came
  back as recorded (still answered); if not, gray *"not re-sent"*. In a game it is the overclaim the player
  must catch; on any other page *"both attacks are blocked"* appears only in a column or panel headed
  *Goes too far*. The true sentence: *"The screen stands in front of the Price Match agent. The
  customer-record attack reaches an agent with no screen in front of it."*
- **"Blocked" or "refused" only beside a quote.** A message is *refused* only where the sheet holds the
  reply that came back: the status as recorded and the body **copied character for character**, with its
  time. Never write the reply from memory or from the skill: the template may return its own message
  (for example *"Your request was blocked by our content filter…"*) rather than one naming Model Armor —
  quote whichever the file shows. A server-error status is shown beside its body, never alone: *"the status
  says server error; the words say the screen refused it"*. No reply in the file → gray *"no reply
  recorded"*, never a refusal.
- **The screen is fail-open.** Wherever the screen is described, say it is *set to let traffic through if
  its check cannot run* (`failOpen: true`, as the file records it). It is a setting someone chose, not a
  property of the product. Never *"guaranteed"*, *"always blocks"*, *"enforced"*.
- **What it looks for.** The filter looks for **manipulation** (prompt injection and jailbreak attempts)
  and **harmful content**, at the categories and levels the sheet records (quote a level such as
  `MEDIUM_AND_ABOVE` only if the sheet holds it). ⛔ It does **not** look for names or email addresses:
  never *"stops customer data leaking"*, *"redacts personal data"*, *"screens replies for PII"*.
- **Outbound screening is not demonstrated.** If the sheet shows the filter also named for replies, say
  *"replies: configured, not demonstrated"* (dashed, *from configuration, not a test*). No reply was
  shown blocked: never claim one was.
- ⛔ **No Cloud Logging verdict.** The record of a refusal is the refused call's reply in the step's
  evidence file. Never *"Model Armor logged the block"*, *"the audit log shows the verdict"* or *"the
  verdict is in Cloud Logging"*, unless the sheet quotes such a row — and then only that row, as recorded.
- **M2's outbound gateway is a different control.** The back office sits behind the outbound gateway since
  M2 (*where it may reach*); it screens no content. Draw it only as Step 2 read it, labelled *"outbound
  gateway (M2) — where it may reach, not content screening"*. Never count it as screening, and never say
  M3 changed it.
- **Step 1 is the before.** Both attacks' replies as recorded, and the two ordinary requests if the file
  holds them. The customer-record reply is described **by its count and column names only**, never a
  value, never a redacted-looking sample row on the page.
- **Step 2 changed nothing.** What it read: what screens messages today (as recorded — "nothing" only if
  the file says so); the content filter, its settings and created time if read, and that nothing
  references it, only as the reads show. Labelled *"read, no change made"*.
- **Step 3's changes** are the `Change:` lines in Step 3's entry; count them from the sheet's index line
  and say the count on the coverage map, the explainer and the board update. Each in plain words (*added a
  screening rule to the inbound gateway*, *routed the Price Match agent through the inbound gateway*) with
  its `When:` time. The routing took a wait to take effect: show a wait only as recorded.
- **Undo is partial.** Show *"undo on record"* only for what each change's `Undo:` lines cover. Detaching
  restores the routing; if the file records that the attach archived the agent's earlier revisions, say
  *"the agent's earlier revisions cannot be restored"*. Never the undo command.
- **Ordinary requests.** *"Still answered"* only if the reply is in the file. A request that needed a
  lookup *"still works"* only if the reply shows the looked-up result; otherwise *"answered — the file does
  not show the lookup"*.
- **The scorecard verdict and coverage line exactly as recorded** at Step 4. `not covered` rows stay
  `not covered` (red word, never a tick); `not verified` rows are gray. If the verdict and a row disagree,
  show both as recorded and resolve nothing.
- **Agent instructions.** A quoted line of an agent's written rules stays exact. Any secret or discount
  code the agents expose is *"the exposed discount code"* — never its value.
- ⛔ **Nothing the files do not hold:** no time for an event with none on record; no mechanism the file
  does not name; no fix, recommendation, owner or plan (no *"next, cover the website agent"*).
- **The project-wide version of the screen** was not tried in this lab. Mention it only as the Instructions
  describe it (Step 3: it inspects everything an agent assembles internally and stopped almost all real
  work), labelled *"from the lab's Instructions — not tried in this run"*, in gray.
- **No customer values**, no project id or number, no email address. Attack and request texts may be
  quoted as recorded.
- **Still open / next:** only the sentences `show_facts.py 3` prints as *Still open*, word for word, and
  nothing added (no "Action:", "priorities", "next steps"). M4 is named only in that wording. There is no
  Step 6 evidence file: never cite one.
- **Footer on every page:** *"Every change is on record with a way to undo it"* — only if every move has an
  `Undo:` line and no change record says part of it cannot be undone. Otherwise *"Every change is on
  record"* plus what has no undo on record (for example the archived earlier revisions).

## 2. The demos

### A · Attack replay — `m3_attack_replay.html` (the one to start with)

*"Build me a replay of the two attacks, before and after the screen."*

**Answers:** what did each attack get before the screen, what did it get after, and why does one still
get through?

**Must show**
1. Hero band with the takeaway built from the sheet: the discount attack's result before and after (as
   recorded); the customer-record attack not covered.
2. **Two lanes, one per attack**, each BEFORE (Step 1) | AFTER (Step 4), stacked on a phone. Each side:
   who sent what to which agent (the message quoted or in plain words), and what came back, quoted as §1
   allows. Discount lane AFTER: the status and the body, exact, with the time. Customer-record lane AFTER:
   red *"not covered — no inbound gateway in front of this agent"* and the reply as recorded (count and
   columns only), or gray *"not re-sent"*.
3. **A timeline**: Step 1's sends → Step 3's change (`When:`) → any recorded wait → Step 4's replay. Play,
   Pause and Step; loads showing the finished timeline.
4. **The ordinary requests strip**: the price match near 5% and the lookup request, before and after, each
   worded as §1 allows.
5. **"Why it looks like a server error"**: the recorded status beside the recorded body; *the words are the
   evidence*. Only if the sheet holds both.
6. The fail-open line. "Still open" band and footer.

**Done when:** no lane, heading or caption says the customer-record attack was blocked; every *refused*
has its quote and time from the sheet; no customer value appears.

### B · Coverage map — `m3_coverage_map.html`

*"Build me a map of which agents the screen covers and which it does not."*

**Answers:** which agent has a screen in front of it, which do not, and what the other gateway is?

**Must show**
1. Hero: *one door, one agent*, built from Step 3's re-read and Step 5's sum-up.
2. **The map** (SVG): customers on the left; the three agents on the right. Customer → inbound gateway
   (with the content filter) → the Price Match agent: blue/green, *"screened"*, only if Step 3's re-read
   shows the attach. Customer → the Customer Personalization agent: red, *"not covered — no inbound
   gateway"*. The back office: its outgoing side through the outbound gateway, labelled as §1 says, or
   gray *"not read"*. Labels 13 px or larger.
3. **Why the other two are not behind this door** — only the reason the sheet records, or the Instructions'
   sentence (*"The other two agents talk over a different protocol that this door does not sit in front
   of."*) labelled as the Instructions'.
4. **What the screen reads**: incoming messages, checked for manipulation and harmful content; replies
   *configured, not demonstrated*; never names or emails.
5. **A legend** in words: *screened* · *not covered* · *different control (where it may reach)* · *not
   read*.
6. The Step 3 change count, the scorecard verdict and coverage line as recorded, the fail-open line,
   "Still open" band and footer.

**Done when:** exactly one agent is drawn as screened; the outbound gateway is never drawn as screening;
nothing places the Customer Personalization agent behind a door.

### C · Filter explainer — `m3_filter_explainer.html`

*"Build me an explainer of the filter we owned and never switched on."*

**Answers:** what did NovaSmart already own, why was it doing nothing, and what changed when it was put at
the door?

**Must show**
1. Hero: *owned, connected to nothing, then connected at one door* — each part only as the sheet shows it.
2. **The Step 2 find**: the content filter, what it is set to look for (categories and levels as read, or
   *"not read"*), its created time if recorded, and the reads showing nothing referenced it.
3. **Two places to switch it on**: project-wide (gray, as §1 allows, from the Instructions) vs at the door
   (Step 3, from the sheet).
4. **A message's path after Step 3** (SVG, Play): customer → inbound gateway → the filter's check →
   refused (the quoted reply) or passed to the Price Match agent (an answered ordinary request). Each hop
   solid only if the sheet holds its record; dashed or gray otherwise.
5. **What the filter does not do**: look for names or emails; screen the other two agents; a demonstrated
   reply block; a log verdict; stay closed when its check cannot run (fail-open).
6. Step 3's changes with *undo on record* as §1 allows. "Still open" band and footer.

**Done when:** every setting shown is in the sheet; "never switched on" describes Step 2's read only;
nothing claims a log record.

### D · Trap or Customer — `m3_trap_or_customer.html` (a game)

*"Build me a game called Trap or Customer from what I screened, for my team to play."*

**Answers:** can your team tell an attack from a real customer, say where each message went, and catch an
overclaim? Three rounds, two to four minutes.

**Must show**
1. **Start screen**, then **Round 1 · Trap or customer?**: the four Step 4 messages (two attacks, two
   ordinary requests) as cards, quoted or in plain words. The player picks *Trap* or *Customer*. **Answers
   are buttons or cards (`aria-pressed`), never a `<select>` dropdown**; every answer, right or wrong,
   reveals its evidence line.
2. **Round 2 · Where did it go, and what came back?**: for each message, which agent received it, then
   *refused at the door* · *answered by the agent* · *not covered — no door in front* · *no reply
   recorded*, settled by Step 4's lines. The customer-record attack's answer is *not covered*, never
   *refused*.
3. **Round 3 · Spot the overclaim**: six to eight statements to mark *the evidence supports this* or *goes
   too far*. Goes too far: *both attacks are now blocked*; *the screen protects every agent*; *the screen
   stops names and emails leaving*; *the block is logged in Cloud Logging*; *if the screen cannot run,
   traffic is stopped*; *the outbound gateway screens the back office's messages*. Supported, if the files
   say so: *the discount attack was refused, and the reply says so*; *an ordinary price match still got an
   answer*; *the screen stands in front of one agent*. Drop any statement the sheet does not settle.
4. **Score** the player, feedback on every answer; **end screen** with their score and what they
   practised; **facilitator view** at `#answers`. "Still open" band on the start and end screens; footer.

**Done when:** every answer is settled by a line in the sheet; *"both attacks are blocked"* appears only as
a *goes too far* answer.

### E · Board update — `m3_board_update.html`

*"Turn what I screened into a two-minute update I can present to the board."*

**Answers:** what is screened now, for which agent, what is proven, what is still open? Six to seven
slides.

**Must show** — one diagram per slide:
1. Title and takeaway: one agent screened; one attack not covered.
2. The problem: Step 1's two attacks and what came back (customer records by count and columns only).
3. What was there: the content filter, owned and connected to nothing (Step 2).
4. The door: the Price Match agent behind the inbound gateway (Step 3, its `When:` and change count).
5. The test: the four messages before and after (Step 4), each worded as §1 allows.
6. What we can now say / what we still cannot — two columns, from the files (fail-open, one agent,
   replies not demonstrated, no log verdict).
7. Still open: the *Still open* sentences (§1) and nothing else — no "Action:" lines, no next-module plan.
Speaker notes (`N`), the timer (`T`), print layout (`showcase.md` §4). The notes follow §1 too: one agent,
not "our agents"; refused only with its quote; no "secure", "protected", "remediation" or verdict words.

**Done when:** no slide says or implies both attacks are blocked or every agent is screened; the notes
carry the detail; every slide has a source line.

**Asked for a poster or picture instead:** build `m3_poster.html` and run the check with `--poster` — the
coverage map and the two attack lanes on one 1600 × 900 canvas, with the takeaway, the "Still open" line
and the footer.
