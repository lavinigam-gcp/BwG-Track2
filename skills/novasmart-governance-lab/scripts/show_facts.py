#!/usr/bin/env python3
"""
show_facts.py - the fact sheet a module's Show step builds from.

The Show step (M0-M3 Step 7, M4 Step 5) turns the module's recorded work into a page. Its only source
is the module's evidence files, but those are large (one step's entry can run past 60 KB) and a command's
printed output is cut to its last few KB, so `cat` cannot re-read them. This script reads the LATEST
entry of each recorded step file and writes one compact fact sheet:

    /config/Desktop/novasmart-showcase/.build/mN_facts.txt

Every line in it is copied from an evidence file, with that file's line number; JSON outputs are
flattened to the fields a page can use (names, identities, times, columns, roles, statuses). Nothing is
summarised and nothing is added. Customer record values are withheld: a record is shown by its column
names only.

It also writes .build/mN_private.txt: values a page must never contain (the project id and number,
every email address, customer record values). show_check.py reads it.

Usage:   python3 show_facts.py 0     (Module 0: Steps 1-4)
         python3 show_facts.py 1     (Module 1: Steps 1-5)
         python3 show_facts.py 2     (Module 2: Steps 1-5)
         python3 show_facts.py 3     (Module 3: Steps 1-5; Step 6 What's next has no file)
         python3 show_facts.py 4     (Module 4: Steps 1-4)
Reads only files under /config/Desktop/novasmart-evidence/. Runs no cloud command, changes nothing.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

# NOVASMART_SHOW_HOME exists only so this script can be tested outside the container. Not set in the lab.
HOME_DIR = os.environ.get("NOVASMART_SHOW_HOME", "/config")
EVIDENCE_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-evidence")
BUILD_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-showcase", ".build")

STEPS = {0: [1, 2, 3, 4], 1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4]}
STEP_TITLES = {
    0: {
        1: "Check your environment",
        2: "Meet your estate",
        3: "Widen the net",
        4: "Who's reading customer data",
    },
    1: {
        1: "Register the shadow agent",
        2: "See what that shared login can do",
        3: "Give each agent its own login",
        4: "Cut off what shouldn't have access",
        5: "Prove it worked",
    },
    2: {
        1: "See who can call the back office",
        2: "See what locking it down would cost",
        3: "Lock it to the front desk",
        4: "Prove the rogue caller is out",
        5: "Lock down what the back office can reach and do",
    },
    3: {
        1: "See if the agents can be talked into breaking their rules",
        2: "See what is screening messages today",
        3: "Turn the screening on",
        4: "Prove the attacks are blocked",
        5: "Sum up what you can actually claim",
    },
    4: {
        1: "Run the evaluation and read the scorecard",
        2: "Build a tougher set and run it",
        3: "See the fix before you make it",
        4: "Make the change and see what is actually running",
    },
}

# What each module's What's next step says is still open: the only wording a page or answer may use
# for "next" (printed with every run, so it is in front of agy at every Show prompt).
STILL_OPEN = {
    0: "register the shadow agent, give each agent its own identity, and scope its access down to "
    "what its job actually needs (Module 1)",
    1: "who may call whom, starting with who is allowed to call that back-office margin agent (Module 2)",
    2: "Cloud permissions stack, and a handful of broad project-wide roles still carry the ability to call "
    "any agent in the project. Closing the back office's own list did not touch those. M3 · Protect the "
    "Content is where you screen what customers can talk your agents into.",
    # M3: quoted from m3-instructions.md Step 6 · What's next (its remaining-work sentences and the M4 line).
    3: "The customer-record attack still works, because that agent is not behind the door and this screen "
    "cannot reach it. The screen is set to fail open, so a screen that cannot run lets everything through "
    "without a sound. And the discount code sitting in plain text in the storefront is untouched. M4 · "
    "Evaluate and Decide (Optional Module) is where you stop spot-checking and start measuring: run the "
    "agent against a full scenario set — the deals it should settle, the ones it should escalate, the ones "
    "it should refuse, and the traps it should catch — and read the score before you roll it out to every "
    "store.",
    # M4: quoted from m4-instructions.md "See it in the console" (M4 is the last module, so this is what it
    # leaves open).
    4: "Its entry is the one the earlier modules left. Nothing here changed it: not the scorecards, not the "
    "tougher set, and not the wording change, which exists only in the folder on this workstation. Getting "
    "that change in front of a customer means a deployment, and that is a separate decision with a separate "
    "owner.",
}

# JSON leaf keys worth a page: names, identities, times, columns, access, statuses.
KEEP = {
    "displayName",
    "agentId",
    "location",
    "name",
    "uri",
    "description",
    "createTime",
    "updateTime",
    "serviceAccount",
    "serviceAccountName",
    "effectiveIdentity",
    "identityType",
    "principalEmail",
    "principalSubject",
    "permission",
    "granted",
    "methodName",
    "callerSuppliedUserAgent",
    "timestamp",
    "fields",
    "reason",
    "code",
    "message",
    "role",
    "members",
    "userByEmail",
    "groupByEmail",
    "specialGroup",
    "iamMember",
    "domain",
    "percent",
    "revisionName",
    "latestReadyRevisionName",
    "status",
    "state",
    "records_analyzed",
    "record_count",
    "result",
    "model",
    "agentFramework",
    "version",
    "title",
    "verdict",
    "check",
    "proof",
}
# Subtrees that only repeat or bury those fields (method lists, environment, protocol plumbing).
SKIP = {
    "classMethods",
    "env",
    "secretEnv",
    "packageSpec",
    "protocols",
    "interfaces",
    "skills",
    "content",
    "containers",
    "conditions",
    "annotations",
    "labels",
}
CUSTOMER_HINTS = {
    "customer_id",
    "email",
    "loyalty_tier",
    "lifetime_value",
    "last_purchase_date",
}
# Extra leaf keys per module: M3's gateway attach, extension and filter settings and the blocked
# reply; M4's per-case evaluation fields (a judge's numeric score is left out: no page shows one).
KEEP_EXTRA = {
    3: {
        "agentGateway",
        "failOpen",
        "service",
        "action",
        "resources",
        "filterEnforcement",
        "confidenceLevel",
        "filterType",
        "customPromptSafetyErrorCode",
        "customPromptSafetyErrorMessage",
        "customResponseSafetyErrorCode",
        "customResponseSafetyErrorMessage",
        "logSanitizeOperations",
        "matchState",
        "filterMatchState",
        "invocationResult",
    },
    4: {
        "prompt",
        "request",
        "reference",
        "response",
        "final_response",
        "expected_response",
        "explanation",
        "error",
        "case_id",
        "eval_case_id",
        "eval_id",
        "metric",
        "metric_name",
        "judge_model",
    },
}
TEXT_HEAD, TEXT_TAIL, TEXT_MAX = 25, 10, 40
ANSI = re.compile(r"\x1b\[[0-9;]*m|\[[0-9;]*m(?=\S)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
PROJECT_ID = re.compile(r"qwiklabs-gcp-[0-9a-z-]+[0-9a-z]")
PROJECT_NUM = re.compile(r"projects/(\d{10,14})\b")
CUST_ID = re.compile(r"\bCUST-\d+\b")
SECRET_CODE = re.compile(r"\bNVST-[A-Z]+-\d+\b")  # the exposed discount code (M3, M4): never on a page

private = set()


def latest_entry(path):
    """(entry_number, first_line_no, lines) of the last ENTRY in an evidence file."""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("ENTRY ")]
    if not starts:
        return None, 0, []
    s = starts[-1]
    m = re.match(r"ENTRY (\d+)", lines[s])
    return (m.group(1) if m else "?"), s + 1, lines[s:]


def all_entries(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("ENTRY ")] + [len(lines)]
    for a, b in zip(starts, starts[1:]):
        m = re.match(r"ENTRY (\d+)", lines[a])
        yield (m.group(1) if m else "?"), a + 1, lines[a:b]


def scan_private(text):
    for m in EMAIL.finditer(text):
        private.add(m.group(0))
    for m in PROJECT_ID.finditer(text):
        private.add(m.group(0))
    for m in PROJECT_NUM.finditer(text):
        private.add(m.group(1))
    for m in CUST_ID.finditer(text):
        private.add(m.group(0))
    for m in SECRET_CODE.finditer(text):
        private.add(m.group(0))


def is_customer_record(d):
    return isinstance(d, dict) and len(CUSTOMER_HINTS & set(d)) >= 2


def has_customer_record(node):
    if is_customer_record(node):
        return True
    if isinstance(node, dict):
        return any(has_customer_record(v) for v in node.values())
    if isinstance(node, list):
        return any(has_customer_record(v) for v in node)
    return False


def collect_customer_values(node):
    if isinstance(node, dict):
        if is_customer_record(node):
            for k, v in node.items():
                if isinstance(v, str) and (
                    k in ("name", "email", "customer_id")
                    or k.endswith(("_name", "_email"))
                ):
                    s = v.strip()
                    if len(s) >= 4 and not s.isdigit():
                        private.add(s)
        for v in node.values():
            collect_customer_values(v)
    elif isinstance(node, list):
        for v in node:
            collect_customer_values(v)


def short(v, n=160):
    s = v if isinstance(v, str) else json.dumps(v)
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def flatten(node, path=()):
    """Yield (display_key, value) for kept leaves; customer records collapse to their column names."""
    if is_customer_record(node):
        yield (
            ".".join(path[-1:]) or "record",
            "<customer record - values withheld; columns: "
            + ", ".join(sorted(node))
            + ">",
        )
        return
    if isinstance(node, dict):
        for k, v in node.items():
            p = path + (k,)
            if k in SKIP:
                continue
            keep = k in KEEP or "Runtime" in k or "lastModifier" in k or "creator" in k
            if keep and not isinstance(v, (dict, list)):
                yield ".".join(p[-2:]), short(v)
            elif (
                keep
                and isinstance(v, list)
                and all(not isinstance(x, (dict, list)) for x in v)
            ):
                vals = [short(x, 80) for x in v]
                more = f" (+{len(vals) - 25} more)" if len(vals) > 25 else ""
                yield ".".join(p[-2:]), "[" + ", ".join(vals[:25]) + "]" + more
            else:
                yield from flatten(v, p)
    elif isinstance(node, list):
        for v in node:
            yield from flatten(v, path)


def items_of(obj):
    """A JSON output as a list of items: a list, a dict wrapping one list, or one dict."""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        lists = [
            v
            for v in obj.values()
            if isinstance(v, list) and v and isinstance(v[0], dict)
        ]
        if len(obj) <= 3 and len(lists) == 1:
            return lists[0]
        return [obj]
    return [obj]


def render_json(obj, first, last, out):
    collect_customer_values(obj)
    items = items_of(obj)
    out.append(
        f"    (JSON, lines L{first}-L{last}, {len(items)} item{'s' if len(items) != 1 else ''}; kept fields only)"
    )
    for n, it in enumerate(items, 1):
        pairs = list(flatten(it))
        if not pairs:
            continue
        out.append(f"    [item {n}]")
        seen = set()
        for k, v in pairs:
            if (k, v) in seen:
                continue
            seen.add((k, v))
            out.append(f"      {k}: {v}")


def try_json(block, i):
    """If a JSON value starts at block[i], return (obj, end_index)."""
    head = block[i][1].strip()
    if not head or head[0] not in "[{":
        return None, i
    if head[-1] in "]}":
        try:
            one = json.loads(head)
        except ValueError:
            one = None
        if has_customer_record(one):
            return one, i  # a one-line JSON value holding customer records: withhold their values
    indent = len(block[i][1]) - len(block[i][1].lstrip())
    for j in range(i, len(block)):
        t = block[j][1]
        st = t.strip()
        if j == i and st in ("[]", "{}"):
            return json.loads(st), j
        if st and st[0] in "]}" and len(t) - len(t.lstrip()) == indent:
            try:
                return json.loads("\n".join(x[1] for x in block[i : j + 1])), j
            except ValueError:
                continue
    try:
        return json.loads("\n".join(x[1] for x in block[i:])), len(block) - 1
    except ValueError:
        return None, i


def render_output(block, out):
    """block: list of (line_no, text) for one [k] output, without its header line."""
    text_run = []

    def flush():
        if not text_run:
            return
        rows = (
            text_run
            if len(text_run) <= TEXT_MAX
            else (
                text_run[:TEXT_HEAD]
                + [
                    (
                        None,
                        f"[... {len(text_run) - TEXT_HEAD - TEXT_TAIL} lines cut ...]",
                    )
                ]
                + text_run[-TEXT_TAIL:]
            )
        )
        for ln, t in rows:
            t = ANSI.sub("", t).rstrip()
            t = t if len(t) <= 300 else t[:299] + "…"
            out.append(f"  L{ln}  {t}" if ln else f"        {t}")
        text_run.clear()

    i = 0
    while i < len(block):
        sse = re.match(r"\s*data:\s*(\{.*\})\s*$", block[i][1])
        if sse:
            try:
                obj = json.loads(sse.group(1))
            except ValueError:
                obj = None
            if obj is not None:
                flush()
                render_json(obj, block[i][0], block[i][0], out)
                i += 1
                continue
        obj, j = try_json(block, i)
        if obj is not None and j >= i:
            flush()
            render_json(obj, block[i][0], block[j][0], out)
            i = j + 1
            continue
        if block[i][1].strip():
            text_run.append(block[i])
        i += 1
    flush()


def render_entry(lines, first_no, out, brief=False):
    """One evidence entry: header, command intents, outputs (compacted), change record (verbatim).
    brief=True (side questions) leaves the outputs out and points at the file instead."""
    section = "head"
    block, block_head = [], None

    def close_block():
        if block_head is not None:
            out.append(f"  L{block_head[0]}  {block_head[1].strip()}")
            render_output(block, out)

    for off, raw in enumerate(lines):
        no = first_no + off
        scan_private(raw)
        if raw.startswith("-- COMMANDS"):
            section = "commands"
            out.append(
                "Commands (intent lines; the commands themselves are in the file):"
            )
            continue
        if raw.startswith("-- OUTPUTS"):
            section = "outputs"
            out.append(f"Outputs: in the file from L{no}" if brief else "Outputs:")
            continue
        if raw.startswith("-- CHANGE RECORD"):
            close_block()
            block, block_head = [], None
            section = "change"
            out.append("Change record (verbatim):")
            continue
        if section == "head":
            if raw.startswith(("ENTRY ", "Written", "You asked", "Corrects")):
                out.append(raw.strip())
        elif section == "commands":
            if re.match(r"#\s*\d+\s", raw):
                out.append(f"  L{no}  {raw.strip()}")
        elif section == "outputs" and brief:
            continue
        elif section == "outputs":
            m = re.match(r"\[(\d+)\]\s", raw)
            if m:
                close_block()
                block, block_head = [], (no, raw)
            elif block_head is not None:
                body = raw[4:] if raw.startswith("    ") else raw
                block.append((no, body))
            elif raw.strip():
                out.append(f"  L{no}  {raw.strip()}")
        elif section == "change":
            if raw.strip() and not raw.startswith("====="):
                out.append(f"  L{no}  {raw.rstrip()}")
    if section == "outputs" and not brief:
        close_block()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in [str(k) for k in STEPS]:
        sys.exit(__doc__)
    mod = int(sys.argv[1])
    KEEP.update(KEEP_EXTRA.get(mod, ()))
    edir = os.path.join(EVIDENCE_DIR, f"m{mod}")
    os.makedirs(BUILD_DIR, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = [
        f"NovaSmart - Module {mod} - fact sheet for the Show step",
        f"Built {now} from the latest entry of each recorded step file in {edir}.",
        "Every line is copied from that file; L<n> is its line number there. JSON outputs keep only",
        "the fields a page can use. Customer record values are withheld. Nothing is summarised.",
        "",
    ]
    index = []
    for step in STEPS[mod]:
        path = os.path.join(edir, f"m{mod}_step{step}.txt")
        title = STEP_TITLES[mod][step]
        if not os.path.isfile(path):
            out += [f"=== Step {step} - {title} - NO FILE: not run yet", ""]
            index.append(f"Step {step} - {title}: no file - show it as not run yet")
            continue
        n, first_no, lines = latest_entry(path)
        if not lines:
            out += [f"=== Step {step} - {title} - file has no entry: not run yet", ""]
            index.append(f"Step {step} - {title}: no entry - show it as not run yet")
            continue
        changes = sum(1 for ln in lines if re.match(r"\s*Change:", ln))
        out.append(
            f"=== Step {step} - {title} - {os.path.basename(path)} - ENTRY {n} (latest)"
        )
        render_entry(lines, first_no, out)
        out.append("")
        index.append(
            f"Step {step} - {title}: {os.path.basename(path)} ENTRY {n}, "
            f"{changes} change record line(s) starting 'Change:'"
        )
    other = os.path.join(edir, f"m{mod}_other.txt")
    if os.path.isfile(other):
        out.append(
            f"=== Side questions - {os.path.basename(other)} (every entry, outputs left out: "
            "show them as side questions and read the file for any detail you use)"
        )
        count = 0
        for n, first_no, lines in all_entries(other):
            count += 1
            render_entry(lines, first_no, out, brief=True)
            out.append("")
        index.append(
            f"Side questions: {os.path.basename(other)}, {count} entr{'y' if count == 1 else 'ies'}"
        )

    facts = os.path.join(BUILD_DIR, f"m{mod}_facts.txt")
    with open(facts, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    priv = os.path.join(BUILD_DIR, f"m{mod}_private.txt")
    with open(priv, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(private)) + "\n")

    print(f"Module {mod} fact sheet")
    for line in index:
        print("  " + line)
    size = os.path.getsize(facts)
    nlines = len(out)
    print(
        f"Fact sheet: {facts} ({size:,} bytes, {nlines} lines) - read it whole with view_file"
    )
    if size > 45000 or nlines > 780:
        half = nlines // 2
        print(
            f"  Too long for one read: view lines 1-{half}, then {half + 1}-{nlines}, and check "
            "that both parts came back."
        )
    print(
        f"Never on a page: {len(private)} values (project id and number, email addresses, customer "
        f"record values, the exposed discount code) in {priv}; show_check.py checks the page against them."
    )
    print(
        "\nThis turn, before you build (showcase.md):\n"
        f"  - Read showcase.md and showcase-m{mod}.md whole, even if you read them earlier.\n"
        "  - Data block first; write the page with write_to_file; run show_check.py until RESULT: clean;\n"
        "    then open every screenshot it lists and fix what looks wrong.\n"
        "  - Nothing beyond the files on the page or in the answer, and no recommendation of your own.\n"
        f"  - Still open, on the page and in the answer, in these words only: {STILL_OPEN[mod].rstrip('.')}."
    )


if __name__ == "__main__":
    main()
