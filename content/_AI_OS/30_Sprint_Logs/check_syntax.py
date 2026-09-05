import re, glob, os

files = [
    r"c:\Simbio\1. 근골격계 공부\골격\좌골결절.md",
    r"c:\Simbio\1. 근골격계 공부\골격\견갑골.md",
    r"c:\Simbio\3. 이론 공부\질환\신경계 질환\후골간신경 마비.md",
    r"c:\Simbio\1. 근골격계 공부\신경\전골간신경.md",
    r"c:\Simbio\1. 근골격계 공부\골격\굴근지대.md",
    r"c:\Simbio\1. 근골격계 공부\골격\횡돌기.md",
    r"c:\Simbio\1. 근골격계 공부\신경\음부대퇴신경.md",
    r"c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\젖산.md",
    r"c:\Simbio\3. 이론 공부\상한론\항배강수수.md",
    r"c:\Simbio\2. 약리 공부\약리성분\인게놀.md",
    r"c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\십조탕.md",
    r"c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\대황자충환.md",
    r"c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\방기황기탕.md",
    r"c:\Simbio\2. 약리 공부\처방\01_해표제\신이산.md",
    r"c:\Simbio\2. 약리 공부\처방\04_이기·화해제\지실해백계지탕.md",
    r"c:\Simbio\2. 약리 공부\처방\01_해표제\계지가후박행자탕.md"
]

all_clean = True
for fpath in files:
    if not os.path.exists(fpath):
        print(f"Missing file: {fpath}")
        all_clean = False
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
        all_clean = False

if all_clean:
    print("ALL 16 FILES 100% CLEAN OF SYNTAX DEFECTS!")
