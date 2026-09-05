#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공공데이터포털 API 클라이언트 (카이 제작)
- 맛집/상가: 소상공인시장진흥공단_상가(상권)정보_API (반경내 상가업소 조회)
- 부동산:   국토교통부_아파트 매매 실거래가 자료 (지역+월별 실거래가)

사용법:
  python 공공데이터_API_클라이언트.py 맛집   --lat 37.4979 --lon 127.0276 --radius 500 [--업종 Q] [--max 100]
  python 공공데이터_API_클라이언트.py 부동산 --code 11680 --ym 202606 [--max 100] [--top 10]

설정: 같은 폴더의 .env 파일에 SERVICE_KEY=발급받은키 입력 (없으면 환경변수 SERVICE_KEY)

업종 대분류 코드 예시 (음식=Q, 커피/카페 중분류=Q12, 부동산중개=A)
  - 전체 목록은 API의 '상권정보 업종 대분류/중분류/소분류 조회' 기능으로 확인 가능
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── API 엔드포인트 (정부 공식) ──────────────────────────────
SANGGA_BASE = "https://apis.data.go.kr/B553077/api/open/sdsc2"           # 상가(상권)정보
SANGGA_LIST_IN_AREA = SANGGA_BASE + "/storeListInRadius"                  # 반경내 상가업소 조회
BUDONGSAN_BASE = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade"    # 아파트 매매 실거래가
BUDONGSAN_TRADE = BUDONGSAN_BASE + "/getRTMSDataSvcAptTrade"


def get_service_key():
    """SERVICE_KEY를 .env 파일 → 환경변수 순서로 찾는다."""
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SERVICE_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return os.environ.get("SERVICE_KEY", "")


