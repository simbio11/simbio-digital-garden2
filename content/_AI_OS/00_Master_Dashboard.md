---
title: "Antigravity AI Master Dashboard"
created: 2026-08-30
updated: 2026-09-04
tags:
  - ai-os
  - dashboard
---

# [[Antigravity AI Master Dashboard]]

> 개요: 임상 AI(Project A), 지능형 자동화(Project B), 에이전트 인프라(Project C), 라이프 OS(Project D)의 4대 핵심 프로젝트(총 27개 서브 프로젝트)와 지식 볼트 진행 과정을 한곳에서 통제하는 통합 제어판입니다.

---

## 📌 1. 상태별 프로젝트 요약 현황

### ⏳ 심문중 (Grill Me 진행 중)
```dataview
TABLE WITHOUT ID
  file.link AS "프로젝트",
  category AS "카테고리",
  priority AS "우선순위",
  updated AS "최근 업데이트"
FROM "_AI_OS/10_Projects"
WHERE status = "심문중"
SORT priority DESC, updated DESC
```

### 🏃‍♂️ 진행중 & ✅ 완료
```dataview
TABLE WITHOUT ID
  file.link AS "프로젝트",
  category AS "카테고리",
  status AS "상태",
  priority AS "우선순위",
  updated AS "최근 업데이트"
FROM "_AI_OS/10_Projects"
WHERE status = "진행중" OR status = "완료"
SORT status ASC, priority DESC, updated DESC
```

### 📋 대기중 (진행전)
```dataview
TABLE WITHOUT ID
  file.link AS "프로젝트",
  category AS "카테고리",
  priority AS "우선순위",
  target_date AS "목표일"
FROM "_AI_OS/10_Projects"
WHERE status = "진행전"
SORT priority DESC, target_date ASC
```

---

## ⚡ 2. AI 실시간 미완료 핵심 Tasks

```dataview
TASK
FROM "_AI_OS/10_Projects"
WHERE !completed
SORT file.name ASC
```

---

## 🗂️ 3. 4대 마스터 프로젝트 전수 바로가기

### 🩺 Project A. 임상 AI & 진료실 지식 베이스 (Medical Core)
* 🗺️ **마스터 로드맵**: [[00_Project_A_Master_Roadmap]]
* 🏃 **현재 스프린트 일지**: [[2026-W35_Project_A_Sprint]]
* 📚 **A-1 지식 볼트 구축 현황**:
  - **172대 근육 전수 표준화**: 172/172 완결 (100.0% 🏆) $\rightarrow$ [[00_Simbio_근육학_임상_지도]]
  - **임상 강의록 원자화**: **51/51강 전수 완결 (100.0% ALL CLEAR 🏆)** $\rightarrow$ [[5. 독서, 노트/강의록/00_강의록_MOC|강의록 MOC]]
  - **독립 임상 꿀팁 아카이브**: **총 49종 6대 체계 완비 💡** $\rightarrow$ [[4. 임상/임상 꿀팁 & 실전 노하우/00_임상_꿀팁_MOC|임상 꿀팁 MOC]]
  - **미노트화 링크 해소 스프린트**: **누적 350종 완결 / 3,892회 참조 클리어 (350종 돌파 🏆)** $\rightarrow$ [[_AI_OS/30_Sprint_Logs/미노트화_링크_목록|미노트화 링크 목록]]
* **서브 프로젝트 (9개)**:
  - [[A-1_Clinical_Knowledge_DB]] : 6대 임상 지식 고도화 & MOC 지식그래프 (완료 100%)
  - [[A-10_Clinical_Metabolic_Synthesis_Engine]] : 임상-대사 융합 합성 노트 자동 생성 엔진 (신규 추가, 🌟)
  - [[A-11_Clinical_Flow_Meta_Analysis_And_Coaching_Engine]] : 진료 녹음 메타 분석 및 1on1 진료 코칭 / 개선 제안 엔진 (신규 추가, 🌟)
  - [[A-2_Clinic_Workflow_Automation]] : faster-whisper 음성 전사 + 2단계 오인식 보정 + SOAP 차팅
  - [[A-3_Clinic_Protocol_Engine]] : 14대 부위별 이학적 검사 & 침/약침/추나 표준 치료 세트
  - [[A-5_Clinical_Prognosis_Timeline_Engine]] : 5대 질환군 예후 예측 & 주차별 회복 타임라인 엔진
  - [[A-6_Treatment_Trigger_Engine]] : 비급여(추나/약침/맞춤한약) 적응증 판정 & 10초 설득 멘트
  - [[A-7_Patient_Handout_Builder]] : 1-Page 진료 직후 맞춤 환자 안내장 빌더
  - [[A-8_Clinical_RedFlag_Alert]] : 응급 전원/처치 금기 Red Flag 실시간 감지 배너
  - [[A-9_Prescription_Safety_Interaction_Engine]] : 한·양방 약물 상호작용 및 안전성 스크리닝

