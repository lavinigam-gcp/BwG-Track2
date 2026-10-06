#!/usr/bin/env bash
# Build with Gemini lab — environment parity check, Track 2 and Track 3.
# The toolchain checks run for both tracks. The rest depend on --track.
# Reference: the lab image of 2026-08-05.
# Exit: 0 all pass · 1 drift · 2 something missing · 3 cannot run (no venv) · 64 bad flag
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LAB_HOME="${LAB_HOME:-$HOME/novasmart-lab}"
LAB_ROOT="${LAB_ROOT:-$HOME}"
KIT_DIR="${KIT_DIR:-}"          # Track 3. Resolved below: it depends on --root.
# The venv is no longer a fixed path. In order: --venv, $LAB_VENV, $LAB_HOME/.venv,
# and finally whatever is already activated. Reporting "cannot run" against a path the
# user never chose is the single most common false failure this script used to produce.
VENV="${LAB_VENV:-}"
VENV_EXPLICIT=0

JSON=0; HINTS=0; READINESS=0; TRACK="${BWG_TRACK:-2}"
# What preflight said at step 2. This script does not and must not derive it: preflight
# owns those three words, and a second opinion computed here would drift from the card
# the attendee already read. It is an input, it affects only the readiness text below,
# and it changes no exit code. Default "unknown" means nobody told us, so the event-side
# logic decides on its own, exactly as it did before this flag existed.
PF_VERDICT=unknown
# Set when the operator named a verdict on the command line. An explicit word always
# beats the one preflight.sh saved, the same way an explicit --venv beats an activated
# virtualenv: reporting on something the operator did not ask for is the bug.
PF_EXPLICIT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON=1 ;;
    --fix-hints) HINTS=1 ;;
    --readiness) READINESS=1; HINTS=1 ;;
    --preflight-verdict) PF_VERDICT="${2:?--preflight-verdict needs go, caveats, no-go or unknown}"; PF_EXPLICIT=1; shift ;;
    --track) TRACK="${2:?--track needs 2 or 3}"; shift ;;
    --root) LAB_ROOT="${2:?--root needs a directory}"; shift ;;
    --lab-home) LAB_HOME="${2:?--lab-home needs a directory}"; shift ;;
    --venv) VENV="${2:?--venv needs a directory}"; VENV_EXPLICIT=1; shift ;;
    --kit-dir) KIT_DIR="${2:?--kit-dir needs a directory}"; shift ;;
    -h|--help) sed -n '2,5p' "$0"
               echo "Usage: verify.sh [--json] [--fix-hints] [--readiness] [--track {2,3}]"
               echo "                 [--root DIR] [--lab-home DIR] [--venv DIR] [--kit-dir DIR]"
               echo "                 [--preflight-verdict {go,caveats,no-go,unknown}]"
               echo ""
               echo "  --preflight-verdict  what preflight.sh said at step 2. Changes only the"
               echo "                       readiness text, never the exit code. Default: unknown"
               exit 0 ;;
    # Without this arm anything unrecognised fell through to the shift and vanished.
    # "verify.sh --trak 3", or "verify.sh 3" from someone copying the installer's own
    # prompt, then ran the Track 2 profile on a Track 3 laptop and reported missing
    # session folders. Every remedy it printed made that machine worse.
    # This has to sit after -h|--help, not before it: a *) placed first shadows help,
    # and shellcheck flags the unreachable arm as SC2221/SC2222.
    *) echo "unknown option: $1 (see --help)" >&2; exit 64 ;;
  esac
  shift
done
case "$TRACK" in 2|3) ;; *) echo "unknown track: $TRACK (use 2 or 3)" >&2; exit 64 ;; esac
# Same treatment as --track: a mistyped verdict must be refused, not silently treated
# as unknown. Silently falling back is how "verify.sh --preflight-verdict nogo" would
# print the day-of block to somebody preflight had already told to use the lab VM.
case "$PF_VERDICT" in
  go|caveats|no-go|unknown) ;;
  *) echo "unknown preflight verdict: $PF_VERDICT (use go, caveats, no-go or unknown)" >&2; exit 64 ;;
esac
# Whether the lab credentials have been issued is decided in one place, shared with
# preflight.sh, so the report card and the readiness report cannot disagree about the
# same laptop. It also validates BWG_PHASE, which is why it is sourced with the other
# argument checks rather than at the top of the file.
# shellcheck source=setup/lab-phase.sh
. "$SCRIPT_DIR/lab-phase.sh"

