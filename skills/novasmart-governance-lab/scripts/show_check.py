#!/usr/bin/env python3
"""
show_check.py - check a Show-step page, then render it so you can look at it.

Usage (run exactly like this, so Chromium is found):
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright /opt/venv/bin/python3 \
        /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/show_check.py \
        /config/Desktop/novasmart-showcase/m0_dashboard.html [--poster]

Static checks on the file:
  - one self-contained file: no script, style, font or image fetched from the network
  - the page's facts sit in <script type="application/json" id="evidence">, and it parses
  - no role names (bigquery.admin, aiplatform.user ...); every <svg> has role="img"; no <select>;
    no reworded API text; no roadmap/remediation; every HH:MM:SS time is in the fact sheet; the fact sheet
    is newer than the other pages (re-run show_facts.py per page); white page, Google Sans, labels >= 11 px
  - no emoji standing in for icons (draw SVG icons); no clickable <div>; prefers-reduced-motion honoured
    when anything moves; a Play button comes with Pause and Step
  - every "mN_stepK.txt L<n>" citation points at a line that exists in that evidence file
  - nothing a page must never show: service-account addresses, resource paths, agent-badge
    identifiers, role names, the project id or number, email addresses, customer IDs, and every
    value in .build/mN_private.txt (written by show_facts.py), the exposed discount code
Render checks (headless Chromium):
  - no JavaScript error on load, or when each button is pressed once
  - no network request
  - no sideways scrolling on a 390 px phone screen
  - screenshots in .build/previews/: <name>_1440.png and <name>_390.png; <name>_play.png (a game
    after its Start button) or <name>_next.png (a presentation two slides in); <name>_answers.png
    when the page has an answers view (#answers). Open them and look before you answer.
  --poster: also saves the 1600 x 900 picture next to the page as <name>.png, and fails if the
    content does not fit inside it.

Prints a short report and ends with RESULT. Exit 0 only when nothing needs fixing.
Reads the page and the fact sheet's private list; runs no cloud command, changes nothing else.
"""

import json
import os
import re
import sys

HOME_DIR = os.environ.get("NOVASMART_SHOW_HOME", "/config")
BUILD_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-showcase", ".build")
EVIDENCE_DIR = os.path.join(HOME_DIR, "Desktop", "novasmart-evidence")
CITE = re.compile(r"(m\d)_(step\d+|other)\.txt\W{0,3}L(\d+)(?:\s*[-–]\s*L?(\d+))?")
CLICK_DIV = re.compile(r"<(div|span|li|td|tr|article|section|p|img|svg|g|rect)\b[^>]*\sonclick\s*=", re.I)

