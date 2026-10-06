# Which rules win

## The precedence line

The honesty contract in ../references/build-and-ground.md overrides every vendored file,
always, without asking. Vendored guidance governs how the page looks. It never governs what
the page claims.

That is not a tie-breaker for hard cases. It is the rule for every case. If a file under
vendor/ tells you to do something the honesty contract forbids, the honesty contract wins,
you do not ask, and you do not negotiate. If the two appear to agree, the honesty contract
is still the one you are following.

The second constraint, which is not about honesty but is equally hard: the page must open
from a file, in a container with no network, and it must look identical once deployed.
Never emit a link to a stylesheet or font, an @import url(...), a script src to a remote
host, an @font-face whose src is not a local file, or a url(http...) of any kind. A page
that needs the network is a page that fails in the room.

Nothing under vendor/ may be edited to make it agree with us. The disagreements are recorded
below instead, so that whose rule is whose stays legible and the copy stays verifiable
against its upstream commit. See design-rules/ORIGIN.md.

## The collision to know about before you read anything else

design-rules/interaction-and-states.md is the file we most want for an app with controls,
and its own worked example breaks our rule. Line 95 gives the success state a small tick
glyph. Line 94 gives the error state a small warning glyph. The upstream entry point, which
we did not vendor, does the same thing at greater length: its eight-state demo wrapper
prints an hourglass, a warning glyph and a tick.

Keep all eight states. The glyphs are banned outright. A state is worded, in plain language,
with no glyph, no colour coding and no pill. A tick is a verdict, and this lab does not emit
verdicts the platform did not.

## The override table

Each row names the upstream rule, our rule, and which wins. Line numbers are as measured in
the vendored copy at commit 13ac0ec7e148655948100b6396439e481361d690.

| # | Vendored guidance | Ours | Winner |
| :-- | :-- | :-- | :-- |
| O1 | typography.md:40 lists system-ui, Arial and Helvetica among the banned default sans faces | The pairing is Austere (typography.md:129), and the only faces permitted from it are the system ones. The ban is suspended for system-ui for that reason | Ours, expressed in their own vocabulary, so nothing is edited |
| O2 | typography.md:50-52 names three font sources: Google Fonts CDN, Fontshare CDN (a link to api.fontshare.com), foundry-licensed | No webfont from anywhere. No link element, no @import url(), no remote @font-face src | Ours |
| O3 | color.md:7 — OKLCH only; hsl() and rgb() "lie about brightness" | Hex first, oklch() as a second declaration on the same property. Modern browsers take the second; older ones keep the first | Ours, for compatibility. Theirs is right on the merits |
| O4 | color.md:81 — "Red-green pairing as the only signal. Add an icon or pattern." | There is no green and no red token in the palette, by name or by value, and no icon either. Grep-checkable | Ours, and stricter. Their rule is about colour-blindness; ours is about not converting a reading into a verdict |
| O5 | slop-test.md:146 (gate 46) — the remedy for a fabricated metric is an em dash plus a labelled grey block, or the words "metric to confirm" | The literal words not read, at body size, in the muted ink token, in the slot the number would have filled | Ours. A recorded, deliberate divergence: a dash is ambiguous between unread, zero and not applicable, and a grey block is a design signal a reader learns to skip. Words cannot be skipped. Do not let anyone "fix" this later |
| O6 | interaction-and-states.md:94-95 — the error state carries a warning glyph, the success state carries a tick glyph. The dropped upstream SKILL.md:104-116 prints an hourglass, a warning glyph and a tick in its eight-state demo | Keep all eight states. The glyphs are banned outright. States are worded ("try again", "saved") with no glyph, no colour and no pill | Ours. This is the sharpest collision in the set: the file we most want under the functional-app premise ships tick and warning glyphs in its own worked example |
| O7 | interaction-and-states.md — mandatory error and success states | Keep the states; never encode them in green or red; distinguish by words and position | Ours |
| O8 | slop-test.md:146 (gate 46) — "a lead figure carries the hero only alongside a worded headline". The upstream 04-stat-led macrostructure, which we did not vendor, makes a giant number the hero | No hero figure and no summary metric at all. The slot does not exist | Ours, one step beyond theirs |
| O9 | slop-test.md — the whole gate set (numbered 1 to 57, though the file is titled "58 gates"), including the diversification gates (8, 32, and the note at line 81, all of which read .hallmark/log.json) and the hero-enrichment gates | Run the universal, typography, contrast, accessibility, mobile and honest-copy gates. Skip diversification and hero enrichment. Record which subset ran | Ours, by scoping in the sub-skill. The vendored file is not edited |
| O10 | contract.md:20 — "Invent product copy. If the user hasn't given you the words, ask." The dropped upstream SKILL.md goes further and always asks before designing | Never ask the learner what the page should look like; that decision is already made. Ask only what it should show. Never invent copy either — the difference is that we do not ask about taste | Ours. SKILL.md is dropped, but contract.md is kept and repeats the instruction, so the override must be stated |
| O11 | contract.md:23 — "Build logic — state management, data fetching, business rules. It is a visual / interaction layer only." | Our demos do have logic. The vendored guidance governs the surface; references/data-palette.md governs every fact | Both, scoped. Not a conflict once the boundary is named |
| O12 | copy.md — assertive product voice, headlines that land | Headings name what was read, never what it means. No grading word anywhere: secure, safe, protected, compliant, healthy, clean, exposed, vulnerable, risky, at risk | Ours. copy.md is the highest-override-density file in the set; read it on request only |
| O13 | slop-test.md:40 and :83 — consecutive builds must differ structurally from the last one recorded | An explicit anti-goal. Every learner's page should be recognisably the same honest shape, so a room can read them at a glance | Ours. The upstream rotation machinery is dropped, not merely overridden |
| O14 | contract.md:9 offers a tokens.css file; slop-test.md:40, :81 and :83 tell the assistant to read .hallmark/log.json. The dropped SKILL.md wrote both, plus .hallmark/preflight.json and a CSS critique stamp | Write nothing into the learner's demo directory but the demo. No dot-directory, no log, no tokens file, no notes | Ours |

