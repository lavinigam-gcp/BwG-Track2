# Troubleshooting

Every failure we have seen, across macOS, Linux and WSL2, with the cause and the fix.

---

## Start here

Two commands answer most questions. Both are read-only.

```bash
bash setup/preflight.sh                      # can this machine do it at all?
bash setup/verify.sh --fix-hints --track 2   # what is wrong with the current install?
```

**Pass the track you set up.** `verify.sh` defaults to Track 2, and the Track 2 profile looks for
things a Track 3 machine has no reason to have. Running it against Track 3 reports missing session
folders and a missing governance-lab skill, and neither is a real problem. Use `--track 3` and the
Track 3 profile instead. `preflight.sh` also takes `--track`, but only to record it on the report
card: every check it runs is the same for either track.

`--fix-hints` prints the exact `install.sh --only …` command for each failing check. Fix the cause,
re-run that one step, re-verify. **Do not start over** — `install.sh` is idempotent and re-running a
finished step does nothing.

### Exit codes

| Script | 0 | 1 | 2 | 3 | 64 | 66 |
|---|---|---|---|---|---|---|
| `install.sh` | done | a step failed | preflight said NO-GO | — | bad flag, bad `--only` step, or bad track | no terminal to ask for consent on, nothing changed |
| `preflight.sh` | GO | GO WITH CAVEATS | NO-GO | — | bad flag or bad `BWG_PHASE` | — |
| `verify.sh` | all pass | drift | something missing | no virtual environment | bad flag or bad `BWG_PHASE` | — |

**About `install.sh` exit 66.** `install.sh` never changes a machine without disclosing what it is
about to do and getting a yes. When it is run with no terminal attached, for example through a
pipe, under `nohup`, or from an automated rehearsal, there is nothing to ask on, so it prints
`Stopped. Nothing was changed.` and exits 66 before any step runs. The same thing happens on WSL2,
where the limited-support notice is its own consent question. Two ways past it, both deliberate:
run it from a terminal and answer the prompt, or pass `--yes` to accept the disclosed changes in
advance. `--only`, `--skip-preflight` and `BWG_TRACK` do not get you past it: they change what runs
or whether the machine is assessed first, never whether you were asked. A dry run
(`install.sh --dry-run`) changes nothing, so it never asks and never exits 66.

---

## The five most common

**`agents-cli: command not found`, or `python` is the wrong version.**
The virtual environment is not active. Run `source ~/novasmart-lab/.venv/bin/activate`. You need
this in **every new terminal** — it is not permanent, by design.

**`packages` is not 120.**
The Python install diverged, almost always a missing `--no-deps`. `requirements-lock.txt` is the
complete resolved set; without the flag the resolver adds more, unpinned.
Fix: `bash setup/install.sh --only python --force`.

**`no-vendor-sdk` is above 0.**
LiteLLM or an OpenAI client came back. Same cause as above: `google-agents-cli` hard-requires
`google-cloud-aiplatform[evaluation]`, and that extra pulls them in whenever the resolver is allowed
to run. Same fix.

**An exercise writes a file and it is nowhere to be found.**
The skills still contain `/config` paths — the home directory *inside the lab VM's container*, which
does not exist on your machine. Check with:

```bash
grep -rlE '(^|[[:space:]`"(])/config([^a-zA-Z]|$)' ~/Desktop/Session1/.agents/skills
```

Fix: `bash setup/install.sh --only skills`. This can come back after a `git pull`.

**Everything installs cleanly but the lab exercises find nothing in Google Cloud.**
Expected, and not a setup problem. The lab's agents, datasets and gateways live in a Google Cloud
project that has to be provisioned separately. Ask your lab administrator. See
[Expected failures](#expected-failures).

**`node` or `gcloud` reported MISSING by verify.**
The tools step did not complete, or the binary is not on `PATH` in this shell.
Fix: `bash setup/install.sh --only tools`, then open a new terminal. On macOS also see the keg-only
note below.

**Looking for `agy`?** It is not installed and not needed — the labs run in the Antigravity IDE and
nothing in them calls the CLI. Install it separately if you want a terminal client.

---

## macOS

**`cryptography` fails to build (Intel Macs).**
The pinned version no longer publishes an Intel wheel, so it compiles from source and needs Rust:

```bash
xcode-select --install
brew install rust
bash setup/install.sh --only python
```

If you are blocked and need to move on, `uv pip install cryptography==48.0.1` installs from a wheel.
You are then one package away from the reference environment — acceptable for learning, and worth
knowing rather than discovering later.

Apple Silicon is unaffected.

**`node: command not found` right after installing it.**
`node@24` is keg-only in Homebrew, so it is not linked into `PATH`:

```bash
echo 'export PATH="'"$(brew --prefix)"'/opt/node@24/bin:$PATH"' >> ~/.zshrc
exec zsh
```

Use `~/.bash_profile` if your shell is bash, not `~/.bashrc`.

**`Homebrew is required on macOS`.**
Install it from <https://brew.sh> and re-run.

**Antigravity will not open, or macOS blocks it.**
Open it once from Applications by hand so macOS records your approval, then retry.

**Rosetta.** If you are on Apple Silicon but running an x86_64 shell under Rosetta, `uname -m`
reports `x86_64` and you will get Intel wheels on an ARM machine. Preflight detects the real
architecture via `sysctl`, so trust its report over `uname`.

---

## Linux

**The install hangs with no output during the tools step.**
`DEBIAN_FRONTEND` is not reaching `apt`. `sudo` runs with `env_reset` and strips it, so `tzdata`
opens an interactive prompt and waits forever. Every `apt-get` call must carry it explicitly:

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y …
```

The scripts already do this. If you are following the manual steps, do not drop it. To confirm this
is what is happening: `ps -eo etime,cmd | grep -i debconf`.

**`Antigravity will not start`, mentions sandbox.**
Set the sandbox permissions rather than disabling it:

```bash
AG_DIR=$(ls -d /opt/antigravity/Antigravity-*/ | head -1)
sudo chown root:root "${AG_DIR}chrome-sandbox"
sudo chmod 4755 "${AG_DIR}chrome-sandbox"
```

**Never add `--no-sandbox`.** It is the advice you will find online and it disables a real browser
security boundary.

**`glibc 2.28+` FAIL in preflight.**
Antigravity will not launch on older glibc. This is not workaroundable — upgrade the distribution or
use the lab VM.

**Google Chrome will not install on arm64.**
Google publishes no arm64 `.deb`. Chrome is optional; any browser works for sign-in.

---

## WSL2

Windows with WSL2 is **limited support**, not a peer of macOS and Linux. The toolchain and
`gcloud` do work here. Antigravity is the part that has been seen to fail, and the only known
workaround for it is not durable. Preflight reports WSL2 as `GO WITH CAVEATS`, never a clean `GO`,
and `install.sh` asks you to agree to the limitations before it changes anything.

**Antigravity says "folder not found" for a folder that is there.**
This is the known Windows failure. Antigravity is a Windows application and reaches into the Linux
filesystem over the `\\wsl$` network share, so a WSL path such as `/home/you/Desktop/Session1` is
not something Windows can resolve on its own. If the share is not mounted, or the distribution is
not running, Windows concludes the folder does not exist.

The known workaround is to map the WSL share to a drive letter. In File Explorer, Map network
drive, `\\wsl$\Ubuntu` (use your own distribution name), pick a letter such as `Z:`, then open
`Z:\home\you\Desktop\Session1` in Antigravity instead of the WSL path.

**The drive mapping does not survive a restart.** This is not a solved problem. A tester mapped the
drive, finished setup, rebooted, and found the mapping gone. Plan on redoing it after every
restart, and do not treat the first success as the end of it.

If that is not acceptable, both fallbacks are legitimate and neither is a failure on your part:

- Finish your setup on location at the event, where a helper can work through it with you.
- Use the provided lab VM, which has none of this problem.

Do not spend event time fighting this. If you are on Windows and the clock is short, take the VM.

**Antigravity does not open at all.**
WSLg is missing. In PowerShell run `wsl --version`. If the command is unrecognised, you have the
older in-box WSL — install WSL from the Microsoft Store and restart.

**Preflight reports plenty of free disk, but the install fails with no space.**
WSL2's virtual disk is allocated up to 1 TB by default, so `df /` is fiction. The real space is on
Windows. Check `df -h /mnt/c` — preflight does this too and fails if `C:` is short.

