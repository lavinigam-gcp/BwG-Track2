#!/usr/bin/env python3
"""starter_app.py - an honest evidence board for your own cloud project.

Serves one local page. Every panel runs one real command and shows that command
and the UTC time it ran, so nothing here is a claim you cannot trace. Something
it could not read says the words "not read"; a command that ran and broke says
"command failed" and shows the real error. No ticks, scores or verdicts. Never
customer rows - only counts, column names and identities. Read-only apart from
two agent-call triggers, which are calls this lab already makes. No credential
is ever embedded, put on a command line, or written to disk.

  python3 starter_app.py             # first free port in 8901-8940
  python3 starter_app.py --selftest  # run every panel, print a table, exit

Standard library only, and no webfont, stylesheet or script from off the box:
the page must still render with the network unplugged. Its stylesheet is the
layout contract in references/build-and-ground.md section 6, written out - light
paper, one column, a proportional face for prose, monospace kept for commands
and identifiers, and long resource paths that wrap instead of running the width
of the screen.

Look for the ADAPT ME markers - every learner's app should end up different
from this one.
"""

import argparse
import html
import json
import os
import shlex
import socket
import subprocess
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

# ADAPT ME (1 of 3) - what this app looks at.
REGION = os.environ.get("LAB_REGION", "us-central1")
REG_LOC = os.environ.get("LAB_REGISTRY_LOCATION", "global")
DATASET = os.environ.get("LAB_DATASET", "customer_data")
TEMPLATE = os.environ.get("LAB_ARMOR_TEMPLATE", "nvst-jailbreak-template")

HOST = "127.0.0.1"  # loopback only: Chrome runs inside this same container
PORTS = range(8901, 8941)  # 3000, 3001, 8080 and 8088 belong to other services
SECS = 60  # a command that hangs must become a not-read, not a hung page

READ, NOT_READ, FAILED, RAISED = "read", "not read", "command failed", "panel raised"
NO_BINARY = 127


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def run(command, stdin=None):
    """Run one command string. Never raises - a missing tool is a result."""
    argv = shlex.split(command)
    try:
        done = subprocess.run(
            argv, input=stdin, capture_output=True, text=True, timeout=SECS
        )
        return done.returncode, done.stdout.strip(), done.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "no answer within %d seconds" % SECS
    except OSError as exc:
        # The command never started, so there is no output to judge. That is a
        # not-read, not a failure. A box with no gcloud lands here on every
        # panel, and the page still shows the command it would have run.
        # (A missing tool can surface as "no such file" OR "permission denied",
        # depending on the container, so both are handled the same way.)
        return NO_BINARY, "", "%s could not be started here: %s" % (argv[0], exc)


def result(command, state, value=None, detail=""):
    """The one shape every panel returns. Command and clock are not optional."""
    return dict(command=command, at=utc_now(), state=state, value=value, detail=detail)


def read_json(command, stdin=None, shown=None):
    """Run a command expected to print JSON. Returns (parsed or None, result)."""
    rc, out, err = run(command, stdin)
    shown = shown or command
    if rc == NO_BINARY:  # no cloud tooling here at all: honest, not a failure
        return None, result(shown, NOT_READ, detail=err)
    if rc != 0:
        return None, result(shown, FAILED, detail=err or "exit status %d" % rc)
    if not out:
        return None, result(shown, NOT_READ, detail="the command printed nothing")
    try:
        return json.loads(out), result(shown, READ)
    except ValueError:
        return None, result(shown, NOT_READ, detail="the output was not JSON")


def curl_json(url, payload=None):
    """Call an API with curl. The token goes in on STDIN via --config -, so it
    never reaches the process list, this page, or a file."""
    rc, token, err = run("gcloud auth print-access-token")
    post = ""
    if payload is not None:
        post = " -X POST -H 'Content-Type: application/json' -d " + shlex.quote(
            json.dumps(payload)
        )
    command = "curl -sS --config -%s %s" % (post, url)
    if rc != 0 or not token:
        return None, result(command, NOT_READ, detail=err or "no ambient credentials")
    data, res = read_json(
        command, stdin='header = "Authorization: Bearer %s"\n' % token
    )
    if isinstance(data, dict) and "error" in data:
        return None, result(command, FAILED, detail=str(data["error"].get("message")))
    return data, res


