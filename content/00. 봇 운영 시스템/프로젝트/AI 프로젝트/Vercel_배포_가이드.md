---
title: "Vercel 무료 호스팅 및 PWA 배포 가이드"
date: 2026-09-01
tags:
  - deployment
  - vercel
  - pwa
  - guide
작성자: 아린
관련:
  - "[[인물사전_프로젝트]]"
  - "[[00_봇_운영_시스템]]"
---

# 🚀 Vercel 무료 호스팅 및 PWA 배포 가이드

> **목적**: 인물 사전 PWA 웹앱을 Vercel을 통해 무료로 빠르고 안정적으로 배포하는 방법 정리.

---

## 1. Vercel 배포 개요 및 장점
- **무료 플랜 (Hobby Tier)**: 개인 프로젝트에 최적, HTTPS 자동 지원, 글로벌 CDN, GitHub 연동 자동 배포.
- **PWA 지원**: HTTPS가 기본 제공되므로 모바일 기기(iOS/Android)에서 '홈 화면에 추가' 및 오프라인 캐싱 기능(Service Worker)이 원활히 동작함.

---

## 2. 배포 방법 1: GitHub 연동 자동 배포 (추천)

1. **GitHub 저장소 준비**
   - 프로젝트 코드를 GitHub 리포트에 푸시합니다.
   - 예: `person-dict` 리포트 생성 및 코드 업로드.

2. **Vercel 프로젝트 연결**
   - [Vercel 대시보드](https://vercel.com/) 접속 및 로그인 (GitHub 계정 연동).
   - **[Add New...]** -> **[Project]** 클릭.
   - 배포할 GitHub 리포트(`person-dict`) 선택 후 **[Import]**.

3. **빌드 설정 (Build & Development Settings)**
   - **Framework Preset**: Vite, Next.js, React 또는 Static (HTML/JS의 경우 기본 설정 유지).
   - **Build Command**: `npm run build` (또는 정적 HTML인 경우 빈칸 또는 생략).
   - **Output Directory**: `dist` (또는 빌드 결과물 폴더).
   - **Root Directory**: `./` (기본값)

4. **환경 변수 설정 (Environment Variables)**
   - 필요한 경우 `Environment Variables` 탭에서 API 키 등 설정.

5. **Deploy 완료**
   - **[Deploy]** 버튼 클릭 시 몇 초 내 배포 완료 및 고유 도메인(`*.vercel.app`) 발급.

---

## 3. 배포 방법 2: Vercel CLI를 이용한 수동/빠른 배포

1. **Vercel CLI 설치**
   ```bash
   npm i -g vercel
   ```

2. **로그인 및 배포**
   ```bash
   vercel login
   vercel
   ```
   - 프롬프트 안내에 따라 프로젝트 설정 확인 후 배포 진행.
   - 프로덕션 배포 시:
     ```bash
     vercel --prod
     ```

---

## 4. PWA 최적화 체크리스트 (배포 시 필수 확인)

- [ ] **HTTPS 적용 여부**: Vercel은 기본 제공되므로 OK.
- [ ] **Web App Manifest (`manifest.json`)**: 앱 이름, 아이콘, 시작 URL, 디스플레이 모드(`standalone`) 설정 확인.
- [ ] **Service Worker 등록**: 브라우저 오프라인 캐싱 및 푸시/로컬 저장 연동 확인.
- [ ] **모바일 반응형 디자인**: 스마트폰 화면에서 레이아웃 깨짐 없는지 확인.

---
_🕐 작성일: 2026-09-01 (아린)_
