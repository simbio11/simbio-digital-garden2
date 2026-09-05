import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

from analyze_noise import items

# 제거 규칙 정의
def check_noise(name):
    # 1. 날짜 패턴 (예: 2026-08-16 (일), 2026-09-04 등)
    if re.match(r"^\d{4}-\d{2}-\d{2}", name):
        return True, "date_link"
        
    # 2. 템플릿 플레이스홀더
    placeholders = {
        "프로젝트 제목", "개념명", "성분명", "약재명", "문서명", "처방명", "근육명", "노트",
        "index", "제목", "작성자", "템플릿", "플레이스홀더", "YYYY-MM-DD"
    }
    if name in placeholders or any(p in name for p in ["템플릿", "YYYY-MM-DD"]):
        return True, "template_placeholder"
        
    # 3. 봇 운영, AI, 일상, 비의학 카테고리 및 아티클
    non_medical = {
        "주식 브리핑", "유튜브 브리핑", "영화·콘텐츠 추천", "부동산 브리핑", "논문 리뷰",
        "AI 프로젝트", "헤르메스", "여행", "00. 인박스", "A-10", "운동"
    }
    if name in non_medical:
        return True, "non_medical_task"
    if any(k in name for k in ["엔캐리", "브리핑", "유튜브", "헤르메스", "에이전트", "AI Master", "포트폴리오"]):
        return True, "non_medical_article"
        
    # 4. 시스템 / 옵시디언 / 리포트 메타
    if any(k in name.lower() for k in ["report", "audit", "wikilink", "link", "dashboard", "summary", "sprint", "session", "coaching", "links"]):
        return True, "system_obsidian_meta"
    if name in ["위키링크", "위키링크(Wikilinks)", "Links", "Wikilinks", "백링크"]:
        return True, "system_obsidian_meta"
        
    # 5. 상위 카테고리 단독 명칭
    if name in ["본초", "근육", "약리성분", "양방약", "질환", "처방", "경락", "해부학", "생리학", "병리학"]:
        return True, "category_label"
        
    # 6. 침구 혈자리 (지침 2조: 혈자리는 개별 노트 미생성, 순수 텍스트 표기 원칙)
    # 한자 병기 혈자리: 곡지(曲池), 중부(中府), 천종(天宗) 등
    if re.match(r"^[가-힣]{2,4}\([一-龥]{1,4}\)$", name):
        # 단, 의서나 처방 예외 확인 (금궤요략, 태평혜민화제국방 등)
        if not any(b in name for b in ["방", "론", "경", "서", "요략"]):
            return True, "acupoint_with_hanja"
            
    # 7. 단순 일상 컨디션/비질환 상태어/비개념 구
    general_conditions = {
        "피로", "식욕부진", "무기력", "과로", "기의 상승", "면역력 강화", "몸살기", "간기능",
        "소화기 증상", "갱년기 증상", "기침 시 요실금", "이갈이", "피로감", "집중력 저하",
        "수면장애(단순)", "소화불량(단순)"
    }
    if name in general_conditions:
        return True, "general_condition"

    return False, None

noisy = []
clean = []

for count, name in items:
    is_n, reason = check_noise(name)
    if is_n:
        noisy.append((count, name, reason))
    else:
        clean.append((count, name))

print(f"Total: {len(items)} -> Clean: {len(clean)}, Noisy removed: {len(noisy)}")

print("\n--- Noisy Items by Reason ---")
from collections import Counter
counts = Counter(r for _, _, r in noisy)
for r, c in counts.items():
    print(f"  {r}: {c}개")

print("\n--- Sample Noisy Items (top 40) ---")
for c, n, r in sorted(noisy, key=lambda x: x[0], reverse=True)[:40]:
    print(f"  {c:2d}회 | {n} [{r}]")
