import re, os

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

def fix_content(text):
    # unwrap **[[something]]** -> [[something]]
    # Handle patterns like **[[A]], [[B]]** or **[[A]]의 [[B]]**
    def repl_bold(m):
        inner = m.group(1)
        return inner

    # Replace **(...)** where inside contains [[...]]
    # A safe way: if ** contains [[ and ]], unwrap the ** or split
    pattern = re.compile(r'\*\*([^*]*?\[\[[^*]*?\]\][^*]*?)\*\*')
    while pattern.search(text):
        text = pattern.sub(r'\1', text)

    # unwrap `[[...]]` -> [[...]]
    pattern_code = re.compile(r'`([^`]*?\[\[[^`]*?\]\][^`]*?)`')
    while pattern_code.search(text):
        text = pattern_code.sub(r'\1', text)

    return text

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_c = fix_content(content)
    if new_c != content:
        print(f"Fixed: {os.path.basename(fpath)}")
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_c)

print("Fix applied.")
