"""
Integration Tests for Flask Web Application & REST API Endpoints
"""

import json
import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Intelligent Search Ranking" in response.data


def test_api_graph_route(client):
    response = client.get("/api/graph?damping=0.85")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "nodes" in data
    assert "edges" in data
    assert "metadata" in data
    assert len(data["nodes"]) >= 15


def test_api_search_route(client):
    payload = {
        "query": "PageRank Markov",
        "alpha": 0.5,
        "damping": 0.85,
        "filter_unmatched": True
    }
    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "combined_ranking" in data
    assert "keyword_only_ranking" in data
    assert "pagerank_only_ranking" in data
    assert "correlations" in data
    assert len(data["combined_ranking"]) > 0


def test_api_random_walk_route(client):
    payload = {
        "num_steps": 500,
        "damping": 0.85
    }
    response = client.post("/api/random_walk", json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "trajectory_sample" in data
    assert "empirical_distribution" in data
    assert "final_l1_error" in data


def test_api_experiments_routes(client):
    resp_damping = client.get("/api/experiments/damping")
    assert resp_damping.status_code == 200
    data_damping = json.loads(resp_damping.data)
    assert len(data_damping) > 0

    resp_spam = client.get("/api/experiments/spam?target_id=page_16&num_bots=3")
    assert resp_spam.status_code == 200
    data_spam = json.loads(resp_spam.data)
    assert data_spam["pr_percentage_gain"] > 0

    resp_trap = client.get("/api/experiments/trap")
    assert resp_trap.status_code == 200
    data_trap = json.loads(resp_trap.data)
    assert "trap_nodes" in data_trap


def test_api_graph_mutations(client):
    # Add link
    resp_add = client.post("/api/graph/add_link", json={"source": "page_08", "target": "page_01"})
    assert resp_add.status_code == 200
    assert json.loads(resp_add.data)["success"] is True

    # Remove link
    resp_rem = client.post("/api/graph/remove_link", json={"source": "page_08", "target": "page_01"})
    assert resp_rem.status_code == 200
    assert json.loads(resp_rem.data)["success"] is True

    # Reset
    resp_reset = client.post("/api/graph/reset")
    assert resp_reset.status_code == 200
    assert json.loads(resp_reset.data)["success"] is True

