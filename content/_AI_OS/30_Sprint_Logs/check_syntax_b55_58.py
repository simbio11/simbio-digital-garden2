import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\정력대조사폐탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\린코필린.md',
    r'c:\Simbio\2. 약리 공부\약리성분\루비아딘.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\백통탕.md',
    r'c:\Simbio\2. 약리 공부\처방\01_해표제\총두탕.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\삼물백산.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\육일산.md',
    r'c:\Simbio\2. 약리 공부\양방 약\코데인.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\E2.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\AMH.md',
    r'c:\Simbio\3. 이론 공부\질환\대사 질환\쿠싱 증후군.md',
    r'c:\Simbio\2. 약리 공부\양방 약\펜타닐.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\탄수화물.md',
    r'c:\Simbio\3. 이론 공부\질환\부인과 질환\유방암.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\옥살로아세트산.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\효소.md'
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
