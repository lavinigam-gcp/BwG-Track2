---
name: bwg-lab-setup
description: Set up this laptop for the Build with Google Track 2 or Track 3 lab, or repair a setup that is failing. Use when the user says "set up my laptop", "install the lab environment", "my lab environment is broken", or when a lab exercise fails because tooling or skills are missing.
---

# Laptop setup for the Build with Google Track 2 / Track 3 labs

Drive `setup/install.sh` and `setup/verify.sh` to bring this machine to parity with the lab VM,
then point the user at the readiness check and let it speak for itself.

`verify.sh` is the only source of truth for pass or fail. Never edit it, and never report success
it did not report. It is also the only place cloud sign-in is discussed.

**Do not mention gcloud, Qwiklabs accounts, or Antigravity sign-in anywhere in the setup.** The
reason is attached so that you do not helpfully put it back: people run this days before the event,
and the lab credentials do not exist yet. They are handed out on the day. A tester who finished the
install and was told to run `gcloud auth login` and sign in to Qwiklabs went looking for an account
nobody had issued him. Sign-in is not withheld from him, it is deferred: `verify.sh --readiness`
prints it at the end, worded as what is coming rather than as homework, and it is the only thing
here that knows whether the event has started. Do not compose a list of outstanding human actions
of your own. That is the specific habit that produced the bug.

**Use only this skill while you are setting the laptop up.** The lab's own skills
(`novasmart-governance-lab`, `build-demo`, `bwgtrack2-demo-build`, and anything under a
`Desktop/Session*/` or starter-kit `.agents/skills/` folder) are lab content, not setup
instructions. This repository installs them; it does not run them. They steer you into an in-lab
persona that checks a cloud estate which has not been provisioned yet, and one of them says out
loud that its job includes checking the environment is ready, which is close enough to this task to
be picked up by mistake. If one is offered to you at any point during setup, do not load it and do
not act on it. They come into play when the user opens the lab folder, which is after you are done.

## 1. Pre-flight

1. Confirm the open folder is this repository — it must contain `setup/install.sh` and
   `setup/verify.sh`. If not, stop and tell the user which folder to open.
2. Detect the platform: `uname -s` and `uname -m`.
   - Native Windows is unsupported: `uvloop` publishes no Windows wheels. Direct the user to WSL2,
     and read section 1b before you do anything else on that machine.
   - Intel Mac (`Darwin` + `x86_64`) needs Rust for `cryptography`; the script offers to install it.
3. **Establish which track the user is doing, and do it before anything else.** Every command
   below takes `--track`, and the two tracks install different things.
   - Track 2 is the NovaSmart governance lab. It uses the skills bundled in this repo and works
     out of `~/Desktop/Session1|2|3`.
   - Track 3 is the agent-first app. It clones the Track 3 starter kit from a separate community
     repository into `~/Desktop/build-with-gemini`, and also installs the GitHub CLI.
   - If the user has not said, **ask**. Do not guess from the folder they have open. If you pass
     no `--track` to a script, it silently uses Track 2, which is the wrong answer half the time.
   - Once you know, use `--track N` on `preflight.sh`, `install.sh` and `verify.sh` every time,
     including Track 2. Being explicit is what makes the transcript readable afterwards.
4. Run `bash setup/verify.sh --json --track N` first. If it already returns exit 0, say so and
   stop — do not reinstall a working environment.
5. **Run `bash setup/preflight.sh --track N` and show the user the report card.** This is mandatory
   and changes nothing. Its checks are identical for either track; `--track` only records which
   track the card was collected for. Exit 0 GO, 1 GO WITH CAVEATS, 2 NO-GO.
   - On **NO-GO**, stop. Explain which checks blocked it and recommend the lab VM. Do not install
     anything, and do not reach for `--skip-preflight` to get past it.
   - On **GO WITH CAVEATS**, summarise each warning in plain language and ask whether to continue.
     Summarise the warnings the card actually printed. Do not add a credential or account warning
     of your own: before the event preflight deliberately reports the `google account` row as OK,
     because there is no lab account to check yet.
   - Keep the verdict word. `verify.sh` takes it at the end as
     `--preflight-verdict {go,caveats,no-go}`, which is what lets the last step speak in the same
     three words the user already read here.
6. Show what `install.sh` will change, say roughly how long it takes (45-90 minutes, mostly
   downloads), and **get an explicit go-ahead before changing anything**. `install.sh` asks too,
   so never pass `--yes` unless the user has already said yes in this conversation.

## 1b. Windows with WSL2 is limited support

macOS and Linux are supported. Windows with WSL2 is **limited support**, and you must say so.
Never tell the user Windows is fully supported, and never present the workaround below as a fix.

