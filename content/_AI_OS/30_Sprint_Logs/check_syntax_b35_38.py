import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\2. 약리 공부\처방\08_치풍·거풍제\서경탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\6-쇼가올.md',
    r'c:\Simbio\2. 약리 공부\약리성분\다당류.md',
    r'c:\Simbio\2. 약리 공부\처방\09_사상의학\한다열소탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\갈랑긴.md',
    r'c:\Simbio\2. 약리 공부\약리성분\마트린.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\백반.md',
    r'c:\Simbio\2. 약리 공부\처방\04_이기·화해제\과루해백백주탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\하이페로사이드.md',
    r'c:\Simbio\2. 약리 공부\약리성분\시니그린.md',
    r'c:\Simbio\2. 약리 공부\약리성분\아르크티인.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\생강피.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\복령피.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\오피음.md',
    r'c:\Simbio\2. 약리 공부\처방\08_치풍·거풍제\대진교탕.md',
    r'c:\Simbio\2. 약리 공부\처방\06_보익제\통유탕.md'
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
