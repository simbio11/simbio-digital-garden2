# -*- coding: utf-8 -*-
"""발행 본문 검증(관대 비교): 라이브 contentIndex 본문에 미러 문서의 특징 문장이 들어있는지 확인.

렌더링 과정에서 위키링크/URL/따옴표/엔티티가 바뀌므로 '문장 포함' 방식으로 판정한다.
사용: python scripts/_cron_body_verify.py "<content 기준 상대경로.md>" [...]
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE = "https://simbio11.github.io/simbio-digital-garden2"
CB = "cb=" + str(int(time.time()))
CONTENT = Path(r"C:\Users\cmksc\quartz\content")


def tidy(s: str) -> str:
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*`_#>\-]", "", s)
    s = s.replace('"', "").replace("“", "").replace("”", "").replace("·", "")
    s = s.replace("&amp;", "&")
    return re.sub(r"\s+", "", s)


def sample_lines(md: str, n=5):
    lines = [ln.strip() for ln in md.splitlines()]
    body = [ln for ln in lines if len(ln) > 45 and not ln.startswith(("|", "#", ">", "!", "```"))]
    if not body:
        return []
    step = max(1, len(body) // n)
    return body[::step][:n]


def main():
    req = urllib.request.Request(
        f"{BASE}/static/contentIndex.json?{CB}", headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        idx = json.loads(r.read().decode("utf-8"))
    lower = {k.lower(): k for k in idx}

    ok_all = True
    for rel in sys.argv[1:]:
        p = CONTENT / rel
        md = p.read_text(encoding="utf-8")
        body = md.split("---", 2)[-1] if md.startswith("---") else md
        # 슬러그: 미러 상대경로를 Quartz 슬러그 규칙(소문자, 콤마 유지)에 근사
        target = Path(rel)
        cands = [k for k in idx if k.lower().endswith("/" + target.stem.lower())]
        cands = [c for c in cands if target.parent.name.lower() in c.lower()]
        print(f"=== {rel}")
        if not cands:
            print("    !! 슬러그 없음")
            ok_all = False
            continue
        slug = cands[0]
        live = tidy(idx[slug].get("content", "") or "")
        mirror = tidy(body)
        ratio = len(live) / max(1, len(mirror))
        hits = [(ln[:60], tidy(ln)[:35] in live) for ln in sample_lines(body)]
        print(f"    slug={slug} 라이브 {len(live)}자 / 미러 {len(mirror)}자 (비율 {ratio:.2f})")
        for probe, hit in hits:
            print(f"    {'OK  ' if hit else 'MISS'} {probe!r}")
            if not hit:
                ok_all = False
    print("RESULT:", "OK" if ok_all else "CHECK_NEEDED")


main()
