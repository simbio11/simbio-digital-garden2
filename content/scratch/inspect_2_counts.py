import sys
from analyze_noise import items

sys.stdout.reconfigure(encoding="utf-8")

# 2회 참조 항목들 중에서 어떤 패턴들이 있는지 분석
two_counts = [name for count, name in items if count <= 2]
print(f"Total 2-count items: {len(two_counts)}")

# 샘플 100개 확인
print("\n--- Sample 2-count items (1-50) ---")
for n in two_counts[:50]:
    print(n)

print("\n--- Sample 2-count items (51-100) ---")
for n in two_counts[50:100]:
    print(n)
