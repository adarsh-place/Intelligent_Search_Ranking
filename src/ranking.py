"""
Ranking Engine: Candidate Retrieval, Min-Max Normalization & Hybrid Score Fusion
MFCS Project - Intelligent Search Ranking
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from .graph import WebGraph
from .pagerank import PageRankEngine
from .text_engine import TextRelevanceEngine


class RankingEngine:
    """
    Combines textual relevance scores and PageRank scores using candidate-level
    normalization and convex combination:
        FinalScore(p, q) = alpha * R_norm(p, q) + (1 - alpha) * PR_norm(p)
    """

    def __init__(self, graph: WebGraph, text_engine: TextRelevanceEngine, pagerank_engine: PageRankEngine):
        self.graph = graph
        self.text_engine = text_engine
        self.pagerank_engine = pagerank_engine

    @staticmethod
    def min_max_normalize(scores: Dict[str, float], candidate_ids: List[str]) -> Dict[str, float]:
        """
        Normalizes scores across candidate documents to range [0.0, 1.0].
        If all scores are 0 (e.g. no match), returns 0.0 for all candidates.
        If all scores are equal and non-zero, assigns 1.0 to all candidates.
        """
        if not candidate_ids:
            return {}

        values = [scores.get(pid, 0.0) for pid in candidate_ids]
        val_min = min(values)
        val_max = max(values)

        # If all scores are zero, normalized scores are zero
        if val_max < 1e-12:
            return {pid: 0.0 for pid in candidate_ids}

        denom = val_max - val_min
        if denom < 1e-12:
            return {pid: 1.0 for pid in candidate_ids}

        return {pid: (scores.get(pid, 0.0) - val_min) / denom for pid in candidate_ids}

    @staticmethod
    def compute_spearman_rho(ranks1: Dict[str, int], ranks2: Dict[str, int]) -> float:
        """
        Calculates Spearman's rank correlation coefficient rho between two rankings:
        rho = 1 - (6 * sum(d_i^2)) / (k * (k^2 - 1))
        """
        common_keys = [k for k in ranks1 if k in ranks2]
        k = len(common_keys)
        if k <= 1:
            return 1.0

        d_sq_sum = sum((ranks1[key] - ranks2[key]) ** 2 for key in common_keys)
        rho = 1.0 - (6.0 * d_sq_sum) / (k * (k * k - 1))
        return round(float(rho), 4)

    def rank_query(
        self,
        query: str,
        alpha: float = 0.50,
        damping_factor: float = 0.85,
        filter_unmatched: bool = True
    ) -> dict:
        """
        Executes query, computes three-way rankings, and generates analytical comparisons.
        """
        alpha = max(0.0, min(1.0, float(alpha)))

        # 1. Text Relevance
        text_results = self.text_engine.calculate_relevance(query)
        raw_relevance = {pid: res["raw_score"] for pid, res in text_results.items()}

        # 2. PageRank
        pr_scores, pr_meta = self.pagerank_engine.compute(damping_factor=damping_factor)

        # 3. Candidate Selection
        if filter_unmatched:
            candidates = [pid for pid, score in raw_relevance.items() if score > 0.0]
            # Fallback if no matching document found: show all documents
            if not candidates:
                candidates = list(self.graph.pages.keys())
        else:
            candidates = list(self.graph.pages.keys())

        # 4. Score Normalization
        norm_relevance = self.min_max_normalize(raw_relevance, candidates)
        norm_pagerank = self.min_max_normalize(pr_scores, candidates)

        # 5. Hybrid Combined Scoring
        combined_scores = {}
        for pid in candidates:
            r_norm = norm_relevance[pid]
            p_norm = norm_pagerank[pid]
            combined_scores[pid] = alpha * r_norm + (1.0 - alpha) * p_norm

        # 6. Sorting for 3 Perspectives
        keyword_sorted = sorted(candidates, key=lambda pid: (raw_relevance[pid], pr_scores.get(pid, 0.0)), reverse=True)
        pagerank_sorted = sorted(candidates, key=lambda pid: (pr_scores.get(pid, 0.0), raw_relevance[pid]), reverse=True)
        combined_sorted = sorted(candidates, key=lambda pid: combined_scores[pid], reverse=True)

        keyword_ranks = {pid: rank + 1 for rank, pid in enumerate(keyword_sorted)}
        pagerank_ranks = {pid: rank + 1 for rank, pid in enumerate(pagerank_sorted)}
        combined_ranks = {pid: rank + 1 for rank, pid in enumerate(combined_sorted)}

        # Format item record
        def build_record(pid: str) -> dict:
            page = self.graph.pages[pid]
            in_deg = len([u for u, p in self.graph.pages.items() if pid in p.outgoing_links])
            out_deg = len([v for v in page.outgoing_links if v in self.graph.pages])
            kw_rank = keyword_ranks.get(pid, 0)
            comb_rank = combined_ranks.get(pid, 0)
            rank_shift = kw_rank - comb_rank  # positive = boosted upward by PageRank

            return {
                "id": pid,
                "title": page.title,
                "category": page.category,
                "content_snippet": page.content[:140] + "...",
                "matched_terms": text_results.get(pid, {}).get("matched_terms", []),
                "raw_relevance": round(raw_relevance.get(pid, 0.0), 5),
                "norm_relevance": round(norm_relevance.get(pid, 0.0), 4),
                "raw_pagerank": round(pr_scores.get(pid, 0.0), 6),
                "norm_pagerank": round(norm_pagerank.get(pid, 0.0), 4),
                "final_score": round(combined_scores.get(pid, 0.0), 4),
                "keyword_rank": kw_rank,
                "pagerank_rank": pagerank_ranks.get(pid, 0),
                "combined_rank": comb_rank,
                "rank_shift": rank_shift,
                "in_degree": in_deg,
                "out_degree": out_deg
            }

        combined_records = [build_record(pid) for pid in combined_sorted]
        keyword_records = [build_record(pid) for pid in keyword_sorted]
        pagerank_records = [build_record(pid) for pid in pagerank_sorted]

        # 7. Rank Correlations
        rho_keyword_combined = self.compute_spearman_rho(keyword_ranks, combined_ranks)
        rho_pagerank_combined = self.compute_spearman_rho(pagerank_ranks, combined_ranks)

        return {
            "query": query,
            "alpha": alpha,
            "damping_factor": damping_factor,
            "num_candidates": len(candidates),
            "combined_ranking": combined_records,
            "keyword_only_ranking": keyword_records,
            "pagerank_only_ranking": pagerank_records,
            "correlations": {
                "spearman_keyword_vs_combined": rho_keyword_combined,
                "spearman_pagerank_vs_combined": rho_pagerank_combined
            },
            "pagerank_metadata": pr_meta
        }