LEAKS = [
    (
        "service-account address",
        r"iam\.gserviceaccount\.com|developer\.gserviceaccount\.com",
    ),
    ("resource path", r"projects/"),
    ("agent-badge identifier", r"principal://|agents\.global\.org-|system\.id\.goog"),
    ("role name", r"roles/"),
    ("login identifier", r"\bsa://"),
    ("project id", r"qwiklabs-gcp-"),
    (
        "email address",
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}",
    ),
    ("long number (project number or resource id)", r"(?<![\d.])\d{12,}(?![\d.])"),
    ("customer ID", r"\bCUST-\d+"),
    ("the exposed discount code (say 'the exposed discount code')", r"\bNVST-[A-Z]+-\d+"),
    # prose names only: API identifiers such as reasoningEngines.query in a quoted log line are allowed
    ("old product name (say Agent Runtime)", r"(?i)reasoning[ -]engines?\b|agent engine|vertex ai|managed agent runtime"),
    ("reworded or invented API text (quote it exactly or drop it)",
     r"Permission to query agent denied|\bagentruntime\.|AgentExecutionService"),
    ("a plan or remedy of your own (no roadmap, remediation or action items)",
     r"(?i)\broadmap\b|\bremediat\w*|\bAction:"),
    ("role name (say what it lets you do)",
     r"\b(?:bigquery|aiplatform|iap|storage|run|logging|resourcemanager)\.(?:admin|user|jobUser|dataViewer|"
     r"dataEditor|dataOwner|viewer|egressor|invoker|objectViewer|objectAdmin|expressUser|securityAdmin|"
     r"agentContextEditor)\b"),
]
EXTERNAL = re.compile(
    r"""(?:\b(?:src|href)\s*=\s*["']?|url\(\s*["']?|@import\s+["']?)(?:https?:)?//(?!localhost|127\.0\.0\.1)""",
    re.I,
)
SCRIPT_SRC = re.compile(r"<script[^>]*\bsrc\s*=", re.I)
EVIDENCE = re.compile(
    r"""<script[^>]*type\s*=\s*["']?application/json["']?[^>]*id\s*=\s*["']?evidence\b["']?[^>]*>(.*?)</script>"""
    r"""|<script[^>]*id\s*=\s*["']?evidence\b["']?[^>]*type\s*=\s*["']?application/json["']?[^>]*>(.*?)</script>""",
    re.I | re.S,
)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def static_checks(path, html, problems, notes):
    size = os.path.getsize(path)
    notes.append(f"file: {path} ({size:,} bytes)")
    if size < 15000:
        notes.append(
            "  thin: under 15 KB usually means a page with no real visuals; see the recipe"
        )

    m = EVIDENCE.search(html)
    if not m:
        problems.append(
            'no <script type="application/json" id="evidence"> block holding the page\'s facts'
        )
    else:
        try:
            data = json.loads(m.group(1) or m.group(2))
            n = len(data) if isinstance(data, (list, dict)) else 1
            notes.append(
                f"evidence block: parses, {n} top-level entr{'y' if n == 1 else 'ies'}"
            )
        except ValueError as e:
            problems.append(f"evidence block does not parse as JSON: {e}")

    lengths = {}
    bad_cites = []
    for m in CITE.finditer(html):
        mod, step, lo, hi = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        f = os.path.join(EVIDENCE_DIR, mod, f"{mod}_{step}.txt")
        if f not in lengths:
            lengths[f] = (sum(1 for _ in open(f, encoding="utf-8", errors="replace"))
                          if os.path.isfile(f) else 0)
        if not lengths[f] or max(lo, hi) > lengths[f]:
            bad_cites.append(f"{mod}_{step}.txt L{lo}" + (f"-L{hi}" if hi != lo else "")
                             + (f" (the file has {lengths[f]} lines)" if lengths[f] else " (no such file)"))
    for c in sorted(set(bad_cites))[:5]:
        problems.append(f"cites {c} - cite only lines the fact sheet shows")
    for m in list(CLICK_DIV.finditer(html))[:3]:
        problems.append(f"line {line_of(html, m.start())}: a clickable <{m.group(1)}> - use a <button> so "
                        "the keyboard reaches it")
    svgs = len(re.findall(r"<svg\b", html, re.I))
    labelled = len(re.findall(r"<svg\b[^>]*role\s*=\s*[\"']img[\"']", html, re.I))
    if svgs and labelled < svgs:
        problems.append(f"{svgs - labelled} of {svgs} <svg> drawings lack role=\"img\" (add it and a <title>)")
    if re.search(r"<select\b", html, re.I):
        problems.append("a <select> dropdown - use buttons the viewer can press")
    if re.search(r"transition\s*:|@keyframes|animation\s*:|\.animate\(", html) and \
            "prefers-reduced-motion" not in html:
        problems.append("the page moves but never checks prefers-reduced-motion - honour it")

    for m in EXTERNAL.finditer(html):
        problems.append(
            f"line {line_of(html, m.start())}: fetches from the network "
            f"({html[m.start() : m.start() + 60]!r}) - inline it or drop it"
        )
    for m in SCRIPT_SRC.finditer(html):
        problems.append(
            f"line {line_of(html, m.start())}: <script src=...> - scripts must be inline"
        )

    emoji = list(re.finditer(r"[\U0001F000-\U0001FAFF]", html))
    if emoji:
        m = emoji[0]
        problems.append(f"line {line_of(html, m.start())}: {len(emoji)} emoji used as icons "
                        f"({m.group(0)!r} first) - draw a simple SVG icon instead")

    for label, pat in LEAKS:
        hits = list(re.finditer(pat, html))
        for m in hits[:3]:
            snippet = html[max(0, m.start() - 20) : m.end() + 20].replace("\n", " ")
            problems.append(f"line {line_of(html, m.start())}: {label}: …{snippet}…")
        if len(hits) > 3:
            problems.append(f"  …and {len(hits) - 3} more {label} hit(s)")

    mod = os.path.basename(path)[:2]
    priv_file = os.path.join(BUILD_DIR, f"{mod}_private.txt")
    if re.fullmatch(r"m\d", mod) and os.path.isfile(priv_file):
        low = html.lower()
        values = [v.strip() for v in open(priv_file, encoding="utf-8") if v.strip()]
        found = [v for v in values if v.lower() in low]
        for v in found[:5]:
            problems.append(
                f"line {line_of(html, low.index(v.lower()))}: a value from the "
                f"never-on-a-page list: {v!r}"
            )
        notes.append(f"private list: {len(values)} values checked, {len(found)} found")
        facts_file = os.path.join(BUILD_DIR, f"{mod}_facts.txt")
        if os.path.isfile(facts_file):
            facts = open(facts_file, encoding="utf-8", errors="replace").read()
            text = re.sub(r"<script\b(?![^>]*application/json)[^>]*>.*?</script>|<style\b.*?</style>", " ",
                          html, flags=re.S | re.I)
            odd = sorted({t for t in re.findall(r"\b\d{2}:\d{2}:\d{2}\b", text) if t not in facts})
            for t in odd[:5]:
                problems.append(f"time {t} is not in the fact sheet - an event with no recorded time gets no time")
            newer = [os.path.basename(f) for f in
                     (os.path.join(os.path.dirname(os.path.abspath(path)), n)
                      for n in os.listdir(os.path.dirname(os.path.abspath(path))))
                     if os.path.basename(f).startswith(mod + "_") and f.endswith(".html")
                     and os.path.abspath(f) != os.path.abspath(path)
                     and os.path.getmtime(f) > os.path.getmtime(facts_file)]
            if newer:
                problems.append(f"the fact sheet is older than {newer[0]} - run show_facts.py again for this page")
    else:
        notes.append(f"private list: {priv_file} not found - run show_facts.py first")


