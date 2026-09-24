#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_stock_dashboard.py — 📊 주식 브리핑 대시보드 자동 생성기 (2026-09-14 신설)

문제: 볼트 대시보드는 **Dataview** 쿼리로 목록을 만들지만, Quartz 사이트는
      Dataview 플러그인이 없어 쿼리가 **코드블록 그대로** 노출된다(사이트에서 미구현).

해결: 목록을 **정적 표**로 미리 구워 넣고(=옵시디언·사이트 양쪽에서 보임),
      실시간 자료는 ```custom-frames``` 블록으로 넣는다
      → 옵시디언은 Custom Frames 플러그인이, 사이트는 sync_obsidian.py 의
        convert_custom_frames() 가 <iframe> 으로 변환해 양쪽 모두 실시간으로 움직인다.

실행: python gen_stock_dashboard.py   (볼트의 대시보드 노트를 재생성)
  · 본문이 바뀌지 않으면 파일을 건드리지 않는다(불필요한 git 커밋 방지).
  · sync_obsidian.py 가 동기화 **직전**에 호출한다.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(r"C:\Simbio")
REPORT_DIR = VAULT / "_헤르메스" / "보고서" / "주식 브리핑"
OUT = REPORT_DIR / "📊 주식 브리핑 대시보드.md"
CHART_DIR = REPORT_DIR / "차트"
BACKUP_DIR = Path(r"C:\Users\cmksc\AppData\Local\hermes\profiles\vivi\cache")

WIDGET_FRAMES_CANDIDATES = [
    Path(r"C:\Users\cmksc\quartz\scripts\widget_frames.json"),
    Path(__file__).resolve().parent / "widget_frames.json",
]

# ── 실시간 위젯 구성 (프레임명은 widget_spec.py / make_widget_frames.py 와 일치해야 함) ──
LIVE_TOP = [
    ("티커 테이프", 110, "핵심 8지표 한 줄 요약 — S&P500 · 나스닥100 · WTI · VIX선물 · 원/달러 · 반도체 · NVDA · AAPL"),
    ("시장 개요", 640, "①지수 ②금리·환율·변동성 ③원자재·대안 ④관심종목 — 4탭 (탭을 눌러 전환)"),
    ("📊 TV히트맵(실시간)", 560, "S&P500 섹터 히트맵 — 오늘 자금이 어디로 도는지 한눈에 (정규장 기준 · 3분 자동 갱신)"),
]

TV_CHARTS = [
    ("TV차트 S&P500", "🇺🇸 S&P 500", "미국 대형주 전체 방향"),
    ("TV차트 나스닥100", "🇺🇸 나스닥 100", "성장주·빅테크 방향 (QLD 의 기초자산)"),
    ("TV차트 VIX", "😱 VIX (공포지수)", "20 상회 = 위험 구간 (If-Then 4번 트리거)"),
    ("TV차트 미10년물", "🏛️ 미국 10년물", "5.00% 돌파 = 성장주 압박 (If-Then 1번 트리거)"),
    ("TV차트 미2년물", "🏛️ 미국 2년물", "FOMC 정책금리 기대를 가장 먼저 반영"),
    ("TV차트 코스피", "🇰🇷 코스피", "6,800선 이탈 = 국내 분할매수 조건 (If-Then 2번 트리거)"),
]

TICKER_CHARTS = [
    ("차트 QQQ", "QQQ", "나스닥100 ETF"),
    ("차트 QLD", "QLD", "나스닥100 2배 레버리지 — 내 포트 핵심"),
    ("차트 NVDA", "NVDA", "AI 반도체 대장"),
    ("차트 AAPL", "AAPL", "관심종목 1개월 1위"),
    ("차트 AVGO", "AVGO", "커스텀 실리콘·네트워킹"),
    ("차트 MU", "MU", "HBM·메모리 사이클"),
    ("차트 SOXX", "SOXX", "반도체 섹터 ETF"),
    ("차트 RKLB", "RKLB", "우주테크 테마"),
]

