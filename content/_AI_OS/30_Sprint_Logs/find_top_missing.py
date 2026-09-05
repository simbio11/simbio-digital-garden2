import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

list_path = r'c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md'
with open(list_path, 'r', encoding='utf-8') as f:
    text = f.read()

vault_root = r'c:\Simbio'
existing_files = set()
for root, dirs, files in os.walk(vault_root):
    for file in files:
        if file.endswith('.md'):
            existing_files.add(file[:-3])

items = []
for line in text.split('\n'):
    m = re.search(r'- `\s*(\d+)회`\s*→\s*\[\[(.*?)\]\]', line)
    if m:
        refs = int(m.group(1))
        name = m.group(2)
        if name not in existing_files:
            items.append((refs, name))

print(f'Total missing items: {len(items)}')
print('Top 40 missing items:')
for r, n in items[:40]:
    print(f'- {r}회: {n}')