# Resolved once at start. A blank project shows on the page, never as a crash.
PROJECT = (run("gcloud config get-value project")[1] or "").replace("(unset)", "")
API = "https://%s-aiplatform.googleapis.com/v1beta1" % REGION
PROJ = PROJECT or "PROJECT"  # so a panel can still show the command it would run
PARENT = "%s/projects/%s/locations/%s" % (API, PROJ, REGION)
LOG = "projects/%s/logs/cloudaudit.googleapis.com%%2Fdata_access" % PROJ
AUDIT = 'logName="%s" AND resource.type="bigquery_dataset"' % LOG
AUDIT += ' AND resource.labels.dataset_id="%s"' % DATASET
AUDIT += " AND protoPayload.metadata.tableDataRead:*"

PANELS = []


def panel(title, question):
    """Register a panel. ADAPT ME (2 of 3) - add one, it shows up on the page."""

    def register(fn):
        fn.title, fn.question = title, question
        PANELS.append(fn)
        return fn

    return register


def agent_name(item):
    """An agent record carries a display name, or only a resource path."""
    return item.get("displayName") or item.get("name", "?").split("/")[-1]


@panel("Registered agents", "Which agents has somebody registered on purpose?")
def registered_agents():
    cmd = "gcloud agent-registry agents list --location=%s --format=json" % REG_LOC
    data, res = read_json(cmd)
    if data is None:
        return res
    names = [agent_name(a) for a in data]
    res["value"] = "%d registered: %s" % (len(names), ", ".join(names) or "none")
    return res


@panel("Running workloads", "What is running outside the managed runtime?")
def cloud_run_workloads():
    data, res = read_json("gcloud run services list --format=json")
    if data is None:
        return res
    names = [s.get("metadata", {}).get("name", "?") for s in data]
    res["value"] = "%d Cloud Run services: %s" % (len(names), ", ".join(names) or "-")
    return res


@panel("Deployed agents", "What runs ON the managed runtime? Not the same list.")
def managed_agents():
    data, res = curl_json("%s/reasoningEngines" % PARENT)
    if data is None:
        return res
    names = [agent_name(e) for e in data.get("reasoningEngines", [])]
    res["value"] = "%d deployed: %s" % (len(names), ", ".join(names) or "none")
    return res


@panel("Workload identities", "Which login does each running workload sign in as?")
def workload_identities():
    # Two workloads sharing one login is what makes a later read unattributable.
    fields = "metadata.name,spec.template.spec.serviceAccountName"
    cmd = "gcloud run services list --format=value(%s)" % fields
    rc, out, err = run(cmd)
    if rc == NO_BINARY:
        return result(cmd, NOT_READ, detail=err)
    if rc != 0:
        return result(cmd, FAILED, detail=err or "exit status %d" % rc)
    if not out:
        return result(cmd, NOT_READ, detail="no services came back to describe")
    pairs = [line.split("\t") for line in out.splitlines()]
    said = ["%s signs in as %s" % (p[0], p[-1] or "unset") for p in pairs]
    return result(cmd, READ, value="; ".join(said))


@panel("Who read customer data", "Which principal opened the customer table today?")
def customer_data_reads():
    cmd = "gcloud logging read %s --limit=20 --freshness=1d --format=json"
    data, res = read_json(cmd % shlex.quote(AUDIT))
    if data is None:
        return res
    who, columns = [], set()
    for entry in data:
        payload = entry.get("protoPayload", {})
        auth = payload.get("authenticationInfo", {})
        # An Agent Identity has no email address; it lands in principalSubject.
        named = auth.get("principalEmail") or auth.get("principalSubject")
        who.append(named or "no principal on the entry")
        columns.update(
            payload.get("metadata", {}).get("tableDataRead", {}).get("fields", [])
        )
    if not who:
        res["value"] = "no reads of this dataset are recorded in the last 24 hours"
        return res
    # Counts, principals and column names are safe. Customer rows are never shown.
    res["value"] = "%d reads by: %s. Columns touched: %s" % (
        len(who),
        "; ".join(sorted(set(who))),
        ", ".join(sorted(columns)) or "not recorded",
    )
    return res


