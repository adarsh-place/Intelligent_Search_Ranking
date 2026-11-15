# Intelligent Search Ranking Using Web Graphs

A discrete mathematical search engine combining **graph theory, coupled linear recurrence relations, propositional logic, and algebraic matrix rings** for authoritative information retrieval.

---

## 1. System Overview

Traditional search systems based purely on keyword matching fail when websites manipulate search results via keyword stuffing or when authoritative reference sources have concise wording. This project models a collection of webpages as a **directed web graph** $G = (V, E)$, computes the stationary authority distribution via **conservative network flows and linear recurrence relations**, evaluates query relevance via **propositional logic and vector space models**, and combines both into a **hybrid ranking score**.

```
                           ┌───────────────────────────────────┐
                           │   Webpage Corpus & Graph G=(V,E)  │
                           └─────────────────┬─────────────────┘
                                             │
                     ┌───────────────────────┴───────────────────────┐
                     ▼ (Graph Theory & Recurrences)                  ▼ (Logic & Vector Spaces)
         ┌────────────────────────┐                     ┌────────────────────────┐
         │ Recurrence Flow Engine │                     │   Text Relevance (IR)  │
         │  • Network Flow P_ij   │                     │  • Propositional Logic │
         │  • Recurrence x^(t+1)  │                     │  • Inclusion-Exclusion │
         │  • Inductive Proof     │                     │  • TF-IDF Vector Space │
         │  • Matrix Powers A^k   │                     │  • Cosine Similarity   │
         └───────────┬────────────┘                     └───────────┬────────────┘
                     │ [PageRank Flow Vector x*]                    │ [Relevance Score R]
                     └───────────────────────┬───────────────────────┘
                                             ▼
                               ┌──────────────────────────┐
                               │  Candidate Normalization │
                               │  (Min-Max per Query)     │
                               └─────────────┬────────────┘
                                             ▼
                               ┌──────────────────────────┐
                               │   Convex Hybrid Fusion   │
                               │ α·R_norm + (1-α)·PR_norm │
                               └─────────────┬────────────┘
                                             ▼
                               ┌──────────────────────────┐
                               │  3-Way Ranking Dashboard │
                               │  & Spearman Correlation  │
                               └──────────────────────────┘
```

---

## 2. Mathematical Foundations

### 2.1 Graph Theory & Network Flows
* **Web Graph Representation**: A directed graph $G = (V, E)$ where $|V| = N$ webpages and directed edges $(u, v) \in E$ represent hyperlinks from page $u$ to page $v$.
* **Adjacency Matrix** $\mathbf{A} \in \{0, 1\}^{N \times N}$, where $A_{ij} = 1$ if edge $i \to j$ exists.
* **Degree Analysis**:
  * In-degree: $\text{deg}_{\text{in}}(i) = \sum_{j=1}^N A_{ji}$ (number of citations/backlinks).
  * Out-degree: $\text{deg}_{\text{out}}(i) = \sum_{j=1}^N A_{ij}$ (branching factor).
  * Dangling Nodes: $\{i \in V \mid \text{deg}_{\text{out}}(i) = 0\}$ (sinks).
* **Conservative Network Flow**: Each webpage evenly divides its authority among its outgoing links:
  $$P_{ij} = \begin{cases} \frac{1}{\text{deg}_{\text{out}}(i)} & \text{if } (i, j) \in E \\ 0 & \text{otherwise} \end{cases}$$
* **Dangling Sinks Fix**: For nodes with out-degree zero, authority mass is redistributed uniformly $\frac{\mathbf{1}^T}{N}$ to conserve flow.

### 2.2 Combinatorics & Coupled Recurrence Relations
* **Coupled Linear Recurrence Relation**:
  Authority flow across discrete steps is governed by the recurrence relation:
  $$\mathbf{x}^{(t+1)} = d \left( \mathbf{x}^{(t)} \mathbf{P} + \left( \sum_{k \in \text{dangling}} x_k^{(t)} \right) \frac{\mathbf{1}^T}{N} \right) + (1 - d) \frac{\mathbf{1}^T}{N}$$
  Iterations contract geometrically until $\|\mathbf{x}^{(t+1)} - \mathbf{x}^{(t)}\|_1 < 10^{-8}$.
* **Generating Functions & Resolvent Operator**:
  The stationary flow vector satisfies the resolvent $\mathbf{x}^* = \frac{1-d}{N}\mathbf{1}^T (\mathbf{I} - d\mathbf{S})^{-1} = \frac{1-d}{N}\mathbf{1}^T \sum_{k=0}^\infty d^k \mathbf{S}^k$.
* **Combinatorial Path Counting via Matrix Powers $\mathbf{A}^k$**:
  The entry $(\mathbf{A}^k)_{ij}$ counts the exact number of directed paths of length $k$ between vertex $i$ and vertex $j$.
* **Inclusion-Exclusion Principle**:
  Computes multi-term query candidate document set cardinalities across inverted index postings:
  $$|\mathcal{A} \cup \mathcal{B}| = |\mathcal{A}| + |\mathcal{B}| - |\mathcal{A} \cap \mathcal{B}|$$

### 2.3 Logic and Proof Techniques
* **Propositional Logic & Satisfiability**:
  Evaluates Boolean term predicates $P(t_k, d) \in \{0, 1\}$ over inverted index postings lists to identify candidate documents that satisfy the query.
* **Mathematical Induction on Flow Invariance**:
  Proves that total network flow $\sum_{i=1}^N x_i^{(t)} = 1.0$ is strictly conserved for all $t \ge 0$:
  * **Base Step**: $\sum_{i=1}^N x_i^{(0)} = N \cdot (1/N) = 1.0$.
  * **Inductive Step**: $\sum_{i=1}^N x_i^{(t+1)} = d(1.0) + (1 - d)(1.0) = 1.0$.

