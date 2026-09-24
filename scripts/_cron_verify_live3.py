# -*- coding: utf-8 -*-
"""최종 라이브 검증 (커밋 e77995e9 반영 후).

미장 프리뷰 개편 포맷('🎴 테마 덱') 존재 + 옛 포맷('① 한눈 요약 표') 부재 확인 포함.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://simbio11.github.io/simbio-digital-garden2"
HDRS = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}
CB = str(int(time.time()))


def get(url, allow_404=False):
    req = urllib.request.Request(url, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        if allow_404:
            return e.code, b""
        raise


st, body = get(f"{BASE}/static/contentIndex.json?cb={CB}")
idx = json.loads(body.decode("utf-8"))
keys = list(idx.keys())
print(f"contentIndex HTTP {st} · 슬러그 {len(keys)}개")

checks = {
    "sarcopenia MOC": ["sarcopenia-muscle-wasting-disease/00_근감소증_moc", False],
    "sarcopenia 영양": ["sarcopenia-muscle-wasting-disease/13_part7-1_영양", False],
    "주식 브리핑 09-21": ["주식-브리핑/2026-09/w4/주식-브리핑-2026-09-21", False],
    "미장 프리뷰 09-21": ["미장-프리뷰-2026-09-21", False],
    "옛 근감소증 경로": ["독서/근감소증", True],
}
found = {}
for label, (frag, expect_gone) in checks.items():
    hits = [k for k in keys if frag in k.lower()]
    ok = (not hits) if expect_gone else bool(hits)
    print(f"  [index] {'OK ' if ok else 'FAIL'} {label} -> {hits[:1] if hits else '없음'}")
    if hits and not expect_gone:
        found[label] = hits[0]

# 미장 프리뷰 개편 포맷 확인
k = found.get("미장 프리뷰 09-21")
if k:
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    t = b.decode("utf-8", "ignore")
    new_fmt = t.count("🎴 테마 덱")
    old_fmt = t.count("① 한눈 요약 표")
    print(f"  [preview] HTTP {s} · {len(b)}B · '🎴 테마 덱' {new_fmt}회 · 옛 '① 한눈 요약 표' {old_fmt}회")

for label in ("sarcopenia MOC", "주식 브리핑 09-21"):
    k = found.get(label)
    if not k:
        continue
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    print(f"  [page] HTTP {s} · {len(b)}B · {label}")
