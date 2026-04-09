from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import os
from src.neo4j_client import Neo4jClient

app = FastAPI(title="RiC-O Graph Viewer")

def get_db():
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    if os.environ.get("TEST_MODE") == "1":
        return None
    try:
        client = Neo4jClient(uri, user, password)
        return client
    except Exception:
        return None

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", "index.html"), "r") as f:
        return f.read()

@app.get("/api/graph")
async def get_graph(type: str = "record"):
    client = get_db()
    
    if not client:
        return {"nodes": [], "edges": []}
        
    try:
        if type == "knowledge":
            labels_filter = "['Document', 'Chunk', 'Entity', 'Law', 'Article', 'Department', 'Judgment']"
        else:
            labels_filter = "['RecordResource', 'Agent', 'Activity', 'Organization', 'Mandate', 'Date']"

        query = f"""
        MATCH (n)-[r]->(m) 
        WHERE labels(n)[0] IN {labels_filter} 
          AND labels(m)[0] IN {labels_filter}
        RETURN id(n) as source_id, labels(n)[0] as source_label, coalesce(n.name, n.id) as source_name, 
               type(r) as rel_type, 
               id(m) as target_id, labels(m)[0] as target_label, coalesce(m.name, m.id) as target_name 
        LIMIT 2000
        """
        results = client.execute_query(query)
        client.close()
        
        nodes_dict = {}
        edges = []
        for row in results:
            src_id = row['source_id']
            tgt_id = row['target_id']
            nodes_dict[src_id] = {"id": src_id, "label": row['source_label'], "title": row['source_name'] or str(src_id)}
            nodes_dict[tgt_id] = {"id": tgt_id, "label": row['target_label'], "title": row['target_name'] or str(tgt_id)}
            edges.append({"from": src_id, "to": tgt_id, "label": row['rel_type']})
            
        return {
            "nodes": list(nodes_dict.values()),
            "edges": edges
        }
    except Exception as e:
        return {"error": str(e), "nodes": [], "edges": []}

from pydantic import BaseModel
import re

class ChatRequest(BaseModel):
    query: str
    type: str = "record"

@app.post("/api/chat")
async def process_chat(req: ChatRequest):
    client = get_db()
    if not client:
        return {"answer": "데이터베이스 연결에 실패했습니다.", "focus_nodes": []}
    
    query_text = req.query
    # Remove common Korean postpositions and punctuation
    cleaned_query = re.sub(r'(은|는|이|가|에|에서|의|로|으로|을|를|과|와)(?=\s|$)', '', query_text)
    cleaned_query = re.sub(r'[^\w\s]', '', cleaned_query)
    
    stop_words = ["찾아줘", "무엇인가", "어떻게", "기록물", "문서", "자료", "알려줘", "대해", "관련된", "생산한", "작성한"]
    keywords = [word for word in re.split(r'\s+', cleaned_query) if len(word) > 1 and word not in stop_words]
    if req.type == "knowledge":
        labels_filter = "['Document', 'Chunk', 'Entity', 'Law', 'Article', 'Department', 'Judgment']"
    else:
        labels_filter = "['RecordResource', 'Agent', 'Activity', 'Organization', 'Mandate', 'Date']"

    focus_nodes = []
    found_names = []
    try:
        if keywords:
            # Build WHERE clause dynamically to match node names or IDs inside the current tab's scope
            where_clauses = " OR ".join([f"coalesce(n.name, n.id) CONTAINS '{k}'" for k in keywords])
            match_query = f"MATCH (n) WHERE labels(n)[0] IN {labels_filter} AND ({where_clauses}) RETURN id(n) as node_id, coalesce(n.name, n.id) as node_name LIMIT 10"
            results = client.execute_query(match_query)
            
            for row in results:
                focus_nodes.append(row["node_id"])
                found_names.append(row["node_name"])
            
        import urllib.request
        import json
        
        context_str = ""
        if focus_nodes:
            # Fetch 1-hop relationships for LLM Context
            context_query = f"MATCH (n)-[r]-(m) WHERE id(n) IN {focus_nodes} RETURN coalesce(n.name, n.id) as n_name, labels(n)[0] as n_lbl, type(r) as rel, coalesce(m.name, m.id) as m_name, labels(m)[0] as m_lbl LIMIT 30"
            ctx_results = client.execute_query(context_query)
            context_lines = []
            for row in ctx_results:
                context_lines.append(f"[{row['n_lbl']}: {row['n_name']}] -({row['rel']})- [{row['m_lbl']}: {row['m_name']}]")
            context_str = "검색된 지식망 관계 데이터:\n" + "\n".join(context_lines)
            
        client.close()
        
        prompt = f"<start_of_turn>user\n당신은 아카이브 지식망 AI 어시스턴트입니다. 주어진 데이터베이스 관계 통계를 바탕으로 사용자의 질문에 한국어로 깔끔하고 전문적으로 답변하세요. 질문과 답변 형식을 반복해서 출력하지 말고 순수하게 답변만 작성하십시오.\n데이터 정보가 부족하면 모른다고 하십시오.\n\n[데이터베이스 관계 통계]\n{context_str}\n\n사용자 질문: {query_text}<end_of_turn>\n<start_of_turn>model\n"
        
        req_data = {
            "model": "google/gemma-4-26b-a4b",
            "prompt": prompt,
            "max_tokens": 512,
            "temperature": 0.1,
            "stop": ["<end_of_turn>", "<start_of_turn>", "[데이터베이스", "[사용자"]
        }
        
        try:
            req_json = json.dumps(req_data).encode("utf-8")
            req_url = urllib.request.Request("http://localhost:8000/v1/completions", data=req_json, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req_url, timeout=30) as response:
                llm_res = json.loads(response.read().decode("utf-8"))
                llm_answer = llm_res['choices'][0]['text'].strip()
        except Exception as e:
            llm_answer = f"⚠️ 로컬 vLLM (Gemma) 연결에 실패했습니다: {str(e)}"
            
        formatted_answer = llm_answer.replace("\n", "<br>")
        answer = f"{formatted_answer}<br><br><span style='color:#7f8fa6; font-size:11px;'>🤖 Powered by Local vLLM (Gemma-4-26B / Completions) Graph-RAG</span>"
            
        return {"answer": answer, "focus_nodes": focus_nodes}
        
    except Exception as e:
        if client: client.close()
        return {"answer": f"검색 중 오류가 발생했습니다: {str(e)}", "focus_nodes": []}