@panel("Who set the screening level", "Who chose it, and when was it last reviewed?")
def screening_review_owner():
    # Expected to be UNKNOWN, and that is why it is on the page: nothing in the
    # configuration records a human decision, so an honest board says so instead
    # of leaving the question off. (gcloud needs an endpoint override for
    # model-armor commands, which this app will not set - that would be a write.)
    cmd = "gcloud model-armor templates describe %s --location=%s --format=json"
    data, res = read_json(cmd % (TEMPLATE, REGION))
    if data is None:
        return res
    labels = data.get("labels") or {}
    owner = labels.get("owner") or labels.get("reviewed-by")
    if owner:
        res["value"] = "recorded owner: %s" % owner
        return res
    res["state"] = NOT_READ
    res["detail"] = "the template records no owner and no review date, so no \
command on this page can say who chose the level or when"
    return res


# The only writes in this app: two ordinary agent calls, so the learner can cause
# a read and watch attribution happen. ADAPT ME - confirm each payload against
# the DEPLOYED agent. If a shape is wrong the call fails and this page shows the
# real error rather than pretending the trigger worked.
ASK = "What is my loyalty tier?"
TRIGGERS = {
    "personalization": {
        "match": "personal",
        "path": "/a2a/v1/message:stream",
        "body": {"request": {"role": "ROLE_USER", "content": [{"text": ASK}]}},
    },
    "price-match": {
        "match": "price",
        "path": ":streamQuery",
        "body": {"class_method": "stream_query", "input": {"message": ASK}},
    },
}


def fire_trigger(key):
    """Cause one real agent call, then read the audit panel again."""
    spec = TRIGGERS.get(key)
    if spec is None:
        return result("(no such trigger)", NOT_READ, detail="unknown trigger %r" % key)
    listed, res = curl_json("%s/reasoningEngines" % PARENT)
    if listed is None:
        res["detail"] = "could not list deployed agents, so nothing was called"
        return res
    engines = listed.get("reasoningEngines", [])
    hit = [e for e in engines if spec["match"] in (e.get("displayName") or "").lower()]
    if not hit:
        return result(
            "match a deployed agent named like '%s'" % spec["match"],
            NOT_READ,
            detail="no deployed agent matched, so nothing was called",
        )
    url = "%s/%s%s" % (API, hit[0].get("name"), spec["path"])
    data, res = curl_json(url, payload=spec["body"])
    if data is not None:
        res["value"] = "the call returned; re-read the audit panel below"
    return res


# ADAPT ME (3 of 3) - the framing. This title and this list are most of what
# makes one learner's board read differently from the next one's.
PAGE_TITLE = "What my cloud project says right now"
STILL_OPEN = [
    "A panel that says not read is a gap in the evidence, not a clean result.",
    "This page shows what the platform recorded, not what anybody intended.",
    "Nothing here shows a control is switched on - only that a command answered.",
    "No command on this page names a human owner for any of these settings.",
]

