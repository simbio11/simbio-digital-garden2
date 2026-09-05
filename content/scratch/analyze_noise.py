import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

src_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md"
items = []
pattern = re.compile(r"^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]")
with open(src_path, encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            items.append((int(m.group(1)), m.group(2)))

print(f"Total current items: {len(items)}")

# 의심되는 카테고리들 탐색
template_placeholders = []
system_meta = []
categories_meta = []
acupoints = []
articles_or_long = []

for count, name in items:
    # 1. 템플릿/플레이스홀더/메타
    if any(k in name for k in ["제목", "작성자", "템플릿", "플레이스홀더", "날짜", "개요", "요약", "설명", "참고", "내용"]):
        template_placeholders.append((count, name))
    # 2. 영문 시스템/리포트/옵시디언
    elif any(k in name.lower() for k in ["report", "audit", "wikilink", "link", "dashboard", "summary", "sprint", "session", "coaching"]):
        system_meta.append((count, name))
    # 3. 상위 카테고리 단어
    elif name in ["본초", "근육", "약리성분", "양방약", "질환", "처방", "경락", "해부학", "생리학", "병리학", "한의학", "의학", "도서", "독서"]:
        categories_meta.append((count, name))
    # 4. 혈자리: 한자 괄호 포함 또는 침구 혈자리
    elif "(" in name and ")" in name:
        acupoints.append((count, name))
    # 5. 문장형 또는 긴 제목 (공백 2개 이상이거나 길이 12자 이상인데 의학용어가 아닌 것)
    elif len(name.split()) >= 3:
        articles_or_long.append((count, name))

print(f"Template placeholders: {len(template_placeholders)}")
print("  Sample:", template_placeholders[:10])

print(f"System/Obsidian meta: {len(system_meta)}")
print("  Sample:", system_meta[:10])

print(f"Category meta: {len(categories_meta)}")
print("  Sample:", categories_meta[:10])

print(f"Acupoints / Paren names: {len(acupoints)}")
print("  Sample:", acupoints[:10])

print(f"Articles / Long sentences: {len(articles_or_long)}")
print("  Sample:", articles_or_long[:10])
