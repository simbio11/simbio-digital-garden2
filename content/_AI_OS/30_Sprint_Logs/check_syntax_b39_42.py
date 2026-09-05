import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

new_files = [
    r'c:\Simbio\2. 약리 공부\약리성분\브루신.md',
    r'c:\Simbio\3. 이론 공부\영양학\구연산.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\오매.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\TRPM8.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\NO.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\생강즙.md',
    r'c:\Simbio\2. 약리 공부\처방\02_청열제\백두옹탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\베타-엘레멘.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\화적환.md',
    r'c:\Simbio\2. 약리 공부\처방\02_청열제\사묘환.md',
    r'c:\Simbio\2. 약리 공부\약리성분\모루신.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\경미.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\우황.md',
    r'c:\Simbio\2. 약리 공부\본초(약리)\천화분.md',
    r'c:\Simbio\2. 약리 공부\약리성분\제니포사이드.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\궁귀교애탕.md'
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
