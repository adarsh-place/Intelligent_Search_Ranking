"""
Flask Web Application & REST API
MFCS Project - Intelligent Search Ranking Interactive Visualizer
"""

import os
from flask import Flask, render_template, request, jsonify
from .graph import WebGraph
from .pagerank import PageRankEngine
from .random_walk import RandomWalkSimulator
from .text_engine import TextRelevanceEngine
from .ranking import RankingEngine
from .experiments import ExperimentSuite

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "corpus.json")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Global graph & engine state
graph = WebGraph(DATA_PATH)
pr_engine = PageRankEngine(graph)
text_engine = TextRelevanceEngine(graph)
ranking_engine = RankingEngine(graph, text_engine, pr_engine)
exp_suite = ExperimentSuite(DATA_PATH)


def refresh_engines():
    """Refreshes text indexing and ranking engine after graph mutations."""
    global text_engine, ranking_engine, pr_engine
    pr_engine = PageRankEngine(graph)
    text_engine.build_index()
    ranking_engine = RankingEngine(graph, text_engine, pr_engine)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/graph", methods=["GET"])
def get_graph():
    """Returns nodes and edges formatted for Vis.js visualization."""
    damping = float(request.args.get("damping", 0.85))
    scores, meta = pr_engine.compute(damping_factor=damping)
    graph_data = graph.to_visualization_json(scores)
    graph_data["metadata"] = meta
    return jsonify(graph_data)


