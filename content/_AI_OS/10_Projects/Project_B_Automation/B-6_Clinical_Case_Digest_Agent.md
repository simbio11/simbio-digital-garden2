---
project_id: "B-6"
title: "임상 증례 자동 추출 및 아카이빙 에이전트"
category: "Project B (Agent & Automation)"
status: "진행전"
priority: "Medium"
created: 2026-08-31
updated: 2026-08-31
target_date: "2026-10-10"
tags:
  - ai-project
  - case-digest
  - clinical-knowledge
  - soap-archive
  - status/pending
---

# [[B-6_Clinical_Case_Digest_Agent]]

> 개요: 학회지, 한의학 임상 논문, 서적 및 원내 실제 진료 케이스에서 비정형으로 기록된 치험례(Case Report)를 추출하여 표준 SOAP 카드 템플릿으로 구조화하고, `4. 임상/임상 꿀팁 & 실전 노하우/`에 자동 적재하는 증례 아카이빙 에이전트.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. PDF/텍스트 형태의 한의학 임상 논문/증례 리포트 파서
  2. 증례 텍스트 $\to$ [환자프로필 / 주소증 / 변증 / 처방배오 / 치료경과 / 임상포인트] 구조화 엔진
  3. `4. 임상/` 디렉토리 자동 위키링크 및 태깅 아카이빙 파이프라인
* **주요 성공 기준 (KPI)**:
  - [ ] 텍스트 증례 원문 입력 시 5초 이내 표준 마크다운 증례 카드로 100% 구조화
  - [ ] 본초, 처방, 근육, 질환명이 모두 순수 [[위키링크]]로 자동 연결
  - [ ] 원장의 핵심 팁/고찰(`> [임상 꿀팁]`) 블록 자동 생성
* **연동 인프라**: Obsidian Vault (LLM Wiki), A-1 지식 DB, C-4 Vault Graph MCP

---

## 📂 2. 증례 카드 구조화 파이프라인

```mermaid
flowchart TD
    A["임상 논문 PDF / 세미나 필기 / 원내 진료 기록"] --> B["B-6 증례 추출 에이전트 파싱"]
    
    subgraph CASE_CARD ["표준 임상 증례 카드 포맷"]
        C1["1. 환자 프로필 (연령, 성별, 체질, 병력)"]
        C2["2. 주소증 및 변증 (설맥진, 촉진 소견)"]
        C3["3. 치료 처방 및 시술 (침/약침/추나/한약 배오)"]
        C4["4. 치료 경과 및 예후 (회차별 호전도)"]
        C5["5. 💡 원장의 임상 고찰 (성공 요인 & 주의점)"]
    end
    
    B --> CASE_CARD
    CASE_CARD --> D["`4. 임상/` 디렉토리에 자동 마크다운 파일 저장"]
    D --> E["관련 질환([[_MOC_Diseases]]) 및 처방([[_MOC_Formulas]])에 백링크 자동 연결"]
```

---

## 💬 3. Grill Me & 아키텍처 의사결정 기록

> [!abstract]- 📌 질의응답 아카이브 (클릭하여 열기)
> **Q1. 원내 진료 케이스와 외부 학술 논문 증례의 통합 관리**
> - **결정**: 두 소스 모두 동일한 표준 SOAP 증례 템플릿을 공유하되, Frontmatter에 `source: "원내진료"` 또는 `source: "학술논문(대한한의학회지)"` 속성으로 출처를 엄격히 구분하여 메타데이터 인덱싱을 지원함.

---

## ✅ 4. 세부 Task & 체크리스트

### 🏗️ Phase 1. 표준 임상 증례 카드 마크다운 템플릿 정의
- [ ] 증례 카드 템플릿 (`Template_Clinical_Case.md`) 작성
- [ ] 본초, 처방, 근육명 자동 위키링크 정규식 엔진 구현

### 💻 Phase 2. 증례 파싱 및 LLM 구조화 프롬프트 작성
- [ ] 비정형 텍스트 $\to$ 5대 핵심 증례 블록 추출 시스템 프롬프트 개발
- [ ] 옵시디언 `4. 임상/` 자동 저장 및 Dataview 인덱싱 연동

---

## 🔗 5. 관련 리소스 및 백링크
* **마스터 로드맵**: [[00_Project_A_Master_Roadmap]]
* **대시보드**: [[00_Master_Dashboard]]
* **연계 지식**: [[A-1_Clinical_Knowledge_DB]], [[A-3_Clinic_Protocol_Engine]]
