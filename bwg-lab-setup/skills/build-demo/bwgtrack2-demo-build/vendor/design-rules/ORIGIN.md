# Origin and modifications

Upstream    https://github.com/Nutlope/hallmark
Commit      13ac0ec7e148655948100b6396439e481361d690
Commit date 2026-08-06T16:19:18Z ("Merge pull request #57 from Nutlope/add-grid-theme-v2")
Path        skills/hallmark/references/ (and LICENSE from the repository root)
Retrieved   2026-08-19
Licence     MIT — see LICENSE in this directory. Copyright (c) 2026 Hallmark contributors.
Vendored by CloudCode session ses_e5fe79010a4ffeNoWBNC7Mxalz, per
            .lavi-working/.docs/plans/demo-track/16-vendor-ui-skills.md

## Precedence

Where anything in this directory disagrees with the honesty contract in
../../references/build-and-ground.md, the honesty contract wins, without exception and
without asking. The overrides are listed in ../OVERRIDES.md and are repeated in the honesty
contract itself, each naming the upstream rule it displaces and why. Nothing in this
directory may be followed in preference to it.

Vendored guidance governs how the page looks. It never governs what the page claims.

## Files included, unmodified

Each file is a byte-for-byte copy of the upstream file at the commit above. The SHA-256
values are of the files as they sit in this directory; they were verified equal to the
upstream bytes at fetch time, and any future divergence is a modification that must be
disclosed here.

  FILE                                  BYTES  SHA-256
  anti-patterns.md                      25676  a36eb346ad59cafaa26119ed1e7c0bbb8aca6637209ee110eb630dd1a9307070
  color.md                               4339  31c470d16ceb17ccce290cbdd00b9e9a88f2094df8eaaefb67c86ec1e1cdb876
  contract.md                            2027  2923a056b95da63d04100ac56bc8cdff6bc0a717ac3e5da5cef69eb5feb4619c
  copy.md                               12261  703cdbf81fbef6f71d90596a32041d2a33a46fb71ba07ccf5ede6b4b1471d347
  genres/editorial.md                    4121  1e88cd0c94435c6a9edd1c0b93b67db4321fb3481ff0d66ee24869e655847319
  genres/modern-minimal.md               4836  6125db00e38f2baca9369ed4d4aa917d977b85dd5eac6f19dac89707c3c3534b
  interaction-and-states.md             13537  e816eb2d067ba9f6f288a3831549da95624a05f432ed2a50f54136f27dd2d67f
  layout-and-space.md                    6766  987f3a45f5dbe81547117a77987bcedf5376608a6412067e04337047e0c7c839
  macrostructures/02-long-document.md    1722  8ca81106396f2bd00eb9ef5d5d1f00c3aab0500394e706d6a2b3221a6c0d910f
  macrostructures/05-workbench.md        1690  0cbe92772c7b2ffd9b24b9e446b1e1cd9ed22930b39030ef5a6e9cba5512d31f
  motion.md                              4340  330d056810315f65819579f8207afe402703a9192bc76a2009558a59b7c84ccf
  responsive.md                          5918  2bf18d72af704ca5dd3c220359a4c77c718efa19c40f62d9bff61ac4a90209b0
  slop-test.md                          31065  6eb49fc64ca54929d2c1600e2a6014268f1a7593787c0ed3f6ecb4ac8390ad86
  typography.md                         18381  94d7b2d2b138bd8687e09dc3dd618eaafff500b0497a6d69cb4c29b764e94b9c
  LICENSE                                1078  06088a8b94598626f27612dea42300154bf7be967c85d9d3eee4490cb056af7d

  Total: 15 files, 137,757 bytes.

Verification. Each file was fetched from
https://raw.githubusercontent.com/Nutlope/hallmark/13ac0ec7e148655948100b6396439e481361d690/
and its git blob SHA-1 was independently confirmed against the GitHub trees API at the same
commit. LICENSE has git blob SHA-1 f4bfc53d8d773d3b10d95c2d58a5773dd4e2f3aa in both. To
re-check any file later:

  curl -s https://raw.githubusercontent.com/Nutlope/hallmark/13ac0ec7e148655948100b6396439e481361d690/skills/hallmark/references/color.md | sha256sum

