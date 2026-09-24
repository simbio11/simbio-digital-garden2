# -*- coding: utf-8 -*-
"""2026-09-23 12:00 sync 배포 라이브 검증 (슬러그 정본 사용)."""
import json
import sys
import urllib.parse
import urllib.request

BASE = "https://simbio11.github.io/simbio-digital-garden2"
CB = "cb=2026092312b"
HDRS = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    req = urllib.request.Request(url, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""


def slug_of(path):
    return path.lower().replace(" ", "-")


def main():
    ok = True
    st, body = get(f"{BASE}/static/contentIndex.json?{CB}")
    if st != 200:
        print(f"[index] FAIL HTTP {st}")
        return 1
    idx = json.loads(body)
    keys = list(idx.keys())
    lows = {k.lower(): k for k in keys}
    print(f"[index] HTTP {st} slugs {len(keys)}")

    printed = set()
    for frag in ["브리핑-2026-09-23", "개원-리서치-2026-09-23", "부동산-브리핑"]:
        hits = [k for k in lows if frag in k]
        print(f"[search] {frag}: {hits[:5]}")
        printed.add(frag)

    live = [
        "1. 근골격계 공부/신경/천골신경얼기",
        "2. 약리 공부/처방/02_보익제/일관전",
        "3. 이론 공부/질환/부인과/자궁선근증",
        "보고서/부동산 브리핑-2026-09-23",
        "보고서/개원 리서치-2026-09-23",
        "보고서/주식 브리핑-2026-09-23",
        "보고서/2026-09-23-YouTube-Digest",
        "1. 근골격계 공부/이학적 검사/딕스-홀파이크 검사",
    ]
    for p in live:
        key = lows.get(slug_of(p))
        if not key:
            hits = [k for k in lows if slug_of(p).split("/")[-1] in k]
            key = hits[0] if hits else None
        code = 0
        if key:
            code, _ = get(f"{BASE}/{urllib.parse.quote(key)}?{CB}")
        print(f"[live] {p}\n        slug={key} HTTP={code}")
        if code != 200:
            ok = False

    ghosts = [
        "0. 기본의학 공부/04. 신경계 진찰·감별/딕스-홀파이크 검사",
        "보고서/AI 뉴스/AI뉴스_리포트_2026-09-21",
        "6. 개발, 자산",
    ]
    for g in ghosts:
        present = any(slug_of(g) == k for k in lows)
        if not present:
            present = any(slug_of(g) in k for k in lows)
        code, _ = get(f"{BASE}/{urllib.parse.quote(slug_of(g))}?{CB}")
        print(f"[ghost] {g}: inIndex={present} HTTP={code}")
        if code == 200:
            ok = False

    print("RESULT:", "OK" if ok else "CHECK")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
