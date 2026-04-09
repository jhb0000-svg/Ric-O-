import pytest
from fastapi.testclient import TestClient
from src.web_app import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/api/chat", json={"query": "보안 기록물"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "focus_nodes" in data
    assert type(data["focus_nodes"]) == list