---

### 🤖 Project B. 지능형 자동화 & 에이전트 (Agent & Automation)
* **서브 프로젝트 (7개)**:
  - [[B-1_Overnight_Youtube_Worker]] : 🏆 유튜브 시청기록 요약 및 클리퍼 분류 (MVP 완료)
  - [[B-2_Morning_Intelligence_Briefing]] : 아침(07:00) 매크로/뉴스 & 저녁(21:00) 랩업 텔레그램 브리핑
  - [[B-3_Telegram_Interaction_Bot]] : 인라인 버튼 루틴 체크 & 옵시디언 투두 양방향 동기화
  - [[B-4_Vault_Gardener_Agent]] : 볼트 고아노트/깨진링크/볼드중첩 야간 자동 린팅 및 치유
  - [[B-5_Project_Navigator_Agent]] : 대시보드 병목 감지 및 당일 1순위 액션 강제 발행
  - [[B-6_Clinical_Case_Digest_Agent]] : 임상 논문 및 진료 케이스 표준 SOAP 카드 아카이빙
  - [[B-7_Paper_Digest_Ingester]] : PubChem MoA 및 PubMed 최신 논문 온디맨드 패처
  - [[B-8_Vault_Knowledge_Gap_Detector]] : 볼트 내 고아 노트 및 지식 공백 자동 가디언 에이전트 (신규 추가, 🌟)

---

### 🛡️ Project C. 에이전트 인프라 & 보안 (Agentic Tools & Architecture)
* **서브 프로젝트 (7개)**:
  - [[C-1_AI_Coding_Environment]] : Antigravity IDE 전용 Harness Engineering 표준
  - [[C-2_Custom_Agent_Framework]] : 도메인 특화 에이전트 프레임워크 & Tool 체인
  - [[C-3_Security_and_Isolation]] : Docker 컨테이너 격리, UFW 방화벽, Secrets 암호화
  - [[C-4_Vault_Graph_MCP]] : Antigravity 전용 볼트 그래프 순회 MCP 서버
  - [[C-5_Hermes_Daemon_Orchestrator]] : LG 그램 백그라운드 프로세스 관제 및 자동 복구
  - [[C-6_Prompt_Registry_Harness]] : 도메인별 프롬프트 레지스트리 및 회귀 테스트 하네스
  - [[C-7_Clinic_Gram_Sync_Protocol]] : 환자 데이터 로컬 격리 및 프라이빗 Git 지식 동기화

---

### 📱 Project D. 라이프 매니저 & 개인 OS (Personal OS)
* **서브 프로젝트 (10개)**:
  - [[D-1_Life_Manager_Bugfixes]] : 토스 API 파싱 방어 및 자정 날짜 State 갱신 버그 해결
  - [[D-2_Obsidian_Knowledge_Hub]] : 인물 사전(People DB) 및 학술 개념 자동 위키링크
  - [[D-3_Sports_News_Feed_Module]] : 네이버 스포츠 관심 종목 필터링 및 30분 캐싱 피드
  - [[D-4_Gamified_Habit_Tracker]] : 5km 러닝/코딩/공부 EXP 산출 및 Dataview Heatmap UI
  - [[D-5_Health_Fitness_Automation]] : 🏆 삼성 헬스 & 구글 피트니스 자동 연동 및 크론 보정 (완료)
  - [[D-6_Calendar_Obsidian_Sync]] : 🏆 구글 캘린더 ↔ 옵시디언 일정표 양방향 미러링 (완료)
  - [[D-7_Meal_And_Reflection_Pipeline]] : 🏆 점심/저녁 스마트 식단 체크인 및 저녁 회고 (완료)
  - [[D-8_Smart_Ledger_And_Cash_Reserve_Manager]] : 월급 분배, 고정지출 및 예수금 적립 현황 가계부 연동
  - [[D-9_Frictionless_Capture_Hub]] : 제로 프릭션 인박스 캡처 및 AI 자율 분류 허브
  - [[D-10_AI_Routine_And_Errand_Concierge]] : 아린의 일상 루틴 & 생활 심부름 컨시어지 고도화

---

## 📜 4. 최근 스프린트 및 진행 기록
```dataview
TABLE WITHOUT ID
  file.link AS "스프린트 일지",
  sprint AS "스프린트",
  period AS "기간",
  status AS "상태"
FROM "_AI_OS/30_Sprint_Logs"
SORT file.name DESC
```

---

## 🧭 루트 바로가기
* [[00_Simbio_프로젝트_대시보드|📊 Simbio 종합 마스터 프로젝트 대시보드]]
