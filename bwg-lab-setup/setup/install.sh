#!/usr/bin/env bash
# Build with Gemini lab - laptop setup for Track 2 and Track 3.
# Track 2: the NovaSmart governance lab. Track 3: the agent-first app starter kit.
# Idempotent: re-running replaces the lab skill folders it installed under Desktop/Session*/; nothing else is destructive without --force.
# Exit: 0 done · 1 a step failed · 2 preflight NO-GO · 64 bad flag, step or track · 66 no terminal to ask consent on, nothing changed
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"    # this script lives in <repo>/setup/

# Lab skills. Bundled in this repo under skills/, so no flag is needed. Override with
# --skills-src DIR to use a copy from somewhere else.
LAB_SKILLS_SRC="${LAB_SKILLS_SRC:-}"
if [ -z "$LAB_SKILLS_SRC" ] && [ -d "$REPO_DIR/skills" ]; then LAB_SKILLS_SRC="$REPO_DIR/skills"; fi
LAB_HOME="${LAB_HOME:-$HOME/novasmart-lab}"
LAB_ROOT="${LAB_ROOT:-$HOME}"          # session folders live at $LAB_ROOT/Desktop/SessionN
PY_VERSION="3.14"
SESSIONS=(Session1 Session2 Session3)
LAB_SKILLS=(novasmart-governance-lab)
DEMO_SKILLS=(build-demo bwgtrack2-demo-build)
# ALL_STEPS is the registry of every step this script implements. The two lists below
# decide which of them a track actually runs, and in what order. --only validates
# against ALL_STEPS, so every registered step stays individually runnable.
ALL_STEPS=(tools python skills sessions register starterkit)
TRACK2_STEPS=(tools python skills sessions register)
TRACK3_STEPS=(tools python starterkit register)
TRACK_STEPS=()

# Track 3 works out of a starter kit that lives in a separate community repository.
# It is not maintained here and it is not an official Google product. Point --kit-url
# at a fork or an offline mirror if you do not want to fetch the upstream copy.
KIT_URL="${KIT_URL:-https://github.com/cszhu/build-with-gemini}"
KIT_DIR="${KIT_DIR:-}"                 # resolved after the flags: it depends on --root
# The kit is PINNED. A --depth 1 clone of somebody else's default branch is not a thing
# to run in front of a room: upstream can change shape, or disappear, on the morning of
# the event, and nobody here gets a notification when it does. KIT_REF is the exact
# upstream commit this lab has been rehearsed against.
#
# To bump it: read the upstream diff, rehearse Track 3 end to end against the new
# commit, then replace the SHA below and the line under it. Nothing else has to move.
# A full commit SHA, a tag or a branch name all work. Set it to the empty string, or
# pass --kit-ref "", to follow the default branch instead and take whatever is there.
KIT_REF="${KIT_REF:-cdd68490e7df168ba09678e484db94b36e624af9}"
# ^ cszhu/build-with-gemini, default branch as of 2026-09-25. Ships 8 skills, and has
#   both of the upstream paths verify.sh asserts: .agents/mcp_config.json and
#   .agents/skills/publish-to-github/publish.sh.

DRY=0; ONLY=""; ASSUME_YES=0; FORCE=0; WITH_EXTRAS=0; SKIP_PREFLIGHT=0
TRACK="${BWG_TRACK:-}"
LOG="$LAB_HOME/install.log"

usage() { sed -n '2,5p' "$0"; cat <<EOF

Usage: install.sh [options]
  --track {2,3}      which track to set up. Without it the script asks, and falls
                     back to Track 2 when there is no terminal to ask on
  --dry-run          print every command, change nothing (never asks for a track)
  --only STEP        run one step: ${ALL_STEPS[*]}
                     --only starterkit implies --track 3 when no track is given
  --with-extras      also install ffmpeg, VS Code, Playwright's browser
  --force            rebuild an existing venv. The lab skill folders under
                     Desktop/Session*/ are replaced on every run with or without it.
                     On Track 3 it also moves an existing starter-kit folder aside,
                     with any work you have done in it, and fetches the kit again
  --yes              do not prompt (does NOT override a preflight NO-GO)
  --skip-preflight   do not run preflight first
  --root DIR         parent of Desktop/SessionN (default: \$HOME)
  --skills-src DIR   directory holding the lab skills (not shipped in this repo)
  --kit-dir DIR      Track 3 only: where to clone the starter kit
                     (default: \$LAB_ROOT/Desktop/build-with-gemini)
  --kit-url URL      Track 3 only: the starter kit repository, a community repo
                     (default: $KIT_URL)
  --kit-ref REF      Track 3 only: the commit, tag or branch of the starter kit to
                     check out. Pass an empty string to follow the default branch
                     instead of the pin (default: $KIT_REF)
  -h, --help
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --only) ONLY="${2:?--only needs a step}"; shift ;;
    --with-extras) WITH_EXTRAS=1 ;;
    --force) FORCE=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --skip-preflight) SKIP_PREFLIGHT=1 ;;
    --root) LAB_ROOT="${2:?--root needs a directory}"; shift ;;
    --skills-src) LAB_SKILLS_SRC="${2:?--skills-src needs a directory}"; shift ;;
    --track) TRACK="${2:?--track needs 2 or 3}"; shift ;;
    --kit-dir) KIT_DIR="${2:?--kit-dir needs a directory}"; shift ;;
    --kit-url) KIT_URL="${2:?--kit-url needs a URL}"; shift ;;
    # ${2?...} and not ${2:?...}: an empty --kit-ref is a real choice. It means
    # "follow the default branch", which is what this script did before the pin.
    --kit-ref) KIT_REF="${2?--kit-ref needs a commit, tag or branch}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 64 ;;
  esac
  shift
