#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_pilot.py — 청크 검색 데모 + 20문항 배치 평가 인터페이스

단일 검색:  python search_pilot.py "감초의 금기와 주의사항" --top 3
배치 평가:  python search_pilot.py --questions data/eval_20_questions.json --phase 1 --top 3
            (닥터허 평가셋: phase=1 → 현재 133청크로 즉시 측정, phase=2 → 재료 확장 후)

평가셋 JSON 스키마 (닥터허 규격, data/eval_20_questions.json):
{
  "id": "DH-EVAL-01", "phase": 1, "domain": "처방 감별", "difficulty": "하",
  "question": "...", "clinical_intent": "...",
  "expected_evidence_type": ["볼트노트"],
  "gold_docs": ["감초"],            // TOP3에 이 doc_title이 떠야 적중
  "gold_heading_kw": "금기|저칼륨", // (선택) 정밀검증 키워드
  "collect_keywords": null
}
적중 판정: TOP3 청크에 gold_docs 문서 포함(또는 answer_contains 본문 포함) → ✅
gold_heading_kw가 있으면 적중 문서 본문에서 키워드 포함 여부를 세컨더리 정밀검증으로 표시
expected_evidence_type은 evidence_type 라벨 적합 검사로 사용 (한글 라벨 → 코드 라벨 매핑)

