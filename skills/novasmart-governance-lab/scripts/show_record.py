#!/usr/bin/env python3
"""
show_record.py - write the Show step's evidence entry, from what the scripts recorded.

Usage (after the last show_check.py run for the page):
    python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/show_record.py \
        N /config/Desktop/novasmart-showcase/m0_dashboard.html "<the leader's words, verbatim>" \
        [--grep "grep -n 'pattern' /config/Desktop/novasmart-evidence/mN/mN_stepK.txt"]...

show_facts.py and show_check.py append every run, verbatim, to .build/mN_runs.log. This script turns
this turn's runs into one entry in the SKILL.md §3g shape and appends it to the Show step's file
(mN_step7.txt; m4_step5.txt for Module 4):
  - COMMANDS: this turn's show_facts.py run(s), every show_check.py run (failed ones included), each
    --grep you pass (run here, read-only), and `ls -l` of what was saved (the page, and its .png).
  - OUTPUTS: what each one printed, exactly, with its exit code, indented four spaces.
  - CHANGE RECORD: (nothing changed in the estate).
"This turn" is the newest stretch of runs, since the previous recorded entry, that are all about this
page (its checks, and show_facts.py runs for its recipe or for none). It reads the entry count before and after the append and prints both; they must
differ by one. Never writes anywhere else, never overwrites: the file is only appended to.
"""

import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone

HOME_DIR = os.environ.get("NOVASMART_SHOW_HOME", "/config")
EVIDENCE_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-evidence")
SHOW_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-showcase")
BUILD_DIR = os.path.join(SHOW_DIR, ".build")
SHOW_STEP = {0: 7, 1: 7, 2: 7, 3: 7, 4: 5}
SHOW_TITLE = {
    0: "Show what you found",
    1: "Show what you changed",
    2: "Show what you controlled",
    3: "Show what you screened",
    4: "Show what you measured",
}
RULE = "=" * 80


def section(title):
    return f"-- {title} " + "-" * (80 - len(title) - 4)


def parse_log(path):
    """[('run', ts, kind, target, cmd, exit, lines) | ('recorded', text)] in file order."""
    items, cur = [], None
    for ln in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if ln.startswith("#### RUN ") and cur is None:
            parts = ln.split()
            cur = {
                "ts": parts[2],
                "kind": parts[3],
                "target": parts[4] if len(parts) > 4 else "-",
                "cmd": "",
                "exit": None,
                "lines": [],
            }
        elif ln.startswith("#### RECORDED") and cur is None:
            items.append(("recorded", ln))
        elif cur is not None and ln == "#### END":
            items.append(("run", cur))
            cur = None
        elif cur is not None and ln.startswith("$ ") and not cur["cmd"]:
            cur["cmd"] = ln[2:]
        elif (
            cur is not None and cur["exit"] is None and re.fullmatch(r"exit -?\d+", ln)
        ):
            cur["exit"] = int(ln.split()[1])
        elif cur is not None:
            cur["lines"].append(ln)
    return items


