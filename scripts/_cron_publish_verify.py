# -*- coding: utf-8 -*-
"""라이브 스모크 테스트: 홈페이지 정상 + 비공개 경로 404 + contentIndex 로드.

본문 일치 검증은 `_cron_body_verify.py` 가 담당(문장 포함 방식).
사용: python scripts/_cron_publish_verify.py
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "https://simbio11.github.io/simbio-digital-garden2"
CB = "cb=2026092118"
HDRS = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def main():
    ok = True
    st, body = get(f"{BASE}/static/contentIndex.json?{CB}")
    idx = json.loads(body)
    print(f"[index] HTTP {st} · 슬러그 {len(idx)}")

    st, home = get(f"{BASE}/?{CB}")
    print(f"[home] HTTP {st} {len(home)}B")
    for probe in ["4. 임상", "임상례", "약리 공부", "문서"]:
        present = probe in home
        print(f"   home contains {probe!r}: {present}")
    if "4. 임상" in home or "임상례" in home:
        ok = False

    for path in ["4. 임상", "5. 독서, 노트/생각", "7. 첨부·자료/임상례", "6. 개발, 자산"]:
        try:
            st, _ = get(f"{BASE}/{urllib.parse.quote(path)}?{CB}")
            print(f"[probe] {path} → HTTP {st} (404 기대)")
            if st == 200:
                ok = False
        except urllib.error.HTTPError as e:
            print(f"[probe] {path} → HTTP {e.code}")

    print("RESULT:", "OK" if ok else "CHECK_NEEDED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
