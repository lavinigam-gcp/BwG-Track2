#!/usr/bin/env bash
# Shared definition of "have the lab credentials been issued yet?".
# Sourced by setup/verify.sh and setup/preflight.sh. It defines functions and does no
# work of its own, so running it directly succeeds and prints nothing. It is mode 755
# like every other script in this folder, so the shebang at the top is not a trap: a
# reader who tries it gets silence rather than "permission denied".
#
# The two scripts used to carry their own copy of this test and they drifted, so the
# readiness report and the report card could disagree about the same laptop. One
# definition, in one file, is the only way that cannot happen again.
#
# The signal is the active gcloud project, and nothing else.
#
# Lab credentials are handed out at the event. The project that comes with them is a
# Qwiklabs lab project, whose id always starts with the prefix below, for example
# qwiklabs-gcp-01-a70b04a29bf7. So a lab project is present exactly when the event has
# started for this attendee, and anything else means it has not: no project at all, the
# attendee's own project, their work project, or a project left over from another lab.
#
# What is deliberately NOT part of the test: the application-default credentials file at
# $HOME/.config/gcloud/application_default_credentials.json. That file does not measure
# "this attendee has lab credentials". It measures "this attendee has used Google Cloud
# before". It is written by `gcloud auth application-default login`, it is never removed
# by normal use, and it is not tied to any project, so a developer who signed in to their
# own project two years ago still has it today. Keying the phase on it put most of a room
# of professional developers on the day-of branch a week early and told them to run
# sign-in commands for credentials that did not exist yet. The account name is not part
# of the test either, for the same reason.

# The prefix every Qwiklabs lab project id starts with.
LAB_PROJECT_PREFIX="qwiklabs-gcp-"

# An override, for the edge cases a prefix cannot see: a rehearsal on a project that is
# not a Qwiklabs one, a re-run after the lab project has been torn down, or a support
# helper who needs to read the other phase's wording. Set it to pre-event or day-of.
# Anything else is refused here rather than guessed at, the same way the scripts refuse
# a mistyped --track or --preflight-verdict.
case "${BWG_PHASE:-}" in
  ""|pre-event|day-of) ;;
  *) echo "unknown BWG_PHASE: $BWG_PHASE (use pre-event or day-of)" >&2; exit 64 ;;
esac

# lab_project_id - print the active gcloud project id, or nothing at all.
# Older gcloud releases print the literal string "(unset)" for a project that is not
# set. That string is not empty, so without this guard it reads as a project id and
# every attendee lands on the day-of branch. Current gcloud sends it to stderr instead,
# so this is a guard against the versions attendees already have on their laptops
# rather than against the one on any particular machine today.
lab_project_id() {
  local p
  p="$(gcloud config get-value project 2>/dev/null)"
  case "$p" in "(unset)"|"(not set)") p="" ;; esac
  printf '%s' "$p"
}

# lab_account_id - print the active gcloud account, or nothing at all.
# Same "(unset)" guard as the project, for the same reason.
lab_account_id() {
  local a
  a="$(gcloud config get-value account 2>/dev/null)"
  case "$a" in "(unset)"|"(not set)") a="" ;; esac
  printf '%s' "$a"
}

# lab_phase PROJECT_ID - print pre-event or day-of.
# Takes the project id as an argument rather than reading it again, so a caller that
# has already read it once cannot end up reporting on two different readings.
lab_phase() {
  if [ -n "${BWG_PHASE:-}" ]; then printf '%s' "$BWG_PHASE"; return 0; fi
  case "$1" in
    "$LAB_PROJECT_PREFIX"*) printf 'day-of' ;;
    *)                      printf 'pre-event' ;;
  esac
}
