import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update MOC
moc_path = r'c:\Simbio\2. 약리 공부\처방\00_처방_학술_임상_MOC.md'
with open(moc_path, 'r', encoding='utf-8') as f:
    moc = f.read()

# 창부도담탕 into 조습화담·윤폐화담
if '[[03_화담·거습·이수제/창부도담탕|창부도담탕]]' not in moc:
    moc = moc.replace('[[03_화담·거습·이수제/도담탕|도담탕]]', '[[03_화담·거습·이수제/도담탕|도담탕]], [[03_화담·거습·이수제/창부도담탕|창부도담탕]]')

# 현부이경탕 into 활혈거어
if '[[05_활혈거어·지혈제/현부이경탕|현부이경탕]]' not in moc:
    moc = moc.replace('[[05_활혈거어·지혈제/현부리경탕|현부리경탕]]', '[[05_활혈거어·지혈제/현부리경탕|현부리경탕]], [[05_활혈거어·지혈제/현부이경탕|현부이경탕]]')

with open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC updated successfully')

# 2. Update side effects
side_path = r'c:\Simbio\2. 약리 공부\처방\처방 사이드 대처법.md'
with open(side_path, 'r', encoding='utf-8') as f:
    side = f.read()

new_pearls = '''
### 76. 창출·담남성·반하 ([[창부도담탕]]) - 진액 건조 및 임신 중 태기(胎氣) 불안
- **증상 기전**: [[창출]], [[담남성]], [[반하]]의 강력한 조습파담(燥濕破痰) 작용이 담습이 제거된 후에도 지속될 경우 혈허(血虛) 환자의 진액을 말리고 구갈·변비 유발. 특히 착상 후 복용 시 자궁 수축으로 태동불안 유발 가능.
- **예방 및 대처법**:
  - 생리가 시작되거나 임신 반응 양성이 확인되면 즉시 복용을 중단하고 보혈안태 처방([[당귀산]])으로 전환.
  - 비만하지 않고 마른 체형의 무월경 환자에게는 절대 금기.

### 77. 현호색·도인·홍화 ([[현부이경탕]]) - 월경 과다 및 임산부 유산 위험
- **증상 기전**: [[현호색]], [[도인]], [[홍화]]의 강한 활혈거어 및 자궁 수축 촉진 작용이 기혈허약성 월경통 환자에게 출혈량 과다 및 어지럼증을 유발하거나 임신 초기 유산 초래.
- **예방 및 대처법**:
  - 임신 가능성이 있는 여성에게는 복용을 엄격히 금함.
  - 생리혈의 덩어리가 풀리고 통증이 완화되면 생리 2~3일째부터 복용을 중단하여 불필요한 출혈을 방지.
'''

if '76. 창출·담남성·반하' not in side:
    side = side.strip() + '\n\n---\n' + new_pearls.strip() + '\n'
    with open(side_path, 'w', encoding='utf-8') as f:
        f.write(side)
    print('Side effects updated successfully')
