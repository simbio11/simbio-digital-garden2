---
project_id: "A-1"
title: "6대 임상 지식 고도화 & MOC 지식그래프 구축"
category: "Project A (Medical Core)"
status: "진행중"
priority: "High"
created: 2026-08-30
updated: 2026-08-31
target_date: "2026-09-12"
tags:
  - ai-project
  - medical-db
  - llm-wiki
  - clinical-knowledge
  - status/in-progress
---

# [[A-1_Clinical_Knowledge_DB]]

> 개요: 6대 핵심 임상 지식(본초, 처방, 근육, 약리성분, 양방약, 질환) 노트를 완벽하게 표준화하고, 최상위 MOC([[_MOC_Herbs]] 등)와 YAML Frontmatter 속성을 정형화하여 Antigravity가 지식 그래프를 직접 순회·추론할 수 있는 LLM Wiki 기반 임상 지식 엔진을 구축한다.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. 6대 표준 템플릿 기반으로 고도화된 옵시디언 마크다운 지식 베이스
  2. 최상위 MOC(Map of Content) 허브 문서군 ([[_MOC_Herbs]], [[_MOC_Formulas]], [[_MOC_Muscles]], [[_MOC_Compounds]], [[_MOC_WesternDrugs]], [[_MOC_Diseases]])
  3. LLM Wiki 탐색을 위한 표준 YAML Frontmatter 스키마 체계
  4. 로컬 PostgreSQL 6대 정규화 DB 및 파서 엔진
* **주요 성공 기준 (KPI)**:
  - [x] 근골격계 172대 근육 전수 표준화 및 위키링크 100% 완료 (🏆 달성)
  - [x] 정윤봉 원장님 임상 강의록 51강 전수 원자화 및 꿀팁 49종 추출 100% 완료 (🏆 달성)
  - [ ] 6대 지식체계 MOC 허브 전면 구축 및 Dataview 인덱싱 연동
  - [ ] YAML Frontmatter 필수 속성 (`id`, `category`, `meridians`, `related_formulas`, `related_muscles` 등) 표준화
  - [ ] 한·양방 병용 금기 및 질환-근육-처방 상호 탐색 쿼리 무결성 확보
* **연동 인프라**: Obsidian Vault (LLM Wiki), LG 그램 PostgreSQL, C-4 Vault Graph MCP

---

## 🏗️ 2. 6대 임상 지식 Frontmatter 표준 스키마 및 MOC 구조

### 🌿 1) 본초 ([[_MOC_Herbs]])
```yaml
id: "HERB-001"
name_kr: "갈근"
name_hanja: "葛根"
scientific_name: "Pueraria lobata (Willd.) Ohwi"
category: "해표약/발한해표약"
nature_flavor: "평(平), 감(甘)·신(辛)"
meridians: ["비경", "위경"]
sasang_type: "태음인"
key_compounds: ["puerarin", "daidzein"]
related_formulas: ["[[갈근탕]]", "[[갈근해기탕]]"]
target_muscles: ["[[승모근]]", "[[두판상근]]", "[[경판상근]]"]
```

### 🍵 2) 처방 ([[_MOC_Formulas]])
```yaml
id: "FORMULA-001"
name_kr: "갈근탕"
name_hanja: "葛根湯"
source_book: "상한론"
category: "해표제"
constitution: "태음인/마른체형실증"
composition: ["[[갈근]]", "[[마황]]", "[[계지]]", "[[작약]]", "[[감초]]", "[[생강]]", "[[대추]]"]
indications: ["풍한표실증", "항배강수", "경추통"]
contraindications: ["표허인다한", "고혈압중증"]
related_muscles: ["[[승모근]]", "[[견갑거근]]", "[[후두하근]]"]
```

### 🫁 3) 근육 ([[_MOC_Muscles]])
```yaml
id: "MUSCLE-001"
name_kr: "승모근"
name_en: "Trapezius"
body_part: "경항부/견배부"
origin: "후두골 외후두융기, 항인대, C7-T12 극돌기"
insertion: "쇄골 외측 1/3, 견봉, 견갑극"
innervation: "부신경(CN XI), C3-C4 신경총"
action: ["견갑골 거상", "상방회전", "후인", "하강"]
related_diseases: ["[[근막통증증후군]]", "[[긴장성 두통]]", "[[경추 염좌]]"]
```

### 🔬 4) 약리성분 ([[_MOC_Compounds]])
```yaml
id: "COMP-001"
name_kr: "푸에라린"
name_en: "Puerarin"
pubchem_cid: 5281807
class: "Isoflavone"
target_proteins: ["5-HT2C", "GLUT4", "eNOS"]
cyp_profile: ["CYP1A2", "CYP2C9"]
related_herbs: ["[[갈근]]"]
```

### 💊 5) 양방의약품 ([[_MOC_WesternDrugs]])
```yaml
id: "DRUG-001"
generic_name: "Amlodipine"
brand_names: ["노바스크", "아모디핀"]
drug_class: "CCB (DHP계열)"
indications: ["본태성 고혈압", "협심증"]
side_effects: ["하지 부종", "치은 증식", "두통"]
herb_interactions: ["[[자감초]] (위알도스테론증 부종 악화 주의)"]
```

