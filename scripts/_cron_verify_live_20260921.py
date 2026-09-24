# -*- coding: utf-8 -*-
"""2026-09-21 23:00/23:03/23:14 sync 배포 후 라이브 검증 (슬러그 규칙 관대 매칭).

Quartz 슬러그 = 경로를 소문자화 + 공백을 '-'로. 따라서 조각 매칭은 하이픈 기준으로 한다.
사용: python scripts/_cron_verify_live_20260921.py
"""
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


def main():
    st, body = get(f"{BASE}/static/contentIndex.json?cb={CB}")
    idx = json.loads(body.decode("utf-8"))
    keys = list(idx.keys())
    print(f"contentIndex HTTP {st} · 슬러그 {len(keys)}개")

    def show(label, frags):
        hits = [k for k in keys if all(f in k.lower() for f in frags)]
        print(f"  [index] {'OK ' if hits else 'MISS'} {'+'.join(frags)} -> {hits[:3] if hits else '없음'}")
        return hits

    # 신규 게시 확인
    sarc = show("sarcopenia", ["sarcopenia"])
    show("영양", ["sarcopenia", "영양"])
    brf = show("주식브리핑", ["주식-브리핑", "09-21"])
    prev = show("미장프리뷰", ["미장-프리뷰", "09-21"])
    # 소거 확인(prune 된 옛 경로)
    gone = [k for k in keys if "독서/근감소증" in k.lower()]
    print(f"  [index] {'잔존!' if gone else 'OK(소거)'} 5.-독서,-노트/독서/근감소증 -> {gone[:3] if gone else '없음'}")

    for frag in (sarc[:1], brf[:1], prev[:1]):
        for k in frag:
            url = f"{BASE}/{urllib.parse.quote(k)}?cb={CB}"
            s, b = get(url)
            txt = b.decode("utf-8", "ignore")
            title = re.search(r"<title>(.*?)</title>", txt, re.S)
            print(f"  [page] HTTP {s} · {len(b)}B · {k[:60]} · title={title.group(1)[:40] if title else '?'}")

    old = urllib.parse.quote("5.-독서,-노트/독서/근감소증/00_근감소증_moc")
    s, _ = get(f"{BASE}/{old}?cb={CB}", allow_404=True)
    print(f"  [404] HTTP {s} (기대 404) · 옛 근감소증 경로")

    s, h = get(f"{BASE}/?cb={CB}")
    html = h.decode("utf-8", "ignore")
    docs = re.findall(r"([\d,]+)\s*개?\s*문서", html)
    cards = re.findall(r'class="card[^"]*"[^>]*>\s*<a[^>]*href="([^"]+)"', html)
    print(f"  [home] HTTP {s} · 문서수 후보 {docs[:3]} · 카드 {len(cards)}개 · 제목포함={'예' if '<title>' in html else '?'}")


main()