done

on_err() {
  local rc=$?
  printf '\n\033[31mfailed\033[0m during step "%s" (exit %s)\n' "${CURRENT_STEP:-?}" "$rc" >&2
  printf 'retry just this step with:  bash %s --only %s\n' "$SCRIPT_DIR/install.sh" "${CURRENT_STEP:-all}" >&2
  exit "$rc"
}
trap on_err ERR

say()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
info() { printf '    %s\n' "$*"; }
warn() { printf '    \033[33mwarning:\033[0m %s\n' "$*" >&2; }
die()  { printf '\n\033[31mfailed:\033[0m %s\n' "$*" >&2
         # Same form as on_err above. These two used to disagree: one said `bash <path>`
         # and the other said `<path>` with a bare $0, so from a relative invocation the
         # attendee was told to run a command that only worked from the directory they
         # happened to be standing in.
         printf 'retry just this step with:  bash %s --only %s\n' "$SCRIPT_DIR/install.sh" "${CURRENT_STEP:-all}" >&2
         exit 1; }

run() {
  if [ "$DRY" = 1 ]; then printf '    $ %s\n' "$*"; return 0; fi
  printf '    $ %s\n' "$*"
  # date -Is is GNU only. BSD date, which is what macOS ships, has no -I, so every
  # logged line there got an empty timestamp and a "date: illegal option" on stderr.
  [ -d "$LAB_HOME" ] && printf '%s | %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$LOG" 2>/dev/null || true
  "$@"
}

confirm() {
  [ "$ASSUME_YES" = 1 ] && return 0
  [ "$DRY" = 1 ] && return 0
  printf '    %s [y/N] ' "$1"; read -r a; [ "$a" = y ] || [ "$a" = Y ]
}

# ---------- which track ----------
# The track decides which steps run, so it has to be settled before anything else.
# Three ways to say it, in order: --track, then the question below, then Track 2.
#
# A dry run NEVER asks. It exists to be piped, read and diffed, so it has to print the
# same bytes whether or not a human is watching, and it must not block a CI job that
# has no terminal. For the same reason the "we picked one for you" notice goes to
# stderr: it belongs on the operator's screen, not in the transcript of the commands.
# --only starterkit is self-identifying, so it does not need to be asked about.
if [ -z "$TRACK" ] && [ "$ONLY" = starterkit ]; then TRACK=3; fi
if [ -z "$TRACK" ]; then
  if [ "$DRY" = 0 ] && [ -t 0 ]; then
    say "Which track are you doing?"
    info "2) Track 2 - NovaSmart governance lab, three session folders on your Desktop"
    info "3) Track 3 - agent-first app, built from the community Track 3 starter kit"
    printf '    Track [2] '; read -r a
    case "$a" in
      3) TRACK=3 ;;
      ""|2) TRACK=2 ;;
      *) echo "not a track: $a (use 2 or 3)" >&2; exit 64 ;;
    esac
  else
    TRACK=2
    warn "no --track given and no terminal to ask on - setting up Track 2. Pass --track 3 for the Track 3 starter kit."
  fi
fi
case "$TRACK" in
  2) TRACK_STEPS=("${TRACK2_STEPS[@]}") ;;
  3) TRACK_STEPS=("${TRACK3_STEPS[@]}") ;;
  *) echo "unknown track: $TRACK (use 2 or 3)" >&2; usage >&2; exit 64 ;;
esac
[ -n "$KIT_DIR" ] || KIT_DIR="$LAB_ROOT/Desktop/build-with-gemini"

# Step headings count themselves against the selected track's list, so Track 2 still
# reads "Step 3/5" and Track 3 reads "Step 3/4" without either number being written
# down anywhere. A step run outside its track (--only) prints its title with no number.
heading() { # step-name  title
  local name=$1 title=$2 i=1 s
  for s in ${TRACK_STEPS[@]+"${TRACK_STEPS[@]}"}; do
    [ "$s" = "$name" ] && { say "Step $i/${#TRACK_STEPS[@]}  $title"; return 0; }
    i=$((i+1))
  done
  say "$title"
}

