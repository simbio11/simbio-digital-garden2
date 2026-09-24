# -*- coding: utf-8 -*-
"""AI 뉴스 리포트 임베드 이미지 실경로 프로브(페이지 URL 기준 상대경로 해석)."""
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
keys = list(json.loads(body.decode("utf-8")).keys())
slug = next(k for k in keys if "ai뉴스_리포트" in k.lower())
page_url = f"{BASE}/{urllib.parse.quote(slug)}?cb={CB}"
s, b = get(page_url)
t = b.decode("utf-8", "ignore")
srcs = re.findall(r'<img[^>]+src="([^"]+)"', t)
print(f"page HTTP {s} · {len(b)}B · {slug} · img {len(srcs)}개")
base_no_cb = f"{BASE}/{urllib.parse.quote(slug)}"
for src in srcs[:5]:
    absu = urllib.parse.urljoin(base_no_cb, src)
    absu = urllib.parse.quote(absu, safe=":/?&=@%") + f"?cb={CB}"
    try:
        s2, b2 = get(absu)
        print(f"  [img] HTTP {s2} · {len(b2)}B · {urllib.parse.unquote(absu)[:110]}")
    except urllib.error.HTTPError as e:
        print(f"  [img] HTTP {e.code} · {urllib.parse.unquote(absu)[:110]}")
