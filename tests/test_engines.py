"""
Unit Tests for MFCS Intelligent Search Ranking Modules
"""

import os
import pytest
import numpy as np
from src.graph import WebGraph
from src.pagerank import PageRankEngine
from src.random_walk import RandomWalkSimulator
from src.text_engine import TextRelevanceEngine
from src.ranking import RankingEngine
from src.experiments import ExperimentSuite

CORPUS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "corpus.json")


def test_graph_loading_and_adjacency():
    graph = WebGraph(CORPUS_PATH)
    assert graph.num_nodes >= 15
    adj = graph.get_adjacency_matrix()
    assert adj.shape == (graph.num_nodes, graph.num_nodes)
    
    # Verify dangling node detection
    dangling = graph.get_dangling_nodes()
    assert "page_08" in dangling
    assert graph.get_out_degrees()["page_08"] == 0


def test_pagerank_conservation_and_convergence():
    graph = WebGraph(CORPUS_PATH)
    engine = PageRankEngine(graph, damping_factor=0.85)
    scores, meta = engine.compute()

    assert meta["converged"] is True
    assert len(scores) == graph.num_nodes

    # Total probability mass must sum to 1.0
    total_prob = sum(scores.values())
    assert abs(total_prob - 1.0) < 1e-6

    # Verify high-authority page has highest PageRank
    sorted_pages = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_page_id = sorted_pages[0][0]
    assert top_page_id in ["page_03", "page_01", "page_02"]


def test_perron_frobenius_verification():
    graph = WebGraph(CORPUS_PATH)
    engine = PageRankEngine(graph)
    res = engine.verify_eigenvector()
    assert abs(res["dominant_eigenvalue"] - 1.0) < 1e-5
    assert res["matches_perron_frobenius"] is True


def test_random_walk_simulation():
    graph = WebGraph(CORPUS_PATH)
    engine = PageRankEngine(graph)
    pr_scores, _ = engine.compute()

    sim = RandomWalkSimulator(graph, damping_factor=0.85, seed=42)
    walk_res = sim.simulate(num_steps=1000, theoretical_pr=pr_scores)

    assert len(walk_res["trajectory_sample"]) > 0
    assert abs(sum(walk_res["empirical_distribution"].values()) - 1.0) < 1e-5
    assert walk_res["final_l1_error"] is not None


def test_text_relevance_engine():
    graph = WebGraph(CORPUS_PATH)
    engine = TextRelevanceEngine(graph)
    results = engine.calculate_relevance("PageRank Markov chain")

    assert len(results) == graph.num_nodes
    # page_03 (The Anatomy of PageRank) should have a high score
    assert results["page_03"]["raw_score"] > 0.0
    for res in results.values():
        assert 0.0 <= res["raw_score"] <= 1.0


def test_hybrid_ranking():
    graph = WebGraph(CORPUS_PATH)
    pr_engine = PageRankEngine(graph)
    text_engine = TextRelevanceEngine(graph)
    ranker = RankingEngine(graph, text_engine, pr_engine)

    query_res = ranker.rank_query("random walk probability", alpha=0.6)
    assert query_res["num_candidates"] > 0
    assert len(query_res["combined_ranking"]) == query_res["num_candidates"]

    # Check that final scores are within [0, 1]
    for item in query_res["combined_ranking"]:
        assert 0.0 <= item["final_score"] <= 1.0


def test_experiments_suite():
    suite = ExperimentSuite(CORPUS_PATH)
    spam_res = suite.run_spam_experiment(target_node="page_16", num_bots=4)
    assert spam_res["spam_pr"] > spam_res["baseline_pr"]
    assert spam_res["pr_percentage_gain"] > 0

    trap_res = suite.run_spider_trap_experiment()
    assert trap_res["trap_mass_with_damping_099"] > trap_res["trap_mass_with_damping_085"]