# ---------- platform detection ----------
OS=""; PKG=""
case "$(uname -s)" in
  Darwin) OS=macos; PKG=brew ;;
  Linux)  OS=linux; PKG=apt
          grep -qi microsoft /proc/version 2>/dev/null && OS=wsl2 ;;
  *) die "unsupported OS: $(uname -s). Native Windows is unsupported - use WSL2. See TROUBLESHOOTING.md" ;;
esac
ARCH="$(uname -m)"
IS_INTEL_MAC=0
[ "$OS" = macos ] && [ "$ARCH" = x86_64 ] && IS_INTEL_MAC=1

need() { command -v "$1" >/dev/null 2>&1; }

# ---------- Windows / WSL2 consent ----------
# Windows with WSL2 is LIMITED SUPPORT. The toolchain and gcloud do work here, but
# Antigravity has been seen to refuse to open a folder that lives on a WSL path and
# report "folder not found". Mapping the WSL share to a drive letter works around it
# and then disappears on the next restart, so it is a workaround and not a fix. An
# attendee is entitled to hear that before this script changes their machine, because
# for some of them the right answer is the provided VM instead.
#
# A dry run NEVER asks, on the same reasoning as the track question above: it has to
# print the same bytes whether or not a human is watching, and it must not block a CI
# job that has no terminal. In that case the run continues and the notice goes to
# stderr, where operator messages belong. This does nothing at all on macOS or Linux.
wsl_gate() {
  [ "$OS" = wsl2 ] || return 0
  if [ "$DRY" = 0 ] && [ -t 0 ]; then
    say "Windows with WSL2 is limited support"
    info "Read this before you agree to continue:"
    info "  - Windows is not supported to the level macOS and Linux are. Some of this"
    info "    lab has been seen to break here, and setup makes more changes to your"
    info "    machine on WSL2 than it does on the other two."
    info "  - Antigravity may fail to open the setup folder on a WSL path. It reports"
    info "    'folder not found' even though the folder is there."
    info "  - Mapping the WSL share to a drive letter, for example Z:, is the known"
    info "    workaround. It DOES NOT survive a restart, so you may have to redo it."
    info "  - You do not have to do this. You can use the provided lab VM, or set up"
    info "    on location at the event with a helper, instead."
    # --yes is deliberately NOT consulted here. When there is a terminal, a WSL2
    # attendee is shown the limited-support disclosure and answers it themselves,
    # because "I accept the default install" is not the same statement as "I accept
    # that this platform is only partly supported".
    printf '    Continue on WSL2 anyway? [y/N] '; read -r a
    case "$a" in y|Y) ;; *) echo "  Stopped. Nothing was changed."; exit 0 ;; esac
  elif [ "$DRY" = 1 ]; then
    # A dry run changes nothing, so it must never block. It still says the platform is
    # limited support, on stderr, so the notice is not lost in a rehearsal.
    warn "WSL2 detected - dry run, nothing will be changed. Windows is limited support: Antigravity may fail to open folders on WSL paths, the drive-letter workaround does not survive a restart, and the provided lab VM or setup on location at the event remain your alternatives."
  elif [ "$ASSUME_YES" = 1 ]; then
    warn "WSL2 detected and no terminal to ask on - --yes given, continuing. Windows is limited support: Antigravity may fail to open folders on WSL paths, the drive-letter workaround does not survive a restart, and the provided lab VM or setup on location at the event remain your alternatives."
  else
    # A real run, on a limited-support platform, with nothing to ask consent on. This
    # used to warn and carry on, which made the WSL2 disclosure advisory rather than a
    # gate. Same wording and same exit code as the no-TTY arm of gate() below, so an
    # attendee and a log reader see one behaviour and not two.
    printf '\n  Stopped. Nothing was changed.\n' >&2
    printf '  WSL2 was detected and there is no terminal here to ask you for consent on.\n' >&2
    printf '  Windows is limited support: Antigravity may fail to open folders on WSL\n' >&2
    printf '  paths, the drive-letter workaround does not survive a restart, and the\n' >&2
    printf '  provided lab VM or setup on location at the event remain your alternatives.\n' >&2
    printf '  Run this from a terminal, or pass --yes to accept that and continue.\n' >&2
    exit 66
  fi
}

