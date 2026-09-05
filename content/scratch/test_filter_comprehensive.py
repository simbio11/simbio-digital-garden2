import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 1. 본초 효능 링크 로드
vault_dir = r"c:\Simbio"
boncho_dir = r"c:\Simbio\2. 약리 공부\본초(약리)"

boncho_efficacy = set()
for root, dirs, files in os.walk(boncho_dir):
    for f in files:
        if f.endswith(".md"):
            with open(os.path.join(root, f), encoding="utf-8", errors="ignore") as file:
                for line in file:
                    if any(k in line for k in ["효능", "Actions", "기능", "주치"]):
                        for link in re.findall(r"\[\[(.*?)\]\]", line):
                            name = link.split("|")[0].strip()
                            # 영문/숫자/특수문자 위주(NF-kB, 5-HMF 등 약리성분/수용체)는 제외
                            if re.match(r"^[가-힣]{2,6}$", name):
                                boncho_efficacy.add(name)

print(f"Extracted {len(boncho_efficacy)} pure Korean efficacy names from boncho notes.")

# 2. 미노트화 링크 목록 로드
src_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md"
items = []
pattern = re.compile(r"^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]")
with open(src_path, encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            items.append((int(m.group(1)), m.group(2)))

# 3. 효능/치법 어근 정의
actions_verbs = set("보익청해활거건양온산윤소사조통평강승진안수렴지파화개납삽서축연퇴생투배탁절식명강완정제숙촉포")
actions_nouns = set("신기비폐간심위담기혈맥음양한열화조습풍담음수뇨변독어옹종창통해천구토사충림서석경락태유정근골규신맥창조식생")

# 2~5글자 효능/치법 패턴
def is_han_efficacy(word):
    if not re.match(r"^[가-힣]{2,5}$", word):
        return False
    if word in boncho_efficacy:
        return True
    
    # 4글자 패턴 검사 (전형적인 4자 효능어: 예 익신고정, 보간명목, 강근골...)
    if len(word) == 4:
        # 두 글자씩 분해
        w1, w2 = word[:2], word[2:]
        # 둘 다 동사+명사이거나 한의학 술어
        if (word[0] in actions_verbs and word[1] in actions_nouns) or (word[2] in actions_verbs and word[3] in actions_nouns):
            return True
        if word.endswith(("지통", "지혈", "지해", "평천", "안신", "해독", "산결", "소종", "지갈", "통변", "통경", "지구", "지사", "통림", "지양", "강골", "고정", "축뇨", "명목", "배농", "생진", "윤장", "거어", "산어", "잠양", "조습", "화담", "제습", "통락", "활락", "개규", "온중", "건비", "양혈", "보기", "보혈", "자음", "청열", "사화", "거풍", "승습", "산한", "거한")):
            return True
        if word.startswith(("청열", "거풍", "활혈", "화어", "온중", "건비", "보비", "익기", "보기", "보혈", "양혈", "자음", "보신", "익신", "평간", "소종", "조습", "이수", "해표", "발한", "윤폐", "양심", "진경", "개규", "수렴", "사하", "윤장", "온신", "산한")):
            return True

    # 3글자 패턴: 강근골, 속근골, 거풍습, 온비위, 청비열, 생진액, 통경락 등
    if len(word) == 3:
        if word in ["강근골", "속근골", "거풍습", "온비위", "청비열", "생진액", "통경락", "산풍열", "산풍한", "거풍열", "거풍한", "소식적", "행기혈", "활기혈"]:
            return True
        if word.startswith(("거풍", "온비", "청열", "보신", "익신", "강근", "속근", "조습", "활혈", "보혈", "보기")) and word[2] in actions_nouns:
            return True

    # 2글자 패턴: 효능어 목록
    two_char_efficacy = {
        "안태", "지혈", "살충", "지양", "통변", "소적", "하기", "통림", "명목", "강기", "윤장", "청심",
        "지통", "생진", "양혈", "산한", "소종", "이수", "활혈", "파혈", "평간", "안신", "소담", "지해",
        "화담", "통경", "개규", "평천", "화위", "진경", "소갈", "보신", "익신", "보비", "건비", "보폐",
        "보간", "청간", "보심", "양심", "보기", "익기", "행기", "이기", "파기", "승양", "보혈", "화어",
        "산어", "거어", "량혈", "자음", "양음", "렴음", "온양", "온신", "장양", "온중", "거한", "온경",
        "사화", "조습", "화습", "이습", "거습", "행수", "삼습", "배농", "산결", "연견", "도체", "소식",
        "거풍", "소풍", "승습", "완급", "통락", "서근", "강근", "거담", "정천", "사폐", "정경", "진간",
        "잠양", "통규", "고정", "삽정", "축뇨", "축수", "지한", "고표", "렴창", "생기", "지갈", "윤조",
        "사하", "화석", "수렴", "고삽", "강역", "지구", "지사", "하유", "소도", "제번", "강압"
    }
    if word in two_char_efficacy:
        return True

    return False

# 4. 변증/단순상태/치료행위
non_concept_terms = {
    # 변증
    "음허화왕", "비위기허", "간기울결", "기혈양허", "신양허", "신음허", "간신음허", "습열하주",
    "비허습체", "풍한습비", "심비양허", "비신양허", "심신불교", "간양상항", "담탁조폐", "간화상염",
    "기체혈어", "어혈조체", "비기허", "폐기허", "신양부족", "신음부족", "한습곤비", "위열치성",
    "기혈허", "음양구허", "간울기체", "간비불화", "한열협잡", "비위허약", "위기허", "신허요통",
    "수습정체", "담음정체", "담습", "풍습비", "풍열비", "기허발열", "음허발열", "혈허발열",
    # 치료/행위/일반어
    "침치료", "뜸치료", "부항치료", "물리치료", "온열치료", "도수치료", "운동치료", "약침치료",
    "추나요법", "식이요법", "환자 티칭", "생활 티칭", "치료 계획", "치료 원칙", "치법", "치료법",
    "변증", "예후", "감별진단", "병력청취", "이학적 검진", "문진", "망진", "절진", "문진(聞診)",
    "발한", "토법", "하법", "화법", "온법", "청법", "소법", "보법",
    "자가스트레칭", "티칭", "생활관리", "주의사항", "스트레칭", "폼롤러", "마사지", "근막이완"
}

def should_remove(name):
    if name in non_concept_terms:
        return True, "syndrome_or_general"
    if is_han_efficacy(name):
        return True, "han_efficacy"
    return False, None

# 분류 수행
removed = []
kept = []

for count, name in items:
    rem, reason = should_remove(name)
    if rem:
        removed.append((count, name, reason))
    else:
        kept.append((count, name))

print(f"Total: {len(items)} -> Kept: {len(kept)}, Removed: {len(removed)}")

# 제거된 항목 상위 40개 확인
print("\n--- Removed Top 40 ---")
for c, n, r in removed[:40]:
    print(f"{c:3d}회 | {n} [{r}]")

# 보존된 항목 상위 40개 확인 (중요 질환, 본초, 처방, 해부학 등이 잘 살아있는지 확인)
print("\n--- Kept Top 40 ---")
for c, n in kept[:40]:
    print(f"{c:3d}회 | {n}")
