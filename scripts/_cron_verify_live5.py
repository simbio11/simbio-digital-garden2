# -*- coding: utf-8 -*-
"""야간 신규 노트(우귀환·요골관 증후군·용혈성 빈혈) 라이브 반영 확인 — 커밋 d6e5071d."""
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
keys = list(json.loads(body.decode("utf-8")).keys())
print(f"contentIndex HTTP {st} · 슬러그 {len(keys)}개")

for label, frag in {
    "우귀환": "처방/02_보익제/우귀환",
    "요골관 증후군": "요골관-증후군",
    "용혈성 빈혈": "용혈성-빈혈",
    "약리 MOC": "2.-약리-공부/00_약리_공부_moc",
    "독서 MOC": "5.-독서,-노트/00_독서_노트_moc",
}.items():
    hits = [k for k in keys if frag in k.lower()]
    if not hits:
        print(f"  [index] MISS {label} ({frag})")
        continue
    k = hits[0]
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    print(f"  [page] HTTP {s} · {len(b)}B · {label} · {k[:60]}")