def count_entries(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return sum(1 for ln in f if ln.startswith("ENTRY "))


def run_readonly(cmd):
    """Run a grep the caller asked for; return (exit, output lines)."""
    argv = shlex.split(cmd)
    if not argv or argv[0] != "grep":
        sys.exit(f"--grep takes a grep command only, got: {cmd}")
    r = subprocess.run(argv, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).splitlines()


def main():
    args, greps, i = [], [], 1
    while i < len(sys.argv):
        if sys.argv[i] == "--grep" and i + 1 < len(sys.argv):
            greps.append(sys.argv[i + 1])
            i += 2
        else:
            args.append(sys.argv[i])
            i += 1
    if len(args) != 3 or args[0] not in [str(k) for k in SHOW_STEP]:
        sys.exit(__doc__)
    mod, page, asked = int(args[0]), args[1], args[2].strip()
    if not os.path.isabs(page):
        page = os.path.join(SHOW_DIR, os.path.basename(page))
    pname = os.path.basename(page)
    if not os.path.isfile(page):
        sys.exit(
            f"no page at {page} - write it, run show_check.py on it, then run this"
        )
    if not pname.startswith(f"m{mod}_"):
        sys.exit(f"{pname} is not a Module {mod} page (its name starts m{mod}_)")
    log = os.path.join(BUILD_DIR, f"m{mod}_runs.log")
    if not os.path.isfile(log):
        sys.exit(
            f"no run log at {log} - run show_facts.py {mod} <demo> and show_check.py first"
        )

    items = parse_log(log)
    last_mark = max(
        (k for k, it in enumerate(items) if it[0] == "recorded"), default=-1
    )
    runs = [
        (k, it[1]) for k, it in enumerate(items) if it[0] == "run" and k > last_mark
    ]
    if not any(r["kind"] == "show_check" and r["target"] == pname for _, r in runs):
        sys.exit(
            f"no show_check.py run of {pname} since the last recorded entry - run the check first"
        )
    # This turn: walk back from the newest run while each run is about this page (its check, or a
    # show_facts run for its recipe or for no recipe); a run about another page ends the walk.
    end = (
        max(
            j
            for j, (_, r) in enumerate(runs)
            if r["kind"] == "show_check" and r["target"] == pname
        )
        + 1
    )
    start = end
    while start > 0 and runs[start - 1][1]["target"] in (pname, "-"):
        start -= 1
    turn = [r for _, r in runs[start:end]]
    left_out = start

    # Commands this script runs now, recorded the same way.
    extra = []
    for g in greps:
        code, out = run_readonly(g)
        extra.append(("look up a detail in a step file", g, code, out))
    saved = [page]
    png = os.path.splitext(page)[0] + ".png"
    if os.path.isfile(png):
        saved.append(png)
    ls = ["ls", "-l"] + saved
    r = subprocess.run(ls, capture_output=True, text=True)
    extra.append(
        (
            "what was saved",
            " ".join(shlex.quote(a) for a in ls),
            r.returncode,
            (r.stdout + r.stderr).splitlines(),
        )
    )

    ncheck = sum(1 for r in turn if r["kind"] == "show_check")
    entries, k_check = [], 0
    for r in turn:
        if r["kind"] == "show_facts":
            what = "the fact sheet and this page's recipe (show_facts.py)"
        elif r["kind"] == "show_check":
            k_check += 1
            what = f"check and render {r['target']} (show_check.py), run {k_check} of {ncheck}"
        else:
            what = r["kind"]
        entries.append(
            (what, r["cmd"], r["exit"] if r["exit"] is not None else "?", r["lines"])
        )
    entries += extra

    written = datetime.fromtimestamp(os.path.getmtime(page), timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    step = SHOW_STEP[mod]
    edir = os.path.join(EVIDENCE_DIR, f"m{mod}")
    efile = os.path.join(edir, f"m{mod}_step{step}.txt")
    os.makedirs(edir, exist_ok=True)
    open(efile, "a", encoding="utf-8").close()
    before = count_entries(efile)
    n = before + 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out = [
        RULE,
        f"ENTRY {n} - M{mod} Step {step} - {SHOW_TITLE[mod]}",
        f"Written {now}",
        f'You asked: "{asked}"',
        RULE,
        "",
        section("COMMANDS (copy any line below - there is no output in this section)"),
        "",
    ]
    out.append(
        f"# {pname} was written with write_to_file (a tool, not a command); file time {written}"
    )
    out.append("")
    for j, (what, cmd, _, _) in enumerate(entries, 1):
        out += [f"# {j}  {what}", cmd, ""]
    out += [section("OUTPUTS"), ""]
    for j, (_, _, code, lines) in enumerate(entries, 1):
        out.append(f"[{j}] exit {code}")
        out += [("    " + ln).rstrip() for ln in lines]
        out.append("")
    out += [section("CHANGE RECORD"), "", "(nothing changed in the estate)", ""]
    with open(efile, "a", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    after = count_entries(efile)
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"#### RECORDED {os.path.basename(efile)} ENTRY {n} {now}\n")

    failed = sum(1 for e in entries if e[2] != 0)
    print(f"entries in {efile}: {before} before, {after} after")
    if after != before + 1:
        print(
            f"WARNING: the count should read {before + 1}. The file was overwritten or changed while "
            "writing: say so on screen in this answer, and do not write a fresh ENTRY 1 over it."
        )
    print(
        f"wrote ENTRY {n}: {len(entries)} commands, {failed} of them failed "
        f"({ncheck} show_check run(s) of {pname})"
    )
    if left_out:
        print(
            f"note: {left_out} earlier run(s) in the log were not part of this turn and were left out"
        )
    if turn and turn[-1]["kind"] == "show_check" and turn[-1]["exit"] != 0:
        print("note: the last check did not end RESULT: clean - say so in the answer")
    fail_words = "none of them failed" if not failed else f"{failed} of them failed"
    print(
        f"Where the proof is: Every command I ran and everything it printed is saved at `{efile}` - "
        f"{len(entries)} commands, {fail_words}."
    )


if __name__ == "__main__":
    main()
