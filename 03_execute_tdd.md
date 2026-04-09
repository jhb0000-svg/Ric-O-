# 💻 Phase 3: Execute & TDD Log

모든 설계된 Task를 완료했습니다.

### [x] Task 1: 백엔드 - 원문 데이터 연람 API 구축
- `@app.get("/api/document/{doc_id}")` FastAPI 라우터 추가
- `sample_records/` 경로에서 직접 파일을 읽어와 JSON 형태로 렌더링하도록 반영 완.

### [x] Task 2: 프론트엔드 - 뷰 모드 토글 UI
- 상단 영역에 `🕸️ 그래프 뷰`, `📋 목록 뷰` 버튼 삽입.
- Javascript 기반 `toggleView()` 콜백 바인딩 처리 완.

### [x] Task 3: 프론트엔드 - 검색 결과의 렌더링 (목록 뷰)
- `updateListView()` 함수 작성.
- 다중 필터(AND/OR) 및 챗봇 검색으로 발생한 교집합 노드들만을 인자로 받아 `display:table` DOM 엘리먼트를 동적 생성.

### [x] Task 4: 프론트엔드 - 그래프 노드 클릭 팝업 이벤트
- Vis.js의 `network.on("click")` 리스너를 활용해 노드가 클릭될 때 툴팁(#nodePopup)을 노출하고, `관련 기록물 조회하기` 버튼 렌더링.

### [x] Task 5: 프론트엔드 - 관련 기록물 모달(Modal) 뷰
- 클릭된 객체와 그래프상 1-Hop Edge로 묶인 `RecordResource` 타입의 엔티티들을 모두 파싱.
- 500px 너비의 검정 반투명 오버레이 패널(`recordsModalOverlay`)에 목록을 띄우는 `openRecordsModal()` 구축 완.

### [x] Task 6: 프론트엔드 - 원문 텍스트 뷰어
- `fetch('/api/document/XXX')` 비동기 호출 구축.
- 원문 데이터를 받아서 띄워주는 풀스크린 리더 오버레이(`docViewerOverlay`) 구현 완료.