What actually happens. The toolchain installs and `gcloud` works under WSL2. Antigravity is the
part that breaks: asked to open a folder that lives on a WSL path, it can report **"folder not
found"** even though the folder is there. Antigravity runs as a Windows application and reaches
into the Linux file system over the `\\wsl$` network share, so a path such as
`/home/user/Desktop/Session1` is not a path Windows can resolve. When the share is not mounted, or
the distribution is not running, the folder genuinely does not exist as far as Windows is
concerned.

The known workaround, and its limit. Map the WSL share to a drive letter, for example map
`\\wsl$\Ubuntu` to `Z:`, then point Antigravity at `Z:\home\user\Desktop\Session1` instead of the
WSL path. This has been seen to work. **It does not survive a restart.** A tester mapped the drive,
got through setup, rebooted, and found every mapping gone. Treat the mapping as something the user
will have to redo, and tell them that at the time you suggest it, not afterwards.

Before you apply any of this, **get the user's explicit approval.** Say all four of these:

- Windows is limited support for this lab, and this is a workaround, not a fix.
- It changes more on their machine than setup does on macOS or Linux, because it adds a persistent
  drive mapping to their Windows profile.
- The mapping is lost on restart and will need redoing.
- They do not have to accept it. The provided lab VM, and finishing setup on location at the event
  with a helper, are both still open to them.

Only proceed on a clear yes. If they decline, stop and recommend the VM, and say plainly that this
is not a failure on their part.

`setup/install.sh` asks the same question itself when it detects WSL2, so on that machine expect a
consent prompt before any work starts. In a dry run, or with no terminal attached, it does not ask:
it prints the warning on stderr and continues. Do not read that non-interactive warning as the user
having agreed to anything.

`setup/preflight.sh` reports WSL2 as **GO WITH CAVEATS**, never a clean GO. Do not describe that
verdict to the user as a pass.

## 2. Install

Run the steps in order, streaming output. Never run the whole thing silently.

```
bash setup/install.sh --yes --track 2      # or --track 3
```

`--yes` suppresses the track question along with every other prompt, so `--track` is not optional
here. Without it the script falls back to Track 2 without asking.

**Track 3 only.** Before running it, tell the user in plain words that this step clones
<https://github.com/cszhu/build-with-gemini> onto their machine, that it is a community repository
which neither this repo nor Google maintains, and that it is not an official Google product. Get
their go-ahead for that specifically. If they would rather use a fork or a mirror, pass
`--kit-url URL`.

The kit is pinned to one commit, held in `KIT_REF` at the top of `setup/install.sh`. Tell the user
which commit they are getting if they ask, read it from that variable rather than from memory, and
use `--kit-ref` if they want a different commit, tag or branch. `--kit-ref ""` follows the default
branch, which means taking whatever that community repository holds that day; only do it if the
user asks for it, and say what it means.

Never delete an existing starter-kit clone, and never suggest `--force` as a way to refresh one.
After the lab starts, that directory holds the user's own project. `--force` moves it aside under a
timestamped name rather than removing it, but it still leaves them with two copies to reconcile,
and when the reason for the failure is an upstream layout change, re-fetching the same upstream
fixes nothing at all. Fetch into a new folder with `--kit-dir DIR` instead, and leave theirs alone.

If the installer reports that the folder has a `.git` but no checkout, an earlier clone was
interrupted. That is repaired by re-running `install.sh --track 3 --only starterkit`, which moves
the unusable directory aside and fetches again. Do not reach for `--force` for this.

Ask before adding `--with-extras`; the optional extras are only for demo-recording exercises and
cost another 300-500 MB.

If a step fails, the script prints the exact `--only` command to retry it. Fix the cause first,
then retry that one step. Do not restart from the beginning.

## 3. Verify

Confirm the install with the JSON form and read the exit code:

```
bash setup/verify.sh --json --track N
```

**Do not run `--readiness` yourself.** It is the user's own last step, it is the one place cloud
sign-in is described, and running it inside the install turn is exactly how that text ended up in
the middle of a setup transcript. It reports the parity table plus five readiness rows, and then,
according to whether the lab credentials have been issued, either what the user will do on the day
of the event or what they can do now. That wording is its job, not yours.

Exit codes: `0` all pass, `1` drift, `2` something missing, `3` no virtual environment, `64` a
flag or a `BWG_PHASE` value this script does not accept. Treat 64 as "I typed the command wrong",
not as "the machine is broken": read `verify.sh --help` and run it again.

