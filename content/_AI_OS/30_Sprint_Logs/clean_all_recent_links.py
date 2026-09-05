import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

recent_files = [
    # 배치 47~50
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\골반 전방경사.md',
    r'c:\Simbio\1. 근골격계 공부\신경\대퇴방형근신경.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\거위발 점액낭염.md',
    r'c:\Simbio\1. 근골격계 공부\신경\목신경고리.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\망치족.md',
    r'c:\Simbio\1. 근골격계 공부\근육\지근.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\11β-HSD2.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\TGF-β.md',
    r'c:\Simbio\2. 약리 공부\약리성분\노토프테롤.md',
    r'c:\Simbio\2. 약리 공부\약리성분\코릴라진.md',
    r'c:\Simbio\2. 약리 공부\본초\결명자.md',
    r'c:\Simbio\2. 약리 공부\처방\06_청열·해독·사화제\지황백호탕.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\삼자양친탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\살비아놀산 B.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\호모시스테인.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\도핵승기탕.md',
    # 배치 51~54
    r'c:\Simbio\2. 약리 공부\본초\천오.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\ICAM-1.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\당귀사역탕.md',
    r'c:\Simbio\2. 약리 공부\본초\소합향.md',
    r'c:\Simbio\2. 약리 공부\약리성분\멘톨.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\오인환.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\포도당.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\오두탕.md',
    r'c:\Simbio\2. 약리 공부\본초\노근.md',
    r'c:\Simbio\2. 약리 공부\본초\보골지.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\뮤신.md',
    r'c:\Simbio\2. 약리 공부\약리성분\크로신.md',
    r'c:\Simbio\2. 약리 공부\처방\06_청열·해독·사화제\청골산.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\증액탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\이소케르시트린.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\선비탕.md',
    # 배치 55~58
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\정력대조사폐탕.md',
    r'c:\Simbio\2. 약리 공부\약리성분\린코필린.md',
    r'c:\Simbio\2. 약리 공부\약리성분\루비아딘.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\백통탕.md',
    r'c:\Simbio\2. 약리 공부\처방\01_해표제\총두탕.md',
    r'c:\Simbio\2. 약리 공부\처방\07_사하·온리·고삽제\삼물백산.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\육일산.md',
    r'c:\Simbio\2. 약리 공부\양방 약\코데인.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\E2.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\AMH.md',
    r'c:\Simbio\3. 이론 공부\질환\대사 질환\쿠싱 증후군.md',
    r'c:\Simbio\2. 약리 공부\양방 약\펜타닐.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\탄수화물.md',
    r'c:\Simbio\3. 이론 공부\질환\부인과 질환\유방암.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\옥살로아세트산.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\효소.md',
    # 배치 59~62
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\PGI2.md',
    r'c:\Simbio\3. 이론 공부\질환\간 질환\간문맥 고혈압.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\GLP-1.md',
    r'c:\Simbio\2. 약리 공부\처방\03_화담·거습·이수제\창부도담탕.md',
    r'c:\Simbio\2. 약리 공부\처방\05_활혈거어·지혈제\현부이경탕.md',
    r'c:\Simbio\1. 근골격계 공부\근육\판상근.md',
    r'c:\Simbio\1. 근골격계 공부\근육\대후두직근.md',
    r'c:\Simbio\3. 이론 공부\의학개념\분자·세포 기전\옥살산칼슘.md',
    r'c:\Simbio\2. 약리 공부\약리성분\메틸유게놀.md',
    r'c:\Simbio\3. 이론 공부\질환\신경계 질환\안면신경마비.md',
    r'c:\Simbio\1. 근골격계 공부\골격\하악골.md',
    r'c:\Simbio\1. 근골격계 공부\골격\전자와.md',
    r'c:\Simbio\1. 근골격계 공부\골격\대퇴사두건.md',
    r'c:\Simbio\1. 근골격계 공부\골격\경골조면.md',
    r'c:\Simbio\1. 근골격계 공부\근육\설골하근군.md',
    r'c:\Simbio\3. 이론 공부\질환\근골격계 질환\근피신경 포착 증후군.md'
]

fixed_count = 0

for p in recent_files:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    # 1. Fix backtick wikilinks: `[[...]]` -> [[...]]
    content = re.sub(r'`\[\[(.*?)\]\]`', r'[[\1]]', content)
    # 2. Fix bold wikilinks: **[[...]]** -> [[...]]
    content = re.sub(r'\*\*\[\[(.*?)\]\]\*\*', r'[[\1]]', content)

    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"Cleaned backticks/bold in: {os.path.basename(p)}")

print(f"\nTotal files cleaned: {fixed_count}")