# The layout contract, implemented once. references/build-and-ground.md §6 has the
# rules and the reasoning; this is what they look like in CSS. Change the panels and
# the words freely - if you rewrite this block, rewrite it to the same contract, not
# to a fresh guess. Light paper, one column, a proportional face for prose, monospace
# only on commands and identifiers, and long resource paths that wrap. No webfont, no
# @import, no remote anything: the page must survive the network being unplugged.
CSS = """
:root {
  --prose: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  --t-note: 0.8rem; --t-body: 1rem; --t-panel: 1.25rem;
  --t-band: 1.5625rem; --t-page: 1.9531rem;
  --s-xs: 0.5rem; --s-sm: 0.75rem; --s-md: 1rem;
  --s-lg: 1.5rem; --s-xl: 2.5rem;
  --measure: 68ch;  /* prose */
  --column: 52rem;  /* the page's single column */
  /* Hex first so an old engine renders; oklch second so a modern one gets the
     intended colour. No pure black, no pure white, and no state colour at all -
     the palette holds no token that could tell a reader an outcome. */
  --paper: #F6F4EF;  --paper: oklch(97% 0.007 89);
  --panel: #FCFAF5;  --panel: oklch(99% 0.007 89);
  --rule: #DFDACF;   --rule: oklch(89% 0.016 86);
  --muted: #6B665D;  --muted: oklch(51% 0.015 82);
  --ink: #232019;    --ink: oklch(24% 0.014 88);
  --accent: #8A5A2B; --accent: oklch(51% 0.089 63);
}
html, body { overflow-x: clip; }
body { font-family: var(--prose); font-size: var(--t-body); line-height: 1.55;
       color: var(--ink); background: var(--paper); max-width: var(--column);
       margin: var(--s-xl) auto; padding: 0 var(--s-md); }
h1 { font-size: var(--t-page); line-height: 1.2; letter-spacing: -0.02em;
     margin: 0 0 var(--s-xs) 0; }
h2 { font-size: var(--t-panel); line-height: 1.25; margin: 0 0 var(--s-xs) 0; }
p { max-width: var(--measure); margin: 0 0 var(--s-sm) 0; overflow-wrap: anywhere; }
.panel { background: var(--panel); border: 1px solid var(--rule);
         padding: var(--s-lg); margin: 0 0 var(--s-lg) 0; }
.band { margin-top: var(--s-xl); }
.q { color: var(--muted); }
.value { font-variant-numeric: tabular-nums; }
.detail:empty { display: none; }
/* A state is a word in running text - no box, no colour, no capitals. Rendering
   "not read" as a chip is how a reading turns into a verdict. */
.state { font-weight: 600; }
.when { color: var(--muted); font-size: var(--t-note); margin: 0; }
h1 + .when { margin-bottom: var(--s-xl); }
/* Monospace lives here and nowhere else: commands, identifiers, timestamps and
   errors quoted from the platform. Never a heading, never body prose. */
pre, code { font-family: var(--mono); font-size: var(--t-note);
            overflow-wrap: anywhere; word-break: break-word; }
pre { background: var(--paper); border: 1px solid var(--rule); border-radius: 0;
      padding: var(--s-sm); margin: 0 0 var(--s-xs) 0; white-space: pre-wrap;
      min-width: 0; }
ul { margin: 0; padding-left: 1.1rem; } li { margin-bottom: var(--s-xs); }
form { display: inline; }
button { font: inherit; font-size: var(--t-body); color: var(--ink);
         background: var(--panel); border: 1px solid var(--ink); min-height: 44px;
         padding: var(--s-xs) var(--s-md); margin: 0 var(--s-xs) var(--s-xs) 0;
         white-space: nowrap; cursor: pointer; }
button:hover { background: var(--paper); }
button:active { border-width: 1px; background: var(--rule); }
button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
button:disabled { opacity: 0.55; cursor: not-allowed; }
a { color: var(--ink); text-decoration-color: var(--accent); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (max-width: 30rem) { body { margin: var(--s-lg) auto; } }
"""

PANEL_HTML = """<section class='panel'><h2>%(title)s</h2><p class='q'>%(question)s</p>
<p class='value'><span class='state'>%(state)s</span> %(value)s</p>
<p class='detail'>%(detail)s</p>
<pre>%(command)s</pre><p class='when'>ran at %(at)s</p></section>"""

BUTTON = """<form method='post' action='/trigger'>
<input type='hidden' name='agent' value='%s'>
<button type='submit'>call the %s agent</button></form> """

