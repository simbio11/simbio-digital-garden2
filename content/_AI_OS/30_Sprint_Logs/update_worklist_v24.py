import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

resolved_items = [
    "골반 전방경사", "대퇴방형근신경", "거위발 점액낭염", "목신경고리",
    "망치족", "지근", "11β-HSD2", "TGF-β",
    "노토프테롤", "코릴라진", "결명자", "지황백호탕",
    "삼자양친탕", "살비아놀산 B", "호모시스테인", "도핵승기탕"
]

lines = text.split('\n')
new_lines = []
removed_count = 0
removed_refs = 0
removed_names = []

for line in lines:
    matched = False
    for item in resolved_items:
        if f"[[{item}]]" in line:
            matched = True
            removed_count += 1
            removed_names.append(item)
            m = re.search(r'`\s*(\d+)회`', line)
            if m:
                removed_refs += int(m.group(1))
            else:
                removed_refs += 7
            break
    if not matched:
        new_lines.append(line)

new_text = '\n'.join(new_lines)

# Find current numbers
m_stat1 = re.search(r'(\d[\d,]*)종\s*/\s*(\d[\d,]*)회', new_text)
if m_stat1:
    cur_species = int(m_stat1.group(1).replace(',', ''))
    cur_refs = int(m_stat1.group(2).replace(',', ''))
    new_species = cur_species - removed_count
    new_refs = cur_refs - removed_refs
    new_text = new_text.replace(m_stat1.group(0), f"{new_species:,}종 / {new_refs:,}회")

m_stat2 = re.search(r'최상위 핵심 개념\s*(\d[\d,]*)종\s*/\s*약\s*(\d[\d,]*)회', new_text)
if m_stat2:
    cur_done_species = int(m_stat2.group(1).replace(',', ''))
    cur_done_refs = int(m_stat2.group(2).replace(',', ''))
    new_done_species = cur_done_species + removed_count
    new_done_refs = cur_done_refs + removed_refs
    new_text = new_text.replace(m_stat2.group(0), f"최상위 핵심 개념 {new_done_species:,}종 / 약 {new_done_refs:,}회")

# update title version
new_text = new_text.replace('정제판 v23', '정제판 v24')

with open(list_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"Updated worklist v24: Removed {removed_count} items ({', '.join(removed_names)}), {removed_refs} refs.")
