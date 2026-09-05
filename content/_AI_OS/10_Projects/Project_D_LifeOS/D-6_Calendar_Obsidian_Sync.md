---
project_id: "D-6"
title: "구글 캘린더 ↔ 옵시디언 일정표 양방향 동기화 및 아침 리마인드"
category: "Project D (Personal OS)"
status: "완료"
priority: "High"
created: 2026-09-03
updated: 2026-09-03
target_date: "2026-09-03"
tags:
  - ai-project
  - calendar-sync
  - obsidian
  - cron-automation
  - status/completed
---

# [[D-6_Calendar_Obsidian_Sync]]

> 개요: 구글 캘린더(`cmkschcmksch@gmail.com` primary + Family)와 옵시디언 일정표 미러링 파일(`C:\Simbio\5. 독서, 노트\일정관리\일정표.md`)을 매일 아침 자동으로 동기화하고, 당일 일정을 정리하여 디스코드 DM으로 리마인드하는 아침 브리핑 파이프라인.

---

## 🎯 1. 구축 완료된 핵심 기능 및 크론 봇
* **구현된 파이프라인**:
  1. **매일 08:45 일정 동기화 크론 (`d3399cfab632`)**: 구글 캘린더 API를 통해 당일 일정을 조회하고 옵시디언 일정표 및 데일리 노트에 마크다운 형태로 자동 미러링
  2. **아침 맞춤 브리핑**: 보건지소 근무 시간(09:00~18:00) 및 개인 일정을 고려한 친근한 아침 리마인드 발송
* **연동 경로**: `C:\Simbio\5. 독서, 노트\일정관리\일정표.md`

---