PAGE_HTML = """<!doctype html><html lang='en'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>%(title)s</title><style>%(css)s</style></head><body><h1>%(title)s</h1>
<p class='when'>project <code>%(project)s</code>, region <code>%(region)s</code>.
Built %(at)s.</p>%(extra)s
<section class='panel'><h2>Cause a read</h2><p class='q'>Call an agent for real,
then read the audit panel again.</p>%(buttons)s</section>%(panels)s
<section class='panel band'><h2>Still open</h2><ul>%(gaps)s</ul></section>
</body></html>"""


def safe_call(fn):
    """A panel that raises must not take the page down. Report it as raised."""
    try:
        return fn()
    except Exception as exc:  # deliberate: an honest state beats a stack trace
        return result("(%s raised)" % fn.__name__, RAISED, detail=repr(exc))


def render_panel(title, question, res):
    """Words only. There is no colour, tick or score anywhere in this template."""
    fields = dict(res, title=title, question=question)
    return PANEL_HTML % {k: html.escape(str(v or "")) for k, v in fields.items()}


def render_page(extra=None):
    """Every page load re-runs every panel. Stale evidence is not evidence."""
    return PAGE_HTML % dict(
        title=html.escape(PAGE_TITLE),
        css=CSS,
        project=html.escape(PROJECT or "not resolved"),
        region=html.escape(REGION),
        at=utc_now(),
        extra=render_panel(*extra) if extra else "",
        buttons="".join(BUTTON % (html.escape(k), html.escape(k)) for k in TRIGGERS),
        panels="".join(render_panel(f.title, f.question, safe_call(f)) for f in PANELS),
        gaps="".join("<li>%s</li>" % html.escape(x) for x in STILL_OPEN),
    )


class Handler(BaseHTTPRequestHandler):
    def _send(self, page):
        data = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(render_page())

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        key = (parse_qs(raw.decode("utf-8")).get("agent") or [""])[0]
        question = "Did calling this agent produce an attributed read?"
        self._send(render_page(("Trigger: %s" % key, question, fire_trigger(key))))

    def log_message(self, format, *args):
        pass  # the panels are the output; request noise is not


def first_free_port(ports):
    """First port nothing is listening on, so several demos can run at once."""
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            # Same option the server binds with, so the probe's verdict matches
            # what the server can actually do. A port left in TIME_WAIT by an
            # earlier run is free; a port somebody is listening on is not.
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind((HOST, port))
                return port
            except OSError:
                continue
    return None


def selftest():
    """Run every panel once. Non-zero exit only if a panel RAISED."""
    print("starter_app self-test  %s" % utc_now())
    print("project: %s   region: %s\n" % (PROJECT or "(not resolved)", REGION))
    print("%-30s %-14s %s" % ("PANEL", "STATE", "DETAIL"))
    print("%-30s %-14s %s" % ("-" * 30, "-" * 14, "-" * 44))
    tally = {}
    for fn in PANELS:
        res = safe_call(fn)
        tally[res["state"]] = tally.get(res["state"], 0) + 1
        said = str(res["value"] or res["detail"] or "")
        print("%-30s %-14s %s" % (fn.title[:30], res["state"], said[:60]))
    print("")
    for state in (READ, NOT_READ, FAILED, RAISED):
        print("%-14s %d" % (state, tally.get(state, 0)))
    if tally.get(RAISED):
        print("\nA panel raised. That is a bug in the panel, not a finding.")
        return 1
    print("\nNo panel raised: every panel returned a state it can show on a page.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="an honest evidence board")
    parser.add_argument("--selftest", action="store_true", help="run panels, exit")
    if parser.parse_args().selftest:
        return selftest()
    port = first_free_port(PORTS)
    if port is None:
        print("No free port in %d-%d. Stop another demo first." % (PORTS[0], PORTS[-1]))
        return 1
    # flush: a learner who backgrounds this still needs to see the URL at once.
    print("starter_app listening on port %d" % port, flush=True)
    print("Open this in Chrome:  http://%s:%d/" % (HOST, port), flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    server = ThreadingHTTPServer((HOST, port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