## Changes made to the copy

No file body was edited. The changes are structural:

1. This is a partial copy. 92 of the 107 files in the upstream skills/hallmark/ tree were not
   included, including the entry point skills/hallmark/SKILL.md. The list is below.
2. The directory was named design-rules rather than hallmark. The upstream name is recorded
   above and in ../NOTICE.md; it is not used as a label anywhere a learner can see.
3. LICENSE, this ORIGIN.md, ../NOTICE.md and ../OVERRIDES.md were added. They are ours, not
   upstream's. LICENSE is the upstream file, copied unchanged; the other three are ours.
4. Cross-references inside these files point at upstream files that are not present here.
   Ignore any link that resolves to a file not listed above. Do not fetch it. The dangling
   targets, measured: SKILL.md (linked as ../SKILL.md), assets.md, component-cookbook.md
   (also as ../component-cookbook.md), custom-craft.md, hero-enrichment.md,
   macrostructures.md, microinteractions.md, structure.md.

## Observations recorded rather than corrected

These are places where the planning document and the fetched bytes differ, or where a
vendored file needs handling. Nothing was edited to resolve them.

- slop-test.md is titled "58 gates" in its own first line, but its numbered gates run 1
  through 57 with no gate 58. That is an upstream inconsistency, not a truncated copy: the
  file is byte-identical to the pinned commit. Report 16 §1.2 repeats the file's own
  heading. Scope the gate set by number, not by count. The gates named in the plan are
  unaffected: 30 is emoji-as-icon, 46 is the invented metric (line 146), 47 is re-drawn
  chrome (line 152).
- interaction-and-states.md lines 94 and 95 print a warning glyph and a tick glyph in their
  worked error and success states. That is the sharpest collision with our no-verdict rule
  and it is live inside a file we vendored, not only in the dropped SKILL.md. See
  ../OVERRIDES.md, row O6.
- slop-test.md lines 40, 81 and 83 instruct the assistant to read .hallmark/log.json. We
  write no such file and no such directory. See ../OVERRIDES.md, rows O9 and O14.

## Files deliberately not included

  SKILL.md ................. the operating procedure. Replaced by ../../SKILL.md, which
                             routes to these files directly. See build-and-ground.md for
                             why the upstream flow is not followed. It is also an active
                             hazard: it instructs the assistant to interrogate the user
                             before designing, to write .hallmark/preflight.json and
                             .hallmark/log.json into the working directory, to stamp a
                             critique into the CSS, and to rotate layouts between builds.
  themes/ (5) .............. all 21 catalog themes load webfonts from a CDN.
  components/ (50) ......... nav, footer and hero archetypes. Our page has no nav, no
                             footer and no hero.
  macrostructures/ (19 of 21) .. landing-page shapes.
  macrostructures.md, component-cookbook.md, structure.md .. indexes for catalogs we dropped.
  genres/atmospheric.md, genres/playful.md .. registers we do not use.
  study.md, verbs/ (2) ..... the audit, redesign and study verbs.
  hero-enrichment.md, imagery-kit.md, assets.md, custom-craft.md .. imagery pipeline.
  custom-theme.md, design-md.md, export-formats.md, preview-examples.md,
  floating-nav.md, microinteractions.md .. see build-and-ground.md.

There is no file named SKILL.md anywhere under vendor/, and there must never be one. A
SKILL.md here would either be shadowed by the sub-skill above it or, worse, load as a
sibling skill and fire during mission work. Its absence is the safety mechanism.

## Modification policy

Do not edit the body of any file in this directory. An unmodified copy can be verified
against the pinned commit with one command; an edited one cannot. Where our rules differ,
add a row to ../OVERRIDES.md instead. If a body edit ever does become unavoidable, record
the file, the upstream SHA-256, our SHA-256, the exact lines changed and why, both here and
as a header comment in the file itself reading: Modified from upstream
13ac0ec7e148655948100b6396439e481361d690: one line saying what and why.
