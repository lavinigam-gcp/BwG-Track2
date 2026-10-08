#!/usr/bin/env python3
"""
write_entry.py - append one evidence entry to a step's file, from a draft agy wrote with write_to_file.

Usage (from the workspace folder):
    python3 .agents/skills/novasmart-governance-lab/scripts/write_entry.py \
        --to /config/Desktop/novasmart-evidence/m2/m2_step5.txt \
        --draft /config/Desktop/novasmart-evidence/m2/work/entry_draft.txt

Why a draft file and this script: an entry carries commands with quotes, heredocs and backticks. Wrapped
in a shell heredoc, `python3 -c` or a generated script, those can end the wrapper early and run the rest
of the entry as commands (a real run started estate changes that way). write_to_file involves no shell,
and this script only reads the draft and appends it.

The draft is one entry in the SKILL.md §3g shape, with `ENTRY ?` and `Written ?` in its header:
    ================================================================================
    ENTRY ? - M2 Step 5 - Lock down what the back office can reach and do
    Written ?
    You asked: "<the leader's words, verbatim>"
    ================================================================================
    -- COMMANDS ... / -- OUTPUTS ... / -- CHANGE RECORD ...
An output a command saved to a file can be pulled in, byte for byte, with a line of its own:
    @@OUTPUT /config/Desktop/novasmart-evidence/m2/work/proof_ids.txt@@
    @@OUTPUT /config/Desktop/novasmart-evidence/m2/work/attach_op_now.json lines=1-40@@
Each becomes the file's lines indented four spaces; a range adds `[... N lines cut ...]` markers.

The script numbers the entry (entries already in the file plus one), stamps `Written` with the UTC time
now, checks the shape, appends (never overwrites), prints the entry count before and after, and removes
the draft. It refuses, and changes nothing, when: the target is not a step file under
/config/Desktop/novasmart-evidence/mN/; the draft lacks the header or one of the three sections, or holds
more than one entry; an @@OUTPUT file is missing; or the draft contains text only the system writes
(`<SYSTEM_MESSAGE>`, "Notification from task", "finished with result") - a result is evidence only when
a tool returned it.
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

HOME_DIR = os.environ.get(
    "NOVASMART_HOME", "/config"
)  # set only to exercise this outside the lab
EVIDENCE_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-evidence")
RULE = "=" * 80
SECTIONS = ["-- COMMANDS", "-- OUTPUTS", "-- CHANGE RECORD"]
SYSTEM_ONLY = [
    "<SYSTEM_MESSAGE>",
    "</SYSTEM_MESSAGE>",
    "Notification from task",
    "finished with result",
]
INCLUDE = re.compile(r"^\s*@@OUTPUT\s+(\S+)(?:\s+lines=(\d+)-(\d+))?\s*@@\s*$")


def refuse(msg):
    print(f"refused: {msg}")
    print("Nothing was written. Fix the draft and run this again.")
    sys.exit(2)


def count_entries(path):
    if not os.path.isfile(path):
        return 0
    return sum(
        1
        for ln in open(path, encoding="utf-8", errors="replace")
        if ln.startswith("ENTRY ")
    )


def expand(lines):
    out = []
    for ln in lines:
        m = INCLUDE.match(ln)
        if not m:
            out.append(ln)
            continue
        src = m.group(1)
        if not os.path.isfile(src):
            refuse(f"@@OUTPUT file not found: {src}")
        body = open(src, encoding="utf-8", errors="replace").read().split("\n")
        if body and body[-1] == "":
            body.pop()
        if m.group(2):
            a, b = int(m.group(2)), int(m.group(3))
            if a < 1 or b < a:
                refuse(f"bad line range in: {ln.strip()}")
            if a > 1:
                out.append(f"    [... {a - 1} lines cut ...]")
            out += ["    " + x for x in body[a - 1 : b]]
            if b < len(body):
                out.append(f"    [... {len(body) - b} lines cut ...]")
        else:
            out += ["    " + x for x in body]
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Append one evidence entry from a draft file."
    )
    ap.add_argument(
        "--to", required=True, help="the step's evidence file, absolute path"
    )
    ap.add_argument(
        "--draft", required=True, help="the draft written with write_to_file"
    )
    a = ap.parse_args()

    to = os.path.abspath(a.to)
    m = re.fullmatch(
        re.escape(EVIDENCE_DIR) + r"/(m[0-4])/(m[0-4])_(step\d+|other)\.txt", to
    )
    if not m or m.group(1) != m.group(2):
        refuse(
            f"{to} is not a step file (expected {EVIDENCE_DIR}/mN/mN_stepK.txt or mN_other.txt)"
        )
    if not os.path.isfile(a.draft):
        refuse(f"draft not found: {a.draft}")
    text = open(a.draft, encoding="utf-8", errors="replace").read()

    for s in SYSTEM_ONLY:
        if s in text:
            refuse(
                f"the draft contains {s!r}, which only the system writes. Use only what tool results returned."
            )
    lines = text.rstrip("\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if len([ln for ln in lines if ln.startswith("ENTRY ")]) != 1:
        refuse("the draft must hold exactly one entry (one 'ENTRY' header line)")
    if len(lines) < 5 or lines[0] != RULE or lines[4] != RULE:
        refuse(
            "the header must be: a line of 80 '=', ENTRY, Written, You asked, a line of 80 '='"
        )
    if not re.match(r"ENTRY \S+ - .+ - .+", lines[1]):
        refuse("line 2 must read 'ENTRY ? - <slot> - <title>'")
    if not lines[2].startswith("Written"):
        refuse("line 3 must read 'Written ?'")
    if not re.match(r'You asked: ".+"$', lines[3]):
        refuse("line 4 must read 'You asked: \"<the leader's words, verbatim>\"'")
    pos = [
        next((i for i, ln in enumerate(lines) if ln.startswith(s)), -1)
        for s in SECTIONS
    ]
    if -1 in pos or pos != sorted(pos):
        refuse(
            "the draft needs '-- COMMANDS', '-- OUTPUTS' and '-- CHANGE RECORD' sections, in that order"
        )

    before = count_entries(to)
    n = before + 1
    given = lines[1].split(" ", 2)[1]
    lines[1] = re.sub(r"^ENTRY \S+", f"ENTRY {n}", lines[1])
    lines[2] = "Written " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = "\n".join(expand(lines)) + "\n"

    os.makedirs(os.path.dirname(to), exist_ok=True)
    lead = ""
    if os.path.isfile(to) and os.path.getsize(to) > 0:
        with open(to, "rb") as f:
            f.seek(-1, os.SEEK_END)
            lead = "\n" if f.read(1) != b"\n" else ""
        lead += "\n"
    with open(to, "a", encoding="utf-8") as f:
        f.write(lead + body)
    after = count_entries(to)
    os.remove(a.draft)

    note = (
        ""
        if given in ("?", str(n))
        else f" (the draft said ENTRY {given}; the file's count makes it {n})"
    )
    print(f"wrote ENTRY {n} to {to}{note}")
    print(f"entries before: {before}, after: {after}")
    if after != before + 1:
        print(
            "warning: the count did not go up by exactly one - the file changed while writing; say so on screen"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
