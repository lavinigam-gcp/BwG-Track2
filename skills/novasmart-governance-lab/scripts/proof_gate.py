#!/usr/bin/env python3
"""
proof_gate.py - hold a proof (or a log read) until the changes it tests have landed, then let it run.

Usage - always as the first line of the SAME command as the calls it guards, joined with &&:
    python3 .agents/skills/novasmart-governance-lab/scripts/proof_gate.py --dir "$W" \
        --need policy-done,attach-done --after iam-change=180 --once --label proof-gate && <the proof calls>
    python3 .agents/skills/novasmart-governance-lab/scripts/proof_gate.py --dir "$W" \
        --need change-call-done --after change-call-done=180 --label records-wait-done && <the log reads>

Why: a proof sent before an access change has spread tests the old access. If the old access could
write, the "attempted change" lands on real data (a real run changed a price that way), and an answer
written from a guessed "done" makes it worse. This script reads only checkpoint lines that the commands
which observed each event wrote - `policy-done <UTC>`, `attach-done <UTC>`, `iam-change <UTC>`,
`change-call-done <UTC>` - appended to $W/checkpoints.txt with `| tee -a "$W/checkpoints.txt"`.

  --need a,b       every key must have a line in the file; otherwise exit 3 and nothing after && runs
  --after KEY=S    wait until S seconds after KEY's latest time (prints the wait; sleeps only the rest)
  --once           refuse a second run with the same --label (a proof is sent once); --again "<reason>"
                   allows it and records the reason
  --label NAME     the line appended when the gate opens: `NAME <UTC>` (default gate-open)

Prints each checkpoint it relied on with its time, the wait, and the opening line: copy these into the
entry's OUTPUTS. Exit 0 open, 3 closed (never "done" - say which checkpoint is missing), 2 bad usage.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone

FMT = "%Y-%m-%dT%H:%M:%SZ"


def now():
    return datetime.now(timezone.utc)


def stamp(t):
    return t.strftime(FMT)


def latest(path):
    """{key: (time, raw line)} for the latest time of each key in the checkpoint file."""
    out = {}
    if not os.path.isfile(path):
        return out
    for ln in open(path, encoding="utf-8", errors="replace"):
        parts = ln.split()
        if len(parts) < 2:
            continue
        try:
            t = datetime.strptime(parts[1], FMT).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if parts[0] not in out or t >= out[parts[0]][0]:
            out[parts[0]] = (t, ln.rstrip("\n"))
    return out


def closed(msg):
    print(f"GATE CLOSED: {msg}")
    print("Nothing after this gate was run. Report this as the result; never as done.")
    sys.exit(3)


def main():
    ap = argparse.ArgumentParser(
        description="Hold a proof until its checkpoints exist and the wait has passed."
    )
    ap.add_argument("--dir", required=True, help="the step's work folder ($W)")
    ap.add_argument(
        "--need", default="", help="comma-separated checkpoint keys that must exist"
    )
    ap.add_argument(
        "--after", default="", help="KEY=SECONDS: wait until that long after KEY's time"
    )
    ap.add_argument(
        "--once", action="store_true", help="refuse a second run with the same label"
    )
    ap.add_argument(
        "--again", default="", help="the reason for a second run (with --once)"
    )
    ap.add_argument("--label", default="gate-open")
    a = ap.parse_args()

    path = os.path.join(a.dir, "checkpoints.txt")
    marks = latest(path)
    need = [k for k in a.need.split(",") if k]
    after_key, after_s = None, 0
    if a.after:
        try:
            after_key, s = a.after.split("=", 1)
            after_s = int(s)
        except ValueError:
            print("usage error: --after takes KEY=SECONDS")
            return 2
        if after_key not in need:
            need.append(after_key)

    for k in need:
        if k not in marks:
            closed(
                f"no '{k}' line in {path}: the command that observes it has not printed it"
            )
        print(f"checkpoint: {marks[k][1]}")

    if a.once and a.label in marks:
        if not a.again:
            closed(
                f"'{a.label}' already ran at {stamp(marks[a.label][0])}; a second run needs --again \"<reason>\""
            )
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{a.label}-again {stamp(now())} {a.again}\n")
        print(f"second run, reason: {a.again}")

    if after_key:
        due = marks[after_key][0].timestamp() + after_s
        rest = int(due - time.time() + 0.999)
        if rest > 0:
            print(
                f"waiting {rest} s: {after_s} s after {after_key} at {stamp(marks[after_key][0])}",
                flush=True,
            )
            time.sleep(rest)
        else:
            print(
                f"no wait needed: {after_key} was at {stamp(marks[after_key][0])}, more than {after_s} s ago"
            )

    opened = stamp(now())
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{a.label} {opened}\n")
    print(f"{a.label} {opened}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
