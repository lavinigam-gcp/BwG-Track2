#!/usr/bin/env bash
# Can this laptop run the lab? Run this FIRST, before install.sh.
# Produces a pre-setup report card and a GO / GO WITH CAVEATS / NO-GO verdict.
# Every check is track-neutral: it tests the machine, never the lab content.
# Exit: 0 GO · 1 GO WITH CAVEATS · 2 NO-GO · 64 bad flag
# Installs nothing, changes no setting. Records its verdict for verify.sh to read.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_HOME="${LAB_HOME:-$HOME/novasmart-lab}"

# --track changes nothing that is measured. It is recorded on the report card and in
# the JSON so a saved verdict says which track it was collected for, which is what
# makes it traceable when someone pastes one into a support thread. Deliberately not
# a check row: adding one would move the OK/WARN/FAIL counts and the verdict with them.
JSON=0; TRACK="${BWG_TRACK:-}"
while [ $# -gt 0 ]; do case "$1" in
  --json) JSON=1 ;;
  --track) TRACK="${2:?--track needs 2 or 3}"; shift ;;
  -h|--help) sed -n '2,6p' "$0"; echo "Usage: preflight.sh [--json] [--track {2,3}]"; exit 0 ;;
  # Same reasoning as verify.sh: silent fallthrough turned `preflight.sh --jsno` into
  # a human report card printed to a caller that had asked for JSON and would go on
  # to misparse it. A mistyped flag is refused, not guessed at. This arm has to sit
  # after -h|--help, or it shadows help and shellcheck flags the unreachable arm.
  *) echo "unknown option: $1 (see --help)" >&2; exit 64 ;;
esac; shift; done
case "${TRACK:-}" in ""|2|3) ;; *) echo "unknown track: $TRACK (use 2 or 3)" >&2; exit 64 ;; esac
TRACK_LABEL="${TRACK:-not given}"
# One shared definition of "have the lab credentials been issued yet?", the same file
# verify.sh sources, so the report card and the readiness report cannot drift apart.
# shellcheck source=setup/lab-phase.sh
. "$SCRIPT_DIR/lab-phase.sh"

ROWS=(); FAIL=0; WARN=0; OK=0
add() { # name  status(OK|WARN|FAIL)  found  requirement  advice
  ROWS+=("$1|$2|$3|$4|$5")
  case "$2" in OK) OK=$((OK+1));; WARN) WARN=$((WARN+1));; FAIL) FAIL=$((FAIL+1));; esac
}

# ---------- platform ----------
KERNEL="$(uname -s)"; ARCH="$(uname -m)"; OSNAME="?"; OSVER="0"; PLAT="?"
case "$KERNEL" in
  Darwin)
    PLAT=macos; OSNAME="macOS"; OSVER="$(sw_vers -productVersion 2>/dev/null || echo 0)"
    # uname -m lies under Rosetta; this pierces it.
    if [ "$(sysctl -n hw.optional.arm64 2>/dev/null || echo 0)" = 1 ]; then ARCH=arm64; fi
    ;;
  Linux)
    PLAT=linux
    # shellcheck disable=SC1091
    [ -r /etc/os-release ] && . /etc/os-release && OSNAME="${NAME:-Linux}" && OSVER="${VERSION_ID:-0}"
    grep -qi microsoft /proc/version 2>/dev/null && PLAT=wsl2
    ;;
  *) PLAT=unsupported; OSNAME="$KERNEL" ;;
esac

verge() { [ "$(printf '%s\n%s\n' "$2" "$1" | sort -t. -k1,1n -k2,2n | awk 'NR==1')" = "$2" ]; }

if [ "$PLAT" = unsupported ]; then
  add "operating system" FAIL "$OSNAME" "macOS, Linux, or Windows+WSL2" \
      "Native Windows cannot run this: a required package (uvloop) has no Windows build. Install WSL2, or use the lab VM."
