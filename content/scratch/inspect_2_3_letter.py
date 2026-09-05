import sys
from test_refined_filter import kept, is_whitelisted

sys.stdout.reconfigure(encoding="utf-8")

# 2글자, 3글자, 5글자 이상 중 의심 항목 출력
print("=== 2-letter kept items ===")
two_letters = [x for x in kept if len(x[1]) == 2 and not is_whitelisted(x[1])]
for c, n in two_letters[:50]:
    print(f"{c:2d}회 | {n}")

print("\n=== 3-letter kept items ===")
three_letters = [x for x in kept if len(x[1]) == 3 and not is_whitelisted(x[1])]
for c, n in three_letters[:50]:
    print(f"{c:2d}회 | {n}")