# Where the verdict came from, shown in the readiness report so a stale one is visible.
PF_SOURCE="preflight has not recorded a verdict yet"
[ "$PF_EXPLICIT" = 1 ] && PF_SOURCE="given with --preflight-verdict"
# Read the verdict preflight.sh saved, unless the operator named one.
#
# The NO-GO rule used to be reachable only by passing the flag, and nothing printed the
# flag: the README and the landing page both say to run `verify.sh --readiness` bare.
# So the rule held for the assistant and silently did not hold for a human following
# the written instructions. Reading the file closes that gap without asking anybody to
# remember a word. A missing or damaged file means nobody told us, which is `unknown`,
# which is exactly what this script did before the file existed.
if [ "$PF_EXPLICIT" = 0 ] && [ -f "$LAB_HOME/preflight-verdict" ]; then
  pf_w=""; pf_when=""; pf_track=""
  while IFS='=' read -r pf_k pf_v; do
    case "$pf_k" in
      verdict)  pf_w="$pf_v" ;;
      recorded) pf_when="$pf_v" ;;
      track)    pf_track="$pf_v" ;;
    esac
  done < "$LAB_HOME/preflight-verdict"
  case "$pf_w" in
    go|caveats|no-go)
      PF_VERDICT="$pf_w"
      PF_SOURCE="recorded ${pf_when:-at an unknown time} for track ${pf_track:-not given}"
      ;;
    *) PF_SOURCE="the saved verdict could not be read, so treating it as unknown" ;;
  esac
fi

SESSION="$LAB_ROOT/Desktop/Session1"
[ -n "$KIT_DIR" ] || KIT_DIR="$LAB_ROOT/Desktop/build-with-gemini"

[ -n "$VENV" ] || VENV="$LAB_HOME/.venv"
# Falling back to an activated venv is a convenience, not an override. If the operator
# named one with --venv, reporting on a different one is a false pass against the very
# path they asked about.
[ "$VENV_EXPLICIT" = 1 ] || [ -x "$VENV/bin/python" ] || [ -z "${VIRTUAL_ENV:-}" ] || VENV="$VIRTUAL_ENV"
PY="$VENV/bin/python"
[ -x "$PY" ] || PY="$(command -v python3 || true)"

pass=0; drift=0; missing=0
ROWS=()