else
  case "$PLAT" in
    macos) verge "$OSVER" 13 && add "operating system" OK "macOS $OSVER" "macOS 13+" "" \
                              || add "operating system" FAIL "macOS $OSVER" "macOS 13+" "Chrome and the toolchain need macOS 13 Ventura or newer. Upgrade, or use the lab VM." ;;
    linux)
      # Test the actual requirement rather than the release number. Rolling releases
      # legitimately have no VERSION_ID, and Antigravity's real floor is glibc 2.28.
      # awk, not `| head -1`: head closes the pipe early, ldd takes SIGPIPE, and with
      # pipefail the whole substitution fails intermittently and reports glibc 0.
      GLIBC="$(ldd --version 2>/dev/null | awk 'NR==1{print $NF}')"
      [ -n "$GLIBC" ] || GLIBC=0
      if verge "$GLIBC" 2.28; then
        add "operating system" OK "$OSNAME ${OSVER#0} (glibc $GLIBC)" "glibc 2.28+" ""
      else
        add "operating system" FAIL "$OSNAME ${OSVER#0} (glibc $GLIBC)" "glibc 2.28+" \
          "Antigravity requires glibc 2.28 or newer and will not launch here. Upgrade the distribution, or use the lab VM."
      fi ;;
    # Windows is LIMITED SUPPORT, so this row is a warning and never a clean GO.
    # WSL2 runs the toolchain, but Antigravity has been seen to refuse to open a
    # folder that lives on a WSL path, and the only known workaround is not durable.
    # A machine that can do the lab but may strand the attendee is a caveat, not a
    # pass. It is not a NO-GO either: the toolchain and gcloud do work here.
    wsl2)  add "operating system" WARN "$OSNAME $OSVER (WSL2)" "WSL2 (limited support)" \
               "Windows with WSL2 is limited support, not a peer of macOS and Linux. Antigravity may fail to open the setup folder on a WSL path and report 'folder not found'. Mapping the WSL share to a drive letter can work around that, but the mapping DOES NOT survive a restart and has to be redone. Plan to finish setup on location at the event, or use the provided lab VM." ;;
  esac
fi

case "$ARCH" in
  x86_64|amd64|arm64|aarch64) add "cpu architecture" OK "$ARCH" "x86_64 or arm64" "" ;;
  *) add "cpu architecture" FAIL "$ARCH" "x86_64 or arm64" "No builds exist for this architecture. Use the lab VM." ;;
esac

# ---------- capacity ----------
CORES="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 0)"
if   [ "$CORES" -ge 4 ] 2>/dev/null; then add "cpu cores" OK "$CORES" "4+" ""
elif [ "$CORES" -ge 2 ] 2>/dev/null; then add "cpu cores" WARN "$CORES" "4+" "2 cores works but installs and the IDE will feel slow."
else add "cpu cores" FAIL "${CORES:-unknown}" "4+" "Too few cores for the IDE plus a browser. Use the lab VM."; fi

RAM_GIB=0
case "$PLAT" in
  macos) B="$(sysctl -n hw.memsize 2>/dev/null || echo 0)"; RAM_GIB=$(( B / 1073741824 )) ;;
  *)     K="$(awk '/^MemTotal:/{print $2}' /proc/meminfo 2>/dev/null || echo 0)"; RAM_GIB=$(( K / 1048576 )) ;;
esac
# Linux reports usable RAM (~6% below nominal), macOS reports nominal. Gate below the nominal figure.
if   [ "$RAM_GIB" -ge 15 ]; then add "memory" OK "${RAM_GIB} GiB" "16 GB recommended" ""
elif [ "$RAM_GIB" -ge 7 ];  then add "memory" WARN "${RAM_GIB} GiB" "16 GB recommended" "8 GB is the floor. Close other applications during the lab, or expect swapping."
else add "memory" FAIL "${RAM_GIB} GiB" "8 GB minimum" "Not enough memory to run the IDE, a browser and the toolchain. Use the lab VM."; fi
[ "$PLAT" = wsl2 ] && add "wsl memory note" WARN "${RAM_GIB} GiB visible" "host has more" \
  "WSL2 defaults to half the host's RAM. Raise it in .wslconfig if this is tight."

