import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

vault_dir = r"c:\Simbio"

# 모든 마크다운 파일명(확장자 제외) 및 상대경로 매핑
all_notes = {}
for root, dirs, files in os.walk(vault_dir):
    if any(p in root for p in [".git", ".obsidian", ".smart-env", ".smtcmp", ".trash", "30_Sprint_Logs", "scratch"]):
        continue
    for f in files:
        if f.endswith(".md"):
            name = f[:-3]
            rel = os.path.relpath(os.path.join(root, f), vault_dir)
            all_notes[name] = rel

batch2_candidates = [
    "FSH", "파에오니플로린", "페오니플로린", "루틴", "백강잠", "강잠", "양격산화탕", "클로로겐산",
    "교감신경", "상완골", "TRPA1", "토사자", "적복령", "복령", "글리시리진", "iNOS",
    "아밀라아제", "올레아놀산", "로즈마린산", "단백뇨", "경골", "GABA_A 수용체", "GABA",
    "TRPV1", "빈랑", "대복피", "퀘르세틴", "케르세틴", "신이", "신이화", "푸에라린", "형방패독산",
    "연하장애", "삼차신경", "갈비사이신경", "늑간신경", "거북목 증후군", "척골", "중수골", "Substance P"
]

print("--- Batch 2 Candidate Matching ---")
for t in batch2_candidates:
    if t in all_notes:
        print(f"[FOUND] {t} -> {all_notes[t]}")
    else:
        matches = [k for k in all_notes if t in k or k in t]
        if matches:
            print(f"[PARTIAL] {t} -> maybe related to: {matches[:3]}")
        else:
            print(f"[NOT FOUND] {t}")