# ---------- steps ----------
step_tools() {
  heading tools "Install the tools  ($OS/$ARCH)"
  if [ "$PKG" = brew ]; then
    need brew || die "Homebrew is required on macOS: https://brew.sh"
    need git    || run brew install git
    need gcloud || run brew install --cask gcloud-cli
    if ! need node; then
      run brew install node@24
      local nodebin; nodebin="$(brew --prefix)/opt/node@24/bin"
      export PATH="$nodebin:$PATH"
      info "node@24 is keg-only. Added to PATH for this run; make it permanent with:"
      info "  echo 'export PATH=\"$nodebin:\$PATH\"' >> ~/.zshrc"
    fi
    # Track 3 only, and the mirror of the apt branch below. gh used to be installed on
    # the apt side and nowhere else, so every Mac attendee finished install.sh without
    # it, verify.sh --track 3 reported "gh MISSING", and the fix hint it printed pointed
    # back at this step, which did nothing for them. brew is the documented manual
    # equivalent in manual_setup.md. See the note above step_starterkit for why gh is
    # installed here rather than left to the kit's own publish script.
    if [ "$TRACK" = 3 ]; then
      need gh || run brew install gh
    fi
    if [ "$IS_INTEL_MAC" = 1 ] && ! need cargo; then
      warn "Intel Mac: 'cryptography' has no Intel wheel and must be compiled."
      # A real if/else, not `confirm && { ... } || warn`. In that form a failing
      # `brew install rust` fell into the || arm and printed "Skipping", which was
      # untrue: the attendee did not skip, it broke. The || also hid the failure from
      # set -e, so the run carried on into step_python and died there compiling
      # 'cryptography', with an error that named neither Rust nor this prompt.
      if confirm "Install Rust and Xcode command line tools now?"; then
        # This one really is ignorable: it exits non-zero when the tools are already
        # installed, which is the common case.
        run xcode-select --install || true
        run brew install rust \
          || die "could not install Rust. The python step needs it to compile 'cryptography' on an Intel Mac"
      else
        warn "Skipping Rust. The python step will fail without it."
      fi
    fi
  else
    # DEBIAN_FRONTEND must be passed THROUGH sudo: sudo's env_reset strips it, and
    # without it tzdata's postinst opens an interactive debconf prompt that hangs the
    # install forever with no output. Found by the container journey test.
    info "apt steps need sudo."
    run sudo DEBIAN_FRONTEND=noninteractive apt-get update
    run sudo DEBIAN_FRONTEND=noninteractive apt-get install -y curl wget gnupg ca-certificates apt-transport-https git build-essential
    if ! need gcloud; then
      run sudo install -m 0755 -d /usr/share/keyrings
      run bash -c 'curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg'
      run bash -c 'echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list >/dev/null'
    fi
    need node || run bash -c 'curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E DEBIAN_FRONTEND=noninteractive bash -'
    # Track 3 only. gh is not in the Debian or Ubuntu archives at a usable version, so
    # it comes from GitHub's own apt repository, the same shape as gcloud above.
    # See the note above step_starterkit for why this is installed here.
    local pkgs=(google-cloud-cli nodejs)
    if [ "$TRACK" = 3 ]; then
      if ! need gh; then
        run sudo install -m 0755 -d /usr/share/keyrings
        run bash -c 'curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg status=none'
        run sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
        run bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null'
      fi
      pkgs+=(gh)
    fi
    run sudo DEBIAN_FRONTEND=noninteractive apt-get update
    run sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${pkgs[@]}"
  fi
  need uv || run bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
  export PATH="$HOME/.local/bin:$PATH"
  run uv python install "$PY_VERSION"
}

step_python() {
  heading python "The Python environment"
  run mkdir -p "$LAB_HOME"
  if [ -d "$LAB_HOME/.venv" ] && [ "$FORCE" != 1 ]; then
    info "venv exists — reusing it (--force to rebuild)"
  else
    [ -d "$LAB_HOME/.venv" ] && run rm -rf "${LAB_HOME:?}/.venv"
    run uv venv --seed --python "$PY_VERSION" "$LAB_HOME/.venv"
  fi
  local lock="$SCRIPT_DIR/requirements-lock.txt"
  [ -f "$lock" ] || die "requirements-lock.txt not found next to this script ($SCRIPT_DIR)"
  info "installing $(grep -c '==' "$lock") pinned packages (~230 MB)"
  # --no-deps is deliberate: the lockfile is the COMPLETE resolved set. Without it the
  # resolver re-adds packages we removed on purpose (google-agents-cli hard-requires
  # google-cloud-aiplatform[evaluation], whose extra drags in litellm and an OpenAI
  # client), and at unpinned newer versions.
  run env VIRTUAL_ENV="$LAB_HOME/.venv" uv pip install --no-deps -r "$lock"
  if [ "$WITH_EXTRAS" = 1 ]; then
    info "installing Playwright's browser (~170 MB)"
    run "$LAB_HOME/.venv/bin/playwright" install chromium
    if [ "$PKG" = brew ]; then
      need ffmpeg || run brew install ffmpeg
      need code   || run brew install --cask visual-studio-code
    else
      run sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg
      if ! need code; then
        run bash -c 'wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/packages.microsoft.gpg'
        run bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list >/dev/null'
        run sudo DEBIAN_FRONTEND=noninteractive apt-get update && run sudo DEBIAN_FRONTEND=noninteractive apt-get install -y code
      fi
    fi
  fi
}