**Preflight reports about half the RAM the machine has.**
Expected. WSL2 defaults to 50% of host memory. Raise it in `%UserProfile%\.wslconfig`:

```ini
[wsl2]
memory=12GB
```

Then `wsl --shutdown` and reopen.

**Everything is very slow, and file changes are not noticed.**
Your working directory is under `/mnt/c/`. Move it into the Linux filesystem (`~/novasmart-lab`,
`~/Desktop/SessionN`). Crossing the filesystem boundary is slow and breaks file watching.

---

## Native Windows (unsupported)

**`uvloop` will not install.**
It has no Windows build and never has, so the pinned set cannot be installed as written. Use WSL2.

If you truly cannot: remove the `uvloop` line from `requirements-lock.txt` before installing —
`uvicorn` falls back to the standard asyncio loop, slower but working — and expect the shell
scripts not to run. This combination has never been tested end to end.

---

## Network and proxies

**TLS errors, or `pip`/`curl` installers failing on a corporate network.**
An intercepting proxy is re-signing certificates. Preflight flags this as `tls not intercepted WARN`.
Get your organisation's CA bundle from IT and point the tools at it:

```bash
export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt
export SSL_CERT_FILE=/path/to/ca-bundle.crt
```

**Never disable certificate verification** to get past this.

**A preflight endpoint shows `unreachable`.**
Something between you and it is blocking. The install will fail later at the step that needs it, so
fix it first. `github.com` and `pypi.org` are not optional.

**`git clone works` FAIL while `github.com` shows OK.**
The host answers but git over HTTPS is blocked — usually a proxy that permits browsing and not git.

---

## Google Cloud

**`403` with a message about `x-goog-user-project`.**
You missed the quota project. It reads like a permissions problem and is not one:

```bash
gcloud auth application-default set-quota-project YOUR_LAB_PROJECT_ID
```

**Preflight warns about your Google account.**
It does not look like a lab account. Use the **Qwiklabs account issued for the lab** — not personal,
not corporate. A different identity cannot see the lab's project or agents, and anything you create
lands in your own project and bills your own account. Keep them separate:

```bash
gcloud config configurations create lab
gcloud auth login
gcloud auth application-default login
```

Preflight cannot tell for certain what a valid lab account looks like, so the check is advisory. The
judgement is yours.

**`PERMISSION_DENIED` during an exercise.**
Your account is missing an IAM role the lab VM's service account has. Ask your lab administrator for
the list — several are non-obvious, and guessing wastes time. Do not download a service-account key
to impersonate it.

---

## Skills

**`agents-cli info` says no skills are installed.**
Its **skills count refers to the CLI's own general toolkit**, not the lab's. Check the lab's
separately:

```bash
ls ~/Desktop/Session1/.agents/skills
```

**A skill is on disk but the assistant cannot see it.**
Its `SKILL.md` is nested too deep. Every skill must be a **direct child** of `.agents/skills/`, with
`SKILL.md` at the top of its own directory. The tooling scans one level and no further, and a nested
skill fails silently. Confirm:

```bash
for d in ~/Desktop/Session1/.agents/skills/*/; do
  printf "%-28s %s\n" "$(basename "$d")" "$([ -f "$d/SKILL.md" ] && echo ok || echo MISSING)"
done
```

**The assistant cloned the repository but is not using the skill.**
Antigravity enumerates skills when a **session starts**. A repository cloned mid-session has its
`SKILL.md` read as an ordinary file, not loaded as steering. Open the cloned folder and start a new
session.

**`agents-cli setup` exits 0 but nothing changed.**
Exit 0 is not proof. Read the `agents-cli info` output.

---

## Track 3 and the starter kit

Track 3's lab content comes from <https://github.com/cszhu/build-with-gemini>, a **separate
community repository**. It is not maintained by this repository and it is not an official Google
product. Everything in this section is about that clone, not about this repo.

**`verify.sh` reports `sessions` and `lab-skill` failing, but I am on Track 3.**
You ran the Track 2 profile. Track 3 has no `~/Desktop/SessionN` folders and no
`novasmart-governance-lab` skill, so those checks are meaningless for it. Re-run with `--track 3`.
Nothing is broken.

**`verify.sh` reports `packages` drift on Track 3.**
Same cause. There is no `packages` check in the Track 3 profile, on purpose: you install your own
dependencies as you build, so an exact count of 120 would fail on a correct machine.

