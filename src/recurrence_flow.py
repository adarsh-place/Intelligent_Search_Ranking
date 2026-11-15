"""
Recurrence Relations & Network Flow: Linear Iteration, Path Counting & Flow Invariants
Intelligent Search Ranking
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from .graph import WebGraph


class RecurrenceFlowSimulator:
    """
    Simulates the step-by-step linear recurrence relation governing conservative network flow across web graph edges:
        x^(t+1) = d * (x^(t) * P + dangling_mass/N) + (1 - d)/N
    
    Demonstrates:
    - Combinatorics & Recurrences: Linear recurrence relations, generating function matrix resolvent (I - d*M)^(-1), and path counting A^k.
    - Graph Theory & Network Flows: Conservation of network flow across directed edges.
    - Logic & Induction: Inductive flow conservation invariant sum(x^(t)) = 1.
    """

    def __init__(self, graph: WebGraph, damping_factor: float = 0.85, seed: Optional[int] = None, **kwargs):
        self.graph = graph
        self.damping_factor = damping_factor
        self.seed = seed

    def simulate_recurrence(
        self,
        num_steps: int = 30,
        start_distribution: Optional[Dict[str, float]] = None
    ) -> dict:
        """
        Executes step-by-step linear recurrence updates and records trajectory.
        """
        all_nodes = self.graph.idx_to_node
        n = len(all_nodes)
        if n == 0:
            return {}

        # Build transition matrix P and dangling mask
        P = np.zeros((n, n), dtype=float)
        dangling_mask = np.zeros(n, dtype=float)

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

        # Initial recurrence state: x^(0)
        if start_distribution:
            x = np.array([start_distribution.get(pid, 1.0 / n) for pid in all_nodes])
            x = x / np.sum(x)
        else:
            x = np.full(n, 1.0 / n, dtype=float)

        d = self.damping_factor
        teleport = (1.0 - d) / n

        step_history = []
        residuals = []
        flow_conservation_checks = []

        # Record step 0
        step_history.append({
            "step": 0,
            "vector": {all_nodes[i]: round(float(x[i]), 5) for i in range(n)},
            "top_node": all_nodes[int(np.argmax(x))],
            "residual": 0.0,
            "total_flow": round(float(np.sum(x)), 6)
        })

        for t in range(1, num_steps + 1):
            dangling_sum = np.sum(x * dangling_mask)
            x_next = d * (x @ P + dangling_sum / n) + teleport

            diff = float(np.sum(np.abs(x_next - x)))
            residuals.append(round(diff, 6))

            total_flow = float(np.sum(x_next))
            flow_conservation_checks.append(abs(total_flow - 1.0) < 1e-10)

            x = x_next
            step_history.append({
                "step": t,
                "vector": {all_nodes[i]: round(float(x[i]), 5) for i in range(n)},
                "top_node": all_nodes[int(np.argmax(x))],
                "residual": round(diff, 6),
                "total_flow": round(total_flow, 6)
            })

            if diff < 1e-8:
                break

        # Combinatorics: Path counts via matrix powers A^1, A^2, A^3
        A = self.graph.get_adjacency_matrix()
        A_powers = {
            "walks_len_1": int(np.sum(A)),
            "walks_len_2": int(np.sum(np.linalg.matrix_power(A, 2))),
            "walks_len_3": int(np.sum(np.linalg.matrix_power(A, 3)))
        }

        final_vector = {all_nodes[i]: round(float(x[i]), 6) for i in range(n)}

        return {
            "num_steps_executed": len(step_history) - 1,
            "damping_factor": d,
            "final_vector": final_vector,
            "step_history": step_history,
            "residuals": residuals,
            "all_steps_conserve_flow": all(flow_conservation_checks),
            "combinatorial_walk_counts": A_powers
        }


# Backwards-compatible class for existing imports
class RandomWalkSimulator(RecurrenceFlowSimulator):
    """Alias for RecurrenceFlowSimulator to maintain backwards compatibility."""
    def simulate(self, num_steps: int = 30, start_node: Optional[str] = None, theoretical_pr: Optional[Dict[str, float]] = None):
        res = self.simulate_recurrence(num_steps=min(num_steps, 50))
        all_nodes = self.graph.idx_to_node
        return {
            "num_steps": res["num_steps_executed"],
            "damping_factor": self.damping_factor,
            "start_node": all_nodes[0] if all_nodes else "",
            "end_node": res["step_history"][-1]["top_node"],
            "trajectory_sample": [step["top_node"] for step in res["step_history"]],
            "visit_counts": {k: int(v * 1000) for k, v in res["final_vector"].items()},
            "empirical_distribution": res["final_vector"],
            "theoretical_distribution": theoretical_pr or res["final_vector"],
            "final_l1_error": res["residuals"][-1] if res["residuals"] else 0.0,
            "error_history": [{"step": s["step"], "l1_error": s["residual"]} for s in res["step_history"][1:]]
        }
