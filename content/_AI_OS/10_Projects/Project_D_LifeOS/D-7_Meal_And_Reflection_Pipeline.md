---
project_id: "D-7"
title: "식단 체크인 및 저녁 하루 회고 자동화 파이프라인"
category: "Project D (Personal OS)"
status: "완료"
priority: "High"
created: 2026-09-03
updated: 2026-09-03
target_date: "2026-09-03"
tags:
  - ai-project
  - meal-recording
  - daily-reflection
  - cron-automation
  - status/completed
---

# [[D-7_Meal_And_Reflection_Pipeline]]

> 개요: 점심(13:30)과 저녁(20:30) 식단 기록 여부를 옵시디언 파일에서 선행 검증한 뒤 미기록 시에만 다정하게 체크인을 유도하고, 밤 23:00에는 하루의 회고와 데일리노트 업데이트를 진행하는 라이프 케어 자동화 시스템.

---

## 🎯 1. 구축 완료된 핵심 기능 및 크론 봇
* **구현된 파이프라인**:
  1. **점심 식단 체크인 크론 (`66516f5fd6e9`)**: 매일 13:30 실행 (`meal-recording` 스킬), 식단 파일 확인 후 미기록 시 안내
  2. **저녁 식단 체크인 크론 (`65376e5551ca`)**: 매일 20:30 실행, 저녁 식단 기록 확인 및 피드백
  3. **저녁 하루 회고 크론 (`a14aaec752d7`)**: 매일 23:00 실행, 하루 일과 회고 및 데일리노트 갱신
* **연동 경로**: `C:\Simbio\00. 봇 운영 시스템\생활관리\식단\` 및 `일일노트/`

---
