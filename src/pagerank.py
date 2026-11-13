"""
PageRank Engine: Power Iteration, Stochastic Google Matrix & Convergence Analysis
MFCS Project - Intelligent Search Ranking
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from .graph import WebGraph


class PageRankEngine:
    """
    Computes PageRank stationary distribution using Power Iteration
    over the Markov transition Google Matrix G.
    """

    def __init__(self, graph: WebGraph, damping_factor: float = 0.85, tol: float = 1e-8, max_iter: int = 200):
        self.graph = graph
        self.damping_factor = damping_factor
        self.tol = tol
        self.max_iter = max_iter

    def get_transition_matrix(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Builds the raw row-stochastic transition matrix P and the dangling node indicator vector.
        P[i, j] = 1 / L(i) if page i links to page j, else 0.
        dangling_mask[i] = 1 if page i has out-degree 0, else 0.
        """
        n = self.graph.num_nodes
        P = np.zeros((n, n), dtype=float)
        dangling_mask = np.zeros(n, dtype=float)

        if n == 0:
            return P, dangling_mask

        for u_id, page in self.graph.pages.items():
            u_idx = self.graph.node_to_idx[u_id]
            valid_targets = [v for v in page.outgoing_links if v in self.graph.node_to_idx]
            deg = len(valid_targets)
            if deg > 0:
                prob = 1.0 / deg
                for v_id in valid_targets:
                    v_idx = self.graph.node_to_idx[v_id]
                    P[u_idx, v_idx] = prob
            else:
                dangling_mask[u_idx] = 1.0

        return P, dangling_mask

    def get_google_matrix(self, d: Optional[float] = None) -> np.ndarray:
        """
        Constructs the full stochastic, irreducible, aperiodic Google Matrix G:
        G = d * (P + dangling_mask^T * (1/N)) + (1 - d) * (E / N)
        where E is an N x N matrix of ones.
        """
        if d is None:
            d = self.damping_factor

        n = self.graph.num_nodes
        if n == 0:
            return np.zeros((0, 0))

        P, dangling_mask = self.get_transition_matrix()
        # S handles dangling nodes by distributing their mass uniformly (1/N)
        S = P.copy()
        for i in range(n):
            if dangling_mask[i] == 1.0:
                S[i, :] = 1.0 / n

        # Google Matrix with random teleportation
        E = np.ones((n, n)) / n
        G = d * S + (1.0 - d) * E
        return G

    def compute(self, damping_factor: Optional[float] = None) -> Tuple[Dict[str, float], dict]:
        """
        Runs Power Iteration to solve for the stationary probability distribution vector p:
        p^(t+1) = p^(t) * G
        
        Returns:
            scores: Dict mapping page_id -> PageRank score (sums to 1.0)
            metadata: Convergence history, iterations count, L1 residual error.
        """
        d = damping_factor if damping_factor is not None else self.damping_factor
        n = self.graph.num_nodes

        if n == 0:
            return {}, {"iterations": 0, "converged": True, "residuals": []}

        P, dangling_mask = self.get_transition_matrix()

        # Initial uniform probability distribution: p^(0) = [1/N, ..., 1/N]
        p = np.full(n, 1.0 / n, dtype=float)
        teleport = (1.0 - d) / n

        residuals = []
        converged = False

        for iteration in range(1, self.max_iter + 1):
            dangling_sum = np.sum(p * dangling_mask)
            # p^(t+1) update equation
            p_next = d * (p @ P + dangling_sum / n) + teleport

            # Measure L1 norm of difference: ||p^(t+1) - p^(t)||_1
            diff = float(np.sum(np.abs(p_next - p)))
            residuals.append(diff)

            p = p_next

            if diff < self.tol:
                converged = True
                break

        # Normalize to ensure numerical sum is exactly 1.0
        p = p / np.sum(p)

        scores = {self.graph.idx_to_node[i]: float(p[i]) for i in range(n)}
        meta = {
            "iterations": len(residuals),
            "converged": converged,
            "final_residual": residuals[-1] if residuals else 0.0,
            "residuals": residuals,
            "damping_factor": d,
            "entropy": float(-np.sum(p * np.log2(p + 1e-12)))  # Shannon entropy of distribution
        }

        return scores, meta

    def sensitivity_study(self, d_values: Optional[List[float]] = None) -> List[dict]:
        """
        Computes PageRank across varying damping factors to analyze sensitivity.
        """
        if d_values is None:
            d_values = [0.10, 0.30, 0.50, 0.70, 0.85, 0.90, 0.95, 0.99]

        results = []
        for d in d_values:
            scores, meta = self.compute(damping_factor=d)
            # Get top 5 pages
            sorted_pages = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            results.append({
                "damping_factor": d,
                "entropy": meta["entropy"],
                "iterations": meta["iterations"],
                "top_page": sorted_pages[0] if sorted_pages else None,
                "scores": scores
            })
        return results

    def verify_eigenvector(self) -> dict:
        """
        Verifies Perron-Frobenius theorem:
        Computes the dominant left eigenvector of G using scipy/numpy and compares to power iteration.
        """
        G = self.get_google_matrix()
        eigenvalues, left_eigenvectors = np.linalg.eig(G.T)
        
        # Find index of eigenvalue closest to 1.0
        idx_1 = int(np.argmin(np.abs(eigenvalues - 1.0)))
        v = left_eigenvectors[:, idx_1].real
        if np.sum(v) < 0:
            v = -v
        v = np.maximum(v, 0.0)
        v = v / np.sum(v)  # Normalize sum to 1

        power_scores, _ = self.compute()
        p_vec = np.array([power_scores[self.graph.idx_to_node[i]] for i in range(len(v))])

        l1_diff = float(np.sum(np.abs(v - p_vec)))
        return {
            "dominant_eigenvalue": float(eigenvalues[idx_1].real),
            "eigenvector_l1_discrepancy": l1_diff,
            "matches_perron_frobenius": l1_diff < 1e-4
        }