step_skills() {
  heading skills "Prepare the lab skills"
  if [ -z "$LAB_SKILLS_SRC" ]; then
    info "no skills/ directory in this repo and no --skills-src given - skipping."
    info "Re-run with:  install.sh --only skills --skills-src /path/to/skills"
    return 0
  fi
  [ -d "$LAB_SKILLS_SRC" ] || die "--skills-src not a directory: $LAB_SKILLS_SRC"
  [ -f "$LAB_SKILLS_SRC/PROVENANCE.txt" ] && info "skills revision: $(sed -n 2p "$LAB_SKILLS_SRC/PROVENANCE.txt")"

  # The bundled skills are published already portable, so this is normally a no-op.
  # A copy taken straight from the lab VM still hardcodes /config as the home directory.
  # `|| true` matters: grep exits 1 when it matches nothing, and pipefail would kill us.
  local hits
  hits="$(grep -rlE '(^|[[:space:]`\"(])/config([^a-zA-Z]|$)' "$LAB_SKILLS_SRC" 2>/dev/null || true)"
  if [ -z "$hits" ]; then
    info "skills are already path-portable - nothing to rewrite"
    return 0
  fi
  local n; n="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
  info "rewriting $n file(s) that hardcode the VM path /config"
  if [ "$DRY" = 1 ]; then
    printf '    $ sed -i.bak "s#/config#%s#g"  (%s files)\n' "$LAB_ROOT" "$n"
    return 0
  fi
  # Rewrite /config only where it STARTS an absolute path. Two narrower rules were
  # tried and both corrupted shipped text: a bare replace mangles /configure inside a
  # documentation URL, and a component-only guard still mangles deployment/config.
  printf '%s\n' "$hits" | while read -r f; do
    [ -n "$f" ] || continue
    sed -i.bak -E "s#(^|[[:space:]\`\"(])/config([^a-zA-Z]|\$)#\\1$LAB_ROOT\\2#g" "$f"; rm -f "$f.bak"
  done
  # Use the same component-aware pattern as the rewrite: a bare grep for /config
  # also matches /configure inside documentation URLs, which is legitimate.
  if grep -rqE '(^|[[:space:]`\"(])/config([^a-zA-Z]|$)' "$LAB_SKILLS_SRC" 2>/dev/null; then
    die "rewrite incomplete - /config still present in $LAB_SKILLS_SRC"
  fi
  return 0
}

step_sessions() {
  heading sessions "Create the session folders"
  for s in "${SESSIONS[@]}"; do
    run mkdir -p "$LAB_ROOT/Desktop/$s/.agents/skills"
  done
  if [ -z "$LAB_SKILLS_SRC" ]; then
    info "folders created empty - add the lab skills to each .agents/skills/ when you receive them"
    return 0
  fi
  local src="$LAB_SKILLS_SRC"
  for s in "${SESSIONS[@]}"; do
    local dest="$LAB_ROOT/Desktop/$s/.agents/skills"
    for k in "${LAB_SKILLS[@]}"; do
      if [ -d "$src/$k" ]; then
        [ -e "$dest/$k" ] && run rm -rf "${dest:?}/$k"
        run cp -r "$src/$k" "$dest/"
      fi
    done
    # build-demo is a catalog dir; its children must land flat, one level deep.
    for k in "${DEMO_SKILLS[@]}"; do
      if [ -f "$src/build-demo/$k/SKILL.md" ]; then
        [ -e "$dest/$k" ] && run rm -rf "${dest:?}/$k"
        run cp -r "$src/build-demo/$k" "$dest/"
      fi
    done
  done
  info "sessions ready under $LAB_ROOT/Desktop/"
}

# Track 3 only. Everything this step touches belongs to a community repository:
# github.com/cszhu/build-with-gemini. That repo is not maintained here, it is not an
# official Google product, and its contents can change without notice. This step
# clones it and reports what arrived; it does not vendor or rewrite any of it.
#
# There is no "register the kit's skills" command to run. Antigravity reads the
# .agents/ folder of the workspace you open, so cloning the kit IS the registration.
# The kit's own troubleshooting skill talks about `agents-cli setup`, but that is a
# different thing: it installs the global google-agents-cli-* lifecycle skills, which
# step_register already does for both tracks.
#
# gh is installed in step_tools rather than left to the kit. The kit's publish script
# does fetch gh on its own, unauthenticated, into ~/.local/bin, at the very end of the
# lab, when a room full of people is on the same network and short of time. Installing
# it up front moves that download off the critical path and puts gh on PATH properly.
# The kit's fetch is guarded by `command -v gh`, so doing it here makes that a no-op.

# A .git directory is not a usable clone. A clone killed part-way through, by a closed
# lid, a dropped conference network or a Ctrl-C, leaves $KIT_DIR/.git behind with no
# checkout, and "is there a .git" then calls that healthy forever with no way out.
# Ask git instead. verify.sh's `kit` check applies the same test, so the installer and
# the checker can never disagree about whether this folder is usable.
kit_state() { # prints: absent | notgit | broken | wrongremote | ok
  [ -e "$KIT_DIR" ] || { echo absent; return 0; }
  [ -d "$KIT_DIR/.git" ] || { echo notgit; return 0; }
  git -C "$KIT_DIR" rev-parse --verify HEAD >/dev/null 2>&1 || { echo broken; return 0; }
  local origin; origin="$(git -C "$KIT_DIR" remote get-url origin 2>/dev/null || true)"
  [ "${origin%.git}" = "${KIT_URL%.git}" ] || { echo wrongremote; return 0; }
  echo ok
}