MAX_LIST = 40          # 목록에 싣는 최대 개수
# 🌙 데이마켓(주간거래·오버나잇) 섹션에 차트로 넣을 종목 (프레임 `🌙데이마켓 <티커>` = TradingView 심볼 페이지)
DAYMARKET = ["NVDA", "QQQ", "QLD", "AVGO"]
MAX_ARCHIVE = 8        # 차트 아카이브 PNG 개수
TS_RE = re.compile(r"(마지막 생성|데이터 기준):")


# ────────────────────────────── helpers ──────────────────────────────
def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").lstrip("\ufeff")
    except Exception:
        return ""


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    fm = m.group(1) if m else ""
    out = {}
    for line in fm.splitlines():
        mm = re.match(r"^([A-Za-z가-힣]+)\s*:\s*(.+?)\s*$", line)
        if mm:
            out[mm.group(1)] = mm.group(2).strip()
    return out


def section(text: str, prefix: str) -> str:
    """'## <prefix>...' 섹션의 본문(다음 ## 전까지)을 돌려준다."""
    m = re.search(r"^##\s*" + re.escape(prefix) + r"[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def tables(md: str) -> list[str]:
    """본문에서 마크다운 표 블록들을 추출."""
    out, cur = [], []
    for line in md.splitlines():
        if line.strip().startswith("|"):
            cur.append(line.rstrip())
        else:
            if len(cur) >= 2:
                out.append("\n".join(cur))
            cur = []
    if len(cur) >= 2:
        out.append("\n".join(cur))
    return out


def quote_block(md: str) -> str:
    """첫 번째 > 인용 블록(연속된 '>' 줄)을 추출."""
    lines = md.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(">")), None)
    if start is None:
        return ""
    buf = []
    for line in lines[start:]:
        if line.startswith(">"):
            buf.append(line.rstrip())
        elif not line.strip():
            # 인용 블록 안의 빈 줄은 블록 종료로 본다(브리핑 형식상 표 뒤 빈 줄)
            break
        else:
            break
    return "\n".join(buf)


def clean_section(md: str) -> str:
    """섹션 꼬리의 구분선·빈 줄 정리."""
    return re.sub(r"\n-{3,}\s*$", "", md.strip()).strip()


def fence(name: str, height: int, note: str = "") -> str:
    body = f"frame: {name}\nstyle: height: {height}px; border: 0;"
    block = "```custom-frames\n" + body + "\n```"
    return (f"{note}\n\n{block}" if note else block)


def link_for(path: Path, label: str) -> str:
    return f"[[{path.stem}|{label}]]"


def cell_link(path: Path, label: str) -> str:
    """표(테이블) 안에 넣는 위키링크.

    ⚠️ 2026-09-14 실측: 표 안에서 `[[파일|별칭]]` 을 그대로 쓰면 **파이프가 칸 구분자로
    먹혀서** 행이 쪼개진다(사이트 실측: 한 행이 `[[주식 브리핑-2026-09-14` /
    `2026-09-14]]` / `월요일` 3칸으로 깨짐 — 위치 칸이 사라짐).
    → 표 안에서는 반드시 파이프를 **역슬래시로 이스케이프**한다(옵시디언·쿼츠 공통 해법).
    → 별칭 안에 `**굵게**` 를 넣으면 쿼츠가 별표를 그대로 노출하므로 **평문 라벨**만 쓴다.
    검증: 렌더 후 셀 3개 + <a> 태그 확인(public_t6 테스트).
    """
    return f"[[{path.stem}\\|{label}]]"


def rel_folder(path: Path) -> str:
    try:
        return path.parent.relative_to(REPORT_DIR).as_posix()
    except Exception:
        return ""


