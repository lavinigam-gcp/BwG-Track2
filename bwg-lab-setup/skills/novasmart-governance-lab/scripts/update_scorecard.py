#!/usr/bin/env python3
"""
update_scorecard.py
Maintains persistent state of verified missions and generates a visually stunning,
cumulative HTML Governance Scorecard report (governance_scorecard.html).
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone

# --- Output locations --------------------------------------------------------
# On the lab VM the learner's home is $HOME, and $HOME is a bind mount from
# the host, so anything written under it survives a container restart. /tmp is
# container-local and is NOT on that mount, so both the report and the
# cumulative state file live under $HOME.
#
# Every path below is absolute and independent of the current working directory
# (agy runs from $HOME/Desktop/Session1, not from the skill directory).
#
# NOVASMART_SCORECARD_HOME exists only so this script can be exercised outside
# the container without writing to $HOME. It is not set in the lab.
HOME_DIR = os.environ.get("NOVASMART_SCORECARD_HOME", os.path.expanduser("~"))
DESKTOP_DIR = os.path.join(HOME_DIR, "Desktop")

# Dedicated report directory. This is the ONLY directory published on the web
# port, so it must never be the skill directory: SKILL.md and
# references/m0..m5.md are the answer key for every mission, and serving them
# would hand the learner a browsable copy of all the answers.
REPORT_DIR = os.path.join(DESKTOP_DIR, "novasmart-scorecard")
REPORT_NAME = "governance_scorecard.html"
REPORT_PATH = os.path.join(REPORT_DIR, REPORT_NAME)

STATE_FILE = os.path.join(REPORT_DIR, "novasmart_governance_scorecard_state.json")
TARGET_HTML_PATHS = [
    REPORT_PATH,                             # the copy served over HTTP
    os.path.join(DESKTOP_DIR, REPORT_NAME)   # convenience copy on the Desktop
]

SERVE_PORT = 8088
SCORECARD_URL = "http://localhost:%d/%s" % (SERVE_PORT, REPORT_NAME)

# Only these missions have a verification step in this lab, so only these can be scored.
# M0 and M5 have no verify step; M4 is a locked placeholder and is not playable.
SCORED_MISSIONS = ["M1", "M2", "M3"]

ACHIEVEMENTS = {
    "M0": {
        "title": "Estate Visibility & Discovery",
        "badge": "\U0001F50D Scout of the Estate",
        "icon": "visibility",
        "tagline": "\U0001F3C6 Achievement Unlocked: Scout of the Estate \u2014 You swept the estate and surfaced workloads nobody had catalogued."
    },
    "M1": {
        "title": "Identity & Data Least Privilege",
        "badge": "\U0001F194 Identity Fortress",
        "icon": "fingerprint",
        "tagline": "\U0001F3C6 Achievement Unlocked: Eliminator of Shared Credentials \u2014 You split the shared login, gave each workload its own identity, and cut its access back to what the job needs."
    },
    "M2": {
        "title": "Inbound & Outbound Perimeter Controls",
        "badge": "\U0001F6AA Perimeter Shield",
        "icon": "shield",
        "tagline": "\U0001F3C6 Achievement Unlocked: Architect of Agent Boundaries \u2014 You locked the back-office agent so only the front desk can call it, and watched an unauthorised caller be refused."
    },
    "M3": {
        "title": "Ingress Model Armor Screening",
        "badge": "\U0001F6E1\uFE0F Model Armor Guard",
        "icon": "security",
        "tagline": "\U0001F3C6 Achievement Unlocked: Guardian of the Inference Boundary \u2014 You put content screening in front of the Price Match Agent and watched it refuse a jailbreak that used to get through."
    },
    "M5": {
        "title": "Continuous Quality Evaluation & Decision",
        "badge": "\U0001F3C6 Sovereign AI Executive",
        "icon": "military_tech",
        "tagline": "\U0001F3C6 Grand Achievement Unlocked: Sovereign AI Executive \u2014 You measured the agent before trusting it, applied a fix, and measured again."
    }
}

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"missions": {}, "last_updated": None}

def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: could not save state to {STATE_FILE}: {e}", file=sys.stderr)

def render_html_report(state):
    missions = state.get("missions", {})
    total_missions = len(SCORED_MISSIONS)
    passed_missions = sum(1 for c in SCORED_MISSIONS
                          if missions.get(c, {}).get("status") == "PASS")
    progress_pct = int((passed_missions / total_missions) * 100) if total_missions > 0 else 0

    cards_html = []
    for code in SCORED_MISSIONS:
        m_info = ACHIEVEMENTS.get(code, {})
        m_data = missions.get(code)
        
        if m_data and m_data.get("status") == "PASS":
            status_class = "pass"
            status_badge = "PASSED"
            badge_title = m_info.get("badge", code)
            timestamp = m_data.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
            tagline = m_data.get("tagline", m_info.get("tagline", ""))
            checks = m_data.get("checks", [])
            
            checks_html = "".join([
                f"""<tr>
                    <td><span class="chk-icon pass">✓</span></td>
                    <td class="chk-title">{c.get('name', 'Check')}</td>
                    <td class="chk-proof"><code>{c.get('proof', 'Verified')}</code></td>
                    <td><span class="pill pass">PASS</span></td>
                </tr>""" for c in checks
            ])
            if not checks_html:
                checks_html = f"<tr><td colspan='4' style='color:#34a853; text-align:center;'>All module security controls verified live.</td></tr>"

            cards_html.append(f"""
            <div class="mission-card completed">
                <div class="card-header">
                    <div class="mission-identity">
                        <span class="mission-code">{code}</span>
                        <div class="mission-titles">
                            <h3>{m_info.get('title', 'Mission')}</h3>
                            <span class="badge-tag">{badge_title}</span>
                        </div>
                    </div>
                    <div class="mission-status-pill pass">{status_badge}</div>
                </div>
                <div class="achievement-banner">
                    {tagline}
                </div>
                <div class="checks-wrapper">
                    <table class="checks-table">
                        <thead>
                            <tr><th></th><th>Control Verification</th><th>Live Audit Proof</th><th>Result</th></tr>
                        </thead>
                        <tbody>{checks_html}</tbody>
                    </table>
                </div>
                <div class="card-footer">
                    <span>Verified at: <strong>{timestamp}</strong></span>
                    <span>Status: <strong style="color: #34a853;">100% COMPLIANT</strong></span>
                </div>
            </div>
            """)
        elif m_data and m_data.get("status") == "FAIL":
            status_badge = "NON-COMPLIANT"
            badge_title = "⚠️ Incomplete Controls"
            timestamp = m_data.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
            checks = m_data.get("checks", [])
            
            checks_html = "".join([
                f"""<tr>
                    <td><span class="chk-icon {'pass' if c.get('result') == 'PASS' else 'fail'}">{'✓' if c.get('result') == 'PASS' else '✗'}</span></td>
                    <td class="chk-title">{c.get('name', 'Check')}</td>
                    <td class="chk-proof"><code>{c.get('proof', 'Discrepancy observed')}</code></td>
                    <td><span class="pill {'pass' if c.get('result') == 'PASS' else 'fail'}">{c.get('result', 'FAIL')}</span></td>
                </tr>""" for c in checks
            ])
            if not checks_html:
                checks_html = f"<tr><td colspan='4' style='color:#ea4335; text-align:center;'>Some required security controls have not been applied.</td></tr>"

            cards_html.append(f"""
            <div class="mission-card failed">
                <div class="card-header">
                    <div class="mission-identity">
                        <span class="mission-code failed">{code}</span>
                        <div class="mission-titles">
                            <h3>{m_info.get('title', 'Mission')}</h3>
                            <span class="badge-tag failed">{badge_title}</span>
                        </div>
                    </div>
                    <div class="mission-status-pill fail">{status_badge}</div>
                </div>
                <div class="warning-banner">
                    ⚠️ <strong>Audit Discrepancies Found:</strong> Some required security controls for {code} are not yet active or configured in the cloud.
                </div>
                <div class="checks-wrapper">
                    <table class="checks-table">
                        <thead>
                            <tr><th></th><th>Control Verification</th><th>Observed Live State</th><th>Result</th></tr>
                        </thead>
                        <tbody>{checks_html}</tbody>
                    </table>
                </div>
                <div class="card-footer">
                    <span>Audited at: <strong>{timestamp}</strong></span>
                    <span>Status: <strong style="color: #ea4335;">NON-COMPLIANT</strong> — Apply missing steps to pass</span>
                </div>
            </div>
            """)
        else:
            cards_html.append(f"""
            <div class="mission-card pending">
                <div class="card-header">
                    <div class="mission-identity">
                        <span class="mission-code pending">{code}</span>
                        <div class="mission-titles">
                            <h3>{m_info.get('title', 'Mission')}</h3>
                            <span class="badge-tag pending">🔒 Awaiting Verification</span>
                        </div>
                    </div>
                    <div class="mission-status-pill pending">LOCKED</div>
                </div>
                <div class="pending-notice">
                    Complete all hands-on steps in <strong>{code}</strong> and run verification to unlock this badge.
                </div>
            </div>
            """)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>NovaSmart AI Governance · Executive Live Scorecard</title>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto+Mono:wght@400;500&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --blue:#1a73e8; --blue-700:#1967d2; --blue-050:#e8f0fe;
  --green:#1e8e3e; --green-050:#e6f4ea; --green-100:#ceead6;
  --surface:#ffffff; --bg:#f8f9fa; --surface-card:#ffffff;
  --ink:#202124; --ink-muted:#5f6368; --border:#dadce0;
  --radius:12px; --radius-lg:16px;
  --font:'Google Sans',Roboto,system-ui,sans-serif;
  --mono:'Roboto Mono',monospace;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: var(--font); background: var(--bg); color: var(--ink);
  line-height: 1.5; padding: 32px 24px;
}}
.container {{ max-width: 1080px; margin: 0 auto; }}

/* Top Header */
.top-header {{
  background: linear-gradient(135deg, #174ea6 0%, #1a73e8 100%);
  color: #fff; padding: 32px; border-radius: var(--radius-lg);
  box-shadow: 0 4px 16px rgba(26,115,232,0.15); margin-bottom: 28px;
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 20px;
}}
.header-info h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
.header-info p {{ font-size: 15px; opacity: 0.9; }}
.progress-box {{
  background: rgba(255,255,255,0.15); backdrop-filter: blur(8px);
  padding: 16px 24px; border-radius: var(--radius); text-align: center;
  border: 1px solid rgba(255,255,255,0.25);
}}
.progress-box .stat {{ font-size: 28px; font-weight: 700; }}
.progress-box .label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.85; }}

/* Mission Cards */
.mission-card {{
  background: var(--surface-card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 24px; margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(60,64,67,0.08); transition: transform 0.2s ease;
}}
.mission-card.completed {{ border-left: 6px solid var(--green); }}
.mission-card.failed {{ border-left: 6px solid #ea4335; background: #fffcfc; }}
.mission-card.pending {{ opacity: 0.7; border-left: 6px solid #9aa0a6; background: #fdfdfd; }}

.card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
.mission-identity {{ display: flex; align-items: center; gap: 14px; }}
.mission-code {{
  background: var(--blue-050); color: var(--blue-700); font-weight: 700;
  font-size: 16px; padding: 8px 14px; border-radius: 8px; font-family: var(--mono);
}}
.mission-code.failed {{ background: #fce8e6; color: #c5221f; }}
.mission-code.pending {{ background: #f1f3f4; color: #5f6368; }}
.mission-titles h3 {{ font-size: 18px; font-weight: 600; color: var(--ink); }}
.badge-tag {{ font-size: 13px; color: var(--green); font-weight: 500; }}
.badge-tag.failed {{ color: #c5221f; font-weight: 500; }}
.badge-tag.pending {{ color: #70757a; font-weight: normal; }}

.mission-status-pill {{
  padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 700; text-transform: uppercase;
}}
.mission-status-pill.pass {{ background: var(--green-050); color: var(--green); border: 1px solid var(--green-100); }}
.mission-status-pill.fail {{ background: #fce8e6; color: #c5221f; border: 1px solid #fad2cf; }}
.mission-status-pill.pending {{ background: #f1f3f4; color: #5f6368; }}

/* Achievement Banner */
.achievement-banner {{
  background: #fef7e0; color: #b06000; border: 1px solid #fde293;
  padding: 14px 18px; border-radius: 8px; font-size: 14.5px; font-weight: 500;
  margin-bottom: 18px; display: flex; align-items: center; gap: 10px;
}}
.warning-banner {{
  background: #fce8e6; color: #c5221f; border: 1px solid #fad2cf;
  padding: 14px 18px; border-radius: 8px; font-size: 14px; font-weight: 500;
  margin-bottom: 18px; display: flex; align-items: center; gap: 10px;
}}

/* Checks Table */
.checks-wrapper {{ overflow-x: auto; margin-bottom: 14px; }}
.checks-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.checks-table th {{ text-align: left; padding: 8px 12px; color: var(--ink-muted); font-weight: 500; font-size: 12.5px; border-bottom: 1px solid var(--border); }}
.checks-table td {{ padding: 10px 12px; border-bottom: 1px solid #f1f3f4; }}
.chk-icon.pass {{ color: var(--green); font-weight: bold; }}
.chk-icon.fail {{ color: #ea4335; font-weight: bold; }}
.chk-title {{ font-weight: 500; color: var(--ink); }}
.chk-proof code {{ font-family: var(--mono); font-size: 12.5px; background: #f1f3f4; padding: 3px 6px; border-radius: 4px; color: #3c4043; }}
.pill.pass {{ background: var(--green-050); color: var(--green); padding: 2px 8px; border-radius: 4px; font-size: 11.5px; font-weight: 700; }}
.pill.fail {{ background: #fce8e6; color: #c5221f; padding: 2px 8px; border-radius: 4px; font-size: 11.5px; font-weight: 700; }}

.card-footer {{
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12.5px; color: var(--ink-muted); padding-top: 10px; border-top: 1px solid #f1f3f4;
}}
.pending-notice {{ color: #70757a; font-size: 14px; padding: 10px 0; }}
</style>
</head>
<body>
<div class="container">
    <header class="top-header">
        <div class="header-info">
            <h1>🛡️ NovaSmart AI Governance Scorecard</h1>
            <p>Live Audit & Compliance Progress Tracker · Global Head of AI Platform & Security</p>
        </div>
        <div class="progress-box">
            <div class="stat">{progress_pct}%</div>
            <div class="label">Compliance Cleared</div>
        </div>
    </header>

    <main>
        { "".join(cards_html) }
    </main>
</div>
</body>
</html>
"""
    for target in TARGET_HTML_PATHS:
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            # Never fail silently: without this the script could print
            # "Successfully updated" having written nothing at all.
            print(f"Warning: could not write {target}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Update Governance Scorecard state and HTML")
    parser.add_argument("--mission", required=True, choices=SCORED_MISSIONS)
    parser.add_argument("--status", required=True, choices=["PASS", "FAIL"])
    parser.add_argument("--checks-json", help="JSON string containing list of checks: [{'name': '...', 'proof': '...'}]")
    args = parser.parse_args()

    # Both the state file and the served report live here.
    try:
        os.makedirs(REPORT_DIR, exist_ok=True)
    except Exception as e:
        print(f"Warning: could not create {REPORT_DIR}: {e}", file=sys.stderr)

    state = load_state()
    m_info = ACHIEVEMENTS.get(args.mission, {})
    
    checks = []
    if args.checks_json:
        try:
            checks = json.loads(args.checks_json)
        except Exception as e:
            print(f"ERROR: --checks-json is not valid JSON: {e}", file=sys.stderr)
            sys.exit(2)

    # A PASS with no evidence behind it is a fabricated all-clear - the exact failure
    # this lab exists to teach against. Refuse to render one.
    if args.status == "PASS" and not checks:
        print("ERROR: --status PASS requires --checks-json with at least one check.",
              file=sys.stderr)
        print("       Each check needs a name and the proof you actually observed, e.g.",
              file=sys.stderr)
        print("       --checks-json '[{\"name\":\"...\",\"proof\":\"...\"}]'",
              file=sys.stderr)
        sys.exit(2)

    state["missions"][args.mission] = {
        "status": args.status,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "tagline": m_info.get("tagline", ""),
        "checks": checks
    }
    state["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    save_state(state)
    render_html_report(state)
    
    # Ensure background HTTP server is running on port 8088
    import subprocess
    import socket

    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    # Serve ONLY the dedicated report directory. Serving the skill directory
    # would publish SKILL.md and references/m0..m5.md - the full answer key for
    # every mission - as a browsable directory listing.
    web_root = REPORT_DIR
    if not is_port_open(SERVE_PORT):
        subprocess.Popen(
            ["python3", "-m", "http.server", str(SERVE_PORT),
             "--bind", "127.0.0.1", "--directory", web_root],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    # Launch browser automatically in background. In this lab a PATH shim ahead
    # of the real xdg-open only logs the URL and exits 0, so this may silently
    # do nothing - the printed links below are the reliable route.
    try:
        subprocess.Popen(["xdg-open", SCORECARD_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except Exception:
        pass

    print(f"Successfully updated Scorecard for {args.mission} -> {args.status}.")
    print(f"📊 Live Scorecard URL: {SCORECARD_URL}")
    print(f"📄 Or open the file directly: file://{REPORT_PATH}")
    print(f"📁 On disk: {REPORT_PATH}")
    print(f"   (a copy is also on the Desktop: {os.path.join(DESKTOP_DIR, REPORT_NAME)})")
    print("   If the browser does not open by itself, paste one of the links above.")

if __name__ == "__main__":
    main()
