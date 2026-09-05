import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\2. 약리 공부\처방\02_청열제\황련아교탕.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\접골단.md',
    r'c:\Simbio\2. 약리 공부\약리성분\오리엔틴.md',
    r'c:\Simbio\2. 약리 공부\약리성분\나린진.md',
    r'c:\Simbio\2. 약리 공부\처방\04_이기·화해제\시호소간산.md',
    r'c:\Simbio\2. 약리 공부\처방\04_이기·화해제\월국환.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\글루타메이트.md',
    r'c:\Simbio\3. 이론 공부\질환\호흡기 질환\비염.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\키모트립신.md',
    r'c:\Simbio\1. 근골격계 공부\근육\내늑간근.md',
    r'c:\Simbio\2. 약리 공부\약리성분\진저롤.md',
    r'c:\Simbio\2. 약리 공부\약리성분\필리린.md',
    r'c:\Simbio\2. 약리 공부\약리성분\파이오놀.md',
    r'c:\Simbio\1. 근골격계 공부\신경\내폐쇄근신경.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\심부 둔부 증후군.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\고관절 충돌증후군.md'
]

def fix_content(text):
    pattern = re.compile(r'\*\*([^*]*?\[\[[^*]*?\]\][^*]*?)\*\*')
    while pattern.search(text):
        text = pattern.sub(r'\1', text)
    return text

for fpath in new_files:
    if not os.path.exists(fpath):
        print(f'Missing: {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed = fix_content(content)
    if fixed != content:
        print(f"Fixed bold in {os.path.basename(fpath)}")
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        content = fixed

    # check bold wiki
    b_wiki = re.findall(r'\*\*(?:\[\[.*?\]\])+\*\*', content)
    b_wiki_code = re.findall(r'`\[\[.*?\]\]`', content)
    
    # check pipes in tables
    table_pipes = []
    for line in content.split('\n'):
        if line.strip().startswith('|') and line.strip().endswith('|'):
            pipes = re.findall(r'\[\[[^\]]+\|[^\]]+\]\]', line)
            if pipes:
                table_pipes.extend(pipes)

    if b_wiki or b_wiki_code or table_pipes:
        print(f"Defect in {os.path.basename(fpath)}: Bold/code: {b_wiki + b_wiki_code}, Table pipes: {table_pipes}")
    else:
        print(f"Clean: {os.path.basename(fpath)}")

print('Audit complete.')
