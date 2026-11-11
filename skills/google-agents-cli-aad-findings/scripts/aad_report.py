#!/usr/bin/env python3
"""Print ONE json object with everything an AAD findings answer needs.

    python3 aad_report.py [DAYS]        # DAYS defaults to 7

Run it, read the json, write the answer. Nothing else to fetch, nothing to
look up. Doing this by hand took ~20 commands and minutes: every curl
re-minted a token (1.6s measured), per-session GETs ran serially, and the
skill got re-read between calls. Here the token is minted once and every
fan-out is parallel.

Keys are stable; missing data is null or [], never an absent key:
  project, window{start,end}, totals{agents,analysed,flagged},
  agents[{displayName,analysed,flagged}],
  sessions[{sessionId,agent,severity,detectors[..],turns[..]}]
Never exits non-zero -- a partial report beats a failed command.
"""
import json, subprocess, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

RAW = "https://aiplatform.us.rep.googleapis.com/v1beta1"
SEV = ["SEVERITY_LOW", "SEVERITY_MEDIUM", "SEVERITY_HIGH", "SEVERITY_CRITICAL"]


def sh(*a):
    try:
        r = subprocess.run(a, capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception:
        return ""


def get(url, params, hdrs):
    """GET json. Returns {} on any failure -- callers degrade, never crash."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception:
        return {}


def worst(sevs):
    got = [s for s in SEV if s in sevs]
    return got[-1] if got else None


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    project = sh("gcloud", "config", "get-value", "project")
    token = sh("gcloud", "auth", "application-default", "print-access-token")
    if not project or not token:
        print(json.dumps({"error": "no project or token; run "
                          "gcloud auth application-default login"}))
        return

    H = {"Authorization": "Bearer " + token, "x-goog-user-project": project}
    # Auth only, deliberately: naming a quota project on Trace needs
    # serviceusage.services.use on it, which the caller may not hold.
    TH = {"Authorization": "Bearer " + token}
    aad = f"{RAW}/projects/{project}/locations/us"
    trace = f"https://cloudtrace.googleapis.com/v1/projects/{project}"
    now = datetime.now(timezone.utc)
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start = (now - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    win = f'detection_time >= "{start}" AND detection_time <= "{end}"'

    # rollup + flagged list, together
    with ThreadPoolExecutor(8) as ex:
        f_agg = ex.submit(get, f"{aad}/monitoredAgents/-/analyzedSessions:aggregate",
                          {"filter": win, "pageSize": 100}, H)
        f_lst = ex.submit(get, f"{aad}/monitoredAgents/-/analyzedSessions",
                          {"filter": win, "pageSize": 100,
                           "orderBy": "max_severity_rank desc, "
                                      "latest_detection_time desc"}, H)
        f_ma = ex.submit(get, f"{aad}/monitoredAgents", {"pageSize": 100}, H)
        agg, lst, mas = f_agg.result(), f_lst.result(), f_ma.result()

    # the enrolment roster. Needed to say which agents are monitored and to
    # name one that is not; the aggregate only lists agents that had sessions.
    enrolled = [{"displayName": m.get("displayName") or None,
                 "maUuid": m.get("name", "").rsplit("/", 1)[-1],
                 "reasoningEngine": (m.get("agentResource", {}) or {})
                                    .get("agent", "").rsplit("/", 1)[-1] or None,
                 "state": m.get("state")}
                for m in mas.get("monitoredAgents", [])]

    agents = [{"displayName": a.get("agentDisplayName"),
               "analysed": a.get("totalSessionsCount", 0),
               "flagged": a.get("anomalousSessionsCount", 0)}
              for a in agg.get("agentAggregates", [])
              if a.get("agentDisplayName")]

    names = [s["name"] for s in lst.get("analyzedSessions", [])
             if s.get("sessionState") == "SESSION_STATE_FLAGGED"][:20]

    # every flagged session in FULL, in parallel
    with ThreadPoolExecutor(8) as ex:
        fulls = list(ex.map(lambda n: get(f"{RAW}/{n}",
                     {"view": "ANALYZED_SESSION_VIEW_FULL"}, H), names))

    def transcript(sid):
        """First 2 traces only -- the answer quotes at most two turns, and a
        60-turn session is ~60 traces."""
        tl = get(f"{trace}/traces", {"filter": f"gen_ai.conversation.id:{sid}",
                 "startTime": start, "endTime": end, "pageSize": 10,
                 "view": "MINIMAL"}, TH)
        ids = [t["traceId"] for t in tl.get("traces", [])][:2]
        turns = []
        for t in ids:
            for sp in get(f"{trace}/traces/{t}", {}, TH).get("spans", []):
                L = sp.get("labels", {}) or {}
                if L.get("gen_ai.input.messages") or L.get("gen_ai.tool.name"):
                    turns.append({
                        "input": (L.get("gen_ai.input.messages") or "")[:400],
                        "output": (L.get("gen_ai.output.messages") or "")[:400],
                        "tool": L.get("gen_ai.tool.name") or None})
        return turns

    sids = [f.get("name", "").rsplit("/", 1)[-1] for f in fulls if f.get("name")][:5]
    with ThreadPoolExecutor(3) as ex:
        tr = dict(zip(sids, ex.map(transcript, sids)))

    sessions = []
    for f in fulls:
        if not f.get("name"):
            continue
        sid = f["name"].rsplit("/", 1)[-1]
        ma = f["name"].split("/monitoredAgents/")[-1].split("/")[0]
        dets = [{"id": d.get("detectorId"), "severity": d.get("severity"),
                 "probability": d.get("probability"),
                 "explanation": d.get("explanation")}
                for d in (f.get("assessment", {}) or {}).get("detectorFindings", [])]
        dets.sort(key=lambda d: SEV.index(d["severity"])
                  if d["severity"] in SEV else -1, reverse=True)
        sessions.append({"sessionId": sid, "agent": ma,
                         "severity": worst([d["severity"] for d in dets]),
                         "detectors": dets, "turns": tr.get(sid, [])})
    sessions.sort(key=lambda s: SEV.index(s["severity"])
                  if s["severity"] in SEV else -1, reverse=True)

    print(json.dumps({
        "project": project,
        "window": {"start": start, "end": end},
        "totals": {"agents": len(agents), "enrolled": len(enrolled),
                   "analysed": sum(a["analysed"] for a in agents),
                   "flagged": sum(a["flagged"] for a in agents)},
        "enrolledAgents": enrolled,
        "agents": agents,
        "sessions": sessions}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
