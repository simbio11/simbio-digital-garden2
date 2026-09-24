import json, sys, urllib.request, urllib.parse

BASE = "https://simbio11.github.io/simbio-digital-garden2"
HDRS = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read()


def main():
    try:
        st, body = get(BASE + "/static/contentIndex.json?cb=2026092112")
        print("contentIndex HTTP", st, "bytes", len(body))
    except Exception as e:
        print("contentIndex FAIL", e)
        return
    idx = json.loads(body.decode("utf-8"))
    keys = list(idx.keys())
    print("contentIndex slugs:", len(keys))

    targets = ["인진사역탕", "이소쿠르쿠메놀", "인동등지골피탕"]
    for t in targets:
        hit = [k for k in keys if t in k]
        print(f"[index] {t}: {hit}")

    # 홈페이지
    try:
        st, html = get(BASE + "/?cb=2026092112")
        h = html.decode("utf-8", "ignore")
        print("home HTTP", st, "bytes", len(h))
        for probe in ["4. 임상", "임상례", "약리 공부", "문서"]:
            print(f"  home contains {probe!r}:", probe in h)
        import re
        m = re.findall(r"(\d[\d,]*)\s*개?\s*문서", h)
        print("  doc-count candidates:", m[:5])
    except Exception as e:
        print("home FAIL", e)

    # 신규 노트 라이브 프로브
    probes = []
    for t in targets:
        for k in keys:
            if t in k:
                probes.append(k)
                break
    for p in probes:
        url = BASE + "/" + urllib.parse.quote(p)
        try:
            st, body = get(url)
            print(f"[live] {st} ({len(body)}B) {p}")
        except urllib.error.HTTPError as e:
            print(f"[live] {e.code} {p}")
        except Exception as e:
            print(f"[live] ERR {e} {p}")

    # 오늘 보고서
    for t in ["주식-브리핑-2026-09-21", "부동산-브리핑-2026-09-21"]:
        hit = [k for k in keys if t in k]
        print(f"[index] {t}: {hit}")


main()
