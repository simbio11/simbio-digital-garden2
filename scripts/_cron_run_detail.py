# -*- coding: utf-8 -*-
"""특정 커밋 SHA 의 Pages 배포 run 상세(잡/스텝 상태)를 출력.

사용: python scripts/_cron_run_detail.py <sha>
"""
import json
import sys
import urllib.request

REPO = "simbio11/simbio-digital-garden2"
HDRS = {"User-Agent": "davinci-cron", "Accept": "application/vnd.github+json"}


def api(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    sha = sys.argv[1]
    runs = api(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=30").get(
        "workflow_runs", []
    )
    mine = [r for r in runs if r.get("head_sha") == sha]
    if not mine:
        print("해당 SHA 의 run 없음")
        return
    for r in mine:
        if "Pages" not in (r.get("name") or ""):
            continue
        print(f"RUN {r['name']} id={r['id']} status={r['status']} concl={r['conclusion']}")
        print(f"  created={r['created_at']} started={r.get('run_started_at')} url={r['html_url']}")
        jobs = api(r["jobs_url"] + "?per_page=20").get("jobs", [])
        for j in jobs:
            print(f"  JOB {j['name']} status={j['status']} concl={j['conclusion']} started={j.get('started_at')}")
            for s in j.get("steps", []):
                if s.get("status") != "completed" or s.get("conclusion") not in ("success", "skipped"):
                    print(f"    STEP {s['number']:>2} {s['name'][:50]:50s} {s['status']} {s['conclusion']} {s.get('started_at')}")


main()
