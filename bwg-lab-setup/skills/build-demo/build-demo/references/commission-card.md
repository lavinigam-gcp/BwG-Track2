# The commission card — your checklist, never their form

⛔ **Never put this file to the learner.** It is the five-slot checklist you fill while you talk. A form
with five dropdowns feels like paperwork; a conversation feels like being taken seriously. Read the five
forms out **only** if they ask what else it could be.

**Why it exists at all.** *"Be creative"* produces convergence: same brief, same assistant, same estate,
twenty identical dashboards. The card is the floor. The conversation is the ceiling. Keep both.

---

## 1. The five slots, and where each one comes from

| Slot | What it settles | Filled by | The learner sees |
|---|---|---|---|
| **A · Audience** | Who is in the room when this is shown | Seed, confirmed or swapped in **Q1** | A statement with an out |
| **B · Form** | What shape the thing is | Seed, same turn | Same turn |
| **C · Front sentence** | The one line on the front | **Q2, verbatim** — their sentence, not an option | Never named as a slot |
| **D · Leftover risk** | The thing M1 did not fix that gets permanent screen space | **Q3**, from what actually unsettled them | Never named as a slot |
| **E · House rule** | One constraint stated on the page | You derive it from Q2's register; they confirm in the read-back | One word changes it |
| **F · Their own idea** | Anything we did not think of | **Q4**, verbatim. **Overrides A–E where they collide** | It is what they asked for |

**Slot F is not a tie-breaker, it is a trump.** If their own idea contradicts the seeded form, the idea
wins and the seed is dropped without comment. Say which part of it the estate can evidence and which part
it cannot, then build the part that can. ⛔ Never rank their idea against one of ours.

**Slot D does the most work of the five.** It is the slot that makes apps *end differently* — different
final panel, different closing sentence, different thing the audience is left holding — and it is the one
that keeps the activity honest, because it forces every app to render something Mission 1 did not fix.

### The option sets — for **your** completeness check, and to read out only on request

| Slot | The five |
|---|---|
| **A · Audience** | 1 the board · 2 an external auditor · 3 the engineer on call at 2am · 4 the marketing director whose agent was just re-badged · 5 your successor on their first day |
| **B · Form** | 1 a **console** (ask → it acts → it answers) · 2 a **timeline** (lanes over time) · 3 a **map** (who signs in as what, who can reach what) · 4 a **live feed** (append-only, every line timestamped) · 5 a **narrative** (paged, one claim per page, each page carrying its own evidence) |
| **C · Front sentence** | 1 *Who read our customer table in the last hour?* · 2 *Can we name every workload and the identity it signs in as?* · 3 *What did today not fix?* · 4 *If marketing's agent tried again right now, what happens?* · 5 *What can I prove, and what can I only assert?* |
| **D · Leftover risk** | 1 the shared login is **vacated but still exists** · 2 the tool layer can read with **its own** credentials · 3 the store portal runs as an **owner-privileged** identity · 4 the customer table's **shape** is readable by principals nobody has enumerated · 5 **nothing alerts anyone** — an event being recorded is not a person being told |
| **E · House rule** | 1 no colour except a single accent · 2 fits one screen, no scrolling · 3 must name at least one number it could **not** get · 4 must still make sense with the network unplugged after load · 5 must be readable aloud in 60 seconds |

⛔ **C and D are never read out as menus.** They are here so you can recognise a match, not so you can
offer a choice. Q2 and Q3 routinely land somewhere no list holds, and that is the point of asking them.

---

## 2. The seed — divergence with zero effort from the learner

```
SEED = the last two hex characters of the learner's own project ID
A    = (int(SEED, 16) %  5) + 1
B    = (int(SEED, 16) // 5 % 5) + 1
```

Read the project ID with `gcloud config get-value project`. **Compute it. Never guess it, and never take
a worked pair from this file as the learner's answer.**

| Project ends | `int` | A | B | You say |
|---|---|---|---|---|
| `0a` | 10 | 1 · the board | 3 · a map | *"a map, for the board"* |
| `12` | 18 | 4 · the marketing director | 4 · a live feed | *"a live feed, for the marketing director"* |

Three properties worth having:
- **A passive learner still diverges** — the seed alone gives 25 audience × form pairs.
- **A swap is a decision, not a preference** — they had to overrule something to make it.
- ⚠️ **It is arbitrary, and you say so.** A learner who believes the computer chose *for a reason* will
  not swap, and the whole opening turn is wasted.

---

## 3. The completeness check, before you hand off
Restate it to yourself in one sentence — *"a **<form>** for **<audience>**, opening on **<their
sentence>**, ending on **<leftover risk>**, under **<house rule>**"* — and confirm every slot has a value.
If **three or more** are still the seeded or first-listed default, ask for **one** change, once. ⛔ Do not
choose for them, do not refuse, and do not ask twice.

This check is why a conversation does not wander: you can see when it is done.

---

## 4. The fallback ladder — used when they skip, or when Q5 also came back thin

**It never picks the first option on a list.** In order:

1. **A and B: keep the seed.** ⛔ Never re-roll and never default. This step costs nothing and it is the
   floor.
2. **D: derive from what actually failed in *this* learner's grounding sweep.** A read that returned
   empty, or was refused, for them and not for the person beside them **is** their leftover risk. Per
   project, per run, genuinely divergent, free — and the most honest possible choice, because it is the
   thing this run could not see. *(You do not run those reads here; the builder does. Record the rule, not
   a result.)*
3. **C: derive from the audience, deterministically — never option 1.**

   | Audience | Front sentence |
   |---|---|
   | the board | *What did today not fix?* |
   | an external auditor | *What can I prove, and what can I only assert?* |
   | the engineer on call | *Who read our customer table in the last hour?* |
   | the marketing director | *If their agent tried again right now, what happens?* |
   | your successor | *Can we name every workload and the identity it signs in as?* |

4. **E: take the house rule most in tension with the seeded form.** A live feed that must fit one screen
   with no scrolling; a map that must name a number it could not get; a narrative readable aloud in 60
   seconds. **A constraint that fights the form produces a visibly different object than one that agrees
   with it**, and it costs the learner nothing.
5. **Say it in one sentence and own it.** *"You'd rather I got on with it, so: a map for the board, ending
   on the one number I couldn't read, in under sixty seconds. One word changes any of that."*
   ⛔ Never pretend they chose. ⛔ Never present the fallback as a question.

> **The house default is not a reachable state.** Even the fully passive path — hatch on line one, zero
> answers — differs from the next learner's on audience, form, leftover risk and house rule. Two of those
> come from their project ID and one from which reads happened to fail in their project. Do not weaken it
> by reaching for the top of a list.

---

## 5. Two ways an open answer goes wrong

| It happens when | Example | You do |
|---|---|---|
| **The answer asks for something the data cannot support** | Q2: *"that no customer data has ever leaked"* | Keep the sentence on the front. Underneath it, plainly: this page cannot show that, here is what it can show. ⛔ Never re-ask, never negotiate the sentence down, never quietly substitute a weaker one |
| **The answer needs a customer record to answer it** | Q4: *"whose records did it read?"* | The one hard stop. Say the reason once — the assistant's own login cannot read those rows by design, and that is the control working — then answer the question the log *can* answer. **The question changes; the app does not** |