def api_get(url, params):
    """GET 요청 후 JSON 또는 XML 문자열 반환"""
    qs = urllib.parse.urlencode(params)
    full = f"{url}?{qs}"
    try:
        with urllib.request.urlopen(full, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.read().decode("utf-8", errors="replace")


def extract_error(text):
    """정부 API 공통 에러 형식 파싱"""
    try:
        obj = json.loads(text)
        hdr = obj.get("OpenAPI_ServiceResponse", {}).get("cmmMsgHeader", {})
        if hdr:
            return hdr.get("returnAuthMsg") or hdr.get("errMsg")
    except Exception:
        pass
    try:
        root = ET.fromstring(text)
        hdr = root.find(".//cmmMsgHeader")
        if hdr is not None:
            return (hdr.findtext("returnAuthMsg") or hdr.findtext("errMsg"))
    except Exception:
        pass
    return None


# ── 맛집/상가 ──────────────────────────────────────────────
def cmd_matzip(args):
    key = get_service_key()
    if not key:
        print("❌ SERVICE_KEY가 없습니다. .env 파일에 SERVICE_KEY=키 를 입력하세요.")
        sys.exit(1)
    params = {
        "serviceKey": key,
        "cx": args.lon,          # 경도
        "cy": args.lat,          # 위도
        "radius": args.radius,   # 반경(미터)
        "numOfRows": 1000,
        "pageNo": 1,
        "type": "json",
    }
    # ── 전체 수집 (업종 필터는 클라이언트에서 처리 — API 서버 필터는 엔드포인트별 제약 있음)
    all_items = []
    total = 0
    for page in range(1, 21):  # 최대 20페이지 (2만건 한도)
        params["pageNo"] = page
        raw = api_get(SANGGA_LIST_IN_AREA, params)
        err = extract_error(raw)
        if err:
            print(f"⚠️ API 에러: {err}")
            print("   → 키가 맞는지, 활용신청이 승인됐는지, URL이 올바른지 확인하세요.")
            sys.exit(1)
        try:
            data = json.loads(raw)
            body = data.get("body", {})
            items = body.get("items", []) or []
            total = body.get("totalCount", 0) or total
        except Exception:
            print("응답 해석 실패:", raw[:300])
            sys.exit(1)
        all_items.extend(items)
        if len(all_items) >= total or not items:
            break
        time.sleep(0.3)  # 정부 API 호출 간격
    items = all_items

    # ── 업종 필터 (코드 또는 이름 매칭)
    if args.업종:
        q = args.업종.upper()
        items = [i for i in items if (
            q in (i.get("indsLclsCd") or "").upper()
            or q in (i.get("indsMclsCd") or "").upper()
            or q in (i.get("indsSclsCd") or "").upper()
            or q in (i.get("indsLclsNm") or "")
            or q in (i.get("indsMclsNm") or "")
            or q in (i.get("indsSclsNm") or "")
        )]
        print(f"🎯 '{args.업종}' 필터 적용 → {len(items)}개")

    print(f"📊 총 {total}개 업소 중 {len(items)}개 표시 (반경 {args.radius}m)")
    # 업종별 집계
    from collections import Counter
    by_type = Counter(i.get("indsSclsNm") or i.get("indsMclsNm") or "기타" for i in items)
    print("— 업종 TOP 10 —")
    for name, cnt in by_type.most_common(10):
        print(f"  {name}: {cnt}개")
    print("— 목록 (첫 20개) —")
    for i in items[:20]:
        print(f"  {i.get('bizesNm', '?')} | {i.get('indsSclsNm', '?')} | {i.get('lnoAdr', i.get('rdnmAdr', ''))}")
    return items


# ── 부동산 실거래가 ────────────────────────────────────────
def cmd_budongsan(args):
    key = get_service_key()
    if not key:
        print("❌ SERVICE_KEY가 없습니다. .env 파일에 SERVICE_KEY=키 를 입력하세요.")
        sys.exit(1)
    params = {
        "serviceKey": key,
        "LAWD_CD": args.code,    # 법정동코드 앞 5자리 (예: 11680 강남구)
        "DEAL_YMD": args.ym,     # 계약년월 6자리 (예: 202606)
        "pageNo": 1,
        "numOfRows": args.max,
    }
    raw = api_get(BUDONGSAN_TRADE, params)
    err = extract_error(raw)
    if err:
        print(f"⚠️ API 에러: {err}")
        print("   → 키가 맞는지, 활용신청이 승인됐는지 확인하세요.")
        sys.exit(1)
    try:
        root = ET.fromstring(raw)
        body = root.find("body")
        items = []
        if body is not None:
            items_el = body.find("items")
            if items_el is not None:
                items = [ {c.tag: (c.text or "") for c in it} for it in items_el.findall("item") ]
        total_el = root.find(".//totalCount")
        total = int(total_el.text) if total_el is not None and total_el.text else len(items)
    except Exception:
        print("응답 해석 실패:", raw[:300])
        sys.exit(1)
    print(f"🏠 실거래 {total}건 중 {len(items)}건 표시 (지역코드 {args.code}, {args.ym})")
    for it in items[: (args.top or 20)]:
        amount = it.get("dealAmount", "?")
        area = it.get("excluUseAr", "?")
        pyeong = round(float(area) / 3.3058, 1) if area.replace(".", "", 1).isdigit() else "?"
        print(f"  {it.get('aptNm','?')} | {area}㎡({pyeong}평) | {it.get('floor','?')}층 | {amount}만원 | {it.get('umdNm','')}")
    return items


def main():
    p = argparse.ArgumentParser(description="공공데이터포털 API 클라이언트")
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("맛집", help="반경내 상가(맛집/카페 등) 조회")
    m.add_argument("--lat", type=float, required=True, help="위도 (예: 37.4979 강남역)")
    m.add_argument("--lon", type=float, required=True, help="경도 (예: 127.0276 강남역)")
    m.add_argument("--radius", type=int, default=500, help="반경 미터 (기본 500)")
    m.add_argument("--업종", default=None, help="업종 대분류 코드 (Q=음식, A=부동산중개 등)")
    m.add_argument("--max", type=int, default=100, help="최대 조회 건수 (기본 100, 최대 1000)")
    b = sub.add_parser("부동산", help="아파트 매매 실거래가 조회")
    b.add_argument("--code", required=True, help="법정동코드 앞5자리 (11680=강남구)")
    b.add_argument("--ym", required=True, help="계약년월 6자리 (202606)")
    b.add_argument("--max", type=int, default=100, help="최대 조회 건수")
    b.add_argument("--top", type=int, default=20, help="출력 개수")
    args = p.parse_args()
    if args.cmd == "맛집":
        cmd_matzip(args)
    elif args.cmd == "부동산":
        cmd_budongsan(args)


if __name__ == "__main__":
    main()
