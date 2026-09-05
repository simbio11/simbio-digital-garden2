import os, re

vault_root = r'c:\Simbio'
notes_dir = os.path.join(vault_root, '1. 근골격계 공부', '근막경선')

# Collect all muscle/note names across the entire vault
all_note_names = set()
for root, dirs, files in os.walk(vault_root):
    # skip hidden/system dirs
    if any(part.startswith('.') or part.startswith('_') for part in root.split(os.sep)):
        continue
    for f in files:
        if f.endswith('.md'):
            name = f[:-3]
            # filter out numbered prefixes like "00_MOC", "1_SBL"
            clean_name = re.sub(r'^\d+[\s_-]*', '', name).strip()
            if clean_name and len(clean_name) >= 2:
                all_note_names.add(clean_name)

# Major anatomical muscles list (comprehensive)
major_muscles = [
    '비복근', '가자미근', '족저근', '전경골근', '후경골근', '장비골근', '단비골근', '제3비골근',
    '장지신근', '단지신근', '장모지신근', '단모지신근', '장지굴근', '단지굴근', '장모지굴근', '단모지굴근',
    '대퇴사두근', '대퇴직근', '외측광근', '내측광근', '중간광근',
    '햄스트링', '대퇴이두근', '반건양근', '반막양근', '대퇴이두근 장두', '대퇴이두근 단두',
    '둔근', '대둔근', '중둔근', '소둔근', '이상근', '상쌍자근', '하쌍자근', '내폐쇄근', '외폐쇄근', '대퇴방형근',
    '내전근', '대내전근', '장내전근', '단내전근', '치골근', '박근',
    '장요근', '대요근', '소요근', '장골근', '요방형근', '복횡근', '복직근', '내복사근', '외복사근', '추체근',
    '골반저근', '항문거근', '미골근', '회음횡근',
    '척추기립근', '장늑근', '최장근', '극근', '다열근', '회선근', '반극근', '두반극근', '경반극근', '흉반극근',
    '후두하근', '대후두직근', '소후두직근', '상두사근', '하두사근',
    '판상근', '두판상근', '경판상근',
    '승모근', '상부승모근', '중부승모근', '하부승모근', '견갑거근', '능형근', '대능형근', '소능형근', '전거근', '소흉근',
    '광배근', '대원근', '소원근', '극상근', '극하근', '견갑하근', '회전근개',
    '삼각근', '전면삼각근', '측면삼각근', '후면삼각근', '오훼완근', '상완이두근', '상완삼두근', '상완근', '완요골근',
    '원회내근', '방형회내근', '회외근', '요측수근굴근', '척측수근굴근', '장장근', '심지굴근', '천지굴근',
    '요측수근신근', '장요측수근신근', '단요측수근신근', '척측수근신근', '지신근', '소지신근', '시지신근',
    '흉쇄유돌근', '사각근', '전사각근', '중사각근', '후사각근', '경장근', '두장근', '설골하근군', '흉골근', '횡격막',
    '족저근막', '흉요근막', '모상건막', '장경인대', '대퇴근막장근'
]

for m in major_muscles:
    all_note_names.add(m)

# Sort target words by length descending so longer words match first
target_words = sorted(list(all_note_names), key=lambda x: len(x), reverse=True)
# filter out single char or generic words
filtered_words = [w for w in target_words if len(w) >= 2 and w not in ['개요', '분류', '평가', '정리', '공부', '근육', '질환', '신경', '처방', '본초', '경락', '원리', '구조', '기전']]

print(f'Total target medical/muscle keywords: {len(filtered_words)}')

# Process markdown files in 근막경선
def linkify_text(content):
    # 1. Clean broken bold around links: e.g. **[[word]]** -> [[word]], **[[word]] -> [[word]]
    content = re.sub(r'\*\*\[\[([^\]]+)\]\]\*\*', r'[[\1]]', content)
    content = re.sub(r'\*\*\[\[([^\]]+)\]\]', r'[[\1]]', content)
    content = re.sub(r'\[\[([^\]]+)\]\]\*\*', r'[[\1]]', content)
    
    # 2. For each keyword, replace outside of existing [[...]], `...`, <...>, url(...)
    # Split content into protected and unprotected blocks
    pattern = re.compile(r'(\[\[[^\]]+\]\]|`[^`]+`|<[^>]+>|!\[[^\]]*\]\([^)]+\)|\$\$.*?\$\$|\$[^\$]+\$)')
    tokens = pattern.split(content)
    
    for i in range(len(tokens)):
        # only process unprotected text (even indices)
        if i % 2 == 0:
            text = tokens[i]
            for w in filtered_words:
                # regex word boundary or korean character boundary
                # Do not replace if already preceded by [[ or followed by ]]
                escaped = re.escape(w)
                text = re.sub(rf'(?<!\[\[)(?<![a-zA-Z가-힣0-9]){escaped}(?![a-zA-Z가-힣0-9])(?!\]\])', f'[[{w}]]', text)
            tokens[i] = text
            
    res = ''.join(tokens)
    
    # Clean up double links if any e.g. [[[[word]]]] -> [[word]]
    res = re.sub(r'\[\[\[\[([^\]]+)\]\]\]\]', r'[[\1]]', res)
    res = re.sub(r'\[\[\[([^\]]+)\]\]\]', r'[[\1]]', res)
    # Clean up orphaned asterisks e.g. **됩니다 -> 됩니다 if unmatched
    return res

md_files = [os.path.join(notes_dir, f) for f in os.listdir(notes_dir) if f.endswith('.md')]
for fpath in md_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        orig = f.read()
    new_c = linkify_text(orig)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_c)
    print(f'Linkified: {os.path.basename(fpath)}')

print('All fascia notes successfully linkified!')