# ────────────────────────────── scans ──────────────────────────────
def collect(pattern: str, exclude_dirs=("주간 요약", "차트", "대시보드")) -> list[Path]:
    files = []
    for p in REPORT_DIR.rglob(pattern):
        if any(d in p.parts for d in exclude_dirs):
            continue
        files.append(p)
    return sorted(files, key=lambda p: p.name, reverse=True)


def date_of(path: Path, fm: dict) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    if m:
        return m.group(1)
    d = fm.get("날짜", "")
    return d


def weekly_files() -> list[Path]:
    wdir = REPORT_DIR / "주간 요약"
    if not wdir.exists():
        return []
    return sorted(wdir.rglob("*.md"), key=lambda p: (p.parent.name, p.name), reverse=True)


def chart_files() -> list[Path]:
    if not CHART_DIR.exists():
        return []
    pngs = [p for p in CHART_DIR.glob("*.png")]
    pngs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return pngs[:MAX_ARCHIVE]


def available_frames() -> set[str] | None:
    for f in WIDGET_FRAMES_CANDIDATES:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            frames = data.get("frames", data) if isinstance(data, dict) else {}
            if frames:
                return set(frames.keys())
        except Exception:
            continue
    return None


def frame_label(name: str) -> str:
    return {
        "TV차트 코스피": "🇰🇷 코스피 — TradingView 원본 차트",
    }.get(name, "")


