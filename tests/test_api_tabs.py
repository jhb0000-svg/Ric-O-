import pytest
from fastapi.testclient import TestClient
from src.web_app import app

client = TestClient(app)

def test_graph_endpoint_records():
    response = client.get("/api/graph?type=record")
    assert response.status_code == 200
    assert "nodes" in response.json()

def test_graph_endpoint_knowledge():
    response = client.get("/api/graph?type=knowledge")
    assert response.status_code == 200
    assert "nodes" in response.json()
