import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

vault_dir = r"c:\Simbio"
boncho_dir = r"c:\Simbio\2. 약리 공부\본초(약리)"

extracted_efficacy_links = set()

# 본초 노트에서 효능 관련 행 파싱
for root, dirs, files in os.walk(boncho_dir):
    for f in files:
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            with open(fp, encoding="utf-8", errors="ignore") as file:
                content = file.read()
                # 효능 행 찾기
                for line in content.splitlines():
                    if "효능" in line or "Actions" in line or "기능" in line:
                        links = re.findall(r"\[\[(.*?)\]\]", line)
                        for link in links:
                            link_clean = link.split("|")[0].strip()
                            if link_clean:
                                extracted_efficacy_links.add(link_clean)

print(f"Extracted {len(extracted_efficacy_links)} distinct efficacy links from boncho notes.")
print("Sample extracted efficacy links:")
for item in sorted(list(extracted_efficacy_links))[:50]:
    print(f"  - {item}")
