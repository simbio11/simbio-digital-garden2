# 🔬 FM 일괄 삽입 · 마이그레이션 실행 설계 (rag_pilot 기준)

> **상태**: 설계 초안 — SCHEMA v1.2 확정 + 비오님 승인 후 구현 (2026-09-04)
> **원칙**: 본문 불가침 · FM은 메타로 승격 · 드라이런 선행 · 리그레션 증명 후 apply

## 판정 파이프라인 (migrate_fm.py)

입력 노트 1건 → 아래 4단계로 신규 FM 결정:

1. **폴더 경로 분기 (최우선)** — RAG 대상 폴더 → type 기본값
   - `2. 약리 공부/본초(약리)/` → `type: herb`
   - `처방/` → `type: formula`
   - `근골격계/` → `type: muscle`
   - `약리성분/` → `type: compound` (+분류 태그 `성분`)
   - `양방 약/` → `type: compound` (+분류 태그 `양방약`)
   - `의학개념/` → `type: concept` (호르몬·치료기법·개념)
   - `질환/` → `type: disease`
2. **헤더 1줄 파싱** (FM 없을 때만) — `# 🌿 [[감초]] (한자, 학명)` 정규식 → title(짧은 한글) + aliases(한자·학명)
3. **기존 type 값 → 2차 확인용** — "폴더와 일치할 때만" 신뢰, 불일치 시 override 테이블 확인
4. **override 테이블 (명시적 예외)** — 기존 type를 무조건 덮는 화이트리스트
   - `약리성분/*` → compound (기존 `의학개념` 무시) — hyperforin·위타놀라이드
   - `양방 약/*` → compound + 양방약 (기존 `의학개념` 무시) — 세마글루타이드·콜히친
   - `본초(약리)/매스틱|세인트존스워트|아슈와간다` → herb + `외국본초` 태그 (evidence 라벨 폴백)

## FM 생성 규칙 (비파괴)

- 기존 FM 키 100% 보존. `aliases`는 **자기 파일명(stem)과 동일한 항목만** 제거 — 교근·측두근의 중복
- 필수: title / type / evidence_type / created / status
  - status 기본값: `drafting` (기존 완성 노트는... QC 판정은 닥터허 담당 — 기본값 합의 필요)
- 제거 금지 태그(`개념사전` 35·`excalidraw` 21 등) → `_migration_unmapped.md`에 모음 (드롭 금지)
- **외국본초 3종은 `type: herb` + `외국본초` 태그** — 원전 근거 없어도 evidence_type=vault_note 폴백으로 라벨 체계 유지

## 마이그레이션 후 ingest 파이프라인 영향 (카이 검토)

- `split_sections()`에 FM 스트립 1함수 추가: `---` 블록 파싱 → meta로 분리 → content 제거
- chunk 메타 확장: `fm_type` / `fm_tags` / `fm_status` / `title` / `wiki_name`
- **doc_title = FM title(짧은 한글)**, wiki_name으로 마스터플랜 링크명 보존 → gold_docs 매칭 유지
- evidence_type: FM 값 우선, 없으면 vault_note 폴백
- **청크 ID는 `wiki_name#n` 유지** — 기존 133청크와 1:1 대응, phase1 리그레션(12/12) 검증 용이