step_starterkit() {
  heading starterkit "Fetch the Track 3 starter kit"
  info "source: $KIT_URL"
  info "this is a community repository - it is not maintained by this repo and not an official Google product"
  local state; state="$(kit_state)"
  case "$state" in
    broken)      warn "$KIT_DIR has a .git but no checkout - an earlier clone did not finish. Fetching it again." ;;
    wrongremote) warn "$KIT_DIR is a clone of a different repository, not $KIT_URL. Fetching it again." ;;
  esac
  if [ "$state" = ok ] && [ "$FORCE" != 1 ]; then
    info "starter kit already at $KIT_DIR — reusing it (--force to move it aside and re-clone)"
    # Reuse never moves an existing checkout to the pin. By mid-lab this folder is the
    # attendee's project, and checking out a different commit under them is exactly the
    # kind of thing --force is criticised for. Say it does not match, and stop there.
    if [ "$DRY" != 1 ] && printf '%s' "$KIT_REF" | grep -qE '^[0-9a-f]{40}$'; then
      local at; at="$(git -C "$KIT_DIR" rev-parse HEAD 2>/dev/null || true)"
      [ "$at" = "$KIT_REF" ] \
        || info "that copy is at ${at:-an unknown commit}, not the pinned $KIT_REF. Leaving it alone - pass --kit-dir DIR to fetch the pinned copy somewhere else"
    fi
  else
    # Never delete this directory. Once the lab starts it holds the participant's own
    # work, so it is moved out of the way rather than removed. Say where it went, and
    # say it twice: by the day of the event this is somebody's project folder.
    if [ -e "$KIT_DIR" ]; then
      local aside; aside="$KIT_DIR.superseded.$(date +%Y%m%d%H%M%S)"
      warn "moving $KIT_DIR aside to $aside - nothing is deleted"
      warn "anything you had built in $KIT_DIR is now in $aside"
      run mv "$KIT_DIR" "$aside"
    fi
    run mkdir -p "$(dirname "$KIT_DIR")"
    # Two things here are deliberate, and neither is what a plain `git clone` does.
    #
    # GIT_TERMINAL_PROMPT=0 and GIT_ASKPASS=true are the event-day guard. If this
    # community repository is renamed, deleted or made private, an anonymous fetch gets
    # a 401 and git asks "Username for 'https://github.com':" on the terminal, where it
    # blocks forever with nothing on screen to search for. --yes does not help: it gates
    # this script's own prompt, not git's. With these two set the same case fails in
    # about a second, and we get to say something useful about it.
    #
    # init, fetch, checkout, rather than `git clone --branch`, is what lets KIT_REF be a
    # commit SHA. --branch accepts only a tag or a branch, and a tag in a repository we
    # do not control can be moved after we rehearse against it. Two extra commands buy a
    # pin that upstream cannot change under us.
    local ref="$KIT_REF"
    if [ -n "$ref" ]; then
      info "pinned to $ref"
    else
      ref=HEAD
      warn "--kit-ref is empty - taking whatever is on the default branch of $KIT_URL today"
    fi
    run git init -q "$KIT_DIR"
    run git -C "$KIT_DIR" remote add origin "$KIT_URL"
    run env GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=true \
        git -C "$KIT_DIR" fetch --depth 1 origin "$ref" || {
      # This directory was created seconds ago and holds no work of anyone's, so clear
      # it rather than leave an empty shell for the next run to move aside.
      run rm -rf "${KIT_DIR:?}"
      warn "nothing was left half-applied - re-running this step is safe"
      die "cannot fetch $ref from $KIT_URL. Check your network, or pass --kit-url pointing at a fork or an offline mirror, or --kit-ref naming a commit that exists. This repository does not control that upstream."
    }
    run git -C "$KIT_DIR" checkout -q --detach FETCH_HEAD
  fi
  if [ "$DRY" = 1 ]; then
    info "the kit ships its skills under .agents/skills/ - Antigravity loads them when you open the folder"
  elif [ -d "$KIT_DIR/.agents/skills" ]; then
    local n; n="$(find "$KIT_DIR/.agents/skills" -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
    info "$n starter-kit skill(s) under $KIT_DIR/.agents/skills"
    info "no registration needed - Antigravity loads them when you open that folder"
  else
    warn "no .agents/skills in $KIT_DIR - the kit layout may have changed, check $KIT_URL"
  fi
  if need gh; then info "gh: $(gh --version 2>/dev/null | awk 'NR==1{print $3}')"
  else warn "gh is missing - the kit's publish-to-github skill will download it into ~/.local/bin at the end of the lab"
  fi
  info "Track 3 working folder: $KIT_DIR"
}

