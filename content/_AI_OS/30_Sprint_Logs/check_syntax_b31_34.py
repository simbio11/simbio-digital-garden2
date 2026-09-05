import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\좌상.md',
    r'c:\Simbio\1. 근골격계 공부\골격\갈퀴족.md',
    r'c:\Simbio\1. 근골격계 공부\골격\무지외반증.md',
    r'c:\Simbio\1. 근골격계 공부\골격\망치족지.md',
    r'c:\Simbio\1. 근골격계 공부\골격\경추.md',
    r'c:\Simbio\1. 근골격계 공부\근육\대능형근.md',
    r'c:\Simbio\1. 근골격계 공부\근육\소능형근.md',
    r'c:\Simbio\1. 근골격계 공부\골격\모상건막.md',
    r'c:\Simbio\1. 근골격계 공부\근골격계\익상견갑.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\흉부(+어깨)\어깨충돌 증후군.md',
    r'c:\Simbio\1. 근골격계 공부\근골격계\외측상과염.md',
    r'c:\Simbio\3. 이론 공부\질환\신경계 질환\정중신경 마비.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\AMPK.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\골다공증.md',
    r'c:\Simbio\2. 약리 공부\약리성분\오스톨.md',
    r'c:\Simbio\1. 근골격계 공부\신경\늑간신경.md'
]

def fix_content(text):
    # safe unwrap of **[[...]]**
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

    # fix bold wiki
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
