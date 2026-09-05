# 인물 사전 PWA (person-dict)

만난 사람을 기록하고 감정·관계 깊이·비즈니스/사적 관계를 관리하는 **로컬 우선(offline-first) PWA** 웹앱 프로토타입.

## 스택

- 순수 HTML + Tailwind CSS (CDN 없음, 로컬 빌드) + Vanilla JS
- 브라우저 `localStorage` 기반 영구 저장 (서버 불필요)
- PWA: `manifest.webmanifest` + 서비스 워커(`sw.js`) → 모바일 홈 화면 설치 & 오프라인 동작

## 주요 기능

- **인물 CRUD**: 이름 / 만난 장소 / 첫 만남 날짜 / 감정 상태(좋음·보통·어려움) / 관계 깊이(1~5 레벨) / 관계 태그(비즈니스·사적·가족·학교·모임) / 메모
- **검색 & 필터**: 이름·장소·메모 검색, 비즈니스/사적/최고 친밀/최근 추가 필터
- **통계**: 전체 인물 / 비즈니스 / 사적 관계 수
- **백업/복원**: JSON 파일 내보내기(⬇ 백업) & 불러오기(⬆ 복원)
- **설치 배너**: Android/iOS 홈 화면 추가 안내 (beforeinstallprompt, iOS Safari 안내 포함)
- **오프라인**: 서비스 워커가 앱 셸 캐싱, 오프라인에서도 읽기·추가·수정 가능

## 실행

```bash
npm install        # tailwindcss 설치
npm run build      # tailwind.css 생성 (public/tailwind.css)
npm start          # http://localhost:4173
```

## 배포 (Vercel)

`vercel.json` 포함 — Vercel 대시보드에서 저장소 연결 후:
- Framework Preset: **Other / Static** (자동 감지됨)
- Build Command: `npm run build`
- Output Directory: `public`

상세 가이드: `C:/Simbio/00. 봇 운영 시스템/프로젝트/AI 프로젝트/Vercel_배포_가이드.md`

## 프로젝트 구조

```
public/
  index.html            # 앱 셸
  app.js                # 로직 (CRUD, 검색/필터, 백업/복원, PWA 설치)
  tailwind.css          # 빌드된 스타일
  manifest.webmanifest  # PWA 매니페스트
  sw.js                 # 서비스 워커 (오프라인 캐싱)
  icons/                # 192/512 + maskable 아이콘
src/input.css           # Tailwind 소스 (커스텀 컴포넌트 클래스)
scripts/gen_icons.py    # 아이콘 생성 스크립트 (PIL)
```

## 데이터 스키마 (localStorage: `person-dict.v1`)

```json
{
  "id": "lxyz123",
  "name": "김비비",
  "place": "커피빈 강남점",
  "metAt": "2026-08-15",
  "emotion": "good | neutral | hard",
  "level": 1,          // 1~5
  "tags": ["business", "personal", "family", "school", "community"],
  "memo": "…",
  "createdAt": 1788250000000,
  "updatedAt": 1788250000000
}
```
