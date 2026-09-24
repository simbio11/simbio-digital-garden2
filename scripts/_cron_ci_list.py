# -*- coding: utf-8 -*-
"""최근 GitHub Actions run 목록(상태/결론) 요약."""
import json
import urllib.request

REPO = "simbio11/simbio-digital-garden2"
HDRS = {"User-Agent": "davinci-cron", "Accept": "application/vnd.github+json"}


def main():
    url = f"https://api.github.com/repos/{REPO}/actions/runs?per_page=15"
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    for run in data.get("workflow_runs", []):
        print(
            f"{run['head_sha'][:8]} | {run['name'][:38]:38s} | {run['status']:10s} | "
            f"{str(run['conclusion']):9s} | created {run['created_at']} | started {run.get('run_started_at')}"
        )


main()
