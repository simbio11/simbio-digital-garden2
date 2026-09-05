import re

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "황련아교탕", "접골단", "오리엔틴", "나린긴",
    "시호소간산", "월국환", "글루타메이트", "비염",
    "키모트립신", "내늑간근", "진저롤", "필리린",
    "파이오놀", "내폐쇄근신경", "심부 둔부 증후군", "고관절 충돌증후군"
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
                removed_refs += 7
            break
    if not matched:
        new_lines.append(line)

new_text = '\n'.join(new_lines)

# update title
new_text = new_text.replace('정제판 v20', '정제판 v21')

# update stats block
# > [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** 2,662종 / 8,369회.
# > *(2026-09-04 배치 1~42차 누적 완료: 최상위 핵심 개념 233종 / 약 3,103회 참조 해결 반영)*
new_text = new_text.replace(
    '2,662종 / 8,369회',
    f'{2662 - removed_count:,}종 / {8369 - removed_refs:,}회'
)
new_text = new_text.replace(
    '배치 1~42차 누적 완료: 최상위 핵심 개념 233종 / 약 3,103회 참조 해결 반영',
    f'배치 1~46차 누적 완료: 최상위 핵심 개념 {233 + removed_count}종 / 약 {3103 + removed_refs:,}회 참조 해결 반영'
)

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"List updated: Removed {removed_count} items, {removed_refs} refs.")
