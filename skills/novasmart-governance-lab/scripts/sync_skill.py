#!/usr/bin/env python3
"""
sync_skill.py - bring this lab's guide (the novasmart-governance-lab skill) up to date from its public repo.

Usage (M0 Step 0 asks agy to run this from the repo; a lab built with an older guide has no copy yet):
    curl -fsSL https://raw.githubusercontent.com/lavinigam-gcp/BwG-Track2/main/skills/novasmart-governance-lab/scripts/sync_skill.py -o /tmp/sync_skill.py && python3 /tmp/sync_skill.py
    python3 .agents/skills/novasmart-governance-lab/scripts/sync_skill.py               # once the guide has it
    python3 .agents/skills/novasmart-governance-lab/scripts/sync_skill.py --check    # M0 Step 1, changes nothing

Labs are provisioned with the guide baked in, so a fix to the guide would otherwise need every running lab
rebuilt. This script fetches the guide from github.com/lavinigam-gcp/BwG-Track2 (branch main, folder
skills/novasmart-governance-lab) and puts it in place of every workspace copy:
/config/Desktop/Session*/.agents/skills/novasmart-governance-lab, plus the current folder's copy if it has one.

  1. Reads the branch's commit with `git ls-remote` (the GitHub API is the fallback).
  2. Downloads that commit's archive and extracts only the guide's folder into a staging folder.
  3. Checks the staging copy is whole (SKILL.md naming this skill, references/, scripts/).
  4. Writes a VERSION file into it (commit, branch, source, time, file count).
  5. For each workspace: moves the old copy to /config/.novasmart-skill-sync/<workspace>/previous (one
     backup, outside every workspace, so agy never sees two guides) and moves the new copy in. Ownership
     follows the .agents/skills folder.
Any failure before step 5 changes nothing and says why; the guide already on the machine keeps working.
Changes files on this workstation only: no cloud project, no account, no permission is touched.

--check reads the VERSION of each workspace copy and the branch's commit, and prints one `status:` line:
current, behind, never-synced (a copy with no VERSION file - the one the lab was built with - or no copy)
or unknown (GitHub not reachable). Exit 0 when it could tell, 2 when it could not.
"""

import argparse
import glob
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from datetime import datetime, timezone

NAME = "novasmart-governance-lab"
REPO = "lavinigam-gcp/BwG-Track2"
REF = "main"
PATH_IN_REPO = "skills/" + NAME
HOME_DIR = os.environ.get(
    "NOVASMART_HOME", "/config"
)  # set only to exercise this outside the lab
DESKTOP_DIR = os.path.join(HOME_DIR, "Desktop")
TIMEOUT = 60
MAX_ARCHIVE = 200 * 1024 * 1024


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def targets():
    """Every workspace copy of the guide: Session* folders, plus the current folder if it has one."""
    found = []
    for skills in sorted(
        glob.glob(os.path.join(DESKTOP_DIR, "*", ".agents", "skills"))
    ):
        if os.path.basename(os.path.dirname(os.path.dirname(skills))).startswith(
            "Session"
        ):
            found.append(os.path.join(skills, NAME))
    here = os.path.join(os.getcwd(), ".agents", "skills")
    if os.path.isdir(here):
        found.append(os.path.join(here, NAME))
    out = []
    for t in found:
        if os.path.realpath(t) not in [os.path.realpath(x) for x in out]:
            out.append(t)
    return out


def read_version(skill_dir):
    """{'commit': ..., 'synced': ...} from VERSION, or None when the copy was never synced."""
    p = os.path.join(skill_dir, "VERSION")
    if not os.path.isfile(p):
        return None
    v = {}
    for ln in open(p, encoding="utf-8", errors="replace"):
        k, _, val = ln.strip().partition(" ")
        if k:
            v[k] = val.strip()
    return v if v.get("commit") else None


def state_of(target, v, sha):
    if not os.path.isfile(os.path.join(target, "SKILL.md")):
        return "missing"
    if v is None:
        return "never-synced"
    return "current" if v["commit"] == sha else "behind"