# ────────────────────────────── build ──────────────────────────────
def build() -> str:
    now = datetime.now()

    briefings = collect("주식 브리핑-*.md")
    previews = collect("미장 프리뷰-*.md")
    weekly = weekly_files()

    avail = available_frames()

    def ok(name: str) -> bool:
        return avail is None or name in avail

    P: list[str] = []
    A = P.append

    A("---")
    A(f"날짜: {now:%Y-%m-%d}")
    A("태그:")
    A("  - 대시보드")
    A("  - 주식브리핑")
    A("---")
    A("")
    A("# 📊 주식 브리핑 대시보드")
    A("")
    A("> [!info] 자동 생성 페이지")
    A("> 이 대시보드는 **동기화 때마다 자동 재생성**됩니다. 사이트(Quartz)는 Dataview 플러그인이 없어서,")
    A("> 목록은 **정적 표**로 미리 구워 두었습니다 — 옵시디언과 사이트 양쪽에서 똑같이 보여요.")
    A("> 실시간 시세·차트는 **실시간 위젯**으로 들어가 있고, 옵시디언=Custom Frames / 사이트=iframe 으로 자동 변환됩니다.")
    # 생성 시각을 쓰지 않는다(내용이 그대로면 파일도 그대로 — 불필요한 커밋·재동기화 방지).
    # 대신 '무엇을 반영했는지'를 적어 내용 기반으로만 바뀌게 한다.
    if briefings:
        _lf = frontmatter(read(briefings[0]))
        _ld = date_of(briefings[0], _lf)
        _pdates = [date_of(p, frontmatter(read(p))) for p in previews[:1]]
        _vd = _pdates[0] if _pdates else "—"
    else:
        _ld, _vd = "—", "—"
    A(f"> 데이터 기준: 최신 브리핑 **{_ld}** · 최신 프리뷰 **{_vd}** ｜ "
      f"브리핑 **{len(briefings)}**건 · 미장 프리뷰 **{len(previews)}**건 · 주간 요약 **{len(weekly)}**건")
    A("")
    A("**바로가기** — [📈 실시간 시장](#-실시간-시장-지금-움직이는-값) · "
      "[🕯️ 실시간 차트뷰](#-실시간-차트뷰) · "
      "[🔥 최신 브리핑 스냅샷](#-최신-브리핑-스냅샷) · "
      "[📄 지난 브리핑 목록](#-최근-브리핑) · "
      "[🖼️ 차트 아카이브](#-차트-아카이브)")
    A("")
    A("---")
    A("")

    # ── 1. 실시간 시장 ────────────────────────────────────────────
    A("## 📈 실시간 시장 (지금 움직이는 값)")
    A("")
    A("> [!tip] 옵시디언에서 위젯이 안 보이면")
    A("> 설정 → 커뮤니티 플러그인 → **Custom Frames** 를 껐다 켜 주세요. (iframes 로딩에 20~30초 걸립니다)")
    A("")
    for name, h, note in LIVE_TOP:
        if not ok(name):
            continue
        A(f"**{note}**")
        A("")
        A(fence(name, h))
        A("")
    A("---")
    A("")

    # ── 2. 실시간 차트뷰 ──────────────────────────────────────────
    A("## 🕯️ 실시간 차트뷰")
    A("")
    A("### 🏛️ 지수 · 금리 · 변동성 — 내 If-Then 트리거가 걸린 6개 차트")
    A("")
    for name, title, note in TV_CHARTS:
        if not ok(name):
            continue
        A(f"#### {title}")
        A("")
        A(f"*{note}*")
        A("")
        if name == "TV차트 코스피":
            A("> [!info] 코스피는 TradingView 임베드가 값을 제공하지 않는 심볼이라 "
              "👉 [**TradingView에서 실시간으로 보기**](https://www.tradingview.com/symbols/KRX-KOSPI/) 로 연결합니다.")
            A("")
            continue
        A(fence(name, 460))
        A("")
    A("")
    A("> [!tip] 🌙 데이마켓(주간거래·오버나잇) 값 읽는 법")
    A("> 미국 정규장이 닫혀 있어도 **데이마켓(주간거래)** 은 계속 거래됩니다 — 각 차트 오른쪽 "
      "**`오버나잇` 태그가 지금 데이마켓 가격**입니다(같은 자리의 `종` 값 = 정규장 종가).")
    A("> **데이마켓 등락률 = 오버나잇 값 ÷ 정규장 종 값 − 1** — 예) 오버나잇 152.00 ÷ 종 150.00 = +1.33%.")
    A("> ⚠️ 티커 테이프·시장 개요의 큰 % 숫자는 **정규장 종가 대비**라 데이마켓 등락률이 아닙니다 "
      "(미국 정규장 개장 22:30 KST 전에는 갱신되지 않음).")
    A("> ✅ **오버나잇 가격과 등락률을 한 화면에서** 보려면 → 옵시디언의 `🌙데이마켓 <티커>` 프레임 "
      "(TradingView 심볼 페이지 · \"212.26 USD +1.21 +0.57% · Overnight via BOATS\"). "
      "사이트에서는 페이지 임베드가 차단되어 5분봉 차트로 대체됩니다.")
    A("> ※ 데이마켓 시세를 무료로 내려주는 API가 없어(TradingView 스캐너·Yahoo·Nasdaq 확장세션은 20:00 ET까지) "
      "**자동 % 계산은 불가** — TradingView 화면이 유일한 실시간 소스입니다.")
    A("")
    A("### 🌙 데이마켓(주간거래·오버나잇) 실시간")
    A("")
    A("| 종목 | 차트에서 볼 것 |")
    A("|---|---|")
    for _t in DAYMARKET:
        A(f"| **{_t}** | 정규장 종(`종`) · **지금 데이마켓 가격(`오버나잇`)** · 연장세션 거래량 |")
    A("")
    for _t in DAYMARKET:
        _name = f"🌙데이마켓 {_t}"
        if not ok(_name):
            continue
        A(f"#### 🌙 {_t}")
        A("")
        A(fence(_name, 420))
        A("")
    A("")
    A("### ⭐ 관심종목 실시간 캔들 차트 (일봉)")
    A("")
    A("| 종목 | 무엇을 보나 |")
    A("|---|---|")
    for name, ticker, note in TICKER_CHARTS:
        A(f"| **{ticker}** | {note} |")
    A("")
    for name, ticker, _ in TICKER_CHARTS:
        if not ok(name):
            continue
        A(f"#### {ticker}")
        A("")
        A(fence(name, 420))
        A("")
    A("---")
    A("")

    # ── 3. 최신 브리핑 스냅샷 ─────────────────────────────────────
    if briefings:
        latest = briefings[0]
        text = read(latest)
        lfm = frontmatter(text)
        ldate = date_of(latest, lfm) or latest.stem
        lweek = lfm.get("요일", "")
        A(f"## 🔥 최신 브리핑 스냅샷 — {ldate} {lweek}".rstrip())
        A("")
        A(f"> 원문 전체: {link_for(latest, f'📈 주식 브리핑-{ldate}')} (위치 `{rel_folder(latest)}`)")
        A("")

        one = quote_block(text)
        if one:
            # 콜아웃 자체에 '☀️ 오늘의 한 줄' 제목이 있으므로 별도 헤딩은 두지 않는다
            A(one)
            A("")

        ifthen = clean_section(section(text, "🔫"))
        if ifthen:
            A("### 🔫 조건부 액션 플랜 (If-Then)")
            A("")
            A(ifthen)
            A("")

        mkt = clean_section(section(text, "📊 시장 지표"))
        mkt_tables = tables(mkt)
        if mkt_tables:
            A("### 📊 시장 지표")
            A("")
            first_tbl = mkt_tables[0]
            pre = mkt.split(first_tbl)[0].strip()
            if pre:
                A(pre)
                A("")
            A(first_tbl)
            A("")

        watch = section(text, "⭐ 관심 종목")
        w_tables = tables(watch)
        if w_tables:
            A("### ⭐ 관심 종목 (내 포트폴리오)")
            A("")
            A(w_tables[0])
            A("")
        A("---")
        A("")

    # ── 4. 목록 (Dataview 대체) ───────────────────────────────────
    A("## 📄 최근 브리핑")
    A("")
    A(f"총 **{len(briefings)}**건" + (f" · 최신 {MAX_LIST}건 표시" if len(briefings) > MAX_LIST else "")
      + " — 사이트에서는 Dataview 대신 이 표가 목록을 대신합니다")
    A("")
    A("| 날짜 | 요일 | 위치 |")
    A("|:---:|:---:|:---:|")
    for p in briefings[:MAX_LIST]:
        pf = frontmatter(read(p))
        d = date_of(p, pf)
        A(f"| {cell_link(p, d)} | {pf.get('요일', '—')} | `{rel_folder(p)}` |")
    A("")

    A("## 🌙 최근 미장 프리뷰")
    A("")
    A(f"총 **{len(previews)}**건" + (f" · 최신 {MAX_LIST}건 표시" if len(previews) > MAX_LIST else ""))
    A("")
    A("| 날짜 | 요일 | 위치 |")
    A("|:---:|:---:|:---:|")
    for p in previews[:MAX_LIST]:
        pf = frontmatter(read(p))
        d = date_of(p, pf)
        A(f"| {cell_link(p, d)} | {pf.get('요일', '—')} | `{rel_folder(p)}` |")
    A("")

    # 월별·주차별 구조
    A("## 📁 월별 · 주차별 구조")
    A("")
    groups: dict[str, list[Path]] = {}
    for p in briefings + previews:
        groups.setdefault(rel_folder(p), []).append(p)
    A("| 위치 | 브리핑 | 미장 프리뷰 |")
    A("|:---:|:---:|:---:|")
    for folder in sorted(groups.keys()):
        files = groups[folder]
        b = [p for p in files if p.name.startswith("주식 브리핑")]
        v = [p for p in files if p.name.startswith("미장 프리뷰")]
        bl = ", ".join(cell_link(p, date_of(p, frontmatter(read(p))) or p.stem) for p in sorted(b, reverse=True))
        vl = ", ".join(cell_link(p, date_of(p, frontmatter(read(p))) or p.stem) for p in sorted(v, reverse=True))
        A(f"| `{folder}` | {bl or '—'} | {vl or '—'} |")
    A("")

    A("## 📅 주간 요약 (주차별)")
    A("")
    A("| 회차 | 월 |")
    A("|:---:|:---:|")
    for p in weekly[:MAX_LIST]:
        A(f"| {cell_link(p, p.stem)} | `{p.parent.name}` |")
    A("")
    A("> 📁 저장: `주식 브리핑/주간 요약/<YYYY-MM>/<N>주차_주식·매크로_주간_요약.md` "
      "(주차는 **매월 1주차부터 다시 시작** → 월 폴더로 구분)")
    A("")
    A("---")
    A("")

    # ── 5. 차트 아카이브 ──────────────────────────────────────────
    charts = chart_files()
    if charts:
        A("## 🖼️ 차트 아카이브")
        A("")
        A("> 실시간 위젯은 **지금**을 보여주고, 여기 PNG는 **그날의 기록**입니다 "
          "(드라이브 공유·아카이브용). 최신 8장.")
        A("")
        for p in charts:
            A(f"**{p.stem}**")
            A("")
            A(f"![[{p.name}|700]]")
            A("")
        A("---")
        A("")

    # ── 6. 시스템 안내 ────────────────────────────────────────────
    A("## 📌 브리핑 시스템 안내")
    A("")
    A("| 시각 | 작업 | 산출물 |")
    A("|:---:|---|---|")
    A("| **평일 09:00** | 주식 브리핑 (전일 미장 리뷰 + 오늘 국장 프리뷰) | `주식 브리핑-YYYY-MM-DD.md` |")
    A("| **평일 22:30** | 미장 프리뷰 (오늘 밤 미국장 관전 포인트) | `미장 프리뷰-YYYY-MM-DD.md` |")
    A("")
    A("- **📁 저장**: `_헤르메스/보고서/주식 브리핑/<YYYY-MM>/<W#>/` (W# = 월요일 시작 주차, 매월 1주차부터)")
    A("- **📚 출처**: SAVE 리포트 · 오선의 미국 증시 라이브 · insidertracking·KimchiTerminal(텔레그램) · "
      "Yahoo Finance · FRED · 한국은행 ECOS · 관세청 · SEC EDGAR · DART · Finviz")
    A("- **⭐ 관심 종목**: QLD · QQQ · TQQQ · TIGER 미국나스닥100 · NVDA · AVGO · AAPL · 반도체(SOXX·MU) · "
      "우주테크(RKLB·ASTS) · 양자(IONQ) · SGOV")
    A("- **🧭 위젯 지표 정의**: `scripts/widget_spec.py` 한 곳에서 관리 — 지표를 바꾸면 브리핑·프리뷰·패널·대시보드에 동시 반영")
    A("")

    return "\n".join(P).rstrip() + "\n"


def main() -> int:
    if not REPORT_DIR.exists():
        print(f"[gen_stock_dashboard] 보고서 폴더 없음: {REPORT_DIR}")
        return 1

    new = build()

    old = read(OUT)
    if old:
        # 타임스탬프 줄만 다른 경우는 '변경 없음'으로 본다(불필요한 커밋 방지)
        norm = lambda t: "\n".join(l for l in t.splitlines() if not TS_RE.search(l)).strip()
        if norm(old) == norm(new):
            print("[gen_stock_dashboard] 변경 없음 — 그대로 둡니다")
            return 0
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(OUT, BACKUP_DIR / "📊 주식 브리핑 대시보드.md.bak")
        except Exception:
            pass

    OUT.write_text(new, encoding="utf-8", newline="\n")
    blocks = new.count("```custom-frames")
    print(f"[gen_stock_dashboard] 생성 완료 → {OUT.name} ({len(new):,}자 · 실시간 위젯 {blocks}개)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
