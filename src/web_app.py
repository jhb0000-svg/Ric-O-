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
def get_index():
    with open(os.path.join(os.path.dirname(__file__), "..", "templates", "index.html"), "r") as f:
        return f.read()

@app.get("/api/graph")
def get_graph(type: str = "record"):
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
        RETURN id(n) as source_id, n.id as source_real_id, labels(n)[0] as source_label, coalesce(n.name, n.id) as source_name, 
               type(r) as rel_type, 
               id(m) as target_id, m.id as target_real_id, labels(m)[0] as target_label, coalesce(m.name, m.id) as target_name 
        LIMIT 2000
        """
        results = client.execute_query(query)
        client.close()
        
        nodes_dict = {}
        edges = []
        for row in results:
            src_id = row['source_id']
            tgt_id = row['target_id']
            nodes_dict[src_id] = {"id": src_id, "recordId": row['source_real_id'], "label": row['source_label'], "title": row['source_name'] or str(src_id)}
            nodes_dict[tgt_id] = {"id": tgt_id, "recordId": row['target_real_id'], "label": row['target_label'], "title": row['target_name'] or str(tgt_id)}
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
def process_chat(req: ChatRequest):
    client = get_db()
    if not client:
        return {"answer": "데이터베이스 연결에 실패했습니다.", "focus_nodes": []}
    
    import urllib.request
    import json
    
    def call_vllm_completion(system_str, user_str, max_tok=512, temp=0.1):
        req_data = {
            "model": "google/gemma-4-26B-A4B-it",
            "messages": [
                {"role": "system", "content": system_str},
                {"role": "user", "content": user_str}
            ],
            "max_tokens": max_tok,
            "temperature": temp,
        }
        try:
            req_json = json.dumps(req_data).encode("utf-8")
            req_url = urllib.request.Request("http://localhost:8000/v1/chat/completions", data=req_json, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req_url, timeout=60) as response:
                llm_res = json.loads(response.read().decode("utf-8"))
                text = llm_res['choices'][0]['message']['content'].strip()
                # 모델 내부 사고(thought) 첫 줄 제거
                lines = text.splitlines()
                if lines and lines[0].strip().lower() == "thought":
                    text = "\n".join(lines[1:]).strip()
                return text
        except Exception as e:
            return None

    query_text = req.query
    
    # 1. LLM Keyword Extraction
    llm_extracted = call_vllm_completion(
        "당신은 기록물 검색 키워드 추출 도구입니다. 사용자 문장에서 검색에 필요한 핵심 고유명사(사람 이름, 기관명, 연도, 단위과제명 등)만 쉼표로 구분하여 출력하세요. 설명 없이 키워드만 출력하세요.",
        query_text,
        max_tok=50, temp=0.1
    )
    
    keywords = []
    if llm_extracted:
        # 모델이 "thought\n키워드" 형태로 응답하는 경우 마지막 줄만 사용
        lines = [l.strip() for l in llm_extracted.splitlines() if l.strip()]
        keyword_line = lines[-1] if lines else ""
        keywords = [k.strip() for k in keyword_line.split(",") if len(k.strip()) > 1]
    
    # Fallback to Regex
    if not keywords:
        cleaned_query = re.sub(r'(은|는|이|가|에|에서|의|로|으로|을|를|과|와)(?=\s|$)', '', query_text)
        cleaned_query = re.sub(r'[^\w\s]', '', cleaned_query)
        stop_words = ["찾아줘", "무엇인가", "어떻게", "기록물", "문서", "자료", "알려줘", "대해", "관련된", "생산한", "작성한"]
        keywords = [word for word in re.split(r'\s+', cleaned_query) if len(word) > 1 and word not in stop_words]
        
    if req.type == "knowledge":
        labels_filter = "['Document', 'Chunk', 'Entity', 'Law', 'Article', 'Department', 'Judgment']"
    else:
        labels_filter = "['RecordResource', 'Agent', 'Activity', 'Organization', 'Mandate', 'Date']"

    frontend_focus_nodes = []
    llm_focus_nodes = []
    try:
        if keywords:
            matched_node_groups = []
            for k in keywords:
                # 연도 키워드 정규화: "2008년" → "2008"
                k_normalized = k.rstrip('년') if k.rstrip('년').isdigit() else k
                q = f"MATCH (n) WHERE labels(n)[0] IN {labels_filter} AND coalesce(n.name, n.id) CONTAINS '{k_normalized}' RETURN id(n) as nid"
                res = client.execute_query(q)
                nids = [r['nid'] for r in res]
                if nids:
                    matched_node_groups.append(nids)
                    frontend_focus_nodes.extend(nids)
            
            record_sets = []
            for nids in matched_node_groups:
                # Find RecordResources connected to these nodes (or if they are themselves Records)
                q2 = f"MATCH (n) WHERE id(n) IN {nids} OPTIONAL MATCH (n)-[]-(m:RecordResource) RETURN collect(DISTINCT id(m)) + collect(DISTINCT id(n)) as combined_ids"
                res2 = client.execute_query(q2)
                for row in res2:
                    if row['combined_ids']:
                        record_sets.append(set(row['combined_ids']))
            
            if record_sets:
                llm_focus_nodes = list(set.intersection(*record_sets))
            
        context_str = ""
        if llm_focus_nodes:
            # We constrain the context to the precise intersected nodes and their 1-hop neighbors
            focus_list = llm_focus_nodes[:15]
            context_query = f"MATCH (n)-[r]-(m) WHERE id(n) IN {focus_list} RETURN coalesce(n.name, n.id) as n_name, labels(n)[0] as n_lbl, type(r) as rel, coalesce(m.name, m.id) as m_name, labels(m)[0] as m_lbl LIMIT 50"
            ctx_results = client.execute_query(context_query)
            context_lines = []
            for row in ctx_results:
                context_lines.append(f"[{row['n_lbl']}: {row['n_name']}] -({row['rel']})- [{row['m_lbl']}: {row['m_name']}]")
            context_str = "검색된 지식망 관계 데이터:\n" + "\n".join(context_lines)
            
        client.close()
        
        if not context_str:
            answer = "검색 조건에 일치하는 기록물이나 연관 지식망 데이터를 찾을 수 없습니다. 키워드를 조정하여 다시 질문해 주세요.<br><br><span style='color:#7f8fa6; font-size:11px;'>🤖 Powered by Local vLLM (Gemma-4-26B / Completions) Graph-RAG</span>"
            return {"answer": answer, "focus_nodes": []}
        
        # 2. LLM RAG Response Generation
        llm_answer = call_vllm_completion(
            f"당신은 아카이브 지식망 AI 어시스턴트입니다. 오직 아래 제공된 [데이터베이스 관계 통계] 데이터에 나타난 내용만을 기반으로 답변하십시오. 창작이나 일반 상식을 동원하지 마십시오.\n\n[데이터베이스 관계 통계]\n{context_str}",
            query_text
        )
        
        if not llm_answer:
            llm_answer = "⚠️ 로컬 vLLM (Gemma) 연결에 실패했거나 응답이 없습니다."

        formatted_answer = llm_answer.replace("\n", "<br>")
        answer = f"{formatted_answer}<br><br><span style='color:#7f8fa6; font-size:11px;'>🤖 Powered by Local vLLM (Gemma-4-26B / Completions) Graph-RAG</span>"
            
        return {"answer": answer, "focus_nodes": llm_focus_nodes}
        
    except Exception as e:
        if client: client.close()
        return {"answer": f"검색 중 오류가 발생했습니다: {str(e)}", "focus_nodes": []}

import os

@app.get("/api/document/{doc_id}")
def get_document(doc_id: str):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_records", f"document_{doc_id}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"id": doc_id, "content": content}
    else:
        return {"id": doc_id, "content": "⚠️ 연결된 원문 파일 리소스를 찾을 수 없습니다."}
