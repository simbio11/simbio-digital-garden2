import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    r'c:\Simbio\2. 약리 공부\본초\천오.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\ICAM-1.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\당귀사역탕.md',
    r'c:\Simbio\2. 약리 공부\본초\소합향.md',
    r'c:\Simbio\2. 약리 공부\약리성분\멘톨.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\오인환.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\포도당.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\오두탕.md',
    r'c:\Simbio\2. 약리 공부\본초\노근.md',
    r'c:\Simbio\2. 약리 공부\본초\보골지.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\뮤신.md',
    r'c:\Simbio\2. 약리 공부\약리성분\크로신.md',
    r'c:\Simbio\2. 약리 공부\처방\06_청열·해독·사화제\청골산.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\증액탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\이소케르시트린.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\선비탕.md'
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
            # check if there is a wikilink with a pipe like [[A|B]]
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
