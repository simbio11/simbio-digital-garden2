#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluate.py — 20문항 평가셋 배치 실행 → 적중률 리포트

입력:  data/eval_questions.jsonl
  {"id": "Q01", "category": "처방감별", "question": "...", 
   "gold_doc": "감초", "gold_heading": "## 6. 핵심 처방 비교 매트릭스"}

채점 기준 (닥터허 gold answer = 볼트 노트/heading):
  - TOP1 적중  : gold_doc이 1순위 청크의 doc_title과 일치?
  - TOP3 적중  : gold_doc이 상위 3개 안에 존재?
  - heading 적중: TOP3 안에 gold_doc + gold_heading 둘 다 존재?

실행:  python evaluate.py                 # 기본 TOP3, 임계 0.8
       python evaluate.py --top 5 --threshold 0.7
"""
import argparse
import json
import os

from search_pilot import load_chunks, search

HERE = os.path.dirname(os.path.abspath(__file__))
QUESTIONS = os.path.join(HERE, "data", "eval_questions.jsonl")

def load_questions(path=QUESTIONS):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def norm_heading(h):
    """'## 6. 핵심 처방...' 에서 마커 제거, 공백 정규화 → 매칭용 키"""
    if not h:
        return ""
    return h.lstrip("#").strip().replace(" ", "")

def hit_heading(chunk, gold_doc, gold_heading):
    """gold_doc + gold_heading(부분일치 허용)이 청크에 있는가"""
    if chunk["doc_title"] != gold_doc:
        return False
    if not gold_heading:
        return True
    gh = norm_heading(gold_heading)
    ch = norm_heading(chunk.get("heading", ""))
    return (gh in ch) or (ch in gh) or (gh[:12] in ch)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=3, help="상위 N개로 적중 판정 (기본 3)")
    ap.add_argument("--threshold", type=float, default=0.8, help="TOP3 적중률 통과 기준 (기본 0.8)")
    args = ap.parse_args()

    questions = load_questions()
    chunks = load_chunks()
    if not questions:
        print(f"[경고] 평가셋 없음: {QUESTIONS}")
        return
    print(f"[평가셋] {len(questions)}문항 | [청크 풀] {len(chunks)}청크 | TOP{args.top} 판정\n")

    stats = {"top1": 0, "top3": 0, "heading": 0}
    by_cat = {}
    misses = []
    for q in questions:
        hits = search(q["question"], chunks, args.top)
        top_docs = [chunks[i]["doc_title"] for i, _ in hits]
        top1 = chunks[hits[0][0]]
        cat = q.get("category", "기타")

        t1 = top1["doc_title"] == q["gold_doc"]
        t3 = q["gold_doc"] in top_docs
        hd = any(hit_heading(chunks[i], q["gold_doc"], q.get("gold_heading", ""))
                 for i, _ in hits)

        stats["top1"] += t1
        stats["top3"] += t3
        stats["heading"] += hd
        by_cat.setdefault(cat, {"n": 0, "top3": 0, "heading": 0})
        by_cat[cat]["n"] += 1
        by_cat[cat]["top3"] += t3
        by_cat[cat]["heading"] += hd

        mark = "✅" if t3 else "❌"
        print(f"{mark} [{q['id']}] ({cat}) {q['question'][:44]}")
        print(f"    gold: {q['gold_doc']} / {q.get('gold_heading','')[:30]}")
        print(f"    TOP: {', '.join(top_docs[:3])}")
        if not t3:
            misses.append(q["id"])

    n = len(questions)
    print("\n" + "=" * 56)
    print(f"[리포트] TOP1 적중: {stats['top1']}/{n} ({stats['top1']/n:.0%})")
    print(f"[리포트] TOP{args.top} 적중: {stats['top3']}/{n} ({stats['top3']/n:.0%})"
          f"  ← 통과 기준 {args.threshold:.0%} {'✅ PASS' if stats['top3']/n >= args.threshold else '❌ FAIL'}")
    print(f"[리포트] heading 정확: {stats['heading']}/{n} ({stats['heading']/n:.0%})")
    print("-" * 56)
    for cat, s in by_cat.items():
        print(f"  {cat}: {s['top3']}/{s['n']} (TOP{args.top})")
    if misses:
        print(f"\n[미스] {', '.join(misses)} — 검색어 재설계 or 볼트 커버리지 확인 대상")

if __name__ == "__main__":
    main()