@app.route("/api/search", methods=["POST"])
def search():
    """Performs hybrid search, returning 3-way ranking comparison."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    alpha = float(data.get("alpha", 0.50))
    damping = float(data.get("damping", 0.85))
    filter_unmatched = bool(data.get("filter_unmatched", True))

    results = ranking_engine.rank_query(
        query=query,
        alpha=alpha,
        damping_factor=damping,
        filter_unmatched=filter_unmatched
    )
    return jsonify(results)


@app.route("/api/random_walk", methods=["POST"])
def random_walk():
    """Simulates Markov random surfer and returns empirical distribution and trajectory."""
    data = request.get_json() or {}
    num_steps = int(data.get("num_steps", 1500))
    damping = float(data.get("damping", 0.85))
    start_node = data.get("start_node", None)

    # Calculate theoretical stationary distribution for comparison
    theoretical_pr, _ = pr_engine.compute(damping_factor=damping)

    simulator = RandomWalkSimulator(graph, damping_factor=damping)
    sim_result = simulator.simulate(
        num_steps=num_steps,
        start_node=start_node,
        theoretical_pr=theoretical_pr
    )
    return jsonify(sim_result)


@app.route("/api/graph/add_link", methods=["POST"])
def add_link():
    data = request.get_json() or {}
    source = data.get("source")
    target = data.get("target")

    if not source or not target:
        return jsonify({"success": False, "error": "Source and target required"}), 400

    success = graph.add_link(source, target)
    if success:
        refresh_engines()
    return jsonify({"success": success})


@app.route("/api/graph/remove_link", methods=["POST"])
def remove_link():
    data = request.get_json() or {}
    source = data.get("source")
    target = data.get("target")

    if not source or not target:
        return jsonify({"success": False, "error": "Source and target required"}), 400

    success = graph.remove_link(source, target)
    if success:
        refresh_engines()
    return jsonify({"success": success})


@app.route("/api/graph/inject_spam", methods=["POST"])
def inject_spam():
    """Injects a link farm pointing to target page."""
    data = request.get_json() or {}
    target_id = data.get("target_id", "page_16")
    num_bots = int(data.get("num_bots", 5))

    try:
        created_ids = graph.inject_link_farm(target_id, num_spam_pages=num_bots)
        refresh_engines()
        return jsonify({"success": True, "created_ids": created_ids})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/graph/inject_trap", methods=["POST"])
def inject_trap():
    """Injects a spider trap into the web graph."""
    try:
        trap_ids = graph.inject_spider_trap(num_nodes=2)
        refresh_engines()
        return jsonify({"success": True, "trap_ids": trap_ids})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/graph/reset", methods=["POST"])
def reset_graph():
    """Resets the graph to the baseline corpus."""
    graph.reset_to_default()
    refresh_engines()
    return jsonify({"success": True})


@app.route("/api/experiments/damping", methods=["GET"])
def experiment_damping():
    """Returns sensitivity analysis across damping factors."""
    results = pr_engine.sensitivity_study()
    return jsonify(results)


@app.route("/api/experiments/spam", methods=["GET", "POST"])
def experiment_spam():
    target_node = request.args.get("target_id", "page_16")
    num_bots = int(request.args.get("num_bots", 5))
    mutate = request.args.get("mutate", "true").lower() == "true"

    if not mutate:
        result = exp_suite.run_spam_experiment(target_node=target_node, num_bots=num_bots)
        return jsonify(result)

    # Execute on live web graph
    base_scores, _ = pr_engine.compute(damping_factor=0.85)
    base_search = ranking_engine.rank_query("PageRank", alpha=0.50, damping_factor=0.85)
    target_base_rank = next((item["combined_rank"] for item in base_search["combined_ranking"] if item["id"] == target_node), None)
    target_base_pr = base_scores.get(target_node, 0.0)

    created_ids = graph.inject_link_farm(target_node, num_spam_pages=num_bots)
    refresh_engines()

    spam_scores, _ = pr_engine.compute(damping_factor=0.85)
    spam_search = ranking_engine.rank_query("PageRank", alpha=0.50, damping_factor=0.85)
    target_spam_rank = next((item["combined_rank"] for item in spam_search["combined_ranking"] if item["id"] == target_node), None)
    target_spam_pr = spam_scores.get(target_node, 0.0)

    pr_increase_pct = ((target_spam_pr - target_base_pr) / (target_base_pr + 1e-12)) * 100.0

    return jsonify({
        "target_node": target_node,
        "target_title": graph.pages[target_node].title if target_node in graph.pages else target_node,
        "num_bots_injected": num_bots,
        "bot_ids": created_ids,
        "baseline_pr": round(target_base_pr, 6),
        "spam_pr": round(target_spam_pr, 6),
        "pr_percentage_gain": round(pr_increase_pct, 2),
        "baseline_combined_rank": target_base_rank,
        "spam_combined_rank": target_spam_rank,
        "rank_jump": (target_base_rank - target_spam_rank) if (target_base_rank and target_spam_rank) else 0
    })


@app.route("/api/experiments/trap", methods=["GET", "POST"])
def experiment_trap():
    mutate = request.args.get("mutate", "true").lower() == "true"
    if not mutate:
        result = exp_suite.run_spider_trap_experiment()
        return jsonify(result)

    trap_nodes = graph.inject_spider_trap(num_nodes=2)
    refresh_engines()

    scores_d85, _ = pr_engine.compute(damping_factor=0.85)
    trap_mass_d85 = sum(scores_d85.get(t, 0.0) for t in trap_nodes)

    scores_d99, _ = pr_engine.compute(damping_factor=0.99)
    trap_mass_d99 = sum(scores_d99.get(t, 0.0) for t in trap_nodes)

    return jsonify({
        "trap_nodes": trap_nodes,
        "trap_mass_with_damping_085": round(float(trap_mass_d85), 5),
        "trap_mass_with_damping_099": round(float(trap_mass_d99), 5),
        "mass_difference_pct": round(((trap_mass_d99 - trap_mass_d85) / max(1e-6, trap_mass_d85)) * 100, 2),
        "theoretical_insight": "Teleportation (1-d) prevents closed cycle subgraphs from absorbing all random walk probability."
    })


@app.route("/api/corpus", methods=["GET"])
def get_corpus():
    """Returns all pages currently in the graph."""
    pages_list = []
    for pid, p in graph.pages.items():
        pages_list.append({
            "id": p.id,
            "title": p.title,
            "category": p.category,
            "content": p.content,
            "outgoing_links": p.outgoing_links
        })
    return jsonify(pages_list)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

