# 🚀 Phase 1 & 2: PRD and Implementation Plan

**Project:** 멀티 탭 그래프 뷰 전환 (RiC-O 기록물 vs 통합 지식베이스)
**Goal:** 상단 탭 메뉴를 통해 '기록물 검색'과 '지식검색(법, 지침, 연구자료 등)' 두 가지 완전히 다른 스키마의 지식 그래프를 하나의 웹 서비스에서 토글(Toggle)하여 볼 수 있도록 통합합니다.

---

## 📌 1. PRD (Product Requirements Document)
### Overview
현재 단일 뷰로 고정된 `index.html` 프론트엔드에 **[기록물 검색]** 및 **[지식 검색]** 탭 내비게이션을 신설합니다. 사용자가 탭을 전환하면 기존 Neo4j DB 안에 혼재되어 저장된 레거시 데이터(Law, Document, Chunk 등)와 신규 아카이브 데이터(RecordResource, Agent 등)를 명확히 분리하여 렌더링합니다.

### Requirements
- **메뉴 탭 UI 추가**: 최상단 헤더 중앙 혹은 좌측에 직관적인 탭(버튼) UI를 신설.
- **백엔드 라우팅 분기**: `/api/graph` 에 `type` 파라미터를 추가하여 쿼리 레이블 필터링을 분기 처리.
  - `?type=record`: `[RecordResource, Agent, Activity, ...]`
  - `?type=knowledge`: `[Document, Chunk, Entity, Law, Article, ...]`
- **동적 범례(Legend) 및 색상 변환**: 탭 전환 시 조회되는 노드 종류가 완전히 달라지므로, **좌측의 팝업 범례 창과 색상 매핑을 모듈화**하여 탭에 맞춰 실시간으로 교체(Re-mount)해야 합니다.

---

## 📝 2. Task Breakdown (작업 계획)

### [ ] Task 1: 백엔드 API 쿼리 다중화 (`src/web_app.py`)
- `/api/graph` 라우트를 수정하여 쿼리 파라미터 `type`을 받습니다.
- `type == 'knowledge'` 일 경우 `MATCH (n) WHERE labels(n)[0] IN ['Document', 'Chunk', 'Entity', 'Law', 'Article', 'Department', 'Judgment']` 로 변경된 전용 Cypher 쿼리를 실행하여 반환하도록 로직을 추가합니다.

### [ ] Task 2: 상단 탭 메뉴 CSS 및 HTML 생성 (`templates/index.html`)
- 헤더 영역에 `<div id="tabs">` 컴포넌트를 만들고 활성화(Active) 애니메이션 효과를 부여합니다.

### [ ] Task 3: 프론트엔드 동적 렌더링 함수 구현 (`templates/index.html`)
- `loadGraph(type)` 함수를 만듭니다. 
- 이 안에서 API를 `fetch`하고, 가져온 데이터가 지식용인지 기록물용인지에 따라:
  - 노드의 색상 분기 로직 재정의 (`Entity`는 파란색, `Law`는 빨간색 등).
  - 범례(Legend Panel)의 HTML 텍스트를 대상 종류에 맞게 통째로 바꿔치기합니다.
- Timeline 슬라이더 UI는 '기록물 검색' 탭에서만 보이도록 시각적으로 제어합니다(지식베이스 탭에서는 불필요할 수 있으므로).

---
**Status:** ⏳ Waiting for your approval. (단일 DB에서 두 마리 토끼를 잡는 이 계획에 동의하시면 '승인' 또는 '진행해' 라고 말씀해 주세요!)