chk() { # name  match  found  mode(exact|prefix|any)  display  hint
  local n=$1 e=$2 f=$3 m=${4:-exact} d=${5:-$2} hint=${6:-} s=DRIFT
  if   [ -z "$f" ];       then s=MISSING
  elif [ "$m" = any ];    then s=OK
  elif [ "$m" = prefix ]; then case "$f" in "$e"*) s=OK ;; esac
  elif [ "$e" = "$f" ];   then s=OK
  fi
  case $s in OK) pass=$((pass+1));; DRIFT) drift=$((drift+1));; MISSING) missing=$((missing+1));; esac
  # A plain "-", not an em dash. printf "%-22s" pads by bytes, an em dash is three of
  # them in UTF-8, and every MISSING row therefore came out two columns short.
  ROWS+=("$n|$d|${f:--}|$s|$hint")
}
ver() { "$PY" -c "import importlib.metadata as m;print(m.version('$1'))" 2>/dev/null; }
# Prints nothing when the count is zero, so chk's "any" mode reports MISSING rather
# than treating the string "0" as a find.
kitskills() { find "$KIT_DIR/.agents/skills" -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ' | grep -v '^0$'; }

if [ ! -x "$VENV/bin/python" ]; then
  if [ "$JSON" = 1 ]; then
    # Escape before interpolating. This is the only JSON field in these three scripts
    # that carries a filesystem path straight from --venv, $LAB_VENV or $LAB_HOME, and
    # a quote or a backslash anywhere in it produced output the skill could not parse.
    # Every other field is a static string or a tool version number.
    esc="${VENV//\\/\\\\}"; esc="${esc//\"/\\\"}"
    printf '{"status":"cannot-run","reason":"no venv at %s"}\n' "$esc"
  else
    echo "cannot run: no virtual environment at $VENV — see install.sh --only python, or pass --venv DIR"
  fi
  exit 3
fi

chk python       "3.14"   "$("$PY" -c 'import platform;print(platform.python_version())' 2>/dev/null)" prefix "3.14.x"           "install.sh --only python"
chk node         "24."    "$(node -v 2>/dev/null | tr -d v)"                                          prefix "24.x"             "install.sh --only tools"
chk gcloud       ""       "$(gcloud version 2>/dev/null | awk '/Google Cloud SDK/{print $4}')"        any    "any (img 579)"    "install.sh --only tools"
chk google-adk   "2.2.0"  "$(ver google-adk)"                                                         exact  "2.2.0"            "install.sh --only python"
chk agents-cli   "1.3.1"  "$(ver google-agents-cli)"                                                  exact  "1.3.1"            "install.sh --only python"
chk google-genai "2.16.0" "$(ver google-genai)"                                                       exact  "2.16.0"           "install.sh --only python"
# litellm and an OpenAI client used to arrive via google-cloud-aiplatform[evaluation].
# Nothing in these labs uses them, so they are excluded - assert they stay excluded,
# which also catches an install that forgot --no-deps and let the resolver re-add them.
chk no-vendor-sdk "0"      "$("$PY" -c "import importlib.metadata as m;print(sum(1 for d in m.distributions() if (d.metadata['Name'] or '').lower() in ('litellm','openai','tiktoken','tokenizers','cdp')))" 2>/dev/null)" exact "0 pkgs" "install.sh --only python --force"

# Everything above is the shared toolchain: both tracks install it and both need it.
# Everything below belongs to one track. A Track 3 laptop has no Desktop/SessionN and
# no governance-lab skill, so asserting those against it reports failures that are not
# real. The fix is a second profile, not a weaker assertion: Track 2 keeps every check
# it had, exactly as it had it.
if [ "$TRACK" = 2 ]; then
  # The hint needs --force. This row goes DRIFT the moment anyone pip-installs one extra
  # thing into the lab venv, and plain --only python runs `uv pip install --no-deps -r
  # lock`, which never uninstalls anything. Only rebuilding the venv clears it. --force
  # is safe here: it rebuilds $LAB_HOME/.venv, which holds no work of the attendee's.
  chk packages     "120"    "$("$PY" -c "import importlib.metadata as m;print(sum(1 for d in m.distributions() if (d.metadata['Name'] or '') not in ('pip','setuptools','wheel')))" 2>/dev/null)" exact "120" "an extra package is installed - rebuild with install.sh --only python --force"
  chk sessions     "3"      "$(ls -d "$LAB_ROOT"/Desktop/Session[123]/.agents/skills 2>/dev/null | wc -l | tr -d ' ')" exact "3"  "install.sh --only sessions"

  # The lab skills ship separately from this repository. If none are installed, these two
  # checks are not applicable - they must not fail a software-only setup.
  if [ -n "$(ls -A "$SESSION/.agents/skills" 2>/dev/null)" ]; then
    chk lab-skill    "ok"   "$([ -f "$SESSION/.agents/skills/novasmart-governance-lab/SKILL.md" ] && echo ok)" exact "ok" "install.sh --only sessions --skills-src DIR"
    # component-aware: a bare /config also matches /configure in documentation URLs
    chk config-paths "0"    "$(grep -rlE '(^|[[:space:]`\"(])/config([^a-zA-Z]|$)' "$SESSION/.agents/skills" 2>/dev/null | wc -l | tr -d ' ')" exact "0 files" "install.sh --only skills --skills-src DIR"
  else
    ROWS+=("lab-skills|not installed|n/a|SKIP|see README - skills are distributed separately")
  fi
else
  # Track 3 profile. The starter kit is a community repository that this repo does not
  # control. There is deliberately no package-count check: Track 3 participants add
  # their own dependencies, so an exact count would fail on a correct machine. There is
  # deliberately no SKIP branch either: unlike the Track 2 skills, install.sh --track 3
  # does fetch the kit, so a missing kit is a real failure.
  #
  # Be honest about the coupling. `kit` and `kit-skills` check the shape the lab depends
  # on. `kit-mcp` and `kit-publish` assert two exact upstream paths, so they are a
  # deliberate pin on someone else's file layout and they will break if upstream
  # reorganises. install.sh pins the kit to KIT_REF for exactly this reason: these two
  # rows and that pin have to be bumped together, after a rehearsal.
  #
  # `kit` asks git rather than looking for a .git directory, and matches install.sh's
  # kit_state. An interrupted clone leaves .git with no checkout, and calling that OK is
  # a false pass on the one machine that cannot run the lab at all.
  chk kit          "ok"     "$([ -d "$KIT_DIR/.git" ] && git -C "$KIT_DIR" rev-parse --verify HEAD >/dev/null 2>&1 && echo ok)" exact "ok" "install.sh --track 3 --only starterkit"
  # Never recommend --force here. These rows fire when upstream changed shape, which
  # re-cloning the same upstream cannot fix, and --force moves the attendee's project
  # folder aside to do it. Point at a fresh folder or at a human instead.
  chk kit-skills   ""       "$(kitskills)"                         any   "1 or more" "fetch into a NEW folder: install.sh --track 3 --only starterkit --kit-dir DIR"
  chk kit-mcp      "ok"     "$([ -f "$KIT_DIR/.agents/mcp_config.json" ] && echo ok)" exact "ok" "upstream kit layout changed - see TROUBLESHOOTING.md. Do not --force over your work"
  chk kit-publish  "ok"     "$([ -f "$KIT_DIR/.agents/skills/publish-to-github/publish.sh" ] && echo ok)" exact "ok" "upstream kit layout changed - see TROUBLESHOOTING.md. Do not --force over your work"
  # gh is not optional for Track 3: publish-to-github is the last step of the lab.
  chk gh           ""       "$(gh --version 2>/dev/null | awk 'NR==1{print $3}')" any "any" "install.sh --track 3 --only tools"
fi

total=$((pass+drift+missing))
code=0; [ "$drift" -gt 0 ] && code=1; [ "$missing" -gt 0 ] && code=2

if [ "$JSON" = 1 ]; then
  printf '{"track":%d,"pass":%d,"drift":%d,"missing":%d,"total":%d,"exit":%d,"checks":[' "$TRACK" "$pass" "$drift" "$missing" "$total" "$code"
  for i in "${!ROWS[@]}"; do
    IFS='|' read -r n d f s hint <<< "${ROWS[$i]}"
    [ "$i" -gt 0 ] && printf ','
    printf '{"name":"%s","needed":"%s","found":"%s","status":"%s","fix":"%s"}' "$n" "$d" "$f" "$s" "$hint"
  done
  printf ']}\n'
else
  printf "  %-16s %-18s %-22s %s\n" CHECK NEEDED FOUND STATUS
  printf '  '; printf '%.0s-' {1..66}; echo
  for r in "${ROWS[@]}"; do
    IFS='|' read -r n d f s hint <<< "$r"
    printf "  %-16s %-18s %-22s %s\n" "$n" "$d" "$f" "$s"
  done
  echo
  echo "  track      : $TRACK"
  echo "  venv       : $VENV"
  [ -f "$REPO_DIR/skills/PROVENANCE.txt" ] && echo "  skills     : $(head -1 "$REPO_DIR/skills/PROVENANCE.txt")"
  if [ "$TRACK" = 3 ]; then
    echo "  starter kit: $KIT_DIR"
    echo "  kit skills : $(ls -1 "$KIT_DIR/.agents/skills" 2>/dev/null | tr '\n' ' ')"
    echo "  gh         : $(command -v gh >/dev/null 2>&1 && gh --version 2>/dev/null | awk 'NR==1{print $3}' || echo MISSING)"
  else
    echo "  in Session1: $(ls -1 "$SESSION/.agents/skills" 2>/dev/null | tr '\n' ' ')"
    echo "  scorecard  : ${NOVASMART_SCORECARD_HOME:-UNSET — set it, see runbook 4.4}"
  fi
  # Identity is read once, here, and both output zones below use these four values.
  # It used to be read again inside --readiness, which is how the footer and the
  # readiness rows ended up disagreeing: the footer had no pre-event wording at all,
  # so a laptop the readiness report called "expected before the event" was still
  # scolded three lines higher for not being on the lab account.
  ACCT="$(lab_account_id)"
  PROJ="$(lab_project_id)"
  ADC=0
  [ -f "$HOME/.config/gcloud/application_default_credentials.json" ] && ADC=1
  # The phase comes from lab-phase.sh, which keys it on the lab project and nothing
  # else. See that file for why the credentials file is not part of the test.
  PRE_EVENT=0; [ "$(lab_phase "$PROJ")" = pre-event ] && PRE_EVENT=1
  if [ "$PRE_EVENT" = 1 ]; then
    # Before the event this footer has to stay true for a laptop that is already set
    # up for the attendee's own work. Saying "project: none" to someone who has one,
    # or "adc: MISSING" to someone who has credentials, is how the old wording lost
    # people's trust in the rest of the report. State what is there, and say plainly
    # that it is not the lab's.
    echo "  gcp account: ${ACCT:-none} (the lab account is issued to you at the event)"
    if [ -n "$PROJ" ]; then
      echo "  gcp project: $PROJ (your own, not a lab project - the lab project is issued to you at the event)"
    else
      echo "  gcp project: none (issued to you at the event)"
    fi
    if [ "$ADC" = 1 ]; then
      echo "  adc        : present (your own, not a lab credential)"
    else
      echo "  adc        : MISSING (expected before the event)"
    fi
  else
    echo "  gcp account: $ACCT (must be the lab account, not personal or work)"
    echo "  gcp project: $PROJ"
    echo "  adc        : $([ "$ADC" = 1 ] && echo present || echo MISSING)"
  fi
  echo
  echo "  $pass of $total checks OK"
  if [ "$READINESS" = 1 ]; then
    echo
    echo "  READINESS REPORT"
    printf '  '; printf '%.0s=' {1..66}; echo
    sw="not ready"; est="not ready"; auth="not ready"
    # The lab content row means a different thing per track, so name it per track too.
    if [ "$TRACK" = 3 ]; then
      open_dir="$KIT_DIR"; est_label="starter kit cloned"
      est_fix="    - fetch the starter kit: bash setup/install.sh --track 3 --only starterkit"
      [ -d "$KIT_DIR/.agents/skills" ] && est="installed"
    else
      open_dir="$SESSION"; est_label="lab skills in Session1"
      est_fix="    - install the lab skills: bash setup/install.sh --only sessions"
      [ -f "$SESSION/.agents/skills/novasmart-governance-lab/SKILL.md" ] && est="installed"
    fi
    [ "$code" = 0 ] && sw="ready"
    # Whether a LAB project has been issued is the only signal this script has for
    # telling the week before the event apart from the morning of it. Before the
    # event nobody has one, so the sign-in below cannot be done yet: the credentials
    # do not exist. Printing it as homework is what confused every early tester.
    # ACCT, PROJ, ADC and PRE_EVENT were read once above, before the footer.
    # "Signed in" means signed in TO THE LAB: day-of, plus credentials on the machine.
    # A personal project with personal credentials is not signed in to anything the
    # lab can use, and calling it so is what sent people looking for the lab content
    # under their own project.
    [ "$ADC" = 1 ] && [ "$PRE_EVENT" = 0 ] && auth="signed in"
    auth_row="$auth"; proj_row="ask your lab administrator"
    if [ "$PRE_EVENT" = 1 ]; then
      auth_row="$auth - expected before the event"
      proj_row="issued to you at the event"
    fi
    printf "  %-34s %s\n" "software toolchain"        "$sw"
    printf "  %-34s %s\n" "$est_label"                "$est"
    printf "  %-34s %s\n" "google cloud sign-in"      "$auth_row"
    printf "  %-34s %s\n" "antigravity IDE"           "check by hand - open it"
    printf "  %-34s %s\n" "cloud project provisioned" "$proj_row"
    # Say which verdict this report is speaking under and where it came from. Without
    # this line a saved verdict is invisible, and a laptop that was a NO-GO in the
    # hotel last night reads the same as one assessed a minute ago.
    printf "  %-34s %s\n" "preflight verdict"         "$PF_VERDICT ($PF_SOURCE)"
    echo
    # "Still to do" is now only for things the attendee can act on right now, on this
    # laptop. Cloud sign-in is not one of them before the event, so it left this list
    # entirely and became the forward-looking block underneath. Listing it here as a
    # task is what sent a tester hunting for credentials a week before they exist.
    if [ "$sw" = ready ] && [ "$est" = installed ]; then
      if [ "$PF_VERDICT" = no-go ]; then
        # Preflight found something blocking. Everything this script owns is in place,
        # and saying more than that would contradict the block below.
        echo "  Everything this script installs is in place."
      elif [ "$auth" = "signed in" ]; then
        echo "  Your laptop is ready. Open $open_dir in Antigravity and begin."
      else
        echo "  Your laptop is ready. Nothing left to install."
      fi
    else
      echo "  Still to do:"
      [ "$sw"   != ready ]       && echo "    - fix the failing checks above (bash setup/verify.sh --fix-hints --track $TRACK)"
      [ "$est"  != installed ]   && echo "$est_fix"
    fi
    # ---------- what comes next ----------
    # Four arms, and which one runs is decided by the verdict preflight already gave
    # at step 2, plus the phase, plus whether the lab sign-in is finished. Preflight's
    # three words are printed verbatim so the attendee reads the same phrase they saw
    # on the report card. The verdict changes this text and nothing else: the exit
    # code below is the same either way.
    if [ "$PF_VERDICT" = no-go ]; then
      echo
      echo "  Preflight said NO-GO for this laptop."
      echo "    - use the provided lab VM instead"
      echo "    - or ask for a loaner laptop at the event"
      echo "    Your gcloud authentication credentials are given to you at the event."
    elif [ "$auth" = "signed in" ]; then
      # Day of the event, signed in to the lab project. Saying so out loud matters:
      # the report used to simply stop here, and an attendee who reads nothing after
      # the table cannot tell "all good" apart from "the script gave up".
      #
      # "You are ready." is a verdict on the WHOLE card, so it is gated on the whole
      # card passing. It used to be derived from the sign-in alone, and printed under
      # a card that read "software toolchain not ready", "lab skills in Session1 not
      # ready" and "Still to do: fix the failing checks above". The sign-in claim on
      # its own is still worth making, so the else arm makes exactly that claim and
      # nothing wider. $code is 0 only when no row drifted and none is missing.
      echo
      if [ "$sw" = ready ] && [ "$est" = installed ] && [ "$code" = 0 ]; then
        echo "  Signed in to the lab project. You are ready."
      else
        echo "  Signed in to the lab project. Nothing left to do for Google Cloud."
        echo "  Fix the failing checks above and run this again."
      fi
    elif [ "$PRE_EVENT" = 1 ]; then
      # Before the event this is not a to-do list and must not read like one. It
      # carries no commands at all, not even ones labelled "do not run these yet":
      # a command on the screen is read as a thing to type, the label is not, and
      # two rounds of testers proved it by typing them. What the attendee needs to
      # know here is that the wait is expected and that the check will tell them
      # what to do once there is something to do.
      echo
      echo "  Next steps, on the day of the event"
      echo "    Nothing to do for Google Cloud yet. No lab project is set on this"
      echo "    laptop, and before the event that is expected."
      [ -n "$PROJ" ] && echo "    The project set right now, $PROJ, is your own. The lab does not use it."
      [ "$ADC" = 1 ] && echo "    The Google Cloud credentials already on this laptop are your own too."
      echo "    Your gcloud authentication credentials are given to you at the event."
      echo
      echo "    At the event you will be given a lab account and a project ID, and you"
      echo "    will switch this laptop over to them then. Run this readiness check"
      echo "    again once you have them, and it will show you what to do at that"
      echo "    point. There is nothing you can usefully do for Google Cloud before"
      echo "    then."
      [ "$TRACK" = 3 ] && echo "    Track 3 also asks you to sign in to GitHub at the end of the lab. That" \
                       && echo "    one is your own GitHub account, not a lab credential, so it can wait too."
    else
      # A lab project is set but the sign-in is not finished, so it is the day of the
      # event and these are real, runnable instructions rather than a description of
      # the future.
      echo
      echo "  Next steps, now that your lab credentials have been issued"
      echo "    - gcloud auth login && gcloud auth application-default login"
      echo "      then: gcloud config set project PROJECT_ID"
      echo "            gcloud auth application-default set-quota-project PROJECT_ID"
      # This used to repeat "your credentials are given to you at the event", which is
      # the right sentence in the pre-event and NO-GO blocks and a contradiction three
      # lines under a heading that says the credentials have already been issued. What
      # the attendee needs here is where to read the value, not when it arrives.
      echo "      PROJECT_ID is on the lab credentials card you were given."
      echo "    - open Antigravity and sign in with 'Use Google Cloud project instead'"
      echo "    - confirm with your lab administrator that the cloud estate is provisioned"
      [ "$TRACK" = 3 ] && echo "    - gh auth login, for your own GitHub account, when you publish at the end"
    fi
  fi
  if [ "$HINTS" = 1 ] && [ "$code" != 0 ]; then
    echo; echo "  how to fix:"
    for r in "${ROWS[@]}"; do
      IFS='|' read -r n d f s hint <<< "$r"
      # SKIP is not a failure. The lab-skills row is SKIP precisely to say "this must
      # not fail a software-only setup", and listing its hint under "how to fix" put
      # it back alongside the genuine failures it was written to stay out of.
      [ "$s" != OK ] && [ "$s" != SKIP ] && [ -n "$hint" ] && printf "    %-16s %s\n" "$n" "$hint"
    done
  fi
fi
exit "$code"
