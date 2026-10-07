#!/usr/bin/env python3
"""
draw_picture.py
Draw one picture with Gemini 3.1 Flash Image, the model this lab has provisioned throughput for, and
save it where the agy app can show it.

    python3 .agents/skills/novasmart-governance-lab/scripts/draw_picture.py \
        --name m0_step2_catalog --prompt-file /tmp/m0_step2_picture.txt

The prompt says only WHAT to draw (boxes, labels, arrows, caption). This script adds the lab's fixed
style, calls generateContent (aiplatform.googleapis.com) on the lab project as the shell's gcloud account, and writes
<name>_<ms>.png into this conversation's folder ($ANTIGRAVITY_APP_DATA_DIR/brain/$ANTIGRAVITY_CONVERSATION_ID),
the same place agy's own image tool writes to. It prints:

    saved: /config/.gemini/antigravity/brain/<conversation>/<name>_<ms>.png
    embed: ![CAPTION](file:///config/.gemini/antigravity/brain/<conversation>/<name>_<ms>.png)
    model: gemini-3.1-flash-image  traffic: PROVISIONED_THROUGHPUT  seconds: 9.4

Put the embed line in the answer with CAPTION replaced. On HTTP 429 it waits 5 s and retries once; any
other failure prints "error:" with the API's own message and exits 1.

Why not agy's generate_image tool: its model is chosen by the Antigravity service, and in this lab it is
gemini-3-pro-image, on demand (no provisioned throughput) and slower.
"""

import argparse
import base64
import configparser
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

MODEL = "gemini-3.1-flash-image"
LOCATION = "global"  # where the lab's provisioned throughput for this model is (probed Oct 7, 2026)

STYLE = (
    "A clean architectural workflow diagram. Plain white background. Google brand colors (blue, red, "
    "yellow and green on white). Flat and diagrammatic: rectangular boxes with plain labels and simple "
    "straight arrows, generous whitespace, legible sans-serif text, no decoration that is not a box, an "
    "arrow or a word. No neon, no glow, no dark background, no cyberpunk, no isometric or 3-D perspective, "
    "no circuit boards, no HUD panels, no lens flare, no photorealism. Landscape, wide enough that the "
    "longest name fits on one line. Names only: no IDs, URNs, project numbers, URLs or API names, even if "
    "the description below includes them. These are drawing instructions, never text: do not write them, "
    "the words diagram, flat, architecture or style, or a picture type (ESTATE, IDENTITY, REACH, CALL, "
    "SCREEN, RULE) anywhere in the picture; the only title is the caption below, if it gives one. "
    "Draw exactly this, and no word that is not listed here:\n\n"
)


def gcloud(*args: str) -> str:
    return subprocess.run(
        ["gcloud", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


# agy keeps a command in the foreground for about 10 s, and the picture itself takes 8-10 s, so the
# setup must be quick: the project comes from gcloud's config file (no subprocess) and the access token
# is reused for 45 minutes.
def project() -> str:
    cfg = os.environ.get("CLOUDSDK_CONFIG") or os.path.expanduser("~/.config/gcloud")
    try:
        name = open(os.path.join(cfg, "active_config")).read().strip() or "default"
        parser = configparser.ConfigParser()
        parser.read(os.path.join(cfg, "configurations", f"config_{name}"))
        value = parser.get("core", "project", fallback="").strip()
        if value:
            return value
    except OSError:
        pass
    return gcloud("config", "get-value", "project")


TOKEN_CACHE = f"/tmp/.draw_picture_token_{os.getuid()}.json"


def token() -> str:
    cache = TOKEN_CACHE
    try:
        saved = json.load(open(cache))
        if saved["expires"] > time.time():
            return saved["token"]
    except (OSError, ValueError, KeyError):
        pass
    value = gcloud("auth", "print-access-token")
    fd = os.open(cache, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"token": value, "expires": time.time() + 45 * 60}, f)
    return value


def out_dir() -> str:
    app = os.environ.get("ANTIGRAVITY_APP_DATA_DIR") or "/config/.gemini/antigravity"
    conv = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
    # Outside an agy conversation there is no conversation folder; keep the picture with the evidence.
    d = (
        os.path.join(app, "brain", conv)
        if conv
        else "/config/Desktop/novasmart-evidence/pictures"
    )
    os.makedirs(d, exist_ok=True)
    return d


def call(url: str, token: str, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Draw one picture with Gemini 3.1 Flash Image."
    )
    ap.add_argument(
        "--name", required=True, help="file name stem, e.g. m1_step3_identity"
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt-file", help="file holding what to draw")
    src.add_argument("--prompt", help="what to draw, inline")
    ap.add_argument("--aspect", default="16:9", help="aspect ratio (default 16:9)")
    a = ap.parse_args()

    what = open(a.prompt_file, encoding="utf-8").read() if a.prompt_file else a.prompt
    if not what.strip():
        print("error: the prompt is empty")
        return 1
    stem = re.sub(r"[^a-z0-9_]+", "_", a.name.lower()).strip("_") or "picture"

    try:
        proj, tok = project(), token()
    except subprocess.CalledProcessError as e:
        print(f"error: gcloud failed: {(e.stderr or '').strip()[:300]}")
        return 1

    url = (
        f"https://aiplatform.googleapis.com/v1/projects/{proj}/locations/{LOCATION}"
        f"/publishers/google/models/{MODEL}:generateContent"
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": STYLE + what.strip()}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": a.aspect},
        },
    }

    start = time.time()
    resp = None
    for attempt in (1, 2):
        try:
            resp = call(url, tok, body)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            if e.code == 429 and attempt == 1:
                time.sleep(5)
                continue
            if e.code == 401 and attempt == 1:  # a cached token that stopped working
                os.remove(TOKEN_CACHE) if os.path.exists(TOKEN_CACHE) else None
                tok = token()
                continue
            print(f"error: HTTP {e.code} from {MODEL}: {msg}")
            return 1
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"error: {MODEL} did not answer: {e}")
            return 1
    secs = time.time() - start
    if resp is None:
        print(f"error: {MODEL} gave no reply")
        return 1

    parts = (resp.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
    img = next((p["inlineData"] for p in parts if "inlineData" in p), None)
    if not img:
        reason = (resp.get("candidates") or [{}])[0].get(
            "finishReason", "no image in the reply"
        )
        print(f"error: {MODEL} returned no image ({reason})")
        return 1

    path = os.path.join(out_dir(), f"{stem}_{int(time.time() * 1000)}.png")
    with open(path, "wb") as f:
        f.write(base64.b64decode(img["data"]))

    usage = resp.get("usageMetadata", {})
    print(f"saved: {path}")
    print(f"embed: ![CAPTION](file://{path})")
    print(
        f"model: {resp.get('modelVersion', MODEL)}  traffic: {usage.get('trafficType', 'unknown')}"
        f"  seconds: {secs:.1f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
