#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingest_vault.py — 마스터플랜 [x] 완료 노트 → 섹션 단위 청크화 → chunks.jsonl

실행:  python ingest_vault.py
출력:  data/chunks.jsonl (청크 메타 + 본문)

청크 규칙 (감초 노트 구조 기준):
  - '## ' 섹션 단위 분할, 앞의 '#' 제목 라인 + 본문을 한 청크로
  - 목차, mermaid/코드블록, 표, [[위키링크]]는 원문 보존 (검색 자산)
  - 각 청크에 source / doc_title / heading / char_count 메타 부여
"""
import json
import os
import re
import sys

VAULT = r"C:\Simbio"
MASTERPLAN = os.path.join(
    VAULT, "00. 봇 운영 시스템", "프로젝트", "AI 프로젝트",
    "Simbio_임상지식_고도화_마스터플랜.md",
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT_PATH = os.path.join(OUT_DIR, "chunks.jsonl")

# 마스터플랜에서 "[x] [[이름]]" 완료 항목 추출
def extract_done_notes(masterplan_path):
    with open(masterplan_path, encoding="utf-8") as f:
        text = f.read()
    names = re.findall(r"\[x\]\s*\[\[([^\]|]+)", text)
    # "A & B" 복수 링크 항목은 첫 링크만 취하되, 본초 폴더 매칭에서 처리
    return sorted(set(n.strip() for n in names))

def find_note_file(name):
    """볼트 전체에서 '{name}.md' 탐색 (첫 매칭 반환)"""
    for root, dirs, files in os.walk(VAULT):
        # .obsidian, .git 등 제외
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if f"{name}.md" in files:
            return os.path.join(root, f"{name}.md")
    return None

def split_sections(text):
    """## 섹션 단위로 분할. 파일 헤더(# 제목 + > 요약)는 section='(머리말)'으로."""
    lines = text.splitlines()
    sections = []
    cur = []
    cur_heading = "(머리말)"
    for ln in lines:
        if ln.startswith("## "):
            if cur:
                sections.append((cur_heading, "\n".join(cur).strip()))
            cur_heading = ln.strip()
            cur = []
        elif ln.startswith("# "):
            # 문서 타이틀은 머리말에 흡수
            cur.append(ln)
        else:
            cur.append(ln)
    if cur:
        sections.append((cur_heading, "\n".join(cur).strip()))
    return sections

def main():
    names = extract_done_notes(MASTERPLAN)
    print(f"[마스터플랜] [x] 완료 링크 {len(names)}개 추출")
    os.makedirs(OUT_DIR, exist_ok=True)

    chunks = []
    missing = []
    for name in names:
        path = find_note_file(name)
        if not path:
            missing.append(name)
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        rel = os.path.relpath(path, VAULT)
        secs = split_sections(text)
        n = 0
        for heading, body in secs:
            if len(body) < 40:  # 빈/파편 섹션 제외
                continue
            chunks.append({
                "id": f"{name}#{n}",
                "doc_title": name,
                "source": rel,
                "heading": heading,
                "char_count": len(body),
                "evidence_type": "vault_note",  # 비비 수급물과 합의한 근거 라벨 스키마
                "content": body,
            })
            n += 1
        print(f"  ✓ {name}: {n}청크 ({path})")

    if missing:
        print(f"[경고] 볼트에서 못 찾은 노트: {missing}")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    total_chars = sum(c["char_count"] for c in chunks)
    print(f"\n완료: {len(chunks)}청크 → {OUT_PATH} (총 {total_chars:,}자)")

if __name__ == "__main__":
    main()