def describe(v):
    if v is None:
        return "the copy this lab was built with (never synced)"
    return f"{v['commit'][:12]} (synced {v.get('synced', 'unknown')})"


def remote_commit(repo, ref):
    """The branch's commit id, or raise RuntimeError with the reason."""
    url = f"https://github.com/{repo}"
    reasons = []
    try:
        r = subprocess.run(
            ["git", "ls-remote", url, f"refs/heads/{ref}"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        line = r.stdout.strip().split("\n")[0]
        if r.returncode == 0 and line and len(line.split()[0]) == 40:
            return line.split()[0]
        reasons.append(
            f"git ls-remote exit {r.returncode} {(r.stderr or r.stdout).strip()[:200]}"
        )
    except (OSError, subprocess.SubprocessError) as e:
        reasons.append(f"git ls-remote: {e}")
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/commits/{ref}",
            headers={
                "Accept": "application/vnd.github.sha",
                "User-Agent": "novasmart-lab-sync",
            },
        )
        sha = urllib.request.urlopen(req, timeout=TIMEOUT).read().decode().strip()
        if len(sha) == 40:
            return sha
        reasons.append(f"GitHub API returned {sha[:80]!r}")
    except (
        Exception
    ) as e:  # network errors come in many types; all mean "could not reach"
        reasons.append(f"GitHub API: {e}")
    raise RuntimeError("; ".join(reasons))


def fetch(repo, sha, path_in_repo, dest):
    """Extract the guide's folder at commit `sha` into dest. Returns the file count."""
    url = f"https://codeload.github.com/{repo}/tar.gz/{sha}"
    req = urllib.request.Request(url, headers={"User-Agent": "novasmart-lab-sync"})
    data = urllib.request.urlopen(req, timeout=TIMEOUT).read(MAX_ARCHIVE + 1)
    if len(data) > MAX_ARCHIVE:
        raise RuntimeError("the archive is larger than expected; refusing it")
    count = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for m in tar.getmembers():
            parts = m.name.split("/", 1)  # archive entries start with "<repo>-<sha>/"
            if len(parts) < 2 or not (parts[1] + "/").startswith(path_in_repo + "/"):
                continue
            rel = parts[1][len(path_in_repo) :].lstrip("/")
            if not rel or "__pycache__" in rel.split("/"):
                continue
            if rel.startswith("/") or ".." in rel.split("/"):
                raise RuntimeError(f"unsafe path in the archive: {m.name}")
            out = os.path.join(dest, rel)
            if m.isdir():
                os.makedirs(out, exist_ok=True)
            elif m.isfile():
                src = tar.extractfile(m)
                if src is None:
                    raise RuntimeError(f"could not read {m.name} from the archive")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, "wb") as f:
                    f.write(src.read())
                os.chmod(out, 0o755 if m.mode & 0o111 else 0o644)
                count += 1
            else:
                raise RuntimeError(
                    f"unexpected link or device in the archive: {m.name}"
                )
    return count


def check_whole(d):
    skill = os.path.join(d, "SKILL.md")
    if not os.path.isfile(skill):
        raise RuntimeError(f"{PATH_IN_REPO}/SKILL.md is missing at that commit")
    head = open(skill, encoding="utf-8", errors="replace").read(600)
    if f"name: {NAME}" not in head:
        raise RuntimeError("SKILL.md at that commit does not name this guide")
    for sub in ("references", "scripts"):
        if not os.path.isdir(os.path.join(d, sub)) or not os.listdir(
            os.path.join(d, sub)
        ):
            raise RuntimeError(
                f"{PATH_IN_REPO}/{sub}/ is missing or empty at that commit"
            )


def chown_like(path, ref):
    if os.geteuid() != 0:
        return
    st = os.stat(ref)
    for dp, dns, fns in os.walk(path):
        os.chown(dp, st.st_uid, st.st_gid)
        for n in fns:
            os.chown(os.path.join(dp, n), st.st_uid, st.st_gid)


