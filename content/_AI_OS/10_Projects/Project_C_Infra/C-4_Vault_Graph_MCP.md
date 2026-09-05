---
project_id: "C-4"
title: "볼트 그래프 탐색 전용 MCP 서버 (Vault Graph MCP)"
category: "Project C (Agentic Tools & Architecture)"
status: "진행전"
priority: "High"
created: 2026-08-31
updated: 2026-08-31
target_date: "2026-10-01"
tags:
  - ai-project
  - mcp-server
  - graph-traversal
  - llm-wiki
  - status/pending
---

# [[C-4_Vault_Graph_MCP]]

> 개요: Antigravity IDE가 옵시디언 볼트의 마크다운 위키링크([[...]]), YAML Frontmatter 메타데이터, 최상위 MOC를 고속 인메모리 그래프로 인덱싱하여, Vector RAG 없이도 직접 그래프를 순회(Graph Traversal)하며 환각 없이 의학 지식을 탐색할 수 있도록 지원하는 전용 MCP(Model Context Protocol) 서버.

---

## 🎯 1. 프로젝트 핵심 목표
* **최종 결과물**:
  1. FastMCP/Python 기반의 로컬 Vault Graph MCP 서버
  2. 주요 MCP 도구셋 (`get_node_metadata`, `traverse_links`, `get_moc_children`, `find_path_between_concepts`)
  3. 볼트 파일 변경 감지(File Watcher) 기반 실시간 그래프 인덱스 갱신 엔진
* **주요 성공 기준 (KPI)**:
  - [ ] 940+ 전체 마크다운 파일의 위키링크/Frontmatter 인덱싱을 1초 이내 완료
  - [ ] 3-Hop 이상의 복합 지식 경로(예: [[승모근]] $\to$ [[경추 염좌]] $\to$ [[갈근탕]] $\to$ [[갈근]]) 탐색 쿼리 지원
  - [ ] Antigravity와의 표준 stdio 통신 무결성 100% 확보
* **연동 인프라**: Antigravity IDE, Python 3.11+, NetworkX / Rust 기반 그래프 인덱서, Obsidian Vault

---

## 🧭 2. MCP 도구셋 및 그래프 순회 아키텍처

```mermaid
flowchart LR
    subgraph ANTIGRAVITY ["Antigravity IDE Agent"]
        QUERY["'갈근탕과 연관된 근육 및 적응 질환 경로 탐색'"]
    end

    subgraph MCP_SERVER ["C-4 Vault Graph MCP Server"]
        ROUTER["MCP Tool Router"]
        GRAPH[("NetworkX 인메모리\n지식 그래프")]
        WATCHER["Obsidian File Watcher\n(실시간 동기화)"]
    end

    subgraph OBSIDIAN ["옵시디언 볼트 (LLM Wiki)"]
        MOC["_MOC_Formulas / _MOC_Muscles"]
        MD_FILES["개별 마크다운 노트 (Frontmatter & [[Links]])"]
    end

    ANTIGRAVITY <-->|stdio (MCP Protocol)| ROUTER
    ROUTER <--> GRAPH
    WATCHER --> OBSIDIAN
    WATCHER --> GRAPH
```

### 📌 노출 MCP 도구(Tools) 명세
1. `vault_get_node(node_name)`: 특정 노트의 Frontmatter 속성 및 인/아웃바운드 링크 목록 반환
2. `vault_traverse_links(start_node, max_depth=2, filter_category=None)`: 시작 노드로부터 N단계 연결된 개념 순회
3. `vault_query_by_frontmatter(key, value)`: 특정 속성(예: `meridians: ["비경"]`)을 만족하는 노드 집합 조회
4. `vault_get_moc(moc_name)`: 지정 MOC([[_MOC_Herbs]] 등)의 직계 분류 트리 반환

---

## 💬 3. Grill Me & 아키텍처 의사결정 기록

> [!abstract]- 📌 질의응답 아카이브 (클릭하여 열기)
> **Q1. Vector 임베딩 DB 대비 MCP 그래프 탐색의 강점**
> - **결정**: 임베딩 유사도 검색의 고질적 한계인 '모호한 연관성 검색'과 '환각(Hallucination)'을 완전히 배제하고, 사람이 직접 구축한 엄격한 마크다운 위키링크 연결망만을 100% 신뢰하여 추론 정확도를 극대화함.

---

## ✅ 4. 세부 Task & 체크리스트

### 🏗️ Phase 1. 그래프 인덱서 및 파서 구축
- [ ] 마크다운 Frontmatter 및 [[...]] 정규식 추출 파서 작성
- [ ] NetworkX 기반 방향성 그래프(DiGraph) 데이터 구조 정립

### 💻 Phase 2. FastMCP 서버 구현 및 도구 등록
- [ ] stdio 기반 MCP 서버 스켈레톤 작성
- [ ] 4대 핵심 탐색 Tool 함수 구현 및 단위 테스트
- [ ] Antigravity `mcp_config.json`에 `vault-graph-mcp` 등록

---

## 🔗 5. 관련 리소스 및 백링크
* **마스터 로드맵**: [[00_Project_A_Master_Roadmap]]
* **대시보드**: [[00_Master_Dashboard]]
* **연계 프로젝트**: [[A-1_Clinical_Knowledge_DB]], [[B-4_Vault_Gardener_Agent]], [[C-1_AI_Coding_Environment]]
