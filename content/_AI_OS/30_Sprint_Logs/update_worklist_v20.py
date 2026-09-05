import re

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "브루신", "시트르산", "오매", "TRPM8",
    "NO", "생강즙", "백두옹탕", "베타-엘레멘",
    "화적환", "사묘환", "모루신", "경미",
    "우황", "천화분", "제니포사이드", "궁귀교애탕"
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
new_text = new_text.replace('정제판 v19', '정제판 v20')

# update stats block
# > [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** 2,678종 / 8,497회.
# > *(2026-09-04 배치 1~38차 누적 완료: 최상위 핵심 개념 217종 / 약 2,975회 참조 해결 반영)*
new_text = new_text.replace(
    '2,678종 / 8,497회',
    f'{2678 - removed_count:,}종 / {8497 - removed_refs:,}회'
)
new_text = new_text.replace(
    '배치 1~38차 누적 완료: 최상위 핵심 개념 217종 / 약 2,975회 참조 해결 반영',
    f'배치 1~42차 누적 완료: 최상위 핵심 개념 {217 + removed_count}종 / 약 {2975 + removed_refs:,}회 참조 해결 반영'
)

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"List updated: Removed {removed_count} items, {removed_refs} refs.")