DISK_GIB="$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2{print int($4/1048576)}')"
DISK_GIB="${DISK_GIB:-0}"
if   [ "$DISK_GIB" -ge 15 ]; then add "free disk" OK "${DISK_GIB} GiB" "15 GiB" ""
elif [ "$DISK_GIB" -ge 10 ]; then add "free disk" WARN "${DISK_GIB} GiB" "15 GiB" "Tight. Skip the optional extras, or free up space first."
else add "free disk" FAIL "${DISK_GIB} GiB" "15 GiB" "Not enough free space. Free some up, or use the lab VM."; fi
if [ "$PLAT" = wsl2 ] && [ -d /mnt/c ]; then
  CGIB="$(df -Pk /mnt/c 2>/dev/null | awk 'NR==2{print int($4/1048576)}')"
  [ -n "${CGIB:-}" ] && [ "$CGIB" -lt 15 ] && add "windows C: space" FAIL "${CGIB} GiB" "15 GiB" \
    "WSL2 reports a large virtual disk, but the real space is on C:. Free space on Windows first."
fi

# ---------- prerequisites ----------
for t in git curl; do
  if command -v "$t" >/dev/null 2>&1; then add "$t" OK "present" "required" ""
  else add "$t" FAIL "missing" "required" "Install $t before continuing."; fi
done
if command -v python3 >/dev/null 2>&1; then add "python3" OK "$(python3 -V 2>&1 | awk '{print $2}')" "any (3.14 installed later)" ""
else add "python3" WARN "missing" "any" "Not fatal: uv installs its own Python 3.14."; fi
if [ "$PLAT" = macos ]; then
  command -v brew >/dev/null 2>&1 && add "homebrew" OK "present" "required on macOS" "" \
    || add "homebrew" FAIL "missing" "required on macOS" "Install Homebrew first: https://brew.sh"
fi
if command -v sudo >/dev/null 2>&1 && [ "$PLAT" != macos ]; then
  sudo -n true 2>/dev/null && add "sudo" OK "no password needed" "needed for apt" "" \
    || add "sudo" WARN "will prompt" "needed for apt" "You will be asked for your password during the tool step."
fi

# ---------- identity ----------
# The lab is played with the issued Qwiklabs account. A personal or corporate login
# points at the wrong project and fails in ways that look like broken tooling.
#
# Before the event nobody has that account yet, so this row cannot be a warning then.
# It fired for every attendee on every pre-event run, its advice asked for credentials
# that do not exist, and because any WARN below becomes GO WITH CAVEATS it made a clean
# GO unreachable for everyone. install.sh re-runs this script inside its own gate, so
# that advice also reached the attendee mid-install, which is where it did the damage.
# The row still earns its place on the day; it is only the pre-event status and advice
# that change. The phase comes from lab-phase.sh, the same file verify.sh sources, so
# the two scripts cannot disagree about one laptop. It is keyed on the lab project and
# nothing else: see that file for why a credentials file left over from the attendee's
# own work is not evidence that the event has started.
# PHASE is settled OUTSIDE the gcloud branch, exactly as verify.sh:249 settles it, and
# with the same empty project id when gcloud is absent. It used to be assigned inside
# the branch, so on a laptop with no gcloud at all BWG_PHASE=day-of moved verify.sh to
# the day-of branch while preflight.sh went on reporting "phase":"pre-event". That is
# the two scripts disagreeing about one laptop, which is the whole reason lab-phase.sh
# exists, reintroduced one line above the shared helper. lab_phase returns $BWG_PHASE
# first and validates it, so the override and the exit 64 on a bad value both work here
# whether or not gcloud is installed.
PROJ=""
PHASE="$(lab_phase "$PROJ")"
PRE_EVENT=0
[ "$PHASE" = pre-event ] && PRE_EVENT=1
if command -v gcloud >/dev/null 2>&1; then
  ACCT="$(lab_account_id)"
  PROJ="$(lab_project_id)"
  PHASE="$(lab_phase "$PROJ")"
  PRE_EVENT=0
  [ "$PHASE" = pre-event ] && PRE_EVENT=1
  case "${ACCT:-}" in
    "")
      if [ "$PRE_EVENT" = 1 ]; then
        add "google account" OK "not signed in" "issued at the event" ""
      else
        add "google account" WARN "not signed in" "the lab account" \
          "Sign in with the Qwiklabs account issued for this lab, not a personal or work account."
      fi ;;
    *@qwiklabs.net|*@gcpstudent*|*@qwiklabs*)
      add "google account" OK "$ACCT" "the lab account" "" ;;
    *)
      if [ "$PRE_EVENT" = 1 ]; then
        # A personal or work account before the event is normal, so this is not a
        # finding and it carries no advice. Nothing appears under WHAT TO DO, because
        # there is nothing this attendee can do about it yet. The lab project is
        # issued at the event and they switch to it then.
        add "google account" OK "$ACCT" "issued at the event" ""
      else
        add "google account" WARN "$ACCT" "the lab account" \
          "This does not look like a Qwiklabs lab account. Using a personal or corporate account points at the wrong project and can bill your own account. Verify before continuing."
      fi ;;
  esac
