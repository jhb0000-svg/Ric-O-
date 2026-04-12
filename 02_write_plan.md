# Task Plan - 8006 Service Hang Fix

## Context
Based on the approved Approach 1 from the Brainstorming Phase (@01_brainstorm.md), we will correct the event loop blocking issue by transforming all concurrent API handlers from `async def` to regular `def`. FastAPI will then manage them automatically via its internal thread pool. Finally, the service needs to be safely restarted and everything pushed to GitHub.

## Potential Breaking Changes
- Since we are simply removing `async` keywords from synchronous-style endpoint code that does not use `await`, there should be zero breaking changes to API consumers. 
- Local service performance may slightly change due to ThreadPool load, but stability will infinitely improve compared to the prior event loop deadlock.

## Task Breakdown

### 1. Code Fixes (Atomic Refactoring)
- [x] 1.1 In `src/web_app.py`, change `async def get_index():` to `def get_index():`.
- [x] 1.2 In `src/web_app.py`, change `async def get_graph(type: str = "record"):` to `def get_graph(type: str = "record"):`.
- [x] 1.3 In `src/web_app.py`, change `async def process_chat(req: ChatRequest):` to `def process_chat(req: ChatRequest):`.
- [x] 1.4 In `src/web_app.py`, change `async def get_document(doc_id: str):` to `def get_document(doc_id: str):`.

### 2. Service Restart & Verification
- [x] 2.1 Start the `uvicorn src.web_app:app --host 0.0.0.0 --port 8006 --reload` background process with `nohup` (saving logs to `web_app.log`).
- [x] 2.2 Verify the `/` and `/api/graph` endpoints using `curl` to ensure the server correctly responds without hanging.

### 3. Version Control (GitHub Push)
- [x] 3.1 `git add src/web_app.py` and commit with a clear message explaining the asyncio block fix.
- [x] 3.2 `git push` to synchronize changes to the remote GitHub repository.
