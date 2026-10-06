# Manual setup

Do everything by hand, with no scripts. Use this if you want full control over what touches your
machine, if you cannot run the installer, or if you want to understand exactly what it does.

**Read the disclaimer in the [README](README.md) first.** It applies here too: this is not an
official Google repository, versions are not maintained for security, and you assume all risk.
The lab-provided VM remains the supported option.

Every command below is what `setup/install.sh` runs, in the same order. Doing this by hand and
running the installer should produce the same environment, and `setup/verify.sh` checks either way.

**Decide your track before you start.** Steps 1, 2, 5, 6 and 7 are shared. After that the tracks
part company, and each step below says who it is for:

| Step | Track 2 | Track 3 |
|---|---|---|
| 1 — System tools | yes | yes, plus the GitHub CLI |
| 2 — Python environment | yes | yes |
| 3 — Make the lab skills portable | yes | **skip** |
| 4 — Create the session folders | yes | **skip** |
| 4b — Clone the Track 3 starter kit | **skip** | yes |
| 5 — Register the skills | yes | yes |
| 6 — Google Cloud | yes | yes |
| 7 — Check it worked | yes | yes, with `--track 3` |

**Time:** 45–90 minutes, mostly downloads (~850 MB).

---

## Before you start

**Antigravity IDE** — install it yourself from <https://antigravity.google/download>. It is the
editor the labs run in, so it cannot install itself.

**Sign in with the Qwiklabs account issued for the lab.** Not a personal Google account and not a
work or corporate one. A different identity cannot see the lab's project or agents, and anything you
create lands in your own project and bills your own account. Keep it separate:

```bash
gcloud config configurations create lab
```

