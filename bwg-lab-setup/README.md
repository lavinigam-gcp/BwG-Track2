# bwg-lab-setup

Set up a personal laptop with the software stack for the Build with Google **Track 2 and Track 3**
labs, so you can run them without the provided cloud VM. macOS and Linux are supported. Windows
via WSL2 is on limited support.

Windows is **limited support**. It is not unsupported, but it is not a peer of macOS and Linux
either: Antigravity has been seen to fail to open folders on WSL paths, and the known workaround
does not survive a restart. Read [Windows with WSL2](#windows-with-wsl2) before you start.

Pick your track with `--track 2` or `--track 3`. Without the flag the installer asks, and falls back
to Track 2 when there is no terminal to ask on. See [Which track](#which-track).

---

## Before you run anything

**This is not an officially supported Google product.** It is a personal project. Google does not
create, endorse, sponsor, support, or maintain it, nothing in it represents the views of Google, and
no Google warranty or support commitment applies.

**Use the lab-provided VM if you can.** It is the supported, tested environment for this lab. This
repository is for people who are comfortable administering their own machine, have read these
scripts, and accept the risks of running them.

**These scripts change your computer.** They install system packages, add third-party package
repositories and signing keys, download and run installer scripts from the internet, and create and
delete directories under your home directory. They do not edit your shell profile: Track 2 prints
one `export` line for you to add yourself. On Linux and
WSL2 they use `sudo`, so they run with administrative privileges. Run
`bash setup/install.sh --dry-run` to print every command first, and back up anything you cannot
afford to lose before you begin.

**Versions are pinned and not maintained.** This repository is not monitored for security advisories
and has no update mechanism. If a pinned package is later found to be vulnerable, you will get no
notice here. Checking these pins against current advisories, and patching your machine afterwards,
is your responsibility.

**You run this at your own risk.** The software is provided "AS IS", without warranties or conditions
of any kind. To the maximum extent permitted by law, neither the author nor any contributor is liable
for any loss or damage that follows from using it, or from being unable to use it. See
[LICENSE](LICENSE) for the governing terms.

---

Everything is pinned to a reference environment. Verified 19 August 2026.

## Which track

Both tracks share the same toolchain: Python 3.14, the pinned package set, the Google Cloud CLI,
Node.js 24, and the `agents-cli` lifecycle skills. What differs is the lab content.

| | Track 2 | Track 3 |
|---|---|---|
| Lab | NovaSmart governance lab | Agent-first app on Google Cloud |
| Command | `bash setup/install.sh --track 2` | `bash setup/install.sh --track 3` |
| Lab content | The skills bundled in this repo's `skills/` | The Track 3 starter kit, cloned from GitHub |
| Where you work | `~/Desktop/Session1`, `Session2`, `Session3` | `~/Desktop/build-with-gemini` |
| Also installs | none | The GitHub CLI (`gh`), which the kit needs to publish your project. `brew` on macOS, `apt` on Linux and WSL2 |
| Third-party code | none | The starter kit, pinned to one commit. `--kit-ref` changes it |
| Verify with | `bash setup/verify.sh --readiness` | `bash setup/verify.sh --readiness --track 3` |
| Checks run | 11 | 12 |

If you do not pass `--track`, the installer asks you. When nothing can ask you, such as a pipe, a CI
job, or `--dry-run`, it sets up **Track 2** and says so on stderr. Track 2 is unchanged in every
respect for anyone who does not pass the flag.

### About the Track 3 starter kit

Track 3 works out of a starter kit that lives in a **separate community repository**,
<https://github.com/cszhu/build-with-gemini>. It is **not** part of this repository, it is **not**
maintained by this repository's author, and like this repository it is **not an official Google
product**. `install.sh --track 3` clones it as-is. It does not vendor it, patch it, or review it for
you. Read that repository before you run anything it ships, exactly as you should read this one.

You can point somewhere else with `--kit-url URL`, for example at your own fork or an offline
mirror, and change where it lands with `--kit-dir DIR`.

**The kit is pinned to one commit.** Taking whatever sits on somebody else's default branch on the
morning of a lab is not something this repository is willing to do, so `install.sh` fetches a single
commit that has been rehearsed against. The pin is the `KIT_REF` variable at the top of
`setup/install.sh`, next to `KIT_URL`, with a comment recording what it is and how to bump it. To
use a different one, pass `--kit-ref COMMIT`, `--kit-ref TAG` or `--kit-ref BRANCH`. To go back to
following the default branch, pass `--kit-ref ""`, and the installer will say out loud that it is
taking whatever is there today.

The clone is treated as **yours** from the moment it exists, because that is where you build your
project. Re-running the installer leaves an existing clone alone, including when the pin has since
moved: it tells you the two differ and changes nothing. Even `--force` does not delete anything. It
moves the old directory aside with a timestamped name, says where it went, and fetches a fresh one
next to it. Prefer `--kit-dir DIR` to fetch a clean copy somewhere else and keep your work where
it is.

You do **not** need to run anything to register the kit's skills. Antigravity reads the `.agents/`
folder of whatever workspace you open, so opening the cloned folder is what loads them.

## Three ways to do this

Pick one. They produce the same environment, and `setup/verify.sh` checks all three the same way.

| | Path | Best for |
|---|---|---|
| **A** | [Ask the assistant](#a--ask-the-assistant) | You have Antigravity and want it driven for you |
| **B** | [Run the scripts](#b--run-the-scripts) | You want automation without an agent |
| **C** | [Do it by hand](manual_setup.md) | You want to see and approve every command |

Something not working? **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**.

---

## A — Ask the assistant

Clone the repository, open **that folder** in Antigravity, and say:

> **Set up my laptop for the lab.**

Or do it in one step, pasting the repository URL into the prompt:

> **Set up my laptop for the lab. Everything you need is at
> https://github.com/lavinigam-gcp/bwg-lab-setup — clone it and follow its setup process.**

Both work; the one-step version has been run on macOS with Gemini 3.8 Flash. The two-step version is
marginally safer, because Antigravity loads skills when a session **starts** — a repository cloned
mid-session has its `SKILL.md` read as an ordinary file rather than loaded as steering. Clone first,
open the folder, then prompt if you want the skill fully in force.

Either way the assistant runs preflight, shows you the report card, lists exactly what it will
change, and **waits for your go-ahead** before installing anything.

---

## B — Run the scripts

**Step 1 — check your laptop can do this.** Nothing is installed by this step.

```bash
git clone https://github.com/lavinigam-gcp/bwg-lab-setup.git ~/novasmart-lab/setup
cd ~/novasmart-lab/setup
bash setup/preflight.sh
```

You get a report card and one of three verdicts:

| Verdict | Meaning |
|---|---|
| **GO** | Your laptop is suitable. Continue to step 2. |
| **GO WITH CAVEATS** | It will probably work. Read the warnings — if any look serious for your machine, use the lab VM instead. |
| **NO-GO** | Something is missing that cannot be worked around. Fix it, or use the lab VM. |

Preflight checks your OS and version, CPU architecture, cores, memory, free disk, required tools,
and whether you can actually reach GitHub, PyPI, Google Cloud and the Antigravity download — plus
whether a corporate proxy is intercepting TLS, which breaks installers in confusing ways.

**Step 2 — install.** This changes your machine, so it runs preflight again and asks first.

```bash
bash setup/install.sh --dry-run     # optional: see every command it would run
bash setup/install.sh               # asks which track, then installs it
```

Or name the track up front, which is what you want in a script or over a slow link:

```bash
bash setup/install.sh --track 2     # NovaSmart governance lab
bash setup/install.sh --track 3     # agent-first app, with the Track 3 starter kit
```

**Step 3 — confirm you are ready.** Use the same track you installed. Run this from the
setup folder, in a terminal:

```bash
cd ~/novasmart-lab/setup
bash setup/verify.sh --readiness              # Track 2
bash setup/verify.sh --readiness --track 3    # Track 3
```

Run it as a command rather than asking the assistant, and run it before you open the lab
folder. On Track 3 the starter kit ships a skill of its own called `troubleshoot-lab-setup`,
which answers questions like "am I ready to start" and tells you to sign in to Google Cloud.
That skill belongs to the lab, not to setup, and before the event there is nothing to sign
in with. Running the command yourself avoids the question entirely and gives you the
readiness report itself rather than a summary of it. If you would rather ask the assistant,
ask it with the SETUP folder open, not the lab folder.

`verify.sh` checks the shared toolchain for both tracks, then the part that belongs to your track:
session folders and the governance-lab skill for Track 2, the cloned starter kit and `gh` for
Track 3. It never reports a Track 2 requirement as a failure on a Track 3 machine, or the reverse.

---

## C — Do it by hand

Every command, step by step, with no scripts: **[manual_setup.md](manual_setup.md)**.

It is derived from `setup/install.sh` and runs the same commands in the same order, so it produces
the same environment. Use it if you want to approve each step yourself, if the installer will not
run on your machine, or if you simply want to understand what it does.

## Prerequisites

- **Antigravity IDE** — install it yourself from <https://antigravity.google/download>. It is the
  editor the labs run in, so it cannot install itself. The separate `agy` command line tool is
  **not** installed and is not needed: the labs are played in the IDE and nothing in them calls it.
- **On the day of the event, sign in to Antigravity with the Qwiklabs account issued for this
  lab.** Not your personal Google account, and not your work or corporate account. That account is
  handed out at the event, so there is nothing to do here beforehand. See
  [Which account to use](#which-account-to-use).
- macOS 13+, or a Linux with glibc 2.28+ (Ubuntu 20.04+ / Debian 10+). Windows 10 build 19044+
  with WSL2 and WSLg also works, on limited support: see [Windows with WSL2](#windows-with-wsl2)
- 8 GB RAM minimum, 16 GB recommended · 15 GB free disk · 4 CPU cores recommended
- Homebrew on macOS
- **Track 3 only:** a GitHub account, to publish your finished project. The GitHub CLI (`gh`)
  itself is installed for you by `--track 3`; you do not need it beforehand.

Native Windows is **not supported**: a required package (`uvloop`) publishes no Windows builds.
Use WSL2, and read the section below first.

## Windows with WSL2

Windows runs this lab on **limited support**. The toolchain installs and `gcloud` works. The part
that has been seen to fail is Antigravity.

- **Known failure.** Antigravity can report **"folder not found"** for a folder on a WSL path that
  is plainly there. Antigravity is a Windows application and reaches the Linux filesystem over the
  `\\wsl$` network share, so `/home/you/Desktop/Session1` is not a path Windows can resolve.
- **Known workaround, with a real limit.** Mapping the WSL share to a drive letter, for example
  `\\wsl$\Ubuntu` to `Z:`, and opening `Z:\home\you\Desktop\Session1` instead, has worked. **The
  mapping does not survive a restart.** One tester rebooted and found every mapping gone. Expect to
  redo it. This is a workaround, not a fix.
- **Fallbacks, both fine.** Finish your setup on location at the event with a helper, or use the
  provided lab VM, which does not have this problem.

`setup/preflight.sh` reports WSL2 as `GO WITH CAVEATS`, never a clean `GO`. `setup/install.sh`
tells you the above and asks you to agree before it changes anything on a WSL2 machine. Full
detail is in [TROUBLESHOOTING.md](TROUBLESHOOTING.md#wsl2).

## Which account to use

**Use only the Qwiklabs account you were given for this lab**, in Antigravity and in `gcloud`. Do not use a personal Google account, and do not use a work or corporate account.

Why this matters:

- The lab's cloud project, its agents, and its permissions all belong to the issued account. A
  different identity will not see them, and the exercises will fail in ways that look like broken
  tooling rather than a wrong login.
- Signing in with a corporate account can apply your organisation's policies to the session, and may
  route lab activity through accounts and audit logs that have nothing to do with the lab.
- Anything the lab creates while you are signed in as yourself lands in **your** project, and any
  charges land on **your** billing account.

**None of this can be done before the event.** The Qwiklabs account is handed to you on the
day, so there is nothing to sign in with yet. `verify.sh --readiness` tracks where the
sign-in stands and tells you when it is time. What follows is for the day itself.

On the day, confirm all three agree:

```bash
gcloud auth list                  # the active account must be the lab account
gcloud config get-value project   # must be the lab project
                                  # then check Antigravity's own signed-in account in the IDE
```

If you are already signed in as someone else, sign out of Antigravity first, and use a separate
gcloud configuration for the lab so you do not disturb your normal setup:

```bash
gcloud config configurations create lab
gcloud auth login                 # the lab account
gcloud auth application-default login
```

On the day of the event, `setup/preflight.sh` warns if the active account does not look like a lab
account. It cannot tell for certain, so the check is yours to make. Before the event it reports
your own account without comment, because a personal account a week out is expected and there is
nothing you can do about it until the lab credentials exist.

## What gets installed

| | Version | Required |
|---|---|---|
| Python | 3.14 | yes |
| Python packages | 120, pinned in `setup/requirements-lock.txt` | yes |
| Google Cloud CLI | current | yes |
| The Track 2 lab skills | bundled in `skills/` | Track 2 |
| The Track 3 starter kit | cloned from a community repo | Track 3 |
| GitHub CLI (`gh`) | current | Track 3 |
| Node.js | 24 | no — parity with the reference image |
| ffmpeg, VS Code, Playwright's browser | current | no — `--with-extras` |

Roughly 850 MB of downloads, 45–90 minutes, mostly waiting.

## Command reference

```
setup/preflight.sh [--json] [--track {2,3}]
  --track {2,3}      recorded on the report card and in the saved verdict. It changes
                     nothing that is measured: every check is the same for either track
  exit 0 GO · 1 GO WITH CAVEATS · 2 NO-GO · 64 bad flag
  Records its verdict in ~/novasmart-lab/preflight-verdict, which verify.sh reads.

setup/install.sh [options]
  --track {2,3}      which track to set up. Without it the installer asks, and
                     falls back to Track 2 when there is no terminal to ask on
  --dry-run          print every command, change nothing (never asks for a track)
  --only STEP        run one step: tools python skills sessions register starterkit
  --with-extras      also install ffmpeg, VS Code, Playwright's browser
  --force            rebuild an existing virtual environment or session folders.
                     On Track 3 it also moves an existing starter-kit folder aside,
                     with your work in it, and fetches the kit again
  --yes              do not prompt (does NOT override a preflight NO-GO)
  --skip-preflight   do not run preflight first
  --root DIR         parent of Desktop/SessionN (default: $HOME)
  --skills-src DIR   use lab skills from elsewhere instead of the bundled copy
  --kit-dir DIR      Track 3: where to put the starter kit
  --kit-url URL      Track 3: the starter kit repository, a community repo
  --kit-ref REF      Track 3: the commit, tag or branch to check out. Empty
                     follows the default branch instead of the pin
  exit 0 done · 1 a step failed · 2 preflight NO-GO · 64 bad flag, step or track
       · 66 no terminal to ask for consent on, nothing changed
  It always says what it is about to change and asks before it changes it. With
  no terminal to ask on it stops and exits 66. --only, --skip-preflight and
  BWG_TRACK do not get past that; a terminal or --yes does. See TROUBLESHOOTING.md.

setup/verify.sh [--json] [--fix-hints] [--readiness] [--track {2,3}]
                [--root DIR] [--lab-home DIR] [--venv DIR] [--kit-dir DIR]
                [--preflight-verdict {go,caveats,no-go,unknown}]
  --preflight-verdict  what preflight.sh said earlier, in its own three words.
                       Changes only the readiness text, never the exit code.
                       You do not normally need this: preflight records its
                       verdict and verify.sh reads it. Pass it to override that
  exit 0 all pass · 1 drift · 2 missing · 3 no virtual environment · 64 bad flag

Environment variables, for both scripts:
  BWG_TRACK    2 or 3, the same as --track
  BWG_PHASE    pre-event or day-of, overriding how the scripts decide whether
               your lab credentials have been issued. They decide it from the
               active gcloud project: a project id starting with qwiklabs-gcp-
               means the event has started, and anything else means it has not.
               Set this only if that is wrong for you, for example during a
               rehearsal on a project that is not a Qwiklabs one. Anything other
               than those two words exits 64
```

The Python set is installed with `--no-deps`, because `requirements-lock.txt` is the complete
resolved environment. Without that flag the resolver re-adds packages that were deliberately
removed — `google-agents-cli` hard-requires `google-cloud-aiplatform[evaluation]`, whose extra pulls
in LiteLLM and an OpenAI client that nothing in these labs uses — and it adds them unpinned.

`install.sh` is idempotent — re-running a finished step does nothing. If a step fails it prints the
single `--only` command that retries just that step.

## What this cannot do for you

Installing Antigravity, its sign-in wizard, `gcloud auth login`, granting your IAM roles, and
provisioning the Google Cloud project all need a human. Run `verify.sh --readiness` and it will
tell you where each of those stands.

**None of them can be done before the event.** The Qwiklabs account, the project ID and the IAM
roles are all issued to you on the day. If you are setting this laptop up in advance, the cloud
side is not your homework, and `verify.sh --readiness` will say so: it reports the sign-in as
expected-for-now and describes what you will do at the event rather than listing it as a task. If
you pass it `--preflight-verdict no-go`, it stops describing sign-in altogether and tells you to
use the provided lab VM or ask for a loaner laptop, which on a machine that failed preflight is the
only useful answer.

Note that a correctly set up laptop will still fail every lab exercise until the **Google Cloud
project** has been provisioned by your lab administrator. That is expected, and separate from
anything here.

### Which "step 6"?

Three numbering schemes overlap in this material and they are not the same list. The attendee
landing page numbers the whole day 1 to 6 and its step 6 is the readiness check. Path B above has
its own three steps. [manual_setup.md](manual_setup.md) has seven, and **its** Step 6 is the
`gcloud auth login` block, which is an event-day step and not the readiness check. If someone tells
you "the cloud sign-in happens at step 6", they mean the readiness check tells you about it, not
that you should open the manual walkthrough and authenticate now. When in doubt, name the command
rather than the number.

## Testing status

| Platform | Status |
|---|---|
| Linux x86_64 | Tested — preflight, dry run, real run, idempotency, failure injection, repair loop |
| Windows + WSL2 | **Limited support.** Same code path as Linux for the toolchain, and a tester confirmed the toolchain and `gcloud` work. Antigravity failed to open folders on WSL paths for him; a drive-letter mapping worked around it and was then lost on restart. Not run end to end on Windows |
| macOS (Apple Silicon) | Preflight and the assistant flow confirmed on macOS 26.6.2 / arm64 with Gemini 3.8 Flash — report card correct, account warning correct, approval gate held. The install itself not yet completed end to end |
| macOS (Intel) | Not yet run |

Intel Macs need Rust and the Xcode command line tools, because the pinned `cryptography` version no
longer publishes an Intel wheel. `install.sh` detects this and offers to install them.

Problems: **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** covers every failure we have seen, by
operating system. Undoing it all, or rehearsing the setup from a clean machine, is
**[Reset this laptop for a re-test](TROUBLESHOOTING.md#reset-this-laptop-for-a-re-test)**: it
lists exactly what the installer creates per track and the minimal commands to remove it.
Re-running `install.sh` on a machine that is already set up is safe, so you rarely need it.
See [CONTRIBUTING.md](CONTRIBUTING.md) for what to include in an issue.
Licensed under [Apache 2.0](LICENSE).
