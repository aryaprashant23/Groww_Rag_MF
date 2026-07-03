import pytest
from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import patch

# Ensure we can import the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api import app

client = TestClient(app)

def test_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Please provide a valid query."
    assert len(data["sources"]) == 0

def test_guardrails_pii_pan():
    response = client.post("/chat", json={"query": "My PAN is ABCDE1234F. What is the NAV?"})
    assert response.status_code == 200
    data = response.json()
    assert "Blocked: Query contains sensitive information (PAN)" in data["answer"]
    assert len(data["sources"]) == 0

def test_guardrails_subjective():
    response = client.post("/chat", json={"query": "Which fund is better for me, small cap or large cap?"})
    assert response.status_code == 200
    data = response.json()
    assert "Blocked: Query asks for investment advice or subjective opinions" in data["answer"]
    assert len(data["sources"]) == 0

@patch("src.api.pipeline")
def test_valid_factual_query(mock_pipeline):
    # Mocking the RAG Pipeline to avoid hitting the actual Groq API during tests
    mock_pipeline.get_answer.return_value = {
        "answer": "The current NAV of the fund is 123.45. Last updated from sources: 2023-10-24.",
        "sources": ["https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth"],
        "raw_answer": "The current NAV of the fund is 123.45."
    }
    
    response = client.post("/chat", json={"query": "What is the NAV of Nippon India Small Cap Fund?"})
    assert response.status_code == 200
    data = response.json()
    assert "123.45" in data["answer"]
    assert "https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth" in data["sources"]
    
    # Ensure the pipeline was called with the correct query
    mock_pipeline.get_answer.assert_called_once_with("What is the NAV of Nippon India Small Cap Fund?")
