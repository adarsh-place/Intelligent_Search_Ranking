"""
Markov Chain Simulation: Monte Carlo Random Walk Surfer and Empirical Convergence
MFCS Project - Intelligent Search Ranking
"""

import random
from typing import Dict, List, Tuple, Optional
import numpy as np
from .graph import WebGraph


class RandomWalkSimulator:
    """
    Simulates a random surfer navigating the web graph according to a Markov chain.
    Demonstrates the Ergodic Theorem: empirical visit frequencies converge
    to the theoretical stationary distribution pi calculated by PageRank.
    """

    def __init__(self, graph: WebGraph, damping_factor: float = 0.85, seed: Optional[int] = None):
        self.graph = graph
        self.damping_factor = damping_factor
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def simulate(
        self,
        num_steps: int = 2000,
        start_node: Optional[str] = None,
        theoretical_pr: Optional[Dict[str, float]] = None
    ) -> dict:
        """
        Executes a random walk of length `num_steps`.
        Returns:
            - trajectory: list of visited page IDs (capped at 250 for lightweight payload)
            - visit_counts: raw counts for each page
            - empirical_distribution: normalized visit proportions
            - error_history: L1 error evaluated at checkpoints along the walk
        """
        all_nodes = self.graph.idx_to_node
        n = len(all_nodes)
        if n == 0:
            return {}

        current_node = start_node if (start_node and start_node in self.graph.pages) else random.choice(all_nodes)

        visit_counts = {node_id: 0 for node_id in all_nodes}
        trajectory = [current_node]
        visit_counts[current_node] += 1

        # Checkpoints for tracking convergence error over time
        checkpoints = set(np.linspace(10, num_steps, min(30, num_steps), dtype=int))
        error_history = []

        d = self.damping_factor

        for step in range(1, num_steps):
            # Markov decision: Teleport or Follow link?
            rand_val = random.random()
            page = self.graph.pages[current_node]
            valid_outlinks = [v for v in page.outgoing_links if v in self.graph.pages]

            if rand_val < d and len(valid_outlinks) > 0:
                # Follow one outgoing link uniformly at random
                next_node = random.choice(valid_outlinks)
            else:
                # Random teleportation (or dangling node jump)
                next_node = random.choice(all_nodes)

            current_node = next_node
            visit_counts[current_node] += 1
            if len(trajectory) < 250:
                trajectory.append(current_node)

            # Record L1 convergence error if theoretical PR is provided
            if step in checkpoints and theoretical_pr:
                current_empirical = {k: v / (step + 1) for k, v in visit_counts.items()}
                l1_err = sum(abs(current_empirical[k] - theoretical_pr.get(k, 0.0)) for k in all_nodes)
                error_history.append({"step": step + 1, "l1_error": round(float(l1_err), 5)})

        empirical_distribution = {node_id: round(visit_counts[node_id] / num_steps, 6) for node_id in all_nodes}

        final_l1_error = None
        if theoretical_pr:
            final_l1_error = round(
                float(sum(abs(empirical_distribution[k] - theoretical_pr.get(k, 0.0)) for k in all_nodes)), 5
            )

        return {
            "num_steps": num_steps,
            "damping_factor": d,
            "start_node": trajectory[0],
            "end_node": current_node,
            "trajectory_sample": trajectory,
            "visit_counts": visit_counts,
            "empirical_distribution": empirical_distribution,
            "theoretical_distribution": theoretical_pr,
            "final_l1_error": final_l1_error,
            "error_history": error_history
        }

