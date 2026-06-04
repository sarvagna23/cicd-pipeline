import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "uptime" in data
    assert "error_rate" in data

def test_predict_high():
    response = client.post("/predict", json={"value": 0.8})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "high"
    assert data["confidence"] > 0.5

def test_predict_low():
    response = client.post("/predict", json={"value": 0.2})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "low"

def test_predict_boundary():
    response = client.post("/predict", json={"value": 0.5})
    assert response.status_code == 200
    assert "prediction" in response.json()