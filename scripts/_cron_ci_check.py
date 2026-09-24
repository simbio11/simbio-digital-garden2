# -*- coding: utf-8 -*-
"""무인 크론용: 푸시한 커밋의 Pages 배포 워크플로 결론을 폴링.

사용: python scripts/_cron_ci_check.py <head_sha> [timeout_sec]
exit 0 = success, 2 = failure/cancelled, 1 = 아직 진행 중(timeout)
"""
import json
import sys
import time
import urllib.request

REPO = "simbio11/simbio-digital-garden2"
API = f"https://api.github.com/repos/{REPO}/actions/runs?per_page=30"
HDRS = {"User-Agent": "davinci-cron", "Accept": "application/vnd.github+json"}


def fetch():
    req = urllib.request.Request(API, headers=HDRS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    sha = sys.argv[1]
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 420
    deadline = time.time() + budget
    last = None
    while True:
        try:
            runs = fetch().get("workflow_runs", [])
        except Exception as e:
            print("API FAIL", e)
            return 1
        mine = [r for r in runs if r.get("head_sha") == sha]
        dep = [r for r in mine if "Pages" in (r.get("name") or "")]
        rows = [
            (r.get("name"), r.get("status"), r.get("conclusion"), r.get("created_at"))
            for r in (dep or mine)
        ]
        last = rows
        print(f"[{time.strftime('%H:%M:%S')}] runs for {sha[:8]}: {rows}")
        if dep:
            r = dep[0]
            if r.get("status") == "completed":
                c = r.get("conclusion")
                print("DEPLOY", c, r.get("html_url"))
                return 0 if c == "success" else 2
        elif mine and all(r.get("status") == "completed" for r in mine):
            print("완료된 run 중 'Pages' 워크플로 없음 → 판정 불가(워크플로 이름 확인 필요):", last)
            return 1
        if time.time() > deadline:
            print("TIMEOUT — 아직 진행 중:", last)
            return 1
        time.sleep(30)


if __name__ == "__main__":
    sys.exit(main())
