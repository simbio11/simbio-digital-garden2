import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\2. 약리 공부\약리성분\탄산칼슘.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\도홍사물탕.md',
    r'c:\Simbio\2. 약리 공부\처방\08_치풍·거풍제\소활락단.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\육두구.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\소계음자.md',
    r'c:\Simbio\2. 약리 공부\처방\08_치풍·거풍제\견정산.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\택사탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\아비쿨라린.md',
    r'c:\Simbio\2. 약리 공부\처방\02_청열제\서각지황탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\피페린.md',
    r'c:\Simbio\2. 약리 공부\약리성분\호박산.md',
    r'c:\Simbio\2. 약리 공부\약리성분\팔미틴.md',
    r'c:\Simbio\3. 이론 공부\상한론\금궤요략.md',
    r'c:\Simbio\3. 이론 공부\질환\부인과 질환\자궁근종.md',
    r'c:\Simbio\1. 근골격계 공부\근육\복사근.md'
]

for fpath in new_files:
    if not os.path.exists(fpath):
        print(f'Missing: {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

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
