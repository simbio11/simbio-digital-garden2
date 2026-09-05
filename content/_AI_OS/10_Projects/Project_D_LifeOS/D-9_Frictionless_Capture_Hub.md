---
project_id: "D-9"
title: "제로 프릭션 인박스 캡처 및 AI 자율 분류 허브"
category: "Project D (Personal OS)"
status: "진행중"
priority: "High"
created: 2026-09-03
updated: 2026-09-03
target_date: "2026-09-30"
tags:
  - ai-project
  - inbox-capture
  - auto-organizer
  - zero-friction
  - status/in-progress
---

# [[D-9_Frictionless_Capture_Hub]]

> 개요: 디스코드나 텔레그램 봇 채팅창에 아이디어, 할 일, 링크 등을 형식 없이 툭 던지면 인박스(`00. Inbox`)에 즉시 수집되고, 주기적(또는 야간)으로 AI 에이전트가 이를 분석하여 적절한 폴더(데일리노트, 일정표, 지식 노트 등)로 알아서 자율 분류 및 위키링크를 연결해 주는 무중력 캡처 허브.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. 챗봇 인터페이스 기반 제로 프릭션 인박스 수집기 (메시지 $\rightarrow$ `Inbox.md` 자동 Append)
  2. 야간 볼트 가드너 / 인박스 오토 오거나이저 크론 작업 (미분류 노트 내용 분석 및 타겟 노트로 자동 이동/링크)
  3. 분류 완료 후 요약 리포트 디스코드 DM 발송
* **주요 성공 기준 (KPI)**:
  - [ ] 어떤 형태의 잡담이나 메모든 단 1초만에 봇을 통해 인박스에 적재
  - [ ] AI가 문맥을 파악해 80% 이상 정확도로 알맞은 폴더 및 데일리노트로 자동 분배

---

## 📥 2. 제로 프릭션 캡처 & 자율 분류 아키텍처
```mermaid
flowchart TD
    USER["비오님 (디스코드/텔레그램 툭 던지기)"] --> BOT["아린/비비 챗봇 캡처 인터페이스"]
    BOT --> INBOX["옵시디언 `00. Inbox` 실시간 적재"]
    
    INBOX --> AGENT["야간 자율 분류 에이전트 (AI 분석)"]
    
    AGENT --> CATEGORY{"문맥 분석 및 분류"}
    CATEGORY --> |"일정/약속"| CALENDAR["`일정표.md` 또는 데일리노트"]
    CATEGORY --> |"아이디어/프로젝트"| PROJECT["`_AI_OS/10_Projects/`"]
    CATEGORY --> |"임상/학술 지식"| VAULT["`5. 독서, 노트/` MOC"]
```

---
