# Intelligent Search Ranking Using Web Graphs

A miniature search engine combining **graph topology, Markov chains, random walks, and vector-space textual relevance** for the **Mathematical Foundations of Computer Science (MFCS)** curriculum.

---

## 1. System Overview

Traditional search systems based purely on keyword matching fail when websites manipulate search results via keyword stuffing or when authoritative sources have concise wording. This project models a collection of webpages as a **directed web graph** $G = (V, E)$, computes the stationary probability distribution via the **PageRank algorithm**, evaluates content relevance via the **TF-IDF Vector Space Model**, and intelligently combines both into a **hybrid ranking score**.

```
                           ┌───────────────────────────────────┐
                           │   Webpage Corpus & Graph G=(V,E)  │
                           └─────────────────┬─────────────────┘
                                             │
                     ┌───────────────────────┴───────────────────────┐
                     ▼                                               ▼
         ┌────────────────────────┐                     ┌────────────────────────┐
         │     PageRank Engine    │                     │   Text Relevance (IR)  │
         │  • Google Matrix G     │                     │  • Inverted Index      │
         │  • Dangling mass fix   │                     │  • TF-IDF Vectorizer   │
         │  • Power Iteration     │                     │  • Cosine Similarity   │
         └───────────┬────────────┘                     └───────────┬────────────┘
                     │ [PageRank Vector π]                          │ [Relevance Score R]
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

### 2.1 Graph Theory
* **Web Graph Representation**: A directed graph $G = (V, E)$ where $|V| = N$ webpages and directed edges $(u, v) \in E$ represent hyperlinks from page $u$ to page $v$.
* **Adjacency Matrix** $\mathbf{A} \in \{0, 1\}^{N \times N}$, where $A_{ij} = 1$ if edge $i \to j$ exists.
* **Degree Analysis**:
  * In-degree: $\text{deg}_{\text{in}}(i) = \sum_{j=1}^N A_{ji}$ (number of backlinks/citations).
  * Out-degree: $\text{deg}_{\text{out}}(i) = \sum_{j=1}^N A_{ij}$ (number of outgoing links).
  * Dangling Nodes: $\{i \in V \mid \text{deg}_{\text{out}}(i) = 0\}$ (dead ends).

### 2.2 Markov Chains & The Google Matrix
* A random surfer browses the web graph as a discrete-time Markov chain.
* **Row-Stochastic Transition Matrix** $\mathbf{P}$:
  $$P_{ij} = \begin{cases} \frac{1}{\text{deg}_{\text{out}}(i)} & \text{if } (i, j) \in E \\ 0 & \text{otherwise} \end{cases}$$
* **Dangling Node Mass Redistribution**: For nodes with out-degree 0, probability mass is redistributed uniformly $\frac{\mathbf{1}^T}{N}$ to prevent probability leakage.
* **Teleportation & The Stochastic Google Matrix** $\mathbf{G}$:
  With damping factor $d \in (0, 1)$ (typically $d = 0.85$):
  $$\mathbf{G} = d \mathbf{S} + (1 - d) \frac{\mathbf{1}\mathbf{1}^T}{N}$$
* **Perron-Frobenius Theorem**: Because $\mathbf{G}$ has strictly positive entries ($G_{ij} > 0$), the Markov chain is **ergodic (irreducible and aperiodic)**. Thus, there exists a unique stationary distribution $\boldsymbol{\pi}$ satisfying:
  $$\boldsymbol{\pi}\mathbf{G} = \boldsymbol{\pi}, \quad \sum_{i=1}^N \pi_i = 1$$
* **Power Iteration Method**:
  $$\mathbf{p}^{(t+1)} = d \left( \mathbf{p}^{(t)} \mathbf{P} + \left( \sum_{k \in \text{dangling}} p_k^{(t)} \right) \frac{\mathbf{1}}{N} \right) + (1 - d) \frac{\mathbf{1}}{N}$$
  Iterations continue until $\|\mathbf{p}^{(t+1)} - \mathbf{p}^{(t)}\|_1 < 10^{-8}$.

### 2.3 Monte Carlo Random Walk Surfer
* Simulates explicit surfer trajectories of length $T$.
* Demonstrates the **Ergodic Theorem / Strong Law of Large Numbers for Markov Chains**:
  $$\lim_{T \to \infty} \hat{\pi}_i(T) = \lim_{T \to \infty} \frac{C_i(T)}{T} = \pi_i$$
  where $C_i(T)$ is the count of visits to vertex $i$.

### 2.4 Information Retrieval & Vector Space Model
* **Sublinear TF Weighting**: $\text{TF}(t, d) = 1 + \ln(f_{t, d})$ if $f_{t, d} > 0$, else $0$.
* **Smoothed Inverse Document Frequency**:
  $$\text{IDF}(t) = \ln\left( \frac{N + 1}{\text{df}(t) + 1} \right) + 1$$
* **Cosine Similarity**:
  $$R(d, q) = \frac{\mathbf{v}_d \cdot \mathbf{v}_q}{\|\mathbf{v}_d\|_2 \|\mathbf{v}_q\|_2}$$

### 2.5 Hybrid Ranking & Correlation
* **Candidate Normalization**:
  $$R_{\text{norm}}(d) = \frac{R(d, q) - R_{\min}}{R_{\max} - R_{\min} + \epsilon}, \quad PR_{\text{norm}}(d) = \frac{PR(d) - PR_{\min}}{PR_{\max} - PR_{\min} + \epsilon}$$
* **Convex Score Fusion**:
  $$\text{FinalScore}(d, q) = \alpha \cdot R_{\text{norm}}(d) + (1 - \alpha) \cdot PR_{\text{norm}}(d), \quad \alpha \in [0, 1]$$
* **Spearman's Rank Correlation Coefficient**:
  $$\rho = 1 - \frac{6 \sum d_i^2}{k(k^2 - 1)}$$

---

## 3. Directory Structure

```
Intelligent_Search_Ranking/
├── README.md
├── requirements.txt
├── data/
│   └── corpus.json              # 18-page academic corpus with hyperlinks
├── src/
│   ├── __init__.py
│   ├── graph.py                 # Graph data structures, adjacency & degrees
│   ├── pagerank.py              # Power iteration & Perron-Frobenius verification
│   ├── random_walk.py           # Monte Carlo Markov chain surfer
│   ├── text_engine.py           # Inverted index, TF-IDF vectorizer & cosine similarity
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
    ├── test_engines.py          # Math verification unit tests
    └── test_api.py              # Flask endpoint integration tests
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
*(All 13 mathematical and API tests run in < 0.5s)*