### 2.4 Algebraic Structures & Number Theory
* **Matrix Ring $M_N(\mathbb{R})$ & Invariant Subspaces**:
  The transition operator $\mathbf{P}$ and Google matrix $\mathbf{G} = d\mathbf{S} + \frac{1-d}{N}\mathbf{1}\mathbf{1}^T$ act as operators in a matrix ring. The recurrence converges to the dominant invariant subspace ($\lambda = 1$) satisfying $\mathbf{x}^* \mathbf{G} = \mathbf{x}^*$.
* **Metric Vector Space Model in $\mathbb{R}^{|V|}$**:
  Evaluates query-document similarity via inner products and cosine similarity with sublinear TF and smoothed IDF:
  $$R(d, q) = \frac{\langle \mathbf{v}_d, \mathbf{v}_q \rangle}{\|\mathbf{v}_d\|_2 \|\mathbf{v}_q\|_2}$$

### 2.5 Hybrid Ranking & Score Fusion
* **Candidate Normalization**:
  $$R_{\text{norm}}(d) = \frac{R(d, q) - R_{\min}}{R_{\max} - R_{\min} + \delta}, \quad PR_{\text{norm}}(d) = \frac{PR(d) - PR_{\min}}{PR_{\max} - PR_{\min} + \delta}$$
* **Convex Score Fusion**:
  $$\text{FinalScore}(d, q) = \alpha \cdot R_{\text{norm}}(d) + (1 - \alpha) \cdot PR_{\text{norm}}(d), \quad \alpha \in [0, 1]$$
* **Spearman's Rank Correlation**:
  $$\rho = 1 - \frac{6 \sum d_i^2}{k(k^2 - 1)}$$

---

## 3. Directory Structure

```
Intelligent_Search_Ranking/
├── README.md
├── PROBLEM_STATEMENT.md
├── requirements.txt
├── Intelligent_Search_Ranking_Presentation.pptx  # 5-min academic slide deck
├── scripts/
│   └── generate_pptx.py         # 5-minute academic presentation generator
├── data/
│   └── corpus.json              # 18-page academic corpus with hyperlinks
├── src/
│   ├── __init__.py
│   ├── graph.py                 # Graph data structures, adjacency & matrix powers A^k
│   ├── pagerank.py              # Power iteration & mathematical induction verifier
│   ├── recurrence_flow.py       # Step-by-step linear recurrence simulator
│   ├── random_walk.py           # Compatibility wrapper
│   ├── text_engine.py           # Inverted index, TF-IDF vectorizer & inclusion-exclusion
│   ├── ranking.py               # Hybrid score fusion & Spearman rank correlation
│   ├── experiments.py           # Sybil spam & spider trap experiment suites
│   └── app.py                   # Flask server with REST API
├── static/
│   ├── css/
│   │   └── style.css            # Custom design & responsive layout
│   └── js/
│       └── main.js              # Network visualizer (Vis.js) & Chart.js controller
├── templates/
│   └── index.html               # 4-in-1 Interactive Academic Research Studio
└── tests/
    ├── test_engines.py          # Math verification unit tests (Induction, Paths, Rings)
    └── test_api.py              # Flask REST endpoint integration tests
```

---

## 4. How to Run

### Installation
```bash
pip install -r requirements.txt
```

### Run Automated Test Suite
```bash
python -m pytest -v
```
*(All 16 mathematical, algorithmic, and REST API tests pass in < 0.4s)*

### Launch Interactive Web Studio
```bash
python -m src.app
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 5. Interactive Studio Capabilities

1. **Search Studio**:
   * **Clean & Focused Stream**: Modern, spacious search cards with matched keyword tags and rank displacement indicators.
   * **Mathematical Score Inspector**: Clicking any card shows its exact score decomposition bar (Relevance % vs Authority %) and convex combination.
   * **Instant 3-Way Compare Mode**: Toggle from Focused to 3-Way Comparison to inspect **Keyword (TF-IDF)** vs **PageRank** vs **Combined Hybrid** rankings side-by-side.
   * **Real-Time Sliders**: Real-time slider for **$\alpha$ (Relevance vs Authority)** and **$d$ (Damping factor)**.
2. **Graph Explorer**:
   * Interactive physics-based Vis.js directed graph visualization.
   * Node size proportional to PageRank authority score.
   * Vertex inspector displaying in-degree, out-degree, and hyperlink neighborhood.
   * Live dynamic edge editor: add or sever links in real time!
3. **Recurrence & Flow Convergence Lab**:
   * Step-by-step linear recurrence simulation across discrete iterations.
   * Live Chart.js bar chart showing authority flow distribution across nodes.
   * Mathematical Induction flow invariance verification badge ($\sum x_i = 1.0$).
   * Combinatorial walk counts via matrix powers ($A^1, A^2, A^3$).
   * Interactive Inclusion-Exclusion principle verifier ($|A \cup B| = |A| + |B| - |A \cap B|$).
4. **What-If & Adversarial Experiment Lab**:
   * **Sybil / Link Farm Attack**: Injects 5 synthetic bot nodes to demonstrate artificial rank inflation on `page_16`.
   * **Spider Trap Simulation**: Injects a 2-cycle closed loop to demonstrate authority absorption with and without uniform redistribution ($d = 0.85$ vs $d = 0.99$).
   * **Damping Factor Sensitivity Sweep**: Plots distribution entropy and iteration count across $d \in [0.10, 0.99]$.
   * **Reset Graph**: One-click restore to baseline graph topology.
