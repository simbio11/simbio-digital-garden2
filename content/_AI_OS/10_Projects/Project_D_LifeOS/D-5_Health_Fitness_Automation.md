---
project_id: "D-5"
title: "삼성 헬스 & 구글 피트니스 자동 연동 및 생활관리 대시보드"
category: "Project D (Personal OS)"
status: "완료"
priority: "High"
created: 2026-09-03
updated: 2026-09-03
target_date: "2026-09-03"
tags:
  - ai-project
  - health-fitness
  - google-fit
  - cron-automation
  - status/completed
---

# [[D-5_Health_Fitness_Automation]]

> 개요: 갤럭시워치(삼성헬스)와 구글 피트니스 API 연동을 통해 걸음수, 칼로리, 운동 데이터를 자동으로 수집하고, 매일 10시 자동 보정 크론 및 매일 21시 운동 리마인드 루틴을 통해 옵시디언 생활관리 대시보드(`C:\Simbio\00. 봇 운영 시스템\생활관리\운동\index.md`)와 완벽 동기화하는 라이프 OS 핵심 건강 파이프라인.

---

## 🎯 1. 구축 완료된 핵심 기능 및 크론 봇
* **구현된 파이프라인**:
  1. **구글 피트니스 OAuth 연동**: `fitness.activity.read` 스코프 기반 정밀 운동 데이터 수집 (`google_token.json`)
  2. **매일 10:00 운동 기록 자동 보정 크론 (`d7765d226d6a`)**: 전날 걸음수·칼로리 데이터를 산출하여 로컬 대시보드 자동 갱신
  3. **매일 21:00 운동 리마인드 & 기록 봇 (`7ff819432bb2`)**: 오늘의 운동 루틴 추천 및 다정한 운동 독려 텔레그램/디스코드 DM 발송
* **연동 경로**: `C:\Simbio\00. 봇 운영 시스템\생활관리\운동\` (월별/주차별 Markdown 대시보드)

---
