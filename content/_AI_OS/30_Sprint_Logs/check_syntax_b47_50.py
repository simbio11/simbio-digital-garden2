import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\골반 전방경사.md',
    r'c:\Simbio\1. 근골격계 공부\신경\대퇴방형근신경.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\거위발 점액낭염.md',
    r'c:\Simbio\1. 근골격계 공부\신경\목신경고리.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\망치족.md',
    r'c:\Simbio\1. 근골격계 공부\근육\지근.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\11β-HSD2.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\TGF-β.md',
    r'c:\Simbio\2. 약리 공부\약리성분\노토프테롤.md',
    r'c:\Simbio\2. 약리 공부\약리성분\코릴라진.md',
    r'c:\Simbio\2. 약리 공부\본초\결명자.md',
    r'c:\Simbio\2. 약리 공부\처방\06_청열·해독·사화제\지황백호탕.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\삼자양친탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\살비아놀산 B.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\호모시스테인.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\도핵승기탕.md'
]

def fix_content(text):
    pattern = re.compile(r'\*\*([^*]*?\[\[[^*]*?\]\][^*]*?)\*\*')
    while pattern.search(text):
        text = pattern.sub(r'\1', text)
    return text

has_error = False

for fpath in new_files:
    if not os.path.exists(fpath):
        print(f'Missing: {fpath}')
        has_error = True
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
        has_error = True
    else:
        print(f"Clean: {os.path.basename(fpath)}")

if not has_error:
    print('All 16 files are 100% CLEAN and ERROR-FREE!')