### Launch Interactive Web Studio
```bash
python -m src.app
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

*Features a one-click **Light/Dark theme toggle** in the top navigation bar with persistent preference.*

---

## 5. Interactive Studio Capabilities

1. **Search Studio**:
   * Live hybrid search with instant 3-way ranking comparison columns:
     * **Column 1**: Pure Lexical / Keyword matching ($\alpha = 1.0$)
     * **Column 2**: Pure Hyperlink PageRank ($\alpha = 0.0$)
     * **Column 3**: Hybrid Intelligent Combined Ranking
   * Real-time $\alpha$ slider $(0 \le \alpha \le 1)$ and damping factor slider $d \in [0.5, 0.99]$.
   * Live Spearman $\rho$ correlation and rank displacement pills ($\uparrow +3$ or $\downarrow -2$).
2. **Graph Explorer**:
   * Interactive physics-based Vis.js directed graph visualization.
   * Node size proportional to PageRank score.
   * Vertex inspector displaying in-degree, out-degree, and hyperlink neighborhood.
   * Live dynamic edge editor: add or sever links in real time!
3. **Random Surfer Lab**:
   * Monte Carlo random walk simulation across thousands of steps.
   * Live Chart.js bar chart comparing empirical visit frequency $\hat{\pi}_i$ vs theoretical stationary PageRank $\pi_i$.
   * $L_1$ convergence error metric tracking.
4. **What-If & Adversarial Experiment Lab**:
   * **Sybil / Link Farm Attack**: Injects 5 synthetic bot nodes to test artificial rank inflation on `page_16` (Personal Tech Blog).
   * **Spider Trap Simulation**: Injects a 2-cycle closed loop to demonstrate probability absorption with and without teleportation ($d = 0.85$ vs $d = 0.99$).
   * **Damping Factor Sensitivity Curve**: Plots Shannon entropy and iteration count across $d \in [0.10, 0.99]$.
   * **Reset Graph**: One-click restore to baseline graph topology.

