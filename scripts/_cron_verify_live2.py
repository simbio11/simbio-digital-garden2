# -*- coding: utf-8 -*-
"""추가 라이브 검증: 약리성분 신규/갱신 노트 + 주식 브리핑 본문 + 홈 카드."""
import json
import re
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
print(f"슬러그 {len(keys)}개")

for frag in ("약리성분/베타시토스테롤", "약리성분/수소", "약리성분/센노사이드"):
    hits = [k for k in keys if frag in k]
    if not hits:
        print(f"  [index] MISS {frag}")
        continue
    k = hits[0]
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    txt = b.decode("utf-8", "ignore")
    links = txt.count('href="./')
    print(f"  [page] HTTP {s} · {len(b)}B · {k} · 상대링크 {links}개")

k = next(k for k in keys if k.lower().startswith("보고서/주식-브리핑/2026-09/w4/주식-브리핑-2026-09-21"))
s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
txt = b.decode("utf-8", "ignore")
for probe in ("매크로", "민감도", "관심종목", "S&P"):
    print(f"  [body] {probe}: {txt.count(probe)}회 · HTTP {s} · {len(b)}B")

s, h = get(f"{BASE}/?cb={CB}")
html = h.decode("utf-8", "ignore")
m = re.findall(r"([\d,]+)\s*(?:개의?\s*)?(?:문서|notes|Notes)", html)
cards = re.findall(r'href="\./([^"/]+)/?"', html)
print(f"  [home] HTTP {s} · 문서수 후보 {m[:3]} · 카드 href {sorted(set(cards))[:12]}")
