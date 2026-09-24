# -*- coding: utf-8 -*-
"""최종 검증: AI 뉴스 리포트·대시보드·주요 신규분 라이브 반영 확인 (커밋 6807c14f)."""
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
print(f"contentIndex HTTP {st} · 슬러그 {len(keys)}개")

targets = {
    "AI뉴스 리포트 09-21": "ai뉴스_리포트_2026-09-21",
    "주식 대시보드": "📊-주식-브리핑-대시보드",
    "sarcopenia MOC": "sarcopenia-muscle-wasting-disease/00_근감소증_moc",
    "미장 프리뷰 09-21": "미장-프리뷰-2026-09-21",
}
for label, frag in targets.items():
    hits = [k for k in keys if frag in k.lower()]
    if not hits:
        alt = [k for k in keys if "ai뉴스" in k.lower()][:3] if "AI뉴스" in label else []
        print(f"  [index] MISS {label} (대안 {alt})")
        continue
    k = hits[0]
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    t = b.decode("utf-8", "ignore")
    imgs = len(re.findall(r'<img[^>]+src="([^"]+)"', t))
    print(f"  [page] HTTP {s} · {len(b)}B · img {imgs}개 · {k[:70]}")

# AI 뉴스 이미지 한 장 실제 200 확인
imgs = [k for k in keys if "ai뉴스" in k.lower()]
if imgs:
    k = imgs[0]
    s, b = get(f"{BASE}/{urllib.parse.quote(k)}?cb={CB}")
    t = b.decode("utf-8", "ignore")
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', t)[:3]
    for src in srcs:
        base, _, path = src.partition("#")
        url = urllib.parse.urljoin(f"{BASE}/", urllib.parse.quote(base, safe="/:%?&=@")) + ("#" + path if path else "")
        try:
            s2, b2 = get(url)
            print(f"  [img] HTTP {s2} · {len(b2)}B · {src[:80]}")
        except urllib.error.HTTPError as e:
            print(f"  [img] HTTP {e.code} · {src[:80]}")

s, h = get(f"{BASE}/?cb={CB}")
print(f"  [home] HTTP {s} · {len(h)}B")
