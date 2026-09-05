import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

src_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md"
backup_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_제거목록_백업.md"

items = []
pattern = re.compile(r"^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]")
with open(src_path, encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            items.append((int(m.group(1)), m.group(2)))

# ==============================================================================
# 1. 혈자리 사전 로드
# ==============================================================================
STANDARD_ACUPOINTS = {
    "중부", "운문", "천부", "협백", "척택", "공최", "열결", "경거", "태연", "어제", "소상",
    "상양", "이간", "삼간", "합곡", "양계", "편력", "온류", "하렴", "상렴", "수삼리", "곡지",
    "주료", "수오리", "비노", "견우", "거골", "천정", "부돌", "화료", "영향",
    "승읍", "사백", "거료", "지창", "대영", "협거", "하관", "두유", "인영", "수돌", "기사",
    "결분", "기호", "고방", "옥예", "응창", "유중", "유근", "불용", "승만", "양문", "관문",
    "태을", "활육문", "천추", "외릉", "대거", "수도", "귀래", "기충", "비관", "복토", "음시",
    "양구", "독비", "족삼리", "상거허", "조구", "하거허", "풍륭", "해계", "충양", "함곡", "내정", "여태",
    "은백", "대도", "태백", "공손", "상구", "삼음교", "누곡", "지기", "음릉천", "혈해",
    "충문", "부사", "복결", "대횡", "복애", "식두", "천계", "흉향", "주영", "대포",
    "극천", "청령", "소해", "영도", "통리", "음극", "소부", "소충",
    "소택", "전곡", "후계", "양곡", "양로", "지정", "노유", "천종",
    "병풍", "곡원", "견외유", "견중유", "천창", "천용", "관료", "청궁",
    "정명", "찬죽", "미충", "곡차", "오처", "승광", "통천", "락각", "옥침", "천주",
    "대저", "풍문", "폐유", "궐음유", "심유", "독유", "격유", "간유", "담유", "비유", "위유",
    "삼초유", "신유", "기해유", "대장유", "관원유", "소장유", "방광유", "중려유", "백환유",
    "상료", "차료", "중료", "하료", "백호", "고황", "신당", "의희", "격관", "혼문", "양강",
    "의사", "위창", "황문", "지실", "포황", "질변", "승부", "은문", "부극", "위양", "위중",
    "합양", "승근", "승산", "비양", "부양", "곤륜", "복참", "신맥", "금문", "속골",
    "통곡", "지음",
    "용천", "연곡", "태계", "대종", "수천", "조해", "복류", "교신", "축빈", "음곡",
    "횡골", "대혁", "기혈", "사만", "중주", "황유", "상관", "석관", "음도", "복통곡", "유문",
    "보랑", "신봉", "영허", "신장", "욱중", "유부",
    "천천", "곡택", "극문", "간사", "내관", "대릉", "노궁", "중충",
    "관충", "액문", "중저", "양지", "외관", "지구", "회종", "삼양락", "사독", "청랭연",
    "소락", "노회", "견료", "천료", "천유", "예풍", "계맥", "이청", "각손", "이화료", "사죽공",
    "동자료", "청회", "함연", "현로", "현리", "곡빈", "솔곡", "천충", "부백", "규음",
    "본신", "양백", "두임읍", "목창", "정영", "승령", "뇌충", "풍지", "견정",
    "경문", "대맥", "오추", "유도", "환도", "풍시", "중독", "슬양관", "양릉천", "양교",
    "외구", "광명", "양보", "현종", "구허", "족임읍", "지오회", "협계", "족규음",
    "대돈", "행간", "태충", "중봉", "여구", "중도", "슬관", "곡천", "음포", "족오리", "음렴",
    "급맥", "장문",
    "장강", "요유", "요양관", "현추", "척중", "중추", "근축", "영대", "신도",
    "신주", "도도", "아문", "풍부", "뇌호", "강간", "후정", "백회", "전정", "신회",
    "상성", "신정", "소료", "수구", "태단", "은교",
    "회음", "곡골", "중극", "관원", "석문", "기해", "음교", "신궐", "하완", "건리",
    "상완", "거궐", "구미", "중정", "전중", "옥당", "화개", "선기", "염천", "승장"
}

# 중복 주의 어휘(해부학, 본초 등과 겹침)
PROTECTED_OVERLAPS = {
    "대추", "경골", "완골", "신문", "일월", "지구", "대포", "외관", "명문", "중완", "천돌", "자궁", "양강"
}
ACUPOINTS_FILTER = STANDARD_ACUPOINTS - PROTECTED_OVERLAPS

# ==============================================================================
# 2. 노이즈 판정 로직
# ==============================================================================
def is_noise(name):
    # 1) 날짜 링크 (예: 2026-08-16 (일), 2026-09-04 등)
    if re.match(r"^\d{4}-\d{2}-\d{2}", name):
        return True, "date_link"

    # 2) 템플릿 / 플레이스홀더 / 안내문
    template_words = {
        "프로젝트 제목", "개념명", "성분명", "약재명", "문서명", "처방명", "근육명", "노트",
        "index", "제목", "작성자", "템플릿", "플레이스홀더", "YYYY-MM-DD", "포트폴리오", "워크리스트"
    }
    if name in template_words or any(p in name for p in ["템플릿", "YYYY-MM-DD", "워크리스트"]):
        return True, "template_placeholder"

    # 3) 시스템 / 리포트 / 옵시디언 메타
    if any(k in name.lower() for k in ["report", "audit", "wikilink", "link", "dashboard", "summary", "sprint", "session", "coaching"]):
        return True, "system_obsidian_meta"
    if name in ["Wikilinks", "위키링크", "위키링크(Wikilinks)", "Links", "Backlinks", "Tags", "MOC", "대시보드", "인덱스"]:
        return True, "system_obsidian_meta"

    # 4) 상위 카테고리 단독 명칭 (단순 분류 라벨)
    if name in ["본초", "근육", "약리성분", "양방약", "질환", "처방", "경락", "해부학", "생리학", "병리학", "한의학", "의학", "도서", "독서"]:
        return True, "category_label"

    # 5) 침구 혈자리
    # 한자 병기 혈자리: 곡지(曲池), 중부(中府), 천종(天宗) 등
    if re.match(r"^[가-힣]{2,4}\([一-龥]{1,4}\)$", name):
        if not any(b in name for b in ["방", "론", "경", "서", "요략", "증후군"]):
            return True, "acupoint"
    # 순수 한글 혈자리
    if name in ACUPOINTS_FILTER:
        return True, "acupoint"

    # 6) 봇 운영 / 일상 / 비의학 태스크 및 기사 제목
    non_medical = {
        "주식 브리핑", "유튜브 브리핑", "영화·콘텐츠 추천", "부동산 브리핑", "논문 리뷰",
        "AI 프로젝트", "헤르메스", "여행", "00. 인박스", "A-10", "운동", "식단일기", "식단"
    }
    if name in non_medical:
        return True, "non_medical_task"
    if any(k in name for k in ["엔캐리", "브리핑", "유튜브", "헤르메스", "에이전트", "AI Master", "포트폴리오"]):
        return True, "non_medical_article"

    # 7) 단순 컨디션 / 일상 상태 묘사 / 비개념어
    general_conditions = {
        "피로", "식욕부진", "무기력", "과로", "기의 상승", "면역력 강화", "몸살기", "간기능",
        "소화기 증상", "갱년기 증상", "기침 시 요실금", "이갈이", "피로감", "집중력 저하",
        "소화불량(단순)", "인대감", "기의 울체", "스트레스성"
    }
    if name in general_conditions:
        return True, "general_condition"

    return False, None

# ==============================================================================
# 3. 필터링 수행
# ==============================================================================
kept = []
removed_now = []

for count, name in items:
    noisy, reason = is_noise(name)
    if noisy:
        removed_now.append((count, name, reason))
    else:
        kept.append((count, name))

print(f"Original items: {len(items)}")
print(f"Clean kept: {len(kept)}")
print(f"Noise removed: {len(removed_now)}")

# ==============================================================================
# 4. 백업 파일 업데이트 (기존 백업에 추가 누적)
# ==============================================================================
existing_backup = []
if os.path.exists(backup_path):
    with open(backup_path, encoding="utf-8") as f:
        existing_backup = f.readlines()

new_backup_lines = []
new_backup_lines.append("---\n")
new_backup_lines.append('title: "미노트화 제거목록 백업 (효능/플레이스홀더/시스템메타 정제 누적)"\n')
new_backup_lines.append("type: backup\n")
new_backup_lines.append("owner: 다빈치\n")
new_backup_lines.append("updated: 2026-09-04\n")
new_backup_lines.append("---\n\n")

# 새롭게 제거된 항목들을 분류별로 정리
by_reason = defaultdict(list)
for c, n, r in removed_now:
    by_reason[r].append((c, n))

new_backup_lines.append(f"# 🗑️ 추가 제거된 노이즈 항목 ({len(removed_now)}종)\n\n")
new_backup_lines.append("> 템플릿 플레이스홀더, 리포트/시스템/옵시디언 메타, 상위 카테고리 단어, 침구 혈자리, 날짜 링크, 비의학 주제 등\n\n")

for r in sorted(by_reason.keys()):
    group = sorted(by_reason[r], key=lambda x: x[0], reverse=True)
    new_backup_lines.append(f"## {r} ({len(group)})\n")
    for c, n in group:
        new_backup_lines.append(f"- `{c:2d}회` → {n}\n")
    new_backup_lines.append("\n")

# 기존 백업 내용 중 이전 섹션들도 보존
new_backup_lines.append("--- \n\n# 📦 이전 1차/2차 효능·치법 제거 백업 내역\n\n")
# 기존 파일에서 제목 헤더 제외하고 이어붙임
start_append = False
for l in existing_backup:
    if l.startswith("## "):
        start_append = True
    if start_append:
        new_backup_lines.append(l)

with open(backup_path, "w", encoding="utf-8") as f:
    f.writelines(new_backup_lines)

print(f"Updated backup file: {backup_path}")

# ==============================================================================
# 5. 미노트화 링크 목록 파일 업데이트
# ==============================================================================
new_links_lines = []
new_links_lines.append("---\n")
new_links_lines.append('title: "미노트화 링크 목록 (정제판 v4 - 노이즈/메타/혈자리 제거 완료)"\n')
new_links_lines.append("type: worklist\n")
new_links_lines.append("owner: 다빈치\n")
new_links_lines.append("updated: 2026-09-04\n")
new_links_lines.append("---\n\n")

total_refs = sum(c for c, _ in kept)
new_links_lines.append("# 🔗 미노트화 링크 — 생성 대기 개념 후보 (정제판 v4)\n\n")
new_links_lines.append(f"> [[ ]]로 참조되나 파일이 없는 대상 중 **독립 지식 메모로 분류 및 생성할 가치가 있는 후보만** {len(kept)}종 / {total_refs}회.\n")
new_links_lines.append("> (한의학 효능·치법, 템플릿 플레이스홀더, 시스템/리포트 메타, 상위 카테고리 단어, 침구 혈자리, 날짜 링크 전수 제거 완료 — 백업: `미노트화_제거목록_백업.md`)\n\n")
new_links_lines.append("## 📊 참조 빈도\n")

for c, n in kept:
    new_links_lines.append(f"- `{c:4d}회` → [[{n}]]\n")

with open(src_path, "w", encoding="utf-8") as f:
    f.writelines(new_links_lines)

print(f"Updated unnoted links list: {src_path}")