### 🩺 6) 질환 ([[_MOC_Diseases]])
```yaml
id: "DIS-001"
name_kr: "경추 추간판 탈출증"
name_en: "Cervical Herniated Nucleus Pulposus"
body_part: "경추부"
special_tests: ["Spurling Test", "Distraction Test", "Upper Limb Tension Test"]
red_flags: ["급격한 상지 근력 저하(Grade 3 이하)", "보행 장애(Myelopathy)"]
key_muscles: ["[[사각근]]", "[[견갑거근]]", "[[판상근]]"]
standard_formulas: ["[[서경탕]]", "[[오적산]]", "[[갈근가출부탕]]"]
```

---

## 💬 3. Grill Me & 아키텍처 의사결정 기록

> [!abstract]- 📌 질의응답 아카이브 (클릭하여 열기)
> **Q1. Vector RAG 폐기 후 지식 검색 정확도 확보 방안**
> - **결정**: Vector 임베딩 대신 마크다운 위키링크([[...]])와 Frontmatter 속성, MOC 최상위 허브를 LLM이 C-4 MCP를 통해 직접 그래프 순회(Graph Traversal)하도록 구축하여 환각 없이 100% 원문 일치 추론을 달성함.

> [!question]+ 📌 최신 Grill Me 이슈 (진행 중인 질의)
> - **현안**: 기존 작성된 노트들의 Frontmatter 일괄 마이그레이션 스크립트 작성 일정
> - **AI 제안**: C-4 MCP 개발과 병행하여 Python 기반 Frontmatter 린터/시더 스크립트 실행

---

## ✅ 4. 세부 Task & 체크리스트

### 🏗️ Phase 1. MOC 허브 구축 및 Frontmatter 정형화
- [ ] 6대 지식 최상위 MOC 파일 생성 ([[_MOC_Herbs]] ~ [[_MOC_Diseases]])
- [ ] 볼트 내 전체 노트 Frontmatter 정규화 린팅 스크립트 구축

### 💻 Phase 2. 지식 그래프 탐색 엔진 및 로컬 DB 연동
- [ ] C-4 Vault Graph MCP와 연동하는 MOC/위키링크 순회 로직 구현
- [ ] PostgreSQL 로컬 스키마 시딩 및 M:N 관계형 쿼리 뷰 확립

### 🧪 Phase 3. A-2 ~ A-9 임상 OS 연계 검증
- [ ] SOAP 차팅 파서(A-2)에서 증상 $\to$ 질환/근육/처방 자동 그래프 탐색 테스트
- [ ] 한·양방 약물 상호작용(A-9) 즉각 쿼리 검증

---

## 📜 5. 프로젝트 회고 및 발자취 (Retrospective & Logs)

### 🏆 Phase 1.1: 172대 근육 및 51강 임상 강의록 전수 표준화 달성 (2026-08-31)
* **목표**: 파편화된 근육 데이터와 방대한 임상 강의록을 6대 표준 템플릿(본초, 처방, 의약품, 근골격계)에 맞춰 100% 마크다운화 및 위키링크 네트워크화.
* **진행 과정**:
  1. **근육학**: Anatomy Trains 및 기능해부학 기반 172개 근육을 일괄 크롭 이미지와 함께 정형화.
  2. **강의록 (총 9개 배치)**: 
     - 소화기(5) -> 약리(4) -> 심장/호흡기(6) -> 평활근/자침(5) -> 내분비(7) -> 사상체질(6) -> 진단학(9) -> 추나/침구(8) -> 기능의학(1) 순으로 51강 전수 격파.
  3. **원자화 (Atomization)**: 강의록 내 핵심 임상 노하우를 `` 형태의 독립 원자 노트 49종으로 분리하여 `4. 임상/임상 꿀팁 & 실전 노하우` 폴더에 별도 아카이브 구축.
* **트러블슈팅 및 의사결정**:
  - *이슈*: 기존 노트의 마크다운 표 안에 이미지를 삽입할 시 옵시디언 렌더링 깨짐 현상 발생.
  - *해결*: 이미지를 표 밖 단독 블록으로 분리하고 정밀 크롭(Tight-crop) 원칙을 도입.
  - *이슈*: 볼드(`**`)와 위키링크([[ ]]) 중첩 시 파싱 오류.
  - *해결*: 볼드 기호를 전면 제거하고 순수 평문 위키링크 체제로 표준 지침(Rule) 제정.
* **성과**: 어떠한 서드파티 플러그인(Dataview 등)이나 Vector DB 없이도, 오직 옵시디언 네이티브 위키링크만으로 LLM이 완벽하게 지식을 순회하고 추론할 수 있는 'LLM Wiki' 토대 완성.

---

## 🔗 6. 관련 리소스 및 백링크
* **마스터 로드맵**: [[00_Project_A_Master_Roadmap]]
* **대시보드**: [[00_Master_Dashboard]]
* **표준 템플릿**: [[본초(약리) 템플릿]], [[처방 템플릿]], [[근골격계(해부·질환) 템플릿]], [[양방의약품(약리·성분) 템플릿]]