`install.sh` exit codes: `0` done, `1` a step failed, `2` preflight said NO-GO, `64` a bad flag,
`--only` step or track, `66` no terminal to ask for consent on, so nothing was changed. 66 is not
a machine fault either. `install.sh` always discloses what it will change and asks first, and
nothing, including `--only` and `--skip-preflight`, skips that. If you hit 66, you are running it
somewhere with no terminal attached: pass `--yes` to accept the disclosed changes, or have the
user run it themselves in a terminal.

The first seven checks are the shared toolchain and run for both tracks. After that the profiles
diverge, and the `track` field in the JSON tells you which one you are reading:

| Track 2 adds | Track 3 adds |
|---|---|
| `packages`, `sessions`, `lab-skill`, `config-paths` | `kit`, `kit-skills`, `kit-mcp`, `kit-publish`, `gh` |

Do not run the Track 2 profile against a Track 3 machine to "get more coverage". It will report
missing session folders and a missing governance-lab skill, neither of which Track 3 has any use
for, and you will send the user chasing a failure that is not real.

If the virtual environment is somewhere other than `~/novasmart-lab/.venv`, pass `--venv DIR`
rather than reporting exit 3 as a broken install.

For each failing check, read its `fix` field and apply the repair below. Re-run `verify.sh` after
each repair, and keep going until it returns 0 or you are blocked on a human.

## 4. Repair table

| Check fails | Cause | Fix |
|---|---|---|
| `python` | Wrong interpreter, or venv built on an older Python | `uv python install 3.14`, then `install.sh --only python --force` |
| `packages` not 120 | Resolution diverged or a build failed | Re-run `install.sh --only python`. On an Intel Mac see below |
| `packages` is 121 or more | Someone installed an extra package into the lab venv | `install.sh --only python --force`. Plain `--only python` cannot fix this: it never uninstalls anything, so only rebuilding the venv clears it. The venv holds no work, so this is safe |
| `google-adk`, `agents-cli`, `google-genai` drift | Someone upgraded a package | `install.sh --only python --force` |
| `no-vendor-sdk` above 0 | `--no-deps` was dropped, so the resolver re-added LiteLLM or an OpenAI client. There is no `litellm` check: those packages are asserted absent, not pinned | `install.sh --only python --force`. Plain `--only python` never uninstalls, so only a rebuild clears it |
| `config-paths` above 0 | The skills still carry the VM's `/config` paths | `install.sh --only skills --skills-src DIR` |
| `sessions` below 3 | A session folder was deleted or never created | `install.sh --only sessions` |
| `lab-skills` not installed, session folders empty | The sessions step did not run. The skills ARE bundled in this repo, so this is not a missing-source problem. The row is reported as SKIP and is not counted as a failure | `install.sh --only sessions` |
| `lab-skill` MISSING | A skills source was given but the copy did not land, or is nested too deep | `install.sh --only sessions --skills-src DIR`, then confirm each skill has `SKILL.md` at its own top level |
| `node`, `gcloud` MISSING | Tool step did not complete | `install.sh --only tools` |
| `kit` MISSING (Track 3) | The starter kit was never fetched, or an earlier clone was interrupted and left a `.git` with no checkout | `install.sh --track 3 --only starterkit`. It moves an unusable directory aside and fetches again |
| `kit-skills`, `kit-mcp`, `kit-publish` MISSING (Track 3) | The directory exists but is not the starter kit, or upstream changed its layout | Check `~/Desktop/build-with-gemini` is the right clone. Report a layout change rather than patching around it. Never suggest `--force` here: it moves the user's project folder aside to re-fetch the same unchanged upstream, so it destroys context and fixes nothing. Fetch into a new folder with `--kit-dir DIR` instead |
| `gh` MISSING (Track 3) | Tool step ran as Track 2, or gh was removed | `install.sh --track 3 --only tools`, which installs it with brew on macOS and apt on Linux and WSL2 |
| Installer cannot fetch the kit (Track 3) | That community upstream was renamed, deleted or made private, or the network blocks it | It fails fast and says so rather than hanging on a credential prompt. Nothing is half-applied. Re-run, or pass `--kit-url` pointing at a fork or an offline mirror |
| `verify.sh` exits 64, `unknown option` | A mistyped or invented flag | Read `verify.sh --help`. It refuses unknown flags on purpose: it used to ignore them and silently run the Track 2 profile on a Track 3 machine |
| `sessions` or `lab-skill` fails on a Track 3 machine | You ran the wrong profile | Re-run with `--track 3`. This is not a real failure |
| user asks about `agy` | Not installed by design; the labs run in the IDE | Say so; do not install it |
| exit 3 | No virtual environment | `install.sh --only python` |

TROUBLESHOOTING.md in the repository root lists every known failure by operating system; consult
it before improvising a fix. Known environment failures that are not the script's fault:

