import os
import re

src_path = r"c:\Simbio\_AI_OS\30_Sprint_Logs\미노트화_링크_목록.md"

with open(src_path, encoding="utf-8") as f:
    lines = f.readlines()

items = []
pattern = re.compile(r"^-\s+`\s*(\d+)회`\s+→\s+\[\[(.*?)\]\]")

for line in lines:
    m = pattern.match(line.strip())
    if m:
        count = int(m.group(1))
        name = m.group(2)
        items.append((count, name))

print(f"Total parsed: {len(items)}")

# 한의학 효능/치법(사자성어, 2자성어) 패턴 정의
# 4자 패턴 (앞 2글자 또는 뒤 2글자가 효능 술어)
efficacy_roots_2 = {
    "보신", "익신", "보비", "건비", "보폐", "윤폐", "보간", "청간", "보심", "양심", "청심",
    "보기", "익기", "행기", "하기", "강기", "이기", "파기", "승양",
    "보혈", "양혈", "활혈", "화어", "산어", "거어", "파혈", "량혈", "지혈",
    "자음", "양음", "렴음", "온양", "온신", "장양", "온중", "산한", "거한", "온경",
    "청열", "해독", "사화", "조습", "화습", "이습", "거습", "이수", "행수", "삼습",
    "소종", "배농", "산결", "연견", "소적", "도체", "소식",
    "거풍", "소풍", "승습", "지통", "완급", "통락", "서근", "강근",
    "화담", "거담", "소담", "지해", "평천", "정천", "사폐",
    "안신", "정경", "진경", "진간", "잠양", "개규", "통규",
    "고정", "삽정", "축뇨", "축수", "지한", "고표", "렴창", "생기",
    "생진", "지갈", "윤조", "윤장", "통변", "사하",
    "명목", "통림", "화석", "살충", "지양", "수렴", "고삽",
    "화위", "강역", "지구", "지사", "통경", "하유", "안태"
}

def is_efficacy(name):
    # 4글자 효능어 검사
    if len(name) == 4:
        c1 = name[:2]
        c2 = name[2:]
        if c1 in efficacy_roots_2 or c2 in efficacy_roots_2:
            return True, "efficacy_4"
        # 개별 한자 어근 조합
        prefixes = ("보", "익", "청", "해", "활", "거", "건", "양", "온", "산", "윤", "소", "사", "조", "통", "평", "강", "승", "진", "안", "수", "렴", "지", "파", "화", "개", "납", "삽", "서", "축", "연", "퇴", "생", "투", "배", "식", "명")
        suffixes = ("지통", "지혈", "지해", "평천", "안신", "해독", "산결", "소종", "지갈", "통변", "통경", "지구", "지사", "통림", "지양", "강골", "고정", "축뇨", "명목", "배농", "생진", "윤장", "거어", "산어", "잠양", "조습", "화담", "제습", "통락")
        if name.startswith(prefixes) and (any(name.endswith(s) for s in suffixes) or name[2:] in efficacy_roots_2):
            return True, "efficacy_4_prefix"
    # 2글자 효능어 검사
    if len(name) == 2 and name in efficacy_roots_2:
        return True, "efficacy_2"
    return False, None

# 증후/변증 상태어
syndrome_roots = {
    "기허", "혈허", "음허", "양허", "기체", "혈어", "습열", "담음", "수음", "풍열", "풍한", "풍습",
    "음허화왕", "비위기허", "간기울결", "기혈양허", "신양허", "신음허", "간신음허", "습열하주",
    "비허습체", "풍한습비", "심비양허", "비신양허", "심신불교", "간양상항", "담탁조폐", "간화상염",
    "기체혈어", "어혈조체", "비기허", "폐기허", "신양부족", "신음부족", "한습곤비", "위열치성"
}

def is_syndrome(name):
    if name in syndrome_roots:
        return True, "syndrome"
    if len(name) == 4 and (name.endswith("증") or name.endswith("허") or name.endswith("열") or name.endswith("습") or name.endswith("울")):
        if any(name.startswith(p) for p in ["기허", "혈허", "음허", "양허", "기체", "간울", "비허", "신허", "심허", "폐허"]):
            return True, "syndrome"
    return False, None

# 일반 처치/행위/임상 비개념어
general_terms = {
    "침치료", "뜸치료", "부항치료", "물리치료", "온열치료", "도수치료", "운동치료", "약침치료",
    "추나요법", "식이요법", "환자 티칭", "생활 티칭", "치료 계획", "치료 원칙", "치법", "치료법",
    "변증", "예후", "감별진단", "병력청취", "이학적 검진", "문진", "망진", "절진", "문진(聞診)",
    "발한", "토법", "하법", "화법", "온법", "청법", "소법", "보법"
}

def is_general(name):
    if name in general_terms:
        return True, "general_term"
    return False, None

removed = []
kept = []

for count, name in items:
    # 1. efficacy
    eff, reason = is_efficacy(name)
    if eff:
        removed.append((count, name, reason))
        continue
    # 2. syndrome
    syn, reason = is_syndrome(name)
    if syn:
        removed.append((count, name, reason))
        continue
    # 3. general
    gen, reason = is_general(name)
    if gen:
        removed.append((count, name, reason))
        continue
    kept.append((count, name))

print(f"Kept: {len(kept)}, Removed: {len(removed)}")
print("\n--- Sample Removed (top 30) ---")
for count, name, reason in removed[:30]:
    print(f"{count:3d}회 | {name} ({reason})")

print("\n--- Check specific items ---")
for target in ["익신고정", "강근골", "보비지사", "양심안신", "지대지갈", "청열해독", "상한론", "오공약침", "태음인", "두충", "대퇴골"]:
    r = [x for x in removed if x[1] == target]
    k = [x for x in kept if x[1] == target]
    if r:
        print(f"Target '{target}': REMOVED ({r[0][0]}회, {r[0][2]})")
    elif k:
        print(f"Target '{target}': KEPT ({k[0][0]}회)")
    else:
        print(f"Target '{target}': NOT FOUND in items")
