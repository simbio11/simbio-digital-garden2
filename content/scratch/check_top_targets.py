import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

vault_dir = r"c:\Simbio"

# 모든 마크다운 파일명(확장자 제외) 및 상대경로 매핑
all_notes = {}
for root, dirs, files in os.walk(vault_dir):
    if any(p in root for p in [".git", ".obsidian", ".smart-env", ".smtcmp", ".trash", "30_Sprint_Logs"]):
        continue
    for f in files:
        if f.endswith(".md"):
            name = f[:-3]
            rel = os.path.relpath(os.path.join(root, f), vault_dir)
            all_notes[name] = rel

targets = [
    "상한론", "태음인", "오공약침", "COX-2", "COX", "아교", "소양인", "두충", "대퇴골", "소음인",
    "햄스트링", "슬괵근", "열다한소탕", "루테올린", "FSH", "교이", "척추기립근", "기립근",
    "수근관 증후군", "수근관증후군", "손목터널증후군", "척골신경 마비", "척골신경",
    "소엽", "자소엽", "팔정산", "안면신경", "장경인대", "장경인대 증후군", "장경인대증후군",
    "척추측만증", "측만증", "봉약침", "봉독", "백복령", "복령", "5-LOX", "카탈폴", "파에오니플로린",
    "대맥"
]

print(f"Total existing notes scanned: {len(all_notes)}")
print("--- Target Search Results ---")
for t in targets:
    if t in all_notes:
        print(f"[FOUND] {t} -> {all_notes[t]}")
    else:
        # 부분 일치 검색
        matches = [k for k in all_notes if t in k or k in t]
        if matches:
            print(f"[PARTIAL] {t} -> maybe related to: {matches[:3]}")
        else:
            print(f"[NOT FOUND] {t}")