step_register() {
  heading register "Register the skills"
  local py="$LAB_HOME/.venv/bin"
  # Track 2 only: the governance lab's scorecard script is what reads this.
  if [ "$TRACK" = 2 ]; then
    grep -q NOVASMART_SCORECARD_HOME "$HOME/.bashrc" "$HOME/.zshrc" 2>/dev/null \
      || info "add to your shell profile:  export NOVASMART_SCORECARD_HOME=\"$LAB_ROOT\""
  fi
  # This registers the google-agents-cli-* lifecycle skills (scaffold, deploy and the
  # rest) with Antigravity. Both tracks need them. It does NOT register the skills that
  # ship inside a repository's own .agents/ folder: Antigravity reads those itself when
  # you open the folder, so Track 3's starter-kit skills need nothing from this step.
  run "$py/agents-cli" setup  || warn "agents-cli setup failed — non-fatal, the assistant can self-register"
  run "$py/agents-cli" update || warn "agents-cli update failed — a version-mismatch warning may appear"
  run "$py/agents-cli" info   || true
}

# ---------- driver ----------
CURRENT_STEP=""

# Nothing is installed until preflight has run and a human has said yes.
# --skip-preflight exists for re-runs and repairs; --yes alone does NOT bypass a NO-GO.
gate() {
  [ "$DRY" = 1 ] && return 0
  # This function has two halves: run preflight, then ask for consent. Skipping the
  # first must not skip the second. Both of these cases used to `return 0` out of the
  # whole function, so `install.sh --skip-preflight`, and any machine where
  # preflight.sh was missing or not executable, changed the laptop without ever
  # showing the screen that says what is about to change. `--skip-preflight` is
  # documented as "do not run preflight first" and nothing more, and the comment above
  # this function already states the rule the code was breaking.
  if [ -n "$ONLY" ]; then
    # Deliberate: --only runs preflight's SECOND half only. A --only run is a repair on
    # a machine that is already known to be failing something, and it is the command
    # printed by verify.sh --fix-hints and by the skill's repair table. Running
    # preflight there would often return NO-GO and refuse the very repair that clears
    # it, which is a worse outcome than a repair with no fresh assessment. The consent
    # half below still runs, narrowed to the one step, because consent is about what is
    # going to change and that does not stop mattering for a repair.
    info "preflight skipped (--only $ONLY repairs one step)"
  elif [ "$SKIP_PREFLIGHT" = 1 ]; then
    info "preflight skipped (--skip-preflight)"
  elif [ ! -x "$SCRIPT_DIR/preflight.sh" ]; then
    warn "preflight.sh not found - continuing without it"
  else
    # `cmd; rc=$?` is NOT set -e safe: the non-zero exit fires the ERR trap before the
    # assignment runs. preflight returns 1 for GO WITH CAVEATS, which is the common case,
    # so this killed the installer on most real machines.
    local pf=0
    bash "$SCRIPT_DIR/preflight.sh" || pf=$?
    case "$pf" in
      0) say "Preflight: GO" ;;
      1) say "Preflight: GO WITH CAVEATS" ;;
      2) printf '\n\033[31mPreflight says NO-GO.\033[0m This laptop is missing something it cannot do without.\n' >&2
         printf 'Fix the blocking items above, or use the provided lab VM.\n' >&2
         printf 'If you believe this is wrong, re-run with --skip-preflight.\n' >&2
         exit 2 ;;
      *) warn "preflight could not assess this machine (exit $pf)" ;;
    esac
  fi
  echo
  if [ -n "$ONLY" ]; then
    # Narrowed disclosure. A repair changes far less than a full run, and listing the
    # full run's effects here would be a false statement about what is about to happen.
    echo "  install.sh is about to run one step on this machine: $ONLY. It will:"
    case "$ONLY" in
      tools)
        echo "    - install packages with $PKG (this needs sudo on Linux)"
        [ "$TRACK" = 3 ] && echo "    - install the GitHub CLI (gh), which Track 3 needs to publish your project"
        ;;
      python)
        echo "    - create $LAB_HOME and a Python 3.14 virtual environment there"
        echo "    - install 120 pinned packages into that virtual environment"
        [ "$FORCE" = 1 ] && echo "    - --force: delete and rebuild $LAB_HOME/.venv first"
        [ "$WITH_EXTRAS" = 1 ] && echo "    - --with-extras: download Playwright's browser into $HOME/.cache/ms-playwright"
        ;;
      skills)
        echo "    - read the lab skills in ${LAB_SKILLS_SRC:-(no source given, so this step does nothing)}"
        echo "    - it writes nothing outside that directory"
        ;;
      sessions)
        echo "    - create session folders under $LAB_ROOT/Desktop/"
        echo "    - replace the lab skill folders inside their .agents/skills/"
        ;;
      register)
        echo "    - register the agents-cli lifecycle skills with Antigravity"
        [ "$TRACK" = 2 ] && echo "    - print one export line for you to add to your shell profile yourself"
        ;;
      starterkit)
        echo "    - clone the community Track 3 starter kit into $KIT_DIR"
        echo "      from $KIT_URL, which this repository does not maintain,"
        echo "      pinned at ${KIT_REF:-whatever its default branch holds today}"
        [ "$FORCE" = 1 ] && echo "    - --force: move an existing $KIT_DIR aside, with any work in it, and fetch again"
        ;;
    esac
    echo "  It edits no shell profile of yours."
    echo "  No other step runs, and nothing outside those paths is touched."
  else
    echo "  install.sh is about to set up Track $TRACK and change this machine. It will:"
    echo "    - install packages with $PKG (this needs sudo on Linux)"
    echo "    - create $LAB_HOME and a Python 3.14 virtual environment there"
    if [ "$TRACK" = 3 ]; then
      echo "    - install the GitHub CLI (gh), which Track 3 needs to publish your project"
      echo "    - clone the community Track 3 starter kit into $KIT_DIR"
      echo "      from $KIT_URL, which this repository does not maintain,"
      echo "      pinned at ${KIT_REF:-whatever its default branch holds today}"
    else
      echo "    - create session folders under $LAB_ROOT/Desktop/"
      echo "    - print one export line for you to add to your shell profile yourself"
    fi
    # This used to promise a shell-profile edit. step_register only ever printed a line
    # for the user to copy, and on Track 3 it does not print even that. Over-disclosing
    # on a consent screen is the safe direction to be wrong in, but it is still wrong.
    echo "  It edits no shell profile of yours."
    echo "  Nothing outside those paths is touched. Re-runnable and idempotent."
  fi
  echo
  if [ "$ASSUME_YES" = 1 ]; then
    info "--yes given, proceeding without asking"
  elif [ ! -t 0 ]; then
    # A real run with nothing to ask on: a pipe, a nohup, an automated rehearsal.
    # Consent cannot be given, so nothing is installed. This used to fall straight
    # into the `read` below, which hit end of file, returned non-zero, tripped the
    # ERR trap and exited with nothing useful on screen. Someone running
    # `curl ... | bash` saw a bare failure and no reason for it.
    #
    # Exit 66, not 0: nothing was installed, and a caller that cannot see a terminal
    # is exactly the caller that needs to be told that in its exit status. A dry run
    # never reaches here, because gate() returns before this on --dry-run.
    printf '\n  Stopped. Nothing was changed.\n' >&2
    printf '  There is no terminal here to ask you for consent on, and this script does\n' >&2
    printf '  not change a machine without being told to. Run it from a terminal, or\n' >&2
    printf '  pass --yes to accept the changes listed above without being asked.\n' >&2
    exit 66
  else
    printf '  Continue? [y/N] '; read -r a
    case "$a" in y|Y) ;; *) echo "  Stopped. Nothing was changed."; exit 0 ;; esac
  fi
}