**`kit` MISSING.**
The starter kit was never cloned, or it is somewhere else. Clone it:

```bash
bash setup/install.sh --track 3 --only starterkit
```

If you keep it elsewhere, point both scripts at it with `--kit-dir DIR`.

**`kit` OK but `kit-skills`, `kit-mcp` or `kit-publish` MISSING.**
The directory exists but is not the starter kit, or upstream changed its layout. Confirm what you
actually have:

```bash
git -C ~/Desktop/build-with-gemini remote -v
ls ~/Desktop/build-with-gemini/.agents/skills
```

That repository can change at any time without notice to this one. If the layout genuinely moved,
report it rather than editing the checks to pass.

Do **not** run `--force` here. It moves your project folder aside and fetches the same upstream
again, so it destroys your working context and fixes nothing: these rows fire because upstream
changed shape, not because your copy is damaged. If you want a clean copy to compare against, put
it somewhere else and keep yours where it is:

```bash
bash setup/install.sh --track 3 --only starterkit --kit-dir ~/Desktop/kit-fresh
```

**`kit` MISSING, but the folder is there and has a `.git` in it.**
An earlier clone did not finish. A closed lid, a dropped conference network or a Ctrl-C leaves
`.git` behind with no files checked out. That used to be reported as a healthy kit, and re-running
changed nothing, which is the worst combination: a wedged machine that says it is fine. Both
scripts now ask git instead of looking for a `.git` directory, so `verify.sh` reports it MISSING
and the installer repairs it on the next run:

```bash
bash setup/install.sh --track 3 --only starterkit
```

The unusable directory is moved aside under a timestamped name, not deleted.

**The installer says the folder is a clone of a different repository.**
It is, and it is refusing to pretend otherwise. A mistyped `--kit-url`, or a folder that came from
somewhere else, used to be accepted silently and reported as success. The installer now moves that
directory aside and fetches the real kit. If the other repository is one you care about, move it
somewhere safe first, or use `--kit-dir DIR` to put the kit elsewhere.

**The installer stops with "cannot fetch ... from https://github.com/cszhu/build-with-gemini".**
That upstream is a community repository this one does not control. If it is renamed, deleted or
made private, the fetch fails. It now fails in about a second with that message. Previously git
asked `Username for 'https://github.com':` and blocked on the terminal with nothing on screen to
explain it, which on event day looked like a hang. Nothing is left half-applied, so re-running is
safe. Point at a fork or an offline mirror to carry on:

```bash
bash setup/install.sh --track 3 --only starterkit --kit-url https://github.com/YOU/your-fork
```

**The kit I have is not at the pinned commit.**
`install.sh` pins the kit to the `KIT_REF` commit at the top of `setup/install.sh`. When your folder
already exists and sits on a different commit, the installer says so and changes nothing, because
by then that folder is your project. Nothing is wrong with your machine. If you want the pinned
state, fetch it into a new folder with `--kit-dir DIR` and move your work across yourself, or take
a specific one with `--kit-ref`:

```bash
bash setup/install.sh --track 3 --only starterkit --kit-ref TAG --kit-dir ~/Desktop/kit-pinned
```

Pass `--kit-ref ""` to follow the default branch instead of the pin. The installer warns when you
do, because it then takes whatever is there on the day.

**`verify.sh` says `unknown option` and exits 64.**
It means what it says: the flag is not one this script has. It used to ignore anything it did not
recognise, so a mistyped `--trak`, or a bare `3` copied from the installer's own track prompt, ran
the **Track 2** profile on a Track 3 laptop and then reported missing session folders and a missing
governance-lab skill. Every remedy that output offered made the machine worse. Run
`bash setup/verify.sh --help` for the real list.

**The clone failed, or GitHub is blocked.**
`preflight.sh` probes `github.com`, so check its report card first. Note that the Linux `gh`
install uses a **different host**, `cli.github.com`, which preflight does not probe. A network that
allows `github.com` can still block the package host. Use `brew install gh` on macOS, or download a
release binary by hand, if the apt repository is unreachable.

**I already started building, and I want to re-run the installer.**
Re-running is safe. `install.sh --track 3` leaves an existing clone alone and says so. Do **not**
reach for `--force` expecting a refresh: it moves your directory aside under a timestamped name,
with everything you have built in it, and fetches a fresh one, which leaves you with two copies to
reconcile. It warns twice and names where your work went, but the better command is `--kit-dir DIR`
into a new folder, which leaves yours untouched. Nothing is deleted either way.

