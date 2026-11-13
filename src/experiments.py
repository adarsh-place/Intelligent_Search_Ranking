"""
Experimental Laboratory Module: Link Spam, Spider Traps & Sensitivity Analysis
MFCS Project - Intelligent Search Ranking
"""

from typing import Dict, List, Tuple
from .graph import WebGraph
from .pagerank import PageRankEngine
from .text_engine import TextRelevanceEngine
from .ranking import RankingEngine


class ExperimentSuite:
    """
    Automated experimental test suite simulating academic research scenarios:
    1. Sybil / Link Farm Attack Simulation
    2. Spider Trap / Dead End Probability Leak Simulation
    3. Alpha (Relevance vs Authority) Parameter Sweep
    4. Damping Factor Sensitivity Analysis
    """

    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path

    def run_spam_experiment(self, target_node: str = "page_16", num_bots: int = 5) -> dict:
        """
        Tests how an adversarial link farm affects the target page's PageRank and ranking.
        Compares baseline graph vs spammed graph for the query 'PageRank'.
        """
        # Baseline
        base_graph = WebGraph(self.corpus_path)
        base_pr_engine = PageRankEngine(base_graph)
        base_scores, _ = base_pr_engine.compute(damping_factor=0.85)

        base_text = TextRelevanceEngine(base_graph)
        base_ranker = RankingEngine(base_graph, base_text, base_pr_engine)
        base_search = base_ranker.rank_query("PageRank", alpha=0.50, damping_factor=0.85)

        target_base_rank = next((item["combined_rank"] for item in base_search["combined_ranking"] if item["id"] == target_node), None)
        target_base_pr = base_scores.get(target_node, 0.0)

        # Spammed Graph
        spam_graph = WebGraph(self.corpus_path)
        spam_bot_ids = spam_graph.inject_link_farm(target_node, num_spam_pages=num_bots)
        spam_pr_engine = PageRankEngine(spam_graph)
        spam_scores, _ = spam_pr_engine.compute(damping_factor=0.85)

        spam_text = TextRelevanceEngine(spam_graph)
        spam_ranker = RankingEngine(spam_graph, spam_text, spam_pr_engine)
        spam_search = spam_ranker.rank_query("PageRank", alpha=0.50, damping_factor=0.85)

        target_spam_rank = next((item["combined_rank"] for item in spam_search["combined_ranking"] if item["id"] == target_node), None)
        target_spam_pr = spam_scores.get(target_node, 0.0)

        pr_increase_pct = ((target_spam_pr - target_base_pr) / (target_base_pr + 1e-12)) * 100.0

        return {
            "target_node": target_node,
            "target_title": base_graph.pages[target_node].title if target_node in base_graph.pages else target_node,
            "num_bots_injected": num_bots,
            "bot_ids": spam_bot_ids,
            "baseline_pr": round(target_base_pr, 6),
            "spam_pr": round(target_spam_pr, 6),
            "pr_percentage_gain": round(pr_increase_pct, 2),
            "baseline_combined_rank": target_base_rank,
            "spam_combined_rank": target_spam_rank,
            "rank_jump": (target_base_rank - target_spam_rank) if (target_base_rank and target_spam_rank) else 0
        }

    def run_spider_trap_experiment(self) -> dict:
        """
        Tests the behavior of a spider trap (closed loop) with and without teleportation (damping).
        When d = 1.0 (no teleportation), the trap absorbs virtually all probability mass.
        When d = 0.85, teleportation allows the Markov surfer to escape.
        """
        trap_graph = WebGraph(self.corpus_path)
        trap_nodes = trap_graph.inject_spider_trap(num_nodes=2)
        pr_engine = PageRankEngine(trap_graph, max_iter=300)

        # With teleportation (d = 0.85)
        scores_d85, _ = pr_engine.compute(damping_factor=0.85)
        trap_mass_d85 = sum(scores_d85.get(t, 0.0) for t in trap_nodes)

        # Without teleportation (d = 0.999 to approximate no teleportation)
        scores_d99, _ = pr_engine.compute(damping_factor=0.99)
        trap_mass_d99 = sum(scores_d99.get(t, 0.0) for t in trap_nodes)

        return {
            "trap_nodes": trap_nodes,
            "trap_mass_with_damping_085": round(float(trap_mass_d85), 5),
            "trap_mass_with_damping_099": round(float(trap_mass_d99), 5),
            "mass_difference_pct": round(((trap_mass_d99 - trap_mass_d85) / max(1e-6, trap_mass_d85)) * 100, 2),
            "theoretical_insight": "Teleportation (1-d) prevents closed cycle subgraphs from absorbing all random walk probability."
        }

    def run_alpha_sweep(self, query: str = "PageRank Markov") -> List[dict]:
        """
        Sweeps alpha from 0.0 to 1.0 to analyze rank transitions from pure PageRank to pure keyword matching.
        """
        graph = WebGraph(self.corpus_path)
        pr_engine = PageRankEngine(graph)
        text_engine = TextRelevanceEngine(graph)
        ranker = RankingEngine(graph, text_engine, pr_engine)

        steps = [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
        results = []

        for a in steps:
            res = ranker.rank_query(query, alpha=a, damping_factor=0.85)
            top_3 = res["combined_ranking"][:3]
            results.append({
                "alpha": a,
                "top_results": [{"rank": item["combined_rank"], "id": item["id"], "score": item["final_score"]} for item in top_3]
            })

        return results