**Check your machine can cope.** If you would rather not run the script at all, the thresholds are:
macOS 13+ / glibc 2.28+ · x86_64 or arm64 · 4 cores · 8 GB RAM (16 recommended) · 15 GB free disk.
Windows 10 build 19044+ with WSL2 also meets the bar, on **limited support**: read
[Windows with WSL2](#windows-with-wsl2) below before you begin. Otherwise:

```bash
bash setup/preflight.sh        # read-only, changes nothing
```

Throughout, `~/novasmart-lab` is the toolchain. The lab workspace is `~/Desktop/Session1|2|3` on
Track 2, and `~/Desktop/build-with-gemini` on Track 3.

---

## Windows with WSL2

Read this before Step 1 if you are on Windows. macOS and Linux are supported. Windows with WSL2 is
**limited support**: it is not unsupported, but it is not a peer of the other two either.

Every command below runs the same under WSL2 as it does on Linux, and a tester confirmed the
toolchain and `gcloud` work there. Antigravity is the part that has been seen to fail.

- **Known failure.** Antigravity can report **"folder not found"** for a folder on a WSL path that
  is plainly there. Antigravity is a Windows application and reaches the Linux filesystem over the
  `\\wsl$` network share, so `/home/you/Desktop/Session1` is not a path Windows can resolve.
- **Known workaround, with a real limit.** Map the WSL share to a drive letter, for example
  `\\wsl$\Ubuntu` to `Z:`, and open `Z:\home\you\Desktop\Session1` instead. This has worked.
  **The mapping does not survive a restart**, so expect to redo it. It is a workaround, not a fix.
- **Fallbacks, both fine.** Finish your setup on location at the event, or use the provided lab VM,
  which does not have this problem.

`setup/preflight.sh` reports WSL2 as `GO WITH CAVEATS` and never a clean `GO`, and `setup/install.sh`
asks you to agree to these limitations before it changes anything. Doing the steps by hand does not
remove the limitation. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#wsl2).

---

## Step 1 — System tools

*Both tracks.*

Installs `git`, the Google Cloud CLI, Node.js 24, and `uv`. The `agy` command line tool is not
installed: the labs run in the Antigravity IDE and nothing in them calls it.

**Track 3 also needs the GitHub CLI (`gh`)**, because the starter kit's `publish-to-github` skill
uses it at the end of the lab. Install it alongside the rest:

```bash
brew install gh                                     # macOS

# Linux and WSL2 — gh is not in the distribution archives at a usable version
sudo install -m 0755 -d /usr/share/keyrings
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg status=none
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
sudo apt-get update && sudo apt-get install -y gh
```

The kit will download `gh` into `~/.local/bin` by itself if it is missing, but it does that at the
very end of the lab, when you are least able to wait for it. Install it now.

### macOS

```bash
brew install git
brew install --cask gcloud-cli
brew install node@24
echo 'export PATH="'"$(brew --prefix)"'/opt/node@24/bin:$PATH"' >> ~/.zshrc
exec zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`node@24` is keg-only, which is why it needs the `PATH` line. Use `~/.bash_profile` if your shell is
bash.

**Intel Macs only.** One pinned package (`cryptography`) no longer publishes an Intel wheel and must
be compiled:

```bash
xcode-select --install
brew install rust
```

### Linux and WSL2

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
     curl wget gnupg ca-certificates apt-transport-https git build-essential

# Google Cloud CLI
sudo install -m 0755 -d /usr/share/keyrings
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
  | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
  | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list >/dev/null

# Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E DEBIAN_FRONTEND=noninteractive bash -

sudo DEBIAN_FRONTEND=noninteractive apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y google-cloud-cli nodejs

curl -LsSf https://astral.sh/uv/install.sh | sh
```

`DEBIAN_FRONTEND=noninteractive` must be passed **through** `sudo`. `sudo` runs with `env_reset` and
strips it, and without it `tzdata` opens an interactive prompt that hangs the install with no output.

### Both

```bash
uv python install 3.14
```

---

## Step 2 — The Python environment

```bash
mkdir -p ~/novasmart-lab
uv venv --seed --python 3.14 ~/novasmart-lab/.venv
source ~/novasmart-lab/.venv/bin/activate

uv pip install --no-deps -r setup/requirements-lock.txt
```

Three details that matter:

- **`--seed`** installs `pip` into the environment. Without it the venv has none.
- **`--no-deps` is required, not an optimisation.** `requirements-lock.txt` is the complete resolved
  set of 120 packages. Without the flag the resolver adds more — `google-agents-cli` hard-requires
  `google-cloud-aiplatform[evaluation]`, whose extra pulls in LiteLLM and an OpenAI client that
  nothing in these labs uses — and adds them unpinned.
- You must `source ~/novasmart-lab/.venv/bin/activate` in **every new terminal** before using the
  lab tools.

---

## Step 3 — Make the lab skills portable

*Track 2 only. On Track 3, skip to Step 4b.*

The bundled skills in `skills/` are already published portable, so normally there is nothing to do.
Confirm:

```bash
grep -rlE '(^|[[:space:]`"(])/config([^a-zA-Z]|$)' skills/ || echo "already portable"
```

If that lists files, they came from a copy taken off the lab VM, where the home directory is
`/config`. Rewrite them:

```bash
grep -rlE '(^|[[:space:]`"(])/config([^a-zA-Z]|$)' skills/ | while read -r f; do
  sed -i.bak -E "s#(^|[[:space:]\`\"(])/config([^a-zA-Z]|\$)#\1$HOME\2#g" "$f"; rm -f "$f.bak"
done
```

Match `/config` only where it **starts a path**. A blanket replace corrupts `/configure` inside
documentation URLs, and a looser guard still corrupts `deployment/config` in prose. Also set:

```bash
echo 'export NOVASMART_SCORECARD_HOME="$HOME"' >> ~/.zshrc   # ~/.bashrc on Linux/WSL2
```

---

## Step 4 — Create the session folders

*Track 2 only. On Track 3, skip to Step 4b.*

Antigravity works on a folder. Each session folder is a self-contained workspace with its own copy
of the skills, matching the lab VM's layout.

```bash
for s in Session1 Session2 Session3; do
  mkdir -p ~/Desktop/$s/.agents/skills
  cp -r skills/novasmart-governance-lab ~/Desktop/$s/.agents/skills/
  for d in build-demo bwgtrack2-demo-build; do
    [ -d skills/build-demo/$d ] && cp -r skills/build-demo/$d ~/Desktop/$s/.agents/skills/
  done
done
```

**Every skill must be a direct child of `.agents/skills/`, with its `SKILL.md` at the top of its own
directory.** The tooling scans one level deep and no further, which is why `build-demo`'s children
are copied individually rather than copying the parent folder. A nested skill fails silently rather
than with an error. Confirm:

```bash
for d in ~/Desktop/Session1/.agents/skills/*/; do
  printf "%-28s %s\n" "$(basename "$d")" "$([ -f "$d/SKILL.md" ] && echo ok || echo MISSING-SKILL.md)"
done
```

---

## Step 4b — Clone the Track 3 starter kit

*Track 3 only. On Track 2, skip to Step 5.*

Track 3's lab content is not in this repository. It lives in a **separate community repository**,
<https://github.com/cszhu/build-with-gemini>. That repository is not maintained by this one, and it
is not an official Google product. Read it before you run anything it ships.

`install.sh` pins this kit to one rehearsed commit rather than taking whatever is on its default
branch that day. Do the same by hand. The commit below is the pin; the authoritative copy is the
`KIT_REF` variable at the top of `setup/install.sh`, so read it from there if the two ever disagree.

```bash
mkdir -p ~/Desktop/build-with-gemini
cd ~/Desktop/build-with-gemini
git init -q
git remote add origin https://github.com/cszhu/build-with-gemini
git fetch --depth 1 origin cdd68490e7df168ba09678e484db94b36e624af9
git checkout --detach FETCH_HEAD
```

`git clone --depth 1` is the shorter command, and it is what this guide used to say, but it can only
take a branch. A branch moves. Use it only if you have decided you want the latest state of a
repository nobody here controls.

Confirm what arrived:

```bash
ls ~/Desktop/build-with-gemini/.agents/skills     # the workshop skills
ls ~/Desktop/build-with-gemini/.agents/mcp_config.json
```

**There is nothing to run to register these skills.** Antigravity reads the `.agents/` folder of
whatever workspace you open, so opening `~/Desktop/build-with-gemini` is what loads them. This is
not the same thing as Step 5, which installs the separate `google-agents-cli-*` lifecycle skills
globally; you need both, and only Step 5 is a command.

If you clone it again later, clone to a new path or move the old directory aside. Once the lab
starts, this directory holds your own project.

---

## Step 5 — Register the skills

*Both tracks.* On Track 3, run it from `~/Desktop/build-with-gemini` instead of `~/Desktop/Session1`.

```bash
cd ~/Desktop/Session1        # Track 3: cd ~/Desktop/build-with-gemini
source ~/novasmart-lab/.venv/bin/activate
agents-cli setup
agents-cli update
agents-cli info
```

**Run these once, during setup, and not again.** `agents-cli setup` also pulls in unrelated
general-purpose skills from a public repository — harmless now, but an unwanted change if run in the
middle of an exercise.

`agents-cli info`'s **skills count refers to the CLI's own toolkit**, not the lab's. Confirm the lab
skills with `ls ~/Desktop/Session1/.agents/skills` on Track 2, or
`ls ~/Desktop/build-with-gemini/.agents/skills` on Track 3. And `setup` exiting 0 is not proof it
worked — read the `info` output.

This step registers the `google-agents-cli-*` lifecycle skills, the ones that scaffold, deploy and
evaluate an agent. It does **not** register the skills that ship inside a repository's own
`.agents/` folder; Antigravity picks those up itself when you open that folder. Both tracks need
this step, and on Track 3 the kit's own troubleshooting notes point back at `agents-cli setup` for
exactly this reason. If Antigravity has been running throughout, restart it afterwards so it
notices the newly installed lifecycle skills.

---

## Step 6 — Google Cloud, on the day of the event

*Both tracks. Not before the event.*

Everything in this step needs credentials you do not have yet. The Qwiklabs account and the lab
project ID are handed out at the event, so if you are setting this laptop up in advance, read this
step and stop. Nothing below can be run now, and nothing below is needed for the rest of the setup.
Note also that this file has its own numbering: this Step 6 is not the readiness check that the
attendee landing page calls step 6. That one is Step 7 here.

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_LAB_PROJECT_ID
gcloud auth application-default set-quota-project YOUR_LAB_PROJECT_ID
```

**Do not skip the quota-project line.** Without it several APIs return `403` with a message about
`x-goog-user-project` that reads like a permissions problem and is not one.

Confirm the account is the lab one, not yours:

```bash
gcloud auth list
```

Your account also needs IAM roles equivalent to what the lab VM's service account has. **Ask your
lab administrator for the list** rather than guessing — several are non-obvious. Do not download a
service-account key to impersonate it; a long-lived key on a laptop is a worse risk than the gap it
closes.

---

## Step 7 — Check it worked

*Both tracks, with the track you set up.* Run it from the setup folder, in a terminal:

```bash
cd ~/novasmart-lab/setup
bash setup/verify.sh --readiness              # Track 2
bash setup/verify.sh --readiness --track 3    # Track 3
```

Run this as a command, and run it before you open the lab folder. On Track 3 the starter kit
ships its own `troubleshoot-lab-setup` skill, which answers "am I ready to start" and tells you
to sign in to Google Cloud. That skill belongs to the lab rather than to setup, and before the
event there is nothing to sign in with. Running the command yourself avoids that entirely. If
you prefer to ask the assistant, ask it with the setup folder open, not the lab folder.

Expect **11 of 11 checks OK** on Track 2, or **12 of 12** on Track 3, and a readiness summary.

On Track 2, two of those eleven cover the lab skills, which ship separately from this repository.
If none are installed, those two collapse into a single `SKIP` row that is not counted, and the
script prints **9 of 9 checks OK**. That is a correct software-only setup, not a failure.

Pass the right `--track`: the Track 2 profile checks for session folders and the governance-lab
skill, which a correct Track 3 machine does not have, and it will report them as failures. A
mistyped flag is refused rather than guessed at, so `--trak 3` exits 64 and says so instead of
quietly running the Track 2 profile on a Track 3 laptop.

If your virtual environment is not at `~/novasmart-lab/.venv`, add `--venv DIR` rather than
treating exit 3 as a broken install.

Lines worth reading closely on **Track 2**:

- **`packages 120`** — anything else means the Python install diverged, most likely a missing
  `--no-deps`.
- **`no-vendor-sdk 0`** — anything above zero means the resolver re-added LiteLLM or an OpenAI
  client.

There is no `packages` check on Track 3, on purpose: you add your own dependencies as you build, so
an exact count would fail on a perfectly good machine. `no-vendor-sdk` still applies.

On **Track 3**, read these instead:

- **`kit`, `kit-skills`, `kit-mcp`, `kit-publish`** — the starter kit is cloned and has the shape
  the lab expects. If the kit checks fail but the directory exists, you may have cloned something
  else, or upstream may have changed its layout.
- **`gh`** — the GitHub CLI is on `PATH`. You still have to run `gh auth login` yourself, which is
  interactive and needs your GitHub account.

Then open `~/Desktop/Session1` (Track 2) or `~/Desktop/build-with-gemini` (Track 3) in Antigravity
and begin.

---

## Optional extras

Only needed for the optional demo-recording exercises. Skip them for a standard lab run.

```bash
# macOS
brew install ffmpeg
brew install --cask visual-studio-code

# Linux / WSL2
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/packages.microsoft.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  | sudo tee /etc/apt/sources.list.d/vscode.list >/dev/null
sudo DEBIAN_FRONTEND=noninteractive apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y code

# Both, inside the virtual environment
playwright install chromium
```

---

## If something goes wrong

`setup/verify.sh --fix-hints` prints the repair for each failing check. The full list, by operating
system, is in **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**. The ones that catch people most often:

| Symptom | Cause |
|---|---|
| `cryptography` fails to build on an Intel Mac | No Intel wheel for the pinned version. Install Rust and Xcode command line tools |
| The install hangs with no output on Linux | `DEBIAN_FRONTEND` not passed through `sudo`; `tzdata` is waiting on a prompt |
| `uvloop` will not install on Windows | It has no Windows build. Use WSL2, on limited support |
| Antigravity says "folder not found" on a WSL path | Known Windows failure. Map the WSL share to a drive letter, and expect to redo it after every restart. See [Windows with WSL2](#windows-with-wsl2) |
| `agents-cli: command not found` | The virtual environment is not activated |
| An exercise writes a file and it is nowhere | Skills still contain `/config` paths — Step 3 |
| Everything installs but exercises find nothing | Expected until the Google Cloud project is provisioned |