## Rows from the plan that do not apply here

Report 16 carried sixteen rows. Two of them, O15 and O16, govern a file from a second
project (taste-skill) that was not vendored, on the owner's decision D1. They are recorded
here so the ledger is complete and so nobody assumes they were dropped by accident.

  O15  A placeholder-image service for stand-in imagery. Not applicable: nothing from that
       project is present. Our rule stands regardless — no image the learner did not
       generate from their own project, and no image fetched over the network.
  O16  Faux-OS window chrome, three grey circles imitating macOS window controls. Not
       applicable for the same reason, and the vendored material already agrees with us:
       slop-test.md:152 (gate 47) fails a page for a fake browser bar, phone frame, code
       frame, terminal frame or IDE chrome, and anti-patterns.md says the same at length.

## Where the vendored guidance is adopted unchanged

The table above can read as though none of their guidance survives. These are adopted in
substance, and they are the reason vendoring is worth doing at all: the invented-metric
section of anti-patterns.md, gate 46 (invented metric), gate 47 (re-drawn chrome), gate 30
(emoji as icon), one accent at three per cent of the viewport or less, no pure black and no
pure white, tinting the neutrals toward the anchor hue, no purple-to-cyan gradient and two
stops maximum, the four-point spacing scale with varied gaps, asymmetry over centring
everything, depth from weight rather than stacked shadows, the contrast table, at most two
families plus a mono, tabular figures, prefers-reduced-motion, cutting motion before adding
it, the eight-state discipline, the six mobile non-negotiables, and the implementation
safety rail in contract.md that says never to delete the learner's files.

## The precedence line, again

The honesty contract in ../references/build-and-ground.md overrides every vendored file,
always, without asking. If you have read this far and are about to follow a rule from
design-rules/ that puts a tick, a colour, a grade or a number the platform did not report on
the learner's page, stop. The honesty contract wins. It always wins.
