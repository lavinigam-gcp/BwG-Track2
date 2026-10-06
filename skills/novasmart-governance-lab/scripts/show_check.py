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
  - no emoji standing in for icons (draw SVG icons)
  - nothing a page must never show: service-account addresses, resource paths, agent-badge
    identifiers, role names, the project id or number, email addresses, customer IDs, and every
    value in .build/mN_private.txt (written by show_facts.py)
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
    ("old product name (say Agent Runtime)", r"(?i)reasoning[ -]?engines?|agent engine|vertex ai|managed agent runtime"),
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
