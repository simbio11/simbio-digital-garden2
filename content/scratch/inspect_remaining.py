import sys
from test_refined_filter import kept, is_whitelisted, is_blacklisted

sys.stdout.reconfigure(encoding="utf-8")

# 4글자 한글 단어 중 혹시 아직 효능/치법 같은 것이 있는지 확인
potential_unwanted = []
for count, name in kept:
    if len(name) == 4 and not is_whitelisted(name):
        potential_unwanted.append((count, name))

print(f"Total 4-letter kept items: {len(potential_unwanted)}")
print("First 80 4-letter kept items:")
for c, n in potential_unwanted[:80]:
    print(f"{c:2d}회 | {n}")
