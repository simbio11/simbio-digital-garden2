# 🔬 임상지식 RAG 파일럿 (rag_pilot)

> **목적**: 마스터플랜 Phase 2~4 [x] 완료 노트를 재료로 "좁은 RAG 파일럿"을 검증한다.
> 닥터허 제안(좁은 파일럿 → 20문항 평가 → 스케일업) + 비비 수급안(OASIS/PubMed)의 코드 구현부.
>
> **상태**: 2026-09-04 카이 1차 구동 — ✅ 청크화 133청크 / ✅ 로컬 검색 동작 확인

## 구성
```
rag_pilot/
├── ingest_vault.py    # 마스터플랜 [x] 추출 → 볼트 노트 → ## 섹션 청크 → data/chunks.jsonl
├── search_pilot.py    # 청크 검색 (한국어 char n-gram TF-IDF, sklearn)
└── data/chunks.jsonl  # 생성물 (15노트 → 133청크, 66,515자)
```

## 실행
```bash
python ingest_vault.py                                  # 청크 재생성
python search_pilot.py "감초 금기, 저칼륨혈증" --top 2   # 단일 검색
python search_pilot.py --questions data/questions_sample.json --top 3   # 배치 평가
python search_pilot.py --questions data/평가셋_20문항.json --top 3       # 닥터허 20문항 제출 후
```

## 검증 결과 (2026-09-04)
| 질문 | TOP1 적중 |
|---|---|
| 감초 금기·저칼륨혈증 | 감초 ##4 금기 섹션 ✅ |
| 다리 쥐남 경련 완급지통 | 감초 ##6 처방매트릭스(작약감초탕) ✅ |
| 대흉근 유방통 연관통 | 대흉근 ##4 치료 포인트 ✅ |

## ⚖️ evidence_type 스키마 표준 (전 봇 합의안 — 닥터허 근거 분리 설계)
| 값 | 의미 | 출처 예 |
|---|---|---|
| `vault_note` | 비오님 큐레이션 볼트 노트 (1순위 재료) | `2. 약리 공부/본초(약리)/감초.md` |
| `clinical` | 임상 논문 (메타+초록) | OASIS, PubMed, KCI OAI-PMH |
| `cpg` | 임상진료지침 (권고등급 A/B/C 포함) | NIKOM KM-CPG 30종 |
| `classic` | 원전·정제 고전 텍스트 | KTP, OASIS 고의서 |

**답변 생성 시 라벨이 섞이지 않게**: `clinical`과 `classic`을 같은 근거로 제시하지 않는다 (닥터허 조건).

## 📦 비비 수급물 papers.jsonl 스키마 (2026-09-04 합의)
```json
{"title": "", "authors": [], "year": 0, "journal": "", "doi": "",
 "url": "", "abstract": "", "keywords": [], "evidence_type": "clinical", "source_db": "OASIS"}
```
→ ingest/search 양쪽 모두 `evidence_type` 기준으로 필터·라벨링 가능.

## 배치 평가 인터페이스 (2026-09-04 카이 구현 — 심비오트 판정 ②)

`--questions`로 Q&A JSON을 읽어 문항별 적중/탈락 + 카테고리별 적중률 + 근거 라벨 검사를 리포트한다.

**평가셋 JSON 스키마** (닥터허 제출용, 예시: `data/questions_sample.json`):
```json
[
  {"id": 1, "category": "처방 감별", "question": "...",
   "expected_docs": ["감초"], "answer_contains": "작약감초탕"}
]
```
- 적중 판정: TOP3 청크에 `expected_docs` 문서 포함 OR `answer_contains` 핵심어 본문 포함
- 통과 기준 (심비오트 판정 ④): 적중률 ≥80% + 근거 라벨 혼동 0건 — 스크립트가 자동 판정
- 라벨: `data/chunks.jsonl` 전체에 `evidence_type` 필드 존재 (현재 전부 `vault_note`). OASIS 논문 병합 시 `clinical` 라벨 추가 → 혼동 검사 자동 가동

## 자동화 로드맵 (어디까지 자동인가)
| 단계 | 자동화 | 비고 |
|---|---|---|
| ① 볼트 [x] 노트 → 청크 | ✅ 100% | 마스터플랜 파싱 → 위키링크 → 섹션 분할 |
| ② 20문항 평가세트 실행 | ✅ 100% | search_pilot.py에 질문 파일 읽기 추가만 하면 됨 |
| ③ OASIS 논문 메타 수집 | 🟡 80% | 사이트 실사 완료(oasis.kiom.re.kr 응답 OK), 엔드포인트 1회 확인 필요. 공공데이터포털 OASIS 파일데이터가 더 안정적 후보 |
| ④ PubMed E-utilities | 🟡 90% | esearch/efetch 표준 API, 키 불필요 |
| ⑤ 임베딩 벡터 검색 | 🟠 50% | openai text-embedding-3-small 연동 자리(search_pilot.embed) 준비, config 키 연동만 남음 |
| ⑥ 답변 생성 + 출처 라벨 | 🟠 40% | "원전 근거" vs "임상논문 근거" 라벨 분리 스키마 필요 (닥터허 조건) |

## 다음 액션 (파일럿 통과 기준)
1. 닥터허 20문항 → `data/평가셋_20문항.json` 수령 → `python search_pilot.py --questions data/평가셋_20문항.json` 실행 (배치 인터페이스 ✅, 샘플 8문항 100% 검증 완료)
2. 통과 시: 임베딩 계층 활성화 + OASIS/PubMed 수집 파이프라인 (단계 ③④)
3. 재료 확장: 볼트 노트가 더 차면 `ingest_vault.py` 재실행만 하면 자동 반영

## 주의
- 볼트 노트는 비오님 개인 학습 자료. **외부 배포 금지**.
- 교과서·표준처방집 크롤링은 저작권 리스크 — 비오님 소지 자료만 개인 정제(비비 의견 동의).