※ 임베딩 계층(openai text-embedding-3-small) 연동 자리는 `embed()` 참고.
"""
import argparse
import collections
import json
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNKS = os.path.join(HERE, "data", "chunks.jsonl")

# 파일럿 통과 기준 (심비오트 판정 ④ + 닥터허 phase1 제안 10/12)
PASS_RATE = 0.80

# 평가셋 한글 라벨 → chunks.jsonl evidence_type 코드 매핑
LABEL_MAP = {
    "볼트노트": "vault_note", "볼트노트(예정)": "vault_note",
    "임상논문": "clinical", "임상": "clinical",
    "원전": "classic", "고전": "classic", "원전(예정)": "classic",
    "CPG": "cpg", "임상진료지침": "cpg",
}


def load_chunks(path=CHUNKS):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def label_of(c):
    return c.get("evidence_type", "vault_note")  # 아직 라벨 없는 기존 청크는 볼트노트


def vectorizer():
    return TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 3),       # 한국어 형태소 없이 자모 n-gram
        min_df=1,
        sublinear_tf=True,
    )


def build_index(chunks):
    """청크 말뭉치를 한 번만 TF-IDF 피팅 → (vectorizer, X)."""
    corpus = [c["content"] for c in chunks]
    tfidf = vectorizer()
    X = tfidf.fit_transform(corpus)
    return tfidf, X


def search_indexed(query, tfidf, X, chunks, top_k=3):
    q = tfidf.transform([query])
    sims = cosine_similarity(q, X).ravel()
    order = np.argsort(-sims)[:top_k]
    return [int(i) for i in order]


def search(query, chunks, top_k=3):
    """하위호환: 질문마다 피팅하던 구버전 검색. 배치는 build_index 버전을 쓴다."""
    tfidf, X = build_index(chunks)
    return [(i, float(cosine_similarity(tfidf.transform([query]), X).ravel()[i])) for i in search_indexed(query, tfidf, X, chunks, top_k)]


def _match_doc(top_chunks, names):
    """TOP3 청크 중 gold_docs/expected_docs 문서명과 매칭되는 첫 청크 반환."""
    for exp in names:
        exp = str(exp).strip()
        if not exp:
            continue
        for c in top_chunks:
            d = c["doc_title"]
            if exp == d or exp in d or d in exp:
                return c
    return None


def eval_hit(item, top_chunks):
    """한 문항 적중 판정.

    반환: (hit, reason, kw_ok)
      hit  — TOP3에 gold_docs 문서 포함 OR answer_contains 본문 포함
      kw_ok— gold_heading_kw 정밀검증 (해당 시 True/False, 없으면 None)
    """
    gold = _match_doc(top_chunks, item.get("gold_docs") or item.get("expected_docs") or [])
    needle = str(item.get("answer_contains") or "").strip()
    text_hit = None
    if needle:
        for c in top_chunks:
            if needle in c["content"]:
                text_hit = c
                break
    hit_chunk = gold or text_hit
    hit = hit_chunk is not None
    reason = ""
    if gold is not None:
        reason = f"출처적중: {gold['doc_title']}"
    elif text_hit is not None:
        reason = f"본문포함[{text_hit['doc_title']}]: {needle}"

    kw_ok = None
    kw = str(item.get("gold_heading_kw") or "").strip()
    if kw and hit_chunk is not None:
        pats = [p.strip() for p in kw.split("|") if p.strip()]
        kw_ok = any(p in hit_chunk["content"] for p in pats)
    return hit, reason, kw_ok


def run_batch(questions_path, top_k=3, phase=None):
    chunks = load_chunks()
    if not chunks:
        print("청크 없음: 먼저 python ingest_vault.py 실행")
        return 1
    with open(questions_path, encoding="utf-8") as f:
        data = json.load(f)
    questions = data if isinstance(data, list) else data.get("questions", data.get("items", []))
    if phase is not None:
        questions = [q for q in questions if q.get("phase") == phase]

    tfidf, X = build_index(chunks)
    label_dist = collections.Counter(label_of(c) for c in chunks)

    phase_tag = f"phase={phase} " if phase is not None else ""
    print(f"[배치 평가] {phase_tag}{len(questions)}문항 | top_k={top_k} | 청크풀 {len(chunks)}개")
    print("=" * 76)

    runnable, skipped = [], []
    for q in questions:
        has_gold = bool(q.get("gold_docs") or q.get("expected_docs") or q.get("answer_contains"))
        (runnable if has_gold else skipped).append(q)

    results = []
    for q in runnable:
        qtext = str(q.get("question") or q.get("q") or "").strip()
        if not qtext:
            skipped.append(q)
            continue
        qid = q.get("id") or q.get("qid") or "?"
        cat = q.get("category") or q.get("domain") or "-"
        diff = str(q.get("difficulty") or "")
        idxs = search_indexed(qtext, tfidf, X, chunks, top_k)
        top_chunks = [chunks[i] for i in idxs]
        hit, why, kw_ok = eval_hit(q, top_chunks)

        # 근거 라벨 적합 검사: TOP 청크 중 expected_evidence_type(매핑) 포함 여부
        exp_codes = [LABEL_MAP.get(str(x).strip(), str(x).strip())
                     for x in (q.get("expected_evidence_type") or []) if str(x).strip()]
        label_ok = True
        if exp_codes:
            label_ok = any(label_of(c) in exp_codes for c in top_chunks)
        results.append((qid, cat, diff, qtext, hit, why, kw_ok, label_ok, top_chunks))

    for qid, cat, diff, qtext, hit, why, kw_ok, label_ok, top_chunks in results:
        mark = "✅" if hit else "❌"
        kw_tag = "kw✅" if kw_ok else ("kw❌" if kw_ok is False else "kw-")
        lb_tag = "라벨✅" if label_ok else "라벨❌"
        print(f"{mark} #{qid} [{cat}|{diff}] {qtext[:38]}")
        print(f"    → {'적중: ' + why if hit else '미스'} | {kw_tag} {lb_tag}")
        if not hit:
            top_docs = " > ".join(f"{c['doc_title']}#{c['heading'][:18].strip('# ')}" for c in top_chunks)
            print(f"    TOP: {top_docs}")
    print("=" * 76)

    total = len(results)
    n_hit = sum(1 for r in results if r[4])
    rate = n_hit / total if total else 0.0
    # 정밀검증: gold_heading_kw가 있는 문항 중 kw 통과 비율
    kw_items = [(r[0], r[6]) for r in results if r[6] is not None]
    kw_hit = sum(1 for _, ok in kw_items if ok)
    label_bad = sum(1 for r in results if not r[7])

    print(f"[요약] 적중 {n_hit}/{total} ({rate:.1%}) | 통과 기준 ≥{PASS_RATE:.0%} → "
          + ("✅ 충족" if rate >= PASS_RATE else "⛔ 미달"))
    if total >= 12:
        print(f"    (닥터허 phase1 제안 10/12 ≈ 83.3% 기준: {'✅ 충족' if n_hit >= 10 else '⛔ 미달'})")
    by_dom = collections.defaultdict(lambda: [0, 0])
    for qid, cat, diff, qtext, hit, why, kw_ok, label_ok, _ in results:
        by_dom[cat][1] += 1
        by_dom[cat][0] += int(hit)
    for cat, (h, t) in by_dom.items():
        print(f"    [{cat}] {h}/{t}")
    if kw_items:
        print(f"[정밀검증] gold_heading_kw 키워드 포함 {kw_hit}/{len(kw_items)}")
    print(f"[근거 라벨] evidence_type 분포: " + ", ".join(f"{k}={v}" for k, v in label_dist.items()))
    print(f"    라벨 부적합(예상 라벨과 불일치) {label_bad}건"
          + (" → 혼동 0건 ✅" if label_bad == 0 else " ⛔"))
    if skipped:
        print(f"[스킵] gold_docs/answer_contains 없는 문항 {len(skipped)}개"
              f" — 재료 확장(phase 2) 후 측정 예정: "
              + ", ".join(str(q.get("id", "?")) for q in skipped))
    return 0 if rate >= PASS_RATE else 2


def embed(text):  # ← 임베딩 연동 자리 (파일럿 2단계에서 활성화)
    """openai API 연동 시: text-embedding-3-small, 차원 1536."""
    raise NotImplementedError("임베딩 계층은 config의 api_key 연동 후 활성화 예정")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default=None, help="검색 질문 (예: 감초의 금기)")
    ap.add_argument("--questions", default=None, help="배치 평가용 Q&A JSON 파일 경로")
    ap.add_argument("--phase", type=int, default=None, help="배치 평가 시 phase 필터 (1 또는 2)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--full", action="store_true", help="청크 전체 출력")
    args = ap.parse_args()

    if args.questions:
        raise SystemExit(run_batch(args.questions, top_k=args.top, phase=args.phase))
    if not args.query:
        ap.error("query 또는 --questions 중 하나는 필수")

    chunks = load_chunks()
    if not chunks:
        print("청크 없음: 먼저 python ingest_vault.py 실행")
        return
    print(f"[청크 풀] {len(chunks)}청크 로드\n")
    print(f"질문: {args.query}\n" + "-" * 60)
    tfidf, X = build_index(chunks)
    for rank, idx in enumerate(search_indexed(args.query, tfidf, X, chunks, args.top), 1):
        c = chunks[idx]
        print(f"\n■ TOP {rank}")
        print(f"  출처: {c['doc_title']}  |  {c['heading']}  |  {c['source']}")
        body = c["content"] if args.full else c["content"][:300]
        print(f"  {body[:600].replace(chr(10), ' ')}")


if __name__ == "__main__":
    main()