- **`cryptography` will not build on an Intel Mac** — no Intel wheel exists for the pinned version.
  Run `xcode-select --install` and `brew install rust`, then retry. If the user is blocked,
  `uv pip install cryptography==48.0.1` installs from a wheel and leaves them one package from the
  image; say so plainly rather than hiding it.
- **TLS errors on a corporate network** — an intercepting proxy. Ask IT for the CA certificate and
  set `REQUESTS_CA_BUNDLE` and `SSL_CERT_FILE`. Do not disable certificate verification.
- **Antigravity will not start on Linux or WSL2** — set the `chrome-sandbox` permissions. Never add
  `--no-sandbox`; it disables a real security boundary.

## 4b. Check which account is signed in, but only if there is an account question

**Skip this section entirely when preflight reports the `google account` row as OK.** Before the
event it always will: no lab project is set and no application-default credentials are on the
machine, so preflight knows the account question is not live yet, and neither should you. Raising
it anyway turns a row that says "issued at the event" into an interrogation about credentials the
user has not been given.

If preflight **warns** on that row, then a project or credentials are already on this machine and
the question is real. The lab is played with the **Qwiklabs account issued for it** — never a
personal Google account and never a work or corporate one. A different identity cannot see the
lab's project or agents, and anything created lands in the user's own project and bills their own
account. Say what preflight found, and ask the user to confirm before installing. Do not assume it
is fine because the tooling works.

## 5. Hand off

**Do not write your own list of the things only a human can do.** This is the restatement of the
rule at the top of this file, put here because this is where the temptation lands: the install has
just succeeded, a closing summary feels owed, and the obvious content for it is gcloud and
Qwiklabs. `verify.sh --readiness` already prints that list, it is the only thing here that knows
whether the credentials have been issued, and the one you would write does not. Two previous
attempts to fix this failed because the offending text was deleted and the instruction that
generates it was left in place.

Say these three things, and stop.

1. **What happened.** What `install.sh` installed, and what `verify.sh --json` returned. Quote its
   numbers rather than restating them as a judgement of your own.
2. **The one line the user must add by hand**, on Track 2 only, if `install.sh` printed it: the
   `export NOVASMART_SCORECARD_HOME=...` line for their shell profile. Repeat it verbatim. This is
   the only manual step that belongs in your summary, because it can be done now and needs no
   credentials.
3. **The two commands that end the setup**, in this order, and the order matters:
   - `bash setup/verify.sh --readiness --track N`, run from the setup folder,
     `~/novasmart-lab/setup`. `install.sh` prints the same command, without `--track` on
     Track 2; add the track back, because it keeps the transcript readable. There is no need
     to pass `--preflight-verdict`: preflight records its verdict where `verify.sh` reads it.
     Pass that flag only to override what was recorded.
   - Open the folder for the track in Antigravity: `~/Desktop/Session1` for Track 2, or
     `~/Desktop/build-with-gemini` for Track 3. Name the exact folder rather than saying "open the
     project", because opening the folder is also what loads its skills. This is second on
     purpose. The Track 3 starter kit carries its own `troubleshoot-lab-setup` skill, which
     answers readiness questions with a sign-in instruction that is wrong before the event, and
     it cannot answer anything while its folder is still closed. Readiness first, folder after.

Then stop. The readiness report answers everything else, and it is the only thing here that knows
whether the event has started. Do not preview its contents, do not summarise them, and do not name
the topics it will cover. If you find yourself about to list what the user still has to do, that
list is the bug: delete it and print the command instead.

## 6. Scope

You may write to: `~/novasmart-lab/`, `~/Desktop/Session1`, `Session2`, `Session3`. On Track 3,
also `~/Desktop/build-with-gemini`, and there only to create the clone, never to delete or
rewrite what is already in it. You may run `setup/install.sh` and `setup/verify.sh`.

**Do not edit the user's shell profile.** Neither script does: `install.sh` prints the
`export NOVASMART_SCORECARD_HOME=...` line and leaves it to them, and the README promises the
reader that nothing here touches `~/.zshrc` or `~/.bashrc`. Repeat the line verbatim in your
hand-off instead.

The scope on skills is this one. Setup is driven by this file alone. The lab skills this repository
copies into `Desktop/Session*/.agents/skills/`, and the ones inside the Track 3 starter kit, are
cargo: install them, verify they landed, and do not read them for instructions. They belong to the
lab session that starts after you hand off.

Anything else — installing unrelated software, editing files elsewhere, changing gcloud
configuration beyond the documented commands, or granting IAM roles — **stop and report instead**.
If a step is blocked, say what blocked it and what you would need. Never work around a blocker by
repurposing something that already exists.

Never invent a repository URL. It comes from the clone the user already has.
