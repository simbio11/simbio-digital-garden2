---
project_id: "D-8"
title: "스마트 가계부 및 예수금 자산 매니저 (월급 분배 & 예수금 추적)"
category: "Project D (Personal OS)"
status: "진행중"
priority: "High"
created: 2026-09-03
updated: 2026-09-03
target_date: "2026-09-20"
tags:
  - ai-project
  - ledger
  - cash-reserve
  - salary-distribution
  - status/in-progress
---

# [[D-8_Smart_Ledger_And_Cash_Reserve_Manager]]

> 개요: 매달 월급 입금 시 본봉, 수당, 상여금 등을 자동 파싱하고, 고정지출(통신, 옵시디언, AI 구독 등), 생활비, 십일조, 용돈, 그리고 투자 대기 자금인 **예수금 적립 현황**(700만 $\rightarrow$ 2300만 로드맵)을 `C:\Simbio\00. 봇 운영 시스템\생활관리\가계부\가계부.md`와 연동하여 체계적으로 추적·관리하는 재정 매니저 모듈.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. `가계부.md` 내 월별 예수금 적립 목표(매월 200만 원 증액 로드맵: 8월 700만 $\rightarrow$ 9월 900만 $\rightarrow$ ... $\rightarrow$ 익년 4월 2300만) 자동 계산 및 시각화
  2. 월급날(매월 20일 전후) 행동 요령(CMA 이체, 십일조, 카드값 결제) 리마인드 및 정산 자동화
  3. 고정지출 및 카드별 사용 용도(하나신용/체크카드, 서천사랑상품권) 지출 통계 요약
* **주요 성공 기준 (KPI)**:
  - [ ] 월별 예수금 목표 달성률 실시간 트래킹 및 가계부 마크다운 자동 업데이트
  - [ ] 월급날 및 카드 결제일(21일) 맞춤형 재정 브리핑 자동 발송

---

## 💰 2. 예수금 및 월급 분배 로직
```mermaid
flowchart TD
    SALARY["월급 입금 (본봉 + 수당 + 상여)"] --> DISTRIBUTE["자금 분배 플랜 자동 적용"]
    
    DISTRIBUTE --> FIXED["고정지출 (통신, 옵시디언, AI 구독 등 110만)"]
    DISTRIBUTE --> TITHES["십일조 및 용돈"]
    DISTRIBUTE --> CARD["신용카드 및 생활비 결제 (나라사랑/하나카드)"]
    DISTRIBUTE --> RESERVE["투자 대기 예수금 CMA 즉시 이체 (목표: 월 +200만)"]
    
    RESERVE --> LEDGER["`가계부.md` 예수금 누적 잔액 자동 반영"]
```

---
