"""
Graph Theory Module: Directed Web Graph Representation and Topology Analysis
MFCS Project - Intelligent Search Ranking
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import numpy as np


@dataclass
class WebPage:
    id: str
    title: str
    category: str
    content: str
    outgoing_links: List[str] = field(default_factory=list)


class WebGraph:
    """
    Represents a directed web graph G = (V, E).
    V: Set of webpages
    E: Set of directed hyperlinks (u, v) where u links to v.
    """

    def __init__(self, corpus_path: Optional[str] = None):
        self.corpus_path = corpus_path
        self.pages: Dict[str, WebPage] = {}
        self.node_to_idx: Dict[str, int] = {}
        self.idx_to_node: List[str] = []
        self._initial_backup: Optional[str] = None

        if corpus_path:
            self.load_corpus(corpus_path)

    def load_corpus(self, file_path: str):
        """Loads pages from a JSON corpus file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._initial_backup = json.dumps(data)
        self._populate_from_data(data)

    def _populate_from_data(self, data: List[dict]):
        """Populates graph data structures from raw dictionaries."""
        self.pages.clear()
        self.idx_to_node.clear()
        self.node_to_idx.clear()

        for idx, item in enumerate(data):
            page = WebPage(
                id=item["id"],
                title=item["title"],
                category=item.get("category", "General"),
                content=item["content"],
                outgoing_links=list(item.get("outgoing_links", []))
            )
            self.pages[page.id] = page
            self.idx_to_node.append(page.id)
            self.node_to_idx[page.id] = idx

    def reset_to_default(self):
        """Resets the graph back to the original initial corpus."""
        if self._initial_backup:
            data = json.loads(self._initial_backup)
            self._populate_from_data(data)

    @property
    def num_nodes(self) -> int:
        return len(self.pages)

    def get_adjacency_matrix(self) -> np.ndarray:
        """
        Constructs binary adjacency matrix A of size N x N.
        A[i, j] = 1 if page i links to page j, else 0.
        """
        n = self.num_nodes
        A = np.zeros((n, n), dtype=float)
        for u_id, page in self.pages.items():
            u_idx = self.node_to_idx[u_id]
            for v_id in page.outgoing_links:
                if v_id in self.node_to_idx:
                    v_idx = self.node_to_idx[v_id]
                    A[u_idx, v_idx] = 1.0
        return A

    def get_in_degrees(self) -> Dict[str, int]:
        """Calculates in-degree (number of incoming links) for every page."""
        in_deg = {pid: 0 for pid in self.pages}
        for page in self.pages.values():
            for target in page.outgoing_links:
                if target in in_deg:
                    in_deg[target] += 1
        return in_deg

    def get_out_degrees(self) -> Dict[str, int]:
        """Calculates out-degree (number of outgoing links) for every page."""
        return {pid: len([v for v in p.outgoing_links if v in self.pages]) for pid, p in self.pages.items()}

    def get_dangling_nodes(self) -> List[str]:
        """Returns node IDs that have out-degree equal to 0 (dead ends)."""
        out_deg = self.get_out_degrees()
        return [pid for pid, deg in out_deg.items() if deg == 0]

    def add_link(self, source_id: str, target_id: str) -> bool:
        """Adds a directed link source -> target."""
        if source_id in self.pages and target_id in self.pages:
            if target_id not in self.pages[source_id].outgoing_links:
                self.pages[source_id].outgoing_links.append(target_id)
                return True
        return False

    def remove_link(self, source_id: str, target_id: str) -> bool:
        """Removes a directed link source -> target."""
        if source_id in self.pages and target_id in self.pages[source_id].outgoing_links:
            self.pages[source_id].outgoing_links.remove(target_id)
            return True
        return False

    def add_page(self, page_id: str, title: str, content: str, category: str = "Custom", outgoing_links: Optional[List[str]] = None) -> bool:
        """Adds a new page dynamically to the graph."""
        if page_id in self.pages:
            return False
        new_page = WebPage(
            id=page_id,
            title=title,
            category=category,
            content=content,
            outgoing_links=outgoing_links or []
        )
        self.pages[page_id] = new_page
        self.idx_to_node.append(page_id)
        self.node_to_idx[page_id] = len(self.idx_to_node) - 1
        return True

    def remove_page(self, page_id: str) -> bool:
        """Removes a page and all edges connected to it."""
        if page_id not in self.pages:
            return False
        del self.pages[page_id]
        for p in self.pages.values():
            if page_id in p.outgoing_links:
                p.outgoing_links.remove(page_id)
        # Re-index
        self.idx_to_node = list(self.pages.keys())
        self.node_to_idx = {pid: i for i, pid in enumerate(self.idx_to_node)}
        return True

    def inject_link_farm(self, target_id: str, num_spam_pages: int = 5) -> List[str]:
        """
        Injects a synthetic link farm (sybil spam attack):
        Creates `num_spam_pages` auxiliary pages that link to each other
        and all point towards `target_id` to artificially inflate its PageRank.
        """
        if target_id not in self.pages:
            raise ValueError(f"Target page {target_id} does not exist.")

        existing_bots = len([p for p in self.pages if p.startswith("spam_bot_")])
        created_ids = []
        for i in range(1, num_spam_pages + 1):
            spam_id = f"spam_bot_{existing_bots + i}"
            created_ids.append(spam_id)
            self.add_page(
                page_id=spam_id,
                title=f"Spam Directory Farm Node #{existing_bots + i}",
                category="Link Spam",
                content=f"Automated link spam network node {existing_bots + i} promoting {target_id}. Free SEO backlinks and traffic boost.",
                outgoing_links=[target_id]
            )

        # Interlink spam pages to boost internal rank before funneling to target
        for sid in created_ids:
            for other_sid in created_ids:
                if sid != other_sid and other_sid not in self.pages[sid].outgoing_links:
                    self.pages[sid].outgoing_links.append(other_sid)

        return created_ids

    def inject_spider_trap(self, num_nodes: int = 2) -> List[str]:
        """
        Injects a spider trap (closed loop of pages that link only to each other,
        absorbing probability mass if no damping/teleportation is used).
        """
        existing_traps = len([p for p in self.pages if p.startswith("trap_node_")])
        trap_ids = []
        for i in range(1, num_nodes + 1):
            trap_id = f"trap_node_{existing_traps + i}"
            trap_ids.append(trap_id)
            self.add_page(
                page_id=trap_id,
                title=f"Spider Trap Loop Node #{existing_traps + i}",
                category="Spider Trap",
                content=f"This is a closed-cycle spider trap page {existing_traps + i} designed to absorb Markov chain probability.",
                outgoing_links=[]
            )

        # Form a cycle between trap nodes
        for idx, tid in enumerate(trap_ids):
            next_tid = trap_ids[(idx + 1) % len(trap_ids)]
            self.pages[tid].outgoing_links.append(next_tid)

        # Have a normal page point into the trap to test absorption
        if "page_06" in self.pages and trap_ids:
            self.add_link("page_06", trap_ids[0])

        return trap_ids

    def to_visualization_json(self, pagerank_scores: Optional[Dict[str, float]] = None) -> dict:
        """
        Formats graph for frontend rendering (e.g., Vis.js Network).
        Returns nodes list and edges list.
        """
        in_degrees = self.get_in_degrees()
        out_degrees = self.get_out_degrees()

        # Category color map
        category_colors = {
            "Graph Theory": "#6366F1",         # Indigo
            "PageRank": "#8B5CF6",             # Violet
            "Probability": "#EC4899",          # Pink
            "Information Retrieval": "#3B82F6", # Blue
            "Web Architecture": "#10B981",     # Emerald
            "Web Spam": "#EF4444",             # Red
            "Spider Trap": "#F59E0B",          # Amber
            "Link Spam": "#DC2626",            # Dark Red
            "Custom": "#64748B"                # Slate
        }

        nodes = []
        for pid in self.idx_to_node:
            page = self.pages[pid]
            pr = pagerank_scores.get(pid, 1.0 / max(1, self.num_nodes)) if pagerank_scores else (1.0 / max(1, self.num_nodes))
            in_d = in_degrees.get(pid, 0)
            out_d = out_degrees.get(pid, 0)

            # Node size scaled by PageRank (base 18 + proportional boost)
            node_size = 16 + int(pr * 250)

            color = category_colors.get(page.category, "#0EA5E9")
            nodes.append({
                "id": pid,
                "label": pid,
                "title": f"<b>{page.title}</b><br>Category: {page.category}<br>PageRank: {pr:.5f}<br>In-degree: {in_d} | Out-degree: {out_d}",
                "page_title": page.title,
                "category": page.category,
                "content_snippet": page.content[:100] + "...",
                "in_degree": in_d,
                "out_degree": out_d,
                "pagerank": round(pr, 6),
                "value": node_size,
                "color": {
                    "background": color,
                    "border": "#FFFFFF",
                    "highlight": {"background": "#F43F5E", "border": "#FFE4E6"}
                }
            })

        edges = []
        for u_id, page in self.pages.items():
            for v_id in page.outgoing_links:
                if v_id in self.pages:
                    edges.append({
                        "from": u_id,
                        "to": v_id,
                        "arrows": "to",
                        "color": {"color": "#94A3B8", "highlight": "#F43F5E"},
                        "width": 1.5
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "num_nodes": self.num_nodes,
                "num_edges": len(edges),
                "dangling_nodes": self.get_dangling_nodes()
            }
        }

