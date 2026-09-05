import re

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "서경탕", "6-쇼가올", "다당류", "한다열소탕",
    "갈랑긴", "마트린", "백반", "과루해백백주탕",
    "하이페로사이드", "시니그린", "아르크티인", "생강피",
    "복령피", "오피음", "대진교탕", "통유탕"
]

lines = text.split('\n')
new_lines = []
removed_count = 0
removed_refs = 0

for line in lines:
    matched = False
    for item in resolved_items:
        if f"[[{item}]]" in line:
            matched = True
            removed_count += 1
            m = re.search(r'`\s*(\d+)회`', line)
            if m:
                removed_refs += int(m.group(1))
            else:
                removed_refs += 8
            break
    if not matched:
        new_lines.append(line)

new_text = '\n'.join(new_lines)

# update title
new_text = new_text.replace('정제판 v18', '정제판 v19')

# update stats block
# > [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** 2,694종 / 8,625회.
# > *(2026-09-04 배치 1~34차 누적 완료: 최상위 핵심 개념 201종 / 약 2,847회 참조 해결 반영)*
new_text = new_text.replace(
    '2,694종 / 8,625회',
    f'{2694 - removed_count:,}종 / {8625 - removed_refs:,}회'
)
new_text = new_text.replace(
    '배치 1~34차 누적 완료: 최상위 핵심 개념 201종 / 약 2,847회 참조 해결 반영',
    f'배치 1~38차 누적 완료: 최상위 핵심 개념 {201 + removed_count}종 / 약 {2847 + removed_refs:,}회 참조 해결 반영'
)

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"List updated: Removed {removed_count} items, {removed_refs} refs.")
