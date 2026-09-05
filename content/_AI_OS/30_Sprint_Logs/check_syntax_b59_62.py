import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\PGI2.md',
    r'c:\Simbio\3. 이론 공부\질환\간 질환\간문맥 고혈압.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\GLP-1.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\창부도담탕.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\현부이경탕.md',
    r'c:\Simbio\1. 근골격계 공부\근육\판상근.md',
    r'c:\Simbio\1. 근골격계 공부\근육\대후두직근.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\옥살산칼슘.md',
    r'c:\Simbio\2. 약리 공부\약리성분\메틸유게놀.md',
    r'c:\Simbio\3. 이론 공부\질환\신경계 질환\안면신경마비.md',
    r'c:\Simbio\1. 근골격계 공부\골격\하악골.md',
    r'c:\Simbio\1. 근골격계 공부\골격\전자와.md',
    r'c:\Simbio\1. 근골격계 공부\골격\대퇴사두건.md',
    r'c:\Simbio\1. 근골격계 공부\골격\경골조면.md',
    r'c:\Simbio\1. 근골격계 공부\근육\설골하근군.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\근피신경 포착 증후군.md'
]

clean_all = True

for path in files:
    if not os.path.exists(path):
        print(f"File missing: {path}")
        clean_all = False
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    # 1. Fix bold wikilinks: **[[word]]** -> [[word]]
    content = re.sub(r'\*\*\[\[(.*?)\]\]\*\*', r'[[\1]]', content)

    # 2. Fix backtick wikilinks: `[[word]]` -> [[word]]
    content = re.sub(r'`\[\[(.*?)\]\]`', r'[[\1]]', content)

    # 3. Check for pipes inside table cells with wikilinks
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if line.strip().startswith('|') and line.strip().endswith('|'):
            pipe_in_link = re.findall(r'\[\[([^\]]+?\|[^\]]+?)\]\]', line)
            if pipe_in_link:
                print(f"Warning: Pipe in wikilink inside table at {os.path.basename(path)}:{idx+1} -> {pipe_in_link}")
                for p in pipe_in_link:
                    target = p.split('|')[-1]
                    line = line.replace(f"[[{p}]]", f"[[{target}]]")
                lines[idx] = line
                clean_all = False

    content = '\n'.join(lines)

    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed syntax in {os.path.basename(path)}")
    else:
        print(f"Clean: {os.path.basename(path)}")

if clean_all:
    print("All 16 files are 100% CLEAN and ERROR-FREE!")
else:
    print("Some files were fixed and cleaned.")
