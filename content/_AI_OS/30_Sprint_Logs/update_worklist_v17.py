import re

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "탄산칼슘", "도홍사물탕", "소활락단", "육두구",
    "소계음자", "견정산", "택사탕", "아비쿨라린",
    "서각지황탕", "피페린", "호박산", "팔미틴",
    "금궤요략(金匱要略)", "자궁근종", "귤피", "복사근"
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
                removed_refs += 9
            break
    if not matched:
        new_lines.append(line)

new_text = '\n'.join(new_lines)

# update title
new_text = new_text.replace('정제판 v16', '정제판 v17')

# update stats block
# > [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** 2,726종 / 8,896회.
# > *(2026-09-04 배치 1~26차 누적 완료: 최상위 핵심 개념 169종 / 약 2,576회 참조 해결 반영)*
new_text = new_text.replace(
    '2,726종 / 8,896회',
    f'{2726 - removed_count:,}종 / {8896 - removed_refs:,}회'
)
new_text = new_text.replace(
    '배치 1~26차 누적 완료: 최상위 핵심 개념 169종 / 약 2,576회 참조 해결 반영',
    f'배치 1~30차 누적 완료: 최상위 핵심 개념 {169 + removed_count}종 / 약 {2576 + removed_refs:,}회 참조 해결 반영'
)

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"List updated: Removed {removed_count} items, {removed_refs} refs.")
