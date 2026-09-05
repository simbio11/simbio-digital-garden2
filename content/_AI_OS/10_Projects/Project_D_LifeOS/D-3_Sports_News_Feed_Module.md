---
project_id: "D-3"
title: "스포츠 뉴스 피드 모듈 (네이버 API & 30분 단위 스마트 캐싱)"
category: "Project D (Personal OS)"
status: "진행전"
priority: "Low"
created: 2026-08-30
updated: 2026-08-31
target_date: "2026-10-15"
tags:
  - ai-project
  - sports-feed
  - naver-api
  - caching-layer
  - status/pending
---

# [[D-3_Sports_News_Feed_Module]]

> 개요: 네이버 검색/뉴스 API를 활용하여 사용자가 관심 등록한 스포츠 종목(축구, 야구, 러닝/마라톤 등) 및 특정 팀/선수의 최신 경기 결과와 핵심 뉴스를 30분 단위 스마트 캐싱으로 수집하여 라이프 매니저 대시보드에 컴팩트하게 노출하는 피드 모듈.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. 네이버 Open API 기반 스포츠 뉴스/스코어 수집 파이프라인
  2. 30분 TTL(Time-to-Live) 로컬 파일/메모리 캐싱 레이어
  3. 라이프 매니저 대시보드 상단 1-Line 스포츠 스코어보드 & 피드 UI
* **주요 성공 기준 (KPI)**:
  - [ ] 불필요한 가십/어그로성 기사를 제거하고 경기 결과/선발/하이라이트 중심 필터링
  - [ ] 30분 이내 중복 요청 시 네이버 API 호출 없이 로컬 캐시에서 5ms 내 즉시 렌더링
  - [ ] 관심 키워드(예: '토트넘', '손흥민', '기아타이거즈', '순천 마라톤') 커스텀 설정 지원
* **연동 인프라**: Naver Search Open API, Python FastAPI / Local Cache, Life Manager Dashboard

---

## ⚽ 2. 뉴스 수집 및 30분 캐싱 파이프라인

```mermaid
flowchart LR
    A["클라이언트 요청\n(스포츠 피드 조회)"] --> B{"30분 캐시(`sports_cache.json`) 유효?"}
    
    B -- "YES (캐시 유효)" --> C["로컬 캐시 즉시 반환 (5ms)"]
    B -- "NO (만료/미존재)" --> D["네이버 뉴스 API 호출 (관심 키워드)"]
    
    D --> E["노이즈 필터링 & 랭킹 스코어링"]
    E --> F["`sports_cache.json` 저장 (TTL 30분 갱신)"]
    F --> C
```

---

## 💬 3. Grill Me & 아키텍처 의사결정 기록

> [!abstract]- 📌 질의응답 아카이브 (클릭하여 열기)
> **Q1. API 일일 호출 제한(Quota) 초과 방지**
> - **결정**: 네이버 무료 API 쿼터(일 25,000회)는 30분 주기 단일 캐싱 구조로 운영 시 하루 48회만 호출되므로 쿼터의 0.2% 미만으로 극도로 여유롭게 운영 가능함.

---

## ✅ 4. 세부 Task & 체크리스트

### 🏗️ Phase 1. 네이버 API 클라이언트 및 필터 구축
- [ ] 네이버 Client ID/Secret 연동 및 검색 쿼리 모듈 작성
- [ ] 스팸/가십 기사 제외 정규식 블랙리스트 작성

### 💻 Phase 2. 캐싱 레이어 및 UI 위젯 연동
- [ ] TTL 30분 파일 기반 캐시 관리자 구현
- [ ] 라이프 매니저 프론트엔드 스포츠 피드 컴포넌트 개발

---

## 🔗 5. 관련 리소스 및 백링크
* **마스터 로드맵**: [[00_Project_A_Master_Roadmap]]
* **대시보드**: [[00_Master_Dashboard]]
* **연계 프로젝트**: [[D-1_Life_Manager_Bugfixes]]
