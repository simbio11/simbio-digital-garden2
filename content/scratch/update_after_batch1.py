import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

src_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md"

# 배치 1차에서 완결된 항목 집합
COMPLETED_BATCH_1 = {
    # Alias 통합 완료
    "햄스트링", "소엽", "백복령", "척추측만증", "척골신경 마비", "COX-2",
    # 신규 노트 생성 완료
    "상한론", "태음인", "소양인", "소음인", "오공약침", "아교", "두충", "교이", "봉약침",
    "열다한소탕", "팔정산", "대퇴골", "척추기립근", "수근관 증후군", "안면신경", "장경인대",
    "루테올린", "카탈폴", "5-LOX", "대맥"
}

items = []
pattern = re.compile(r"^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]")
with open(src_path, encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            items.append((int(m.group(1)), m.group(2)))

remaining = []
completed_count = 0
completed_refs = 0

for count, name in items:
    if name in COMPLETED_BATCH_1:
        completed_count += 1
        completed_refs += count
    else:
        remaining.append((count, name))

print(f"Original items: {len(items)}")
print(f"Completed in Batch 1: {completed_count} items ({completed_refs} references resolved)")
print(f"Remaining candidates: {len(remaining)}")

# 파일 갱신
new_lines = []
new_lines.append("---\n")
new_lines.append('title: "미노트화 링크 목록 (정제판 v5 - 배치 1차 완료 반영)"\n')
new_lines.append("type: worklist\n")
new_lines.append("owner: 다빈치\n")
new_lines.append("updated: 2026-09-04\n")
new_lines.append("---\n\n")

total_refs = sum(c for c, _ in remaining)
new_lines.append("# 🔗 미노트화 링크 — 생성 대기 개념 후보 (정제판 v5)\n\n")
new_lines.append(f"> [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** {len(remaining)}종 / {total_refs}회.\n")
new_lines.append(f"> *(2026-09-04 배치 1차 완료: 최상위 핵심 개념 {completed_count}종 / {completed_refs}회 참조 해결 반영)*\n\n")
new_lines.append("## 📊 참조 빈도\n")

for c, n in remaining:
    new_lines.append(f"- `{c:4d}회` → [[{n}]]\n")

with open(src_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Updated unnoted links list: {src_path}")