**The kit's skills do not appear in Antigravity.**
Cloning the kit is all the registration it needs, because Antigravity reads the `.agents/` folder
of the workspace you open. So open `~/Desktop/build-with-gemini` itself as the folder, and start a new
session; a repository cloned mid-session is read as ordinary files. This is separate from the
`google-agents-cli-*` lifecycle skills, which **are** installed by a command, `agents-cli setup`,
in the register step. If `/skills` shows the kit's skills but not the lifecycle ones, re-run that
step and restart Antigravity. If it shows the lifecycle ones but not the kit's, you have the wrong
folder open.

**`gh` is missing, or `gh` is installed but not on `PATH`.**
`install.sh --track 3` installs it with brew or apt, which puts it on `PATH` properly. If it is
missing, you probably ran the tool step as Track 2:

```bash
bash setup/install.sh --track 3 --only tools
```

If `gh` exists but the shell cannot find it, the kit's own publish script fetched it into
`~/.local/bin`. Add that to `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

**`gh` is installed but publishing still fails.**
Installing `gh` is not signing in to it. That part is interactive and needs your own GitHub account:

```bash
gh auth login
```

---

## Preflight verdicts

| Verdict | Meaning | What to do |
|---|---|---|
| **GO** | Suitable | Continue |
| **GO WITH CAVEATS** | Will probably work | Read every warning. If any looks serious for your machine, use the lab VM |
| **NO-GO** | Something cannot be worked around | Fix the blocking item, or use the lab VM |

`--skip-preflight` exists for repairs and re-runs. **It is not a way to get past a NO-GO.** If
preflight says your machine cannot do this, it is telling you something true.

---

## Expected failures

These are not bugs, and no amount of reinstalling fixes them.

| | Why |
|---|---|
| Exercises find no agents, datasets or gateways | The Google Cloud project has not been provisioned. Separate from this repository entirely |
| `gcp account` warns on a corporate machine | The check is doing its job |
| `adc MISSING` inside a container | ADC lives in `~/.config/gcloud`; a mounted credential elsewhere is not detected |
| Antigravity version newer than the reference | Expected. Versions are checked for presence, not pinned |
| `lab-skills SKIP` | Session folders exist but are empty. Run `install.sh --only sessions` |
| `sessions` / `lab-skill` / `packages` failing on Track 3 | You ran the Track 2 profile. Add `--track 3` |
| A warning that no `--track` was given | You did not pass one, so Track 2 was assumed. Harmless on Track 2, wrong on Track 3 |
| The starter kit is newer than this repo describes | Expected. It is a separate repository on its own schedule |

---

## Reset this laptop for a re-test

You do not normally need this. Re-running `install.sh` on a machine that is already set up is
safe and is the supported way to repair it: every step is idempotent, and the only thing a re-run
replaces is the lab skill folders it installed itself. Use this section when you want to rehearse
the setup from a clean state, or when you are handing the laptop back.

There is no `--uninstall`. Removing things is deliberately left to you, because most of what the
installer puts on a machine is ordinary developer tooling that you may well want to keep.

**What the installer creates or changes, both tracks**

| Path | Created by | Removed by a re-run? |
|---|---|---|
| `~/novasmart-lab/` | the main run, and the python step | no |
| `~/novasmart-lab/.venv/` | the python step | only with `--force` |
| `~/novasmart-lab/install.log` | every run, appended | no, it grows |
| `~/novasmart-lab/preflight-verdict` | every `preflight.sh` run, overwritten | no |
| `~/.local/bin/uv`, `~/.local/bin/uvx` | the tools step | no |
| uv's Python 3.14 toolchain, under `~/.local/share/uv` | the tools step | no |
| uv's download cache, under `~/.cache/uv` (`~/Library/Caches/uv` on macOS) | the tools and python steps | no, it grows |
| Linux apt packages: `curl wget gnupg ca-certificates apt-transport-https git build-essential google-cloud-cli nodejs` | the tools step | no |
| Linux apt sources: `/usr/share/keyrings/cloud.google.gpg`, `/etc/apt/sources.list.d/google-cloud-sdk.list`, and the NodeSource keyring and list | the tools step | no |
| macOS brew: `git`, `node@24`, the `gcloud-cli` cask, and `rust` on an Intel Mac | the tools step | no |
| whatever `agents-cli setup` and `agents-cli update` register globally | the register step | not by this repo |

**Track 2 adds**

| Path | Created by | Removed by a re-run? |
|---|---|---|
| `~/Desktop/Session1`, `Session2`, `Session3`, each with `.agents/skills/` | the sessions step | no |
| the `novasmart-governance-lab`, `build-demo` and `bwgtrack2-demo-build` folders inside each of those | the sessions step | replaced on every run, with or without `--force` |
| edits in place to `skills/**` in your clone, if any file there hardcodes the VM path `/config` | the skills step | no. This rewrites the clone's own tree |

**Track 3 adds**

| Path | Created by | Removed by a re-run? |
|---|---|---|
| `~/Desktop/build-with-gemini/` | the starterkit step | no |
| `~/Desktop/build-with-gemini.superseded.<timestamp>/` | the starterkit step, under `--force` or on a broken or wrong-remote clone | no, one accumulates per run |
| `gh`, by apt or brew | the tools step | no |

**With `--with-extras`**

| Path | Created by | Removed by a re-run? |
|---|---|---|
| `~/.cache/ms-playwright`, Playwright's Chromium, roughly 170 MB | the python step | no |
| `ffmpeg`, by apt or brew | the tools step | no |
| VS Code, with its keyring and apt list on Linux, or its cask on macOS | the tools step | no |

**Not touched at all:** `~/.zshrc`, `~/.bashrc`, any other shell profile, and any gcloud
credential or configuration. The installer prints the one `export` line for Track 2 and leaves it
to you to add.

**The minimal reset.** This removes everything the lab owns and nothing else:

```bash
rm -rf ~/novasmart-lab
rm -rf ~/Desktop/Session1 ~/Desktop/Session2 ~/Desktop/Session3   # Track 2
rm -rf ~/Desktop/build-with-gemini                                # Track 3
rm -rf ~/Desktop/build-with-gemini.superseded.*                   # Track 3, if any
rm -rf ~/.cache/ms-playwright                                     # --with-extras only
```

Check what is in the Track 3 folder before you delete it. After the lab starts, that folder is
the attendee's own project, and nothing in this repo will have copied it anywhere else.

Those paths are the defaults. If you ran the installer with `--root DIR` the session folders are
under `DIR/Desktop/` instead, if you passed `--kit-dir DIR` the starter kit is at `DIR`, and if
you set `LAB_HOME` the lab home is there rather than at `~/novasmart-lab`. Substitute
accordingly. The `~/.cache/ms-playwright` line only matters if you used `--with-extras`; without
it Playwright's browser was never downloaded and the directory will not exist, and `rm -rf` on a
path that is not there is harmless.

Two more caches are left in place on purpose, because they are uv's and not the lab's: the Python
3.14 toolchain under `~/.local/share/uv` and the download cache under `~/.cache/uv`
(`~/Library/Caches/uv` on macOS). Keeping them is what makes a re-test fast. If you want a
genuinely cold rehearsal, `uv cache clean` and `uv python uninstall 3.14` clear them, and the
next setup will re-download roughly 300 MB.

**Leave the rest alone.** Removing the system packages is optional and usually not worth it:
`git`, `curl`, `node`, `gh`, the Google Cloud CLI and `uv` are normal tools, and other things on
the machine may now depend on them. If you do want them gone, remove them the way you would
remove any other package, one at a time, and expect to re-download roughly 850 MB the next time
you set the laptop up.

To re-test from here, start again at `bash setup/preflight.sh`.

---

## Still stuck

Open an issue with the output of both:

```bash
bash setup/preflight.sh --track 2          # or --track 3
bash setup/verify.sh --fix-hints --track 2 # or --track 3
```

Include your OS and version, whether you are on Apple Silicon, Intel, or WSL2, **and which track
you are doing**. Both outputs now print the track, so a pasted report card says which profile it
came from. Those two outputs
plus the platform are almost always enough to diagnose it.

`~/novasmart-lab/install.log` has a timestamped record of every command the installer ran, which is
useful when a step failed and you have already closed the terminal.