fi

# ---------- connectivity ----------
probe() { # label url
  local code
  # `... || echo 000` was wrong: curl ALSO prints 000 on failure, so the value became
  # "000000", the equality test failed, and a BLOCKED endpoint was reported reachable.
  # Assign the fallback rather than appending to the captured output.
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 12 -L "$2" 2>/dev/null)" || code=""
  case "${code:-000}" in
    000) add "$1" FAIL "unreachable" "reachable" "Blocked or offline. Check your network, VPN or firewall." ;;
    *)   add "$1" OK "HTTP $code" "reachable" "" ;;
  esac
}
probe "github.com"        "https://github.com"
probe "pypi.org"          "https://pypi.org/simple/"
probe "storage.googleapis.com" "https://storage.googleapis.com"
probe "antigravity.google" "https://antigravity.google/download"
probe "googleapis.com"    "https://oauth2.googleapis.com"
[ "$PLAT" = macos ] && probe "formulae.brew.sh" "https://formulae.brew.sh/api/formula/git.json"

# TLS interception: a corporate proxy re-signs certificates and breaks pip, curl installers and gcloud.
ISSUER="$(curl -sS -v --max-time 12 https://pypi.org 2>&1 | sed -n 's/.*issuer: .*O=\([^,]*\).*/\1/p' | awk 'NR==1')"
if [ -n "$ISSUER" ]; then
  case "$ISSUER" in
    *"Let's Encrypt"*|*DigiCert*|*Google*|*Amazon*|*Sectigo*|*GlobalSign*|*"GTS"*)
      add "tls not intercepted" OK "$ISSUER" "public CA" "" ;;
    *) add "tls not intercepted" WARN "$ISSUER" "public CA" \
         "A proxy is re-signing TLS. pip, curl installers and gcloud may fail. Get your CA bundle from IT and set REQUESTS_CA_BUNDLE and SSL_CERT_FILE." ;;
  esac
fi

# git clone over https must actually work, not just github.com responding
if command -v git >/dev/null 2>&1; then
  if git ls-remote --exit-code https://github.com/git/git >/dev/null 2>&1; then
    add "git clone works" OK "yes" "required" ""
  else
    add "git clone works" FAIL "blocked" "required" "github.com answers but git over HTTPS is blocked. Check proxy settings."
  fi
fi

# ---------- verdict ----------
VERDICT="GO"; CODE=0
[ "$WARN" -gt 0 ] && { VERDICT="GO WITH CAVEATS"; CODE=1; }
[ "$FAIL" -gt 0 ] && { VERDICT="NO-GO";           CODE=2; }

# Record the verdict where verify.sh can find it.
#
# The rule that a NO-GO laptop is shown no sign-in content lived only behind
# `verify.sh --preflight-verdict no-go`. Nothing printed that flag: the README and the
# landing page tell the attendee to run `verify.sh --readiness` bare, so the rule held
# when the assistant drove the check and quietly did not hold when a human followed the
# written instructions. That is backwards, because the human path is the fallback for
# exactly the attendee whose machine is in trouble.
#
# So the word is written down here instead of being carried by hand. verify.sh reads
# this file when no flag is given, and an explicit flag still wins. The timestamp and
# the track are recorded too, so verify.sh can show where its verdict came from and a
# stale one is visible rather than silent.
#
# Best effort, always. A machine where this cannot be written still gets its verdict
# and its exit code: this file is a convenience for the next script, never a condition
# of this one. Hence the `|| true` and the discarded errors.
VERDICT_FILE="$LAB_HOME/preflight-verdict"
save_verdict() {
  local word
  case "$CODE" in 0) word=go ;; 1) word=caveats ;; 2) word=no-go ;; *) return 0 ;; esac
  mkdir -p "$LAB_HOME" 2>/dev/null || return 0
  {
    printf 'verdict=%s\n' "$word"
    printf 'exit=%s\n'    "$CODE"
    printf 'recorded=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'track=%s\n'   "$TRACK_LABEL"
  } > "$VERDICT_FILE" 2>/dev/null || true
  return 0
}
save_verdict

