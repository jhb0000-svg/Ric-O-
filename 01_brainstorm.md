# Product Requirements Document (PRD) - 8006 Service Hang Fix

## 1. Context & Problem Statement
The user reported that the service running on port 8006 (`RiC-O Graph Viewer` running via FastAPI/Uvicorn) is behaving strangely and freezing.
Upon investigation, the server process was stuck and unresposive to any HTTP requests (including `curl`). 

**Root Cause:**
FastAPI routes (`get_index`, `get_graph`, `process_chat`, `get_document`) are declared as `async def`. However, inside these endpoints, standard synchronous blocking operations are heavily utilized:
1. File I/O (`open().read()`)
2. Synchronous Database queries (`Neo4jClient.execute_query` using the standard blocking Neo4j driver)
3. Synchronous HTTP requests (`urllib.request.urlopen` to the vLLM server with a 60-second timeout)

In FastAPI, functions declared with `async def` are run directly on the main event loop. If they block, the entire server process is blocked from handling incoming concurrent requests. A slow vLLM inference or Neo4j query will deadlock the event loop entirely.

## 2. Proposed Technical Approaches

### Approach 1: Convert `async def` to `def` (Recommended)
FastAPI is designed such that if an endpoint is declared with `def` rather than `async def`, it will automatically execute the function in an isolated background thread pool (using `starlette.concurrency.run_in_threadpool`). 
* **Pros:** Simplest and safest fix. Requires minimal code changes (just removing `async` from the route definitions). Avoids the need for new dependencies.
* **Cons:** Less parallel concurrency compared to true async programming, but perfectly acceptable for this workload.

### Approach 2: Migrate to Pure Asynchronous Libraries
Refactor all blocking calls to use truly asynchronous equivalents:
* Replace `urllib.request` with `httpx.AsyncClient`.
* Replace standard Neo4j driver connection with `neo4j.AsyncGraphDatabase`.
* Replace standard `open` with `aiofiles`.
* **Pros:** Best performance under high load.
* **Cons:** Requires adding new dependencies (`httpx`, `aiofiles`) and extensive code refactoring, which introduces higher risk.

### Approach 3: Wrap Blocking Calls with `asyncio.to_thread`
Keep the `async def` signatures but explicitly wrap the blocking code segments (the Neo4j queries and the `urlopen` definitions) in `asyncio.to_thread(...)`.
* **Pros:** Keeps the async route signature.
* **Cons:** Makes the code more verbose and harder to maintain compared to Approach 1.

## 3. Implementation Plan (Phase 1)
We will proceed with **Approach 1** due to its minimal footprint and maximum stability.

1. **Modify `src/web_app.py`:**
   - Change `async def get_index():` to `def get_index():`
   - Change `async def get_graph(type: str = "record"):` to `def get_graph(type: str = "record"):`
   - Change `async def process_chat(req: ChatRequest):` to `def process_chat(req: ChatRequest):`
   - Change `async def get_document(doc_id: str):` to `def get_document(doc_id: str):`
2. **Restart the Uvicorn Process:** 
   - Terminate the currently hung process (Already Done).
   - Ensure `uvicorn` restarts smoothly with `--reload` or explicitly start it.
3. **Verify Functionality:** 
   - Ensure the server processes parallel requests correctly without locking up.

## 4. User Approval Required
Please review the problem analysis and confirm if **Approach 1** is acceptable ("Approved" or "LGTM"). Once approved, we will proceed to Phase 2 (Write Plan).
