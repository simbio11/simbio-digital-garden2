import re

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "좌골결절", "견갑골", "후골간신경 마비", "전골간신경",
    "굴근지대", "횡돌기", "음부대퇴신경", "젖산",
    "항배강수수", "인게놀", "십조탕", "대황자충환",
    "방기황기탕", "신이산", "지실해백계지탕", "계지가후박행자탕"
]

lines = text.split('\n')
new_lines = []
removed_count = 0
removed_refs = 0

for line in lines:
    matched = False
    for item in resolved_items:
        # Match pattern: - `   9회` → [[item]]
        if f"[[{item}]]" in line:
            matched = True
            removed_count += 1
            m = re.search(r'`\s*(\d+)회`', line)
            if m:
                removed_refs += int(m.group(1))
            else:
                removed_refs += 9
            break
    if not matched:
        new_lines.append(line)

new_text = '\n'.join(new_lines)

# update title
new_text = new_text.replace('정제판 v15', '정제판 v16')

# update stats block:
# > [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** 2,741종 / 9,015회.
# > *(2026-09-04 배치 1~22차 누적 완료: 최상위 핵심 개념 154종 / 약 2,457회 참조 해결 반영)*
new_text = new_text.replace(
    '2,741종 / 9,015회',
    f'{2741 - removed_count:,}종 / {9015 - removed_refs:,}회'
)
new_text = new_text.replace(
    '배치 1~22차 누적 완료: 최상위 핵심 개념 154종 / 약 2,457회 참조 해결 반영',
    f'배치 1~26차 누적 완료: 최상위 핵심 개념 {154 + removed_count}종 / 약 {2457 + removed_refs:,}회 참조 해결 반영'
)

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"List updated: Removed {removed_count} items, {removed_refs} refs.")