if [ "$JSON" = 1 ]; then
  # Escape every field, the same two substitutions verify.sh:139 uses, in the same
  # order: backslashes first, then double quotes, or the backslash pass would escape
  # the backslashes the quote pass had just added. Several of these fields carry
  # strings this repository does not control and cannot predict:
  #   - "found" on the TLS row is an issuer name read out of curl -v output
  #   - OSNAME comes from NAME= in /etc/os-release
  #   - the account row carries whatever gcloud config get-value account returns
  #   - the python, node and gcloud rows carry third-party version strings
  # One double quote or one backslash in any of them used to produce invalid JSON.
  # The consumers are CI's own json.loads and the setup skill, so the failure showed
  # up as an unexplained CI break, or as a skill unable to read a report card from
  # exactly the one unusual laptop that most needed reading. Every field goes through
  # this, including the static-looking ones, so a future row cannot reopen the hole.
  jesc() { local v="${1//\\/\\\\}"; printf '%s' "${v//\"/\\\"}"; }
  printf '{"verdict":"%s","exit":%d,"track":"%s","phase":"%s","ok":%d,"warn":%d,"fail":%d,"platform":"%s","arch":"%s","checks":[' \
    "$(jesc "$VERDICT")" "$CODE" "$(jesc "$TRACK_LABEL")" "$(jesc "$PHASE")" \
    "$OK" "$WARN" "$FAIL" "$(jesc "$PLAT")" "$(jesc "$ARCH")"
  for i in "${!ROWS[@]}"; do
    IFS='|' read -r n s f r a <<< "${ROWS[$i]}"
    [ "$i" -gt 0 ] && printf ','
    printf '{"check":"%s","status":"%s","found":"%s","needs":"%s","advice":"%s"}' \
      "$(jesc "$n")" "$(jesc "$s")" "$(jesc "$f")" "$(jesc "$r")" "$(jesc "$a")"
  done
  printf ']}\n'
  exit "$CODE"
fi

echo
echo "  PRE-SETUP REPORT CARD"
echo "  $OSNAME $OSVER · $ARCH · $(date +%Y-%m-%d)"
echo "  track $TRACK_LABEL · every check below is the same for either track"
# Say which phase this card was collected in. A support helper reading a pasted card
# needs to know whether the lab project had been issued yet, because that is what
# decides whether the account row means anything.
if [ "$PHASE" = day-of ]; then
  echo "  phase day-of · the lab project is set, so the event has started"
else
  echo "  phase pre-event · no lab project yet, which is expected before the event"
fi
printf '  '; printf '%.0s=' {1..72}; echo
printf "  %-22s %-9s %-22s %s\n" CHECK STATUS FOUND NEEDS
printf '  '; printf '%.0s-' {1..72}; echo
for r in "${ROWS[@]}"; do
  IFS='|' read -r n s f req a <<< "$r"
  [ "${#f}" -gt 22 ] && f="${f:0:19}..."
  printf "  %-22s %-9s %-22s %s\n" "$n" "$s" "$f" "$req"
done
printf '  '; printf '%.0s-' {1..72}; echo
printf "  %d OK · %d warning · %d blocking\n" "$OK" "$WARN" "$FAIL"
echo
if [ "$FAIL" -gt 0 ] || [ "$WARN" -gt 0 ]; then
  echo "  WHAT TO DO"
  for r in "${ROWS[@]}"; do
    IFS='|' read -r n s f req a <<< "$r"
    [ "$s" != OK ] && [ -n "$a" ] && printf "  [%s] %s\n        %s\n" "$s" "$n" "$a"
  done
  echo
fi
printf '  VERDICT: %s\n\n' "$VERDICT"
case "$CODE" in
  0) echo "  This laptop can run the lab. Next:  bash setup/install.sh" ;;
  1) echo "  This laptop can probably run the lab, but read the warnings above first."
     echo "  If any look serious for your machine, use the provided lab VM instead."
     echo "  To continue anyway:  bash setup/install.sh" ;;
  2) echo "  This laptop should NOT be used for the lab."
     echo "  Fix the blocking items above, or use the provided lab VM." ;;
esac
echo
exit "$CODE"