def install(staging, target):
    skills_dir = os.path.dirname(target)
    workspace = os.path.dirname(os.path.dirname(skills_dir))
    work = os.path.join(
        HOME_DIR, ".novasmart-skill-sync", os.path.basename(workspace) or "workspace"
    )
    os.makedirs(work, exist_ok=True)
    new, prev = os.path.join(work, "new"), os.path.join(work, "previous")
    shutil.rmtree(new, ignore_errors=True)
    shutil.copytree(staging, new)
    chown_like(new, skills_dir)
    if os.path.exists(target):
        shutil.rmtree(prev, ignore_errors=True)
        os.rename(target, prev)
    os.rename(new, target)
    chown_like(os.path.dirname(work), skills_dir)


def main():
    ap = argparse.ArgumentParser(
        description="Bring this lab's guide up to date from its public repo."
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="report current / behind / never-synced; change nothing",
    )
    ap.add_argument(
        "--force", action="store_true", help="re-install even when already current"
    )
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--ref", default=REF)
    ap.add_argument(
        "--path", default=PATH_IN_REPO, help="the guide's folder inside the repo"
    )
    a = ap.parse_args()

    tg = targets()
    if not tg:
        print(
            f"error: no workspace copy of the guide found under {DESKTOP_DIR}/Session*/.agents/skills/"
        )
        return 2
    versions = {t: read_version(t) for t in tg}
    source = f"github.com/{a.repo} {a.ref}"

    try:
        sha = remote_commit(a.repo, a.ref)
    except RuntimeError as e:
        if a.check:
            print(f"status: unknown - could not reach GitHub ({e})")
            print(f"guide on this machine: {describe(versions[tg[0]])}")
            return 2
        print(f"error: could not reach GitHub, so nothing changed ({e})")
        print(
            f"The guide already on this machine keeps working: {describe(versions[tg[0]])}."
        )
        return 1

    if a.check:
        states = set()
        for t in tg:
            st = state_of(t, versions[t], sha)
            states.add(st)
            print(f"{t}: {st}" + ("" if st == "missing" else f" - {describe(versions[t])}"))
        if states == {"current"}:
            overall = "current"
        elif states & {"never-synced", "missing"}:
            overall = "never-synced"
        else:
            overall = "behind"
        print(f"repo: {source} is at {sha[:12]}")
        print(f"status: {overall}")
        return 0

    if not a.force and all(v and v["commit"] == sha for v in versions.values()):
        print(f"lab guide: already current at {sha[:12]} ({source}); nothing changed")
        for t in tg:
            print(f"  {t}")
        return 0

    before = " / ".join(sorted({describe(v) for v in versions.values()}))
    with tempfile.TemporaryDirectory(prefix="novasmart-sync-") as tmp:
        staging = os.path.join(tmp, NAME)
        os.makedirs(staging)
        try:
            n = fetch(a.repo, sha, a.path, staging)
            check_whole(staging)
        except Exception as e:
            print(
                f"error: the download did not give a whole guide, so nothing changed ({e})"
            )
            print(f"The guide already on this machine keeps working: {before}.")
            return 1
        with open(os.path.join(staging, "VERSION"), "w", encoding="utf-8") as f:
            f.write(
                f"commit {sha}\nref {a.ref}\nsource https://github.com/{a.repo}/tree/{sha}/{a.path}\n"
            )
            f.write(f"synced {now()}\nfiles {n}\n")
        done = []
        for t in tg:
            try:
                install(staging, t)
                done.append(t)
            except OSError as e:
                print(f"error: could not replace {t} ({e}); that copy is unchanged")
    if not done:
        return 1
    print(f"lab guide: updated from {before} to {sha[:12]} ({source}), {n} files")
    for t in done:
        print(f"  {t}")
    print(
        "Start a new agy conversation now, so agy reads the updated guide, then continue with Step 1."
    )
    return 0 if len(done) == len(tg) else 1


if __name__ == "__main__":
    sys.exit(main())