main() {
  # The Windows notice is its own gate and runs before everything, including the
  # preflight gate, because it can end the run on its own.
  wsl_gate
  [ "$DRY" = 1 ] && say "DRY RUN - nothing will be changed"
  local steps=("${TRACK_STEPS[@]}")
  # Validate --only BEFORE gate, so a typo is still refused with exit 64 straight away
  # instead of after a consent screen for a step that does not exist.
  if [ -n "$ONLY" ]; then
    # shellcheck disable=SC2076
    [[ " ${ALL_STEPS[*]} " == *" $ONLY "* ]] || { echo "unknown step: $ONLY" >&2; exit 64; }
    steps=("$ONLY")
  fi
  # gate is called UNCONDITIONALLY. It used to be `[ -z "$ONLY" ] && gate`, which meant
  # that `install.sh --only python` installed a toolchain, created $LAB_HOME, built a
  # venv and wrote files without ever disclosing any of it or asking anyone. --only is
  # the command this repository tells attendees to run to repair a machine, so it was
  # the most likely path to take and the only one with no consent on it. gate now
  # decides for itself what to skip: preflight yes, consent never.
  gate
  # AFTER the gate, not before it. This used to sit above gate, so a run that then
  # stopped at the consent gate and printed "Stopped. Nothing was changed." had
  # already created $LAB_HOME. One empty directory is a small lie, and on a screen
  # whose whole job is to be believed it is not one worth keeping. Nothing between
  # here and the gate needs the directory: preflight makes its own when it saves a
  # verdict, and run()'s log line is only written once a step is running.
  [ "$DRY" = 1 ] || mkdir -p "$LAB_HOME" 2>/dev/null || true
  for s in "${steps[@]}"; do CURRENT_STEP="$s"; "step_$s"; done
  local vflag=""
  [ "$TRACK" = 3 ] && vflag=" --track 3"
  say "Done. Now run:  bash $SCRIPT_DIR/verify.sh --readiness$vflag"
  if [ "$TRACK" = 3 ]; then
    info "Then open $KIT_DIR in Antigravity."
  else
    info "Then open $LAB_ROOT/Desktop/Session1 in Antigravity."
  fi
}
main