def render_checks(path, html, poster, problems, notes):
    if os.path.isdir("/ms-playwright"):
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/ms-playwright")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        notes.append(
            "render: Playwright is not importable here - run with /opt/venv/bin/python3 "
            "and PLAYWRIGHT_BROWSERS_PATH=/ms-playwright"
        )
        return False

    name = os.path.splitext(os.path.basename(path))[0]
    prev_dir = os.path.join(BUILD_DIR, "previews")
    os.makedirs(prev_dir, exist_ok=True)
    url = "file://" + os.path.abspath(path)
    shots = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()

            def open_page(w, h, frag=""):
                errors, network = [], []
                pg = browser.new_page(viewport={"width": w, "height": h})
                pg.on("pageerror", lambda e: errors.append(str(e).splitlines()[0]))
                pg.on(
                    "console",
                    lambda m: errors.append(m.text.splitlines()[0])
                    if m.type == "error"
                    else None,
                )
                pg.on(
                    "request",
                    lambda r: network.append(r.url)
                    if not r.url.startswith(("file:", "data:", "blob:", "about:"))
                    else None,
                )
                pg.goto(url + frag)
                pg.wait_for_timeout(1500)
                return pg, errors, network

            for w, h in ((1440, 900), (390, 844)):
                pg, errors, network = open_page(w, h)
                out = os.path.join(prev_dir, f"{name}_{w}.png")
                pg.screenshot(path=out, full_page=True)
                shots.append(out)
                sw = pg.evaluate("document.documentElement.scrollWidth")
                ht = pg.evaluate("document.documentElement.scrollHeight")
                notes.append(f"render {w}px: page is {ht} px tall")
                if w == 390 and sw > w + 1:
                    problems.append(
                        f"on a 390 px phone screen the page scrolls sideways (content is "
                        f"{sw} px wide) - let panels stack or wrap"
                    )
                for e in sorted(set(errors))[:5]:
                    problems.append(f"JavaScript error at {w}px: {e}")
                for u in sorted(set(network))[:3]:
                    problems.append(f"network request: {u}")
                pg.close()

            # Press each visible button once and watch for errors.
            pg, errors, _ = open_page(1440, 900)
            look = pg.evaluate("""() => {
              const bg = e => getComputedStyle(e).backgroundColor;
              const tiny = [...document.querySelectorAll('svg text')]
                .filter(t => { const r = t.getBoundingClientRect(); return r.height > 0 && r.height < 11; }).length;
              return {html: bg(document.documentElement), body: bg(document.body),
                      font: getComputedStyle(document.body).fontFamily, tiny};
            }""")
            if look["body"] not in ("rgb(255, 255, 255)", "rgba(0, 0, 0, 0)") or \
                    look["html"] not in ("rgb(255, 255, 255)", "rgba(0, 0, 0, 0)"):
                problems.append(f"the page is not white edge to edge (html {look['html']}, body {look['body']})")
            if "google sans" not in look["font"].lower():
                problems.append(f'the body font is {look["font"]!r} - use "Google Sans", Roboto, Arial, sans-serif')
            if look["tiny"] > 3:
                problems.append(f"{look['tiny']} diagram labels render under 11 px tall - enlarge them")
            labels = [t.strip().lower() for t in pg.locator("button").all_inner_texts()]
            if any(re.search(r"\b(play|replay)\b(?!\s+again)", t) for t in labels) and not (
                any("pause" in t for t in labels) and any("step" in t for t in labels)
            ):
                problems.append("a Play button without Pause and Step buttons - add both")
            buttons = pg.locator("button:visible")
            count = min(buttons.count(), 25)
            for i in range(count):
                try:
                    buttons.nth(i).click(timeout=1500)
                    pg.wait_for_timeout(150)
                except Exception:
                    pass
            notes.append(f"pressed {count} button(s) once each")
            for e in sorted(set(errors))[:5]:
                problems.append(f"JavaScript error after pressing buttons: {e}")
            pg.close()

            # What a viewer sees after the first move: a game's first round (its Start button),
            # or a presentation's third slide (two presses of the right arrow).
            pg, errors, _ = open_page(1440, 900)
            before = pg.screenshot()
            start = pg.locator("button:visible").filter(
                has_text=re.compile(r"^\W*(start|play|begin)", re.I)
            )
            moved = "play"
            try:
                if start.count():
                    start.first.click(timeout=1500)
                else:
                    moved = "next"
                    pg.keyboard.press("ArrowRight")
                    pg.wait_for_timeout(300)
                    pg.keyboard.press("ArrowRight")
                pg.wait_for_timeout(900)
                if pg.screenshot() != before:
                    out = os.path.join(prev_dir, f"{name}_{moved}.png")
                    pg.screenshot(path=out, full_page=True)
                    shots.append(out)
            except Exception:
                pass
            for e in sorted(set(errors))[:3]:
                problems.append(f"JavaScript error after the first move: {e}")
            pg.close()

            if "#answers" in html or re.search(r"""id\s*=\s*["']answers["']""", html):
                pg, errors, _ = open_page(1440, 900, "#answers")
                out = os.path.join(prev_dir, f"{name}_answers.png")
                pg.screenshot(path=out, full_page=True)
                shots.append(out)
                for e in sorted(set(errors))[:3]:
                    problems.append(f"JavaScript error in the answers view: {e}")
                pg.close()

            if poster:
                pg, errors, _ = open_page(1600, 900)
                out = os.path.join(
                    os.path.dirname(os.path.abspath(path)), f"{name}.png"
                )
                pg.screenshot(path=out)
                sw = pg.evaluate("document.documentElement.scrollWidth")
                ht = pg.evaluate("document.documentElement.scrollHeight")
                if sw > 1601 or ht > 901:
                    problems.append(
                        f"poster content is {sw} x {ht} px and does not fit 1600 x 900 - "
                        "shorten the text or tighten the layout"
                    )
                notes.append(f"poster picture: {out}")
                pg.close()
            browser.close()
    except Exception as e:  # a render failure is reported, never hidden
        notes.append(f"render: failed ({str(e).splitlines()[0]})")
        return False
    notes.append("screenshots to open and look at: " + ", ".join(shots))
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not os.path.isfile(args[0]):
        sys.exit(__doc__)
    path, poster = args[0], "--poster" in sys.argv
    html = open(path, encoding="utf-8", errors="replace").read()
    problems, notes = [], []
    static_checks(path, html, problems, notes)
    rendered = render_checks(path, html, poster, problems, notes)
    for n in notes:
        print(n)
    for pr in problems[:25]:
        print("FIX: " + pr)
    if len(problems) > 25:
        print(f"FIX: …and {len(problems) - 25} more")
    if problems:
        print(f"RESULT: fix {len(problems)} problem(s), then run this check again")
        sys.exit(1)
    if not rendered:
        print(
            "RESULT: static checks clean, but the page could not be rendered - say so in one line"
        )
        sys.exit(2)
    print("RESULT: clean - now open the screenshots and look at them")


if __name__ == "__main__":
    main()
