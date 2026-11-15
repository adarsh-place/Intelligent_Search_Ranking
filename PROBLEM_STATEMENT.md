# PROJECT PROBLEM STATEMENT & SYSTEM SPECIFICATION

## Intelligent Search Ranking Using Web Graphs
### *A Discrete Mathematical Search Engine Combining Graph Theory, Conservative Network Flows, Linear Recurrences, and Vector Space Retrieval*

**Technical Specification Document**  
**Core Disciplines Applied:**
* **Directed Graph Theory & Network Flows**: Directed Web Graphs, Adjacency Matrices, In/Out Degrees, Conservative Authority Flow, Singularities & Traps
* **Coupled Linear Recurrence Relations**: Discrete Power Iteration, Damped Mass Redistribution, Geometric Contraction & Stationary Equilibrium
* **Mathematical Induction & Invariance**: Formal Inductive Proof of Flow Conservation across all discrete iterations
* **Information Retrieval & Vector Space Models**: Inverted Index Postings, Sublinear TF-IDF Term Weighting, and Cosine Vector Similarity

---

## 1. Executive Summary & Problem Overview

The explosive expansion of the World Wide Web has produced billions of interconnected hypertext documents. When a user executes a search query, traditional search architectures locate hundreds or thousands of documents containing matching terms. Determining which documents are genuinely authoritative, relevant, and trustworthy constitutes one of the foundational challenges of computer science and information retrieval.

A naive lexical search engine ranks documents strictly by keyword frequency. However, pure keyword retrieval suffers from severe structural vulnerabilities:
1. **Keyword Stuffing & Lexical Manipulation**: A low-quality webpage can artificially inflate target keyword occurrences to dominate term-frequency heuristics without providing substantive value.
2. **Authoritative Conciseness Dilemma**: Pioneering, seminal reference documents are often concise, having lower raw term counts than verbose, unauthoritative blogs.
3. **Absence of Topological Authority (Document Silo Illusion)**: Pure keyword frequency treats documents as isolated, disconnected silos, ignoring the rich structure of peer citations and hyperlink endorsements.

This project, **"Intelligent Search Ranking Using Web Graphs,"** designs and implements an end-to-end discrete mathematical search retrieval and ranking engine. It unifies **Graph Theory & Conservative Network Flows**, **Coupled Linear Recurrence Relations**, **Mathematical Induction**, and **Vector Space Information Retrieval** into an intelligent hybrid ranking framework.

Webpages are modeled as vertices in a directed web graph $G = (V, E)$, structural prestige is computed via a conservative network flow linear recurrence, and textual similarity is computed via inverted index term evaluation in an algebraic vector space model. A candidate-level convex score fusion engine dynamically balances query satisfaction against structural authority, supported by a full interactive research studio.

---

## 2. Core Mathematical Objectives

1. **Directed Web Graph Construction**: Model interconnected webpages as a directed graph $G = (V, E)$, formalizing edge connectivity through adjacency lists and adjacency matrices $\mathbf{A} \in \{0, 1\}^{N \times N}$.
2. **Topological Degree & Singularity Analysis**: Compute in-degree (citation volume), out-degree (branching factor), and detect graph singularities including dead ends (sinks / dangling nodes with out-degree zero) and absorbing cycles (spider traps).
3. **Conservative Network Flow Formulation**: Model hyperlinks as directed conduits where each vertex conserves authority by evenly dividing its flow among outgoing edges with capacity $\frac{1}{\text{deg}_{\text{out}}(u)}$.
4. **Coupled Linear Recurrence Relations**: Formulate authority flow as a discrete first-order linear recurrence relation:
   $$\mathbf{x}^{(t+1)} = d \left( \mathbf{x}^{(t)} \mathbf{P} + \left( \sum_{k \in \text{dangling}} x_k^{(t)} \right) \frac{\mathbf{1}^T}{N} \right) + (1 - d) \frac{\mathbf{1}^T}{N}$$
   establishing geometric convergence to a unique stationary flow distribution.
5. **Mathematical Induction on Flow Invariance**: Prove and verify via Mathematical Induction that the total network flow invariant $\sum_{i=1}^N x_i^{(t)} = 1.0$ is preserved strictly across all iterations $t \ge 0$.
6. **Vector Space Model (VSM) Information Retrieval**: Construct an inner product space $\mathbb{R}^{|V|}$ with sublinear term-frequency scaling and smoothed inverse document frequency (IDF) to evaluate query-document cosine similarity:
   $$R(d, q) = \frac{\langle \mathbf{v}_d, \mathbf{v}_q \rangle}{\|\mathbf{v}_d\|_2 \|\mathbf{v}_q\|_2}$$
7. **Candidate-Level Normalization & Convex Hybrid Fusion**: Implement min-max candidate normalization to place disparate dimensional scales into $[0, 1]$, computing:
   $$\text{FinalScore}(p, q) = \alpha \cdot R_{\text{norm}}(p, q) + (1 - \alpha) \cdot PR_{\text{norm}}(p)$$
8. **Adversarial & Graph Mutation Experiments**: Experimentally investigate the susceptibility and resilience of web graph ranking against Sybil link farm attacks, spider trap absorbing cycles, and variations in the damping factor $d \in [0.10, 0.99]$.
9. **Interactive Research Studio & Visualizer**: Provide an interactive web dashboard with dual light/dark theming, live force-directed graph physics, a step-by-step recurrence convergence lab, and real-time parameter tuning.

---

## 3. Detailed Mathematical Formulations

```
       [Webpage Text Corpus]                      [Directed Hyperlinks]
                 │                                          │
                 ▼ (Vector Space Model)                     ▼ (Graph Topology)
     ┌───────────────────────┐                  ┌───────────────────────┐
     │ Inverted Index & VSM  │                  │  Directed Graph G(V,E)│
     │  • Lexical Postings   │                  │  • Adjacency Matrix A │
     │  • TF-IDF Weighting   │                  │  • In/Out Degrees     │
     │  • Cosine Similarity  │                  │  • Flow Conservation  │
     └───────────┬───────────┘                  └───────────┬───────────┘
                 │                                          │
                 │                                          ▼ (Recurrence & Flows)
                 │                              ┌───────────────────────┐
                 │                              │ Recurrence Flow Engine│
                 │                              │  • Coupled Recurrence │
                 │                              │  • Damped Iteration   │
                 │                              │  • Inductive Proof    │
                 │                              │  • Stationary x*      │
                 │                              └───────────┬───────────┘
                 │ [Relevance Score R]                      │ [Flow Rank Vector x*]
                 └───────────────────────┬──────────────────┘
                                         ▼
                         ┌───────────────────────────────┐
                         │   Candidate Min-Max Normalizer│
                         │      R_norm  &  PR_norm       │
                         └───────────────┬───────────────┘
                                         ▼
                         ┌───────────────────────────────┐
                         │      Convex Score Fusion      │
                         │   α·R_norm + (1-α)·PR_norm    │
                         └───────────────┬───────────────┘
                                         ▼
                         ┌───────────────────────────────┐
                         │   3-Way Comparative Ranking   │
                         │    & Spearman Correlation ρ   │
                         └───────────────────────────────┘
```

### 3.1 Graph Theory & Network Flows
Let $V = \{v_1, v_2, \dots, v_N\}$ be the finite set of $N$ webpage vertices, and $E \subseteq V \times V$ be the set of directed edges where $(u, v) \in E$ indicates an outbound hyperlink from $u$ to $v$.
* **Adjacency Matrix** $\mathbf{A} \in \{0, 1\}^{N \times N}$:
  $$A_{ij} = \begin{cases} 1 & \text{if } (i, j) \in E \\ 0 & \text{otherwise} \end{cases}$$
* **In-Degree** (Citation Volume): $\text{deg}_{\text{in}}(i) = \sum_{j=1}^N A_{ji}$
* **Out-Degree** (Branching Factor): $\text{deg}_{\text{out}}(i) = \sum_{j=1}^N A_{ij} = L(i)$
* **Conservative Network Flow**: Each webpage evenly divides its authority among its outgoing links:
  $$P_{ij} = \begin{cases} \frac{1}{L(i)} & \text{if } (i, j) \in E \\ 0 & \text{otherwise} \end{cases}$$
* **Dangling Node Mass Redistribution**: When $L(i) = 0$ (a sink node), flow cannot leave node $i$. To conserve total flow, dangling rows redistribute their authority evenly to all $N$ vertices via $\frac{\mathbf{1}^T}{N}$:
  $$\mathbf{S} = \mathbf{P} + \mathbf{a} \frac{\mathbf{1}^T}{N}$$
  where $a_i = 1$ if $L(i) = 0$, and $a_i = 0$ otherwise.

### 3.2 Coupled Linear Recurrence Relations & Convergence
* **Coupled Linear Recurrence Relation**:
  Authority flow across discrete iteration steps is governed by the first-order coupled linear recurrence:
  $$\mathbf{x}^{(t+1)} = d \left( \mathbf{x}^{(t)}\mathbf{P} + \left(\sum_{k \in \text{dangling}} x_k^{(t)}\right) \frac{\mathbf{1}^T}{N} \right) + (1 - d) \frac{\mathbf{1}^T}{N}$$
  where $d \in (0, 1)$ is the damping factor (typically $0.85$). The constant injection $\frac{1-d}{N}$ ensures graph reachability and prevents flow stagnation.
* **Geometric Contraction & Unique Fixed Point**:
  The recurrence forms a contraction mapping under the $L_1$ norm:
  $$\|\mathbf{x}^{(t+1)} - \mathbf{x}^{(t)}\|_1 \le d \|\mathbf{x}^{(t)} - \mathbf{x}^{(t-1)}\|_1$$
  Because $d < 1$, the sequence converges geometrically to a unique stationary equilibrium vector $\mathbf{x}^*$ satisfying:
  $$\mathbf{x}^* = d \mathbf{x}^* \mathbf{S} + (1 - d) \frac{\mathbf{1}^T}{N}$$

### 3.3 Flow Invariance Proof by Mathematical Induction
We prove by Mathematical Induction that the total network flow remains strictly invariant across all recurrence steps:
$$\forall t \in \mathbb{N} \cup \{0\}, \quad \sum_{i=1}^N x_i^{(t)} = 1.0$$
* **Base Step ($t = 0$)**:
  Initialize $\mathbf{x}^{(0)} = \left[ \frac{1}{N}, \frac{1}{N}, \dots, \frac{1}{N} \right]$.
  $$\sum_{i=1}^N x_i^{(0)} = N \cdot \frac{1}{N} = 1.0 \quad \text{(Verified)}$$
* **Inductive Hypothesis**:
  Assume that for some $t = k \ge 0$, $\sum_{i=1}^N x_i^{(k)} = 1.0$.
* **Inductive Step ($t = k + 1$)**:
  $$\mathbf{x}^{(k+1)} = d \mathbf{x}^{(k)} \mathbf{S} + (1 - d) \frac{\mathbf{1}^T}{N}$$
  Summing both sides:
  $$\sum_{i=1}^N x_i^{(k+1)} = d \sum_{i=1}^N (\mathbf{x}^{(k)}\mathbf{S})_i + (1 - d) \sum_{i=1}^N \frac{1}{N}$$
  Because $\mathbf{S}$ has row sums equal to 1, $\sum_{i=1}^N (\mathbf{x}^{(k)}\mathbf{S})_i = \sum_{j=1}^N x_j^{(k)} = 1.0$ (by the inductive hypothesis).
  $$\sum_{i=1}^N x_i^{(k+1)} = d(1.0) + (1 - d)(1.0) = d + 1 - d = 1.0 \quad \text{(Verified)}$$
  By the Principle of Mathematical Induction, total network flow is conserved for all $t \ge 0$.

### 3.4 Vector Space Model (VSM) Information Retrieval
Document and query texts are projected as vectors into high-dimensional space $\mathbb{R}^{|V_{\text{vocab}}|}$ with inner product $\langle \mathbf{u}, \mathbf{v} \rangle = \sum u_i v_i$:
* **Sublinear Term Frequency**:
  $$\text{TF}(t, d) = \begin{cases} 1 + \ln(f_{t, d}) & \text{if } f_{t, d} > 0 \\ 0 & \text{otherwise} \end{cases}$$
* **Smoothed Inverse Document Frequency**:
  $$\text{IDF}(t) = \ln\left( \frac{N + 1}{\text{df}(t) + 1} \right) + 1$$
* **Cosine Similarity Metric**:
  $$R(d, q) = \frac{\langle \mathbf{v}_d, \mathbf{v}_q \rangle}{\|\mathbf{v}_d\|_2 \|\mathbf{v}_q\|_2} = \frac{\sum_{t \in q \cap d} w_{t, d} \cdot w_{t, q}}{\sqrt{\sum_{t \in d} w_{t, d}^2} \sqrt{\sum_{t \in q} w_{t, q}^2}}$$

### 3.5 Candidate Score Normalization & Convex Hybrid Fusion
Because cosine similarity $R(d, q) \in [0, 1]$ and PageRank flow vector entries $x^*_d \approx \frac{1}{N}$ occupy disparate numerical scales, candidate-level Min-Max normalization is performed:
$$R_{\text{norm}}(d) = \frac{R(d, q) - R_{\min}}{R_{\max} - R_{\min} + \delta}, \quad PR_{\text{norm}}(d) = \frac{x^*_d - x^*_{\min}}{x^*_{\max} - x^*_{\min} + \delta}$$
where $\delta = 10^{-12}$. The final ranking is determined by the convex combination:
$$\text{FinalScore}(d, q) = \alpha \cdot R_{\text{norm}}(d) + (1 - \alpha) \cdot PR_{\text{norm}}(d), \quad \alpha \in [0, 1]$$

---

## 4. System Architecture & Components

| Component / Layer | Implementation File | Mathematical Foundations |
| :--- | :--- | :--- |
| **Web Graph Engine** | `src/graph.py` | **Graph Theory**: Directed graphs, adjacency matrices, in/out degrees, and dangling sinks. |
| **Recurrence & Flow Engine** | `src/pagerank.py`, `src/recurrence_flow.py` | **Linear Recurrences**: Coupled first-order recurrence, damped power iteration.<br>**Mathematical Induction**: Inductive flow conservation proof ($\sum x_i = 1$). |
| **Information Retrieval Engine** | `src/text_engine.py` | **Vector Space Model**: Inverted index postings, sublinear TF-IDF, and cosine similarity. |
| **Hybrid Ranking Engine** | `src/ranking.py` | Candidate Min-Max normalization, convex combination score fusion, and Spearman rank correlation. |
| **Experimental & Visual Suite** | `src/experiments.py`, `src/app.py`, `static/js/main.js` | Sybil link farm attack simulations, spider trap cycle absorption, damping sensitivity sweeps, and interactive web dashboard. |

---

## 5. Experimental Scenarios & Graph Robustness

### 5.1 Sybil Link Farm Attack (Adversarial Topology)
* **Scenario**: Spammers inject 5 synthetic bot nodes linking cyclically to one another and pointing to a commercial target (`page_16` - Personal Tech Blog) to game keyword ranking.
* **Result**: Injected bot hyperlinks funnel network flow into `page_16`, causing an immediate $150\%$ surge in its flow score and jumping its hybrid rank from #6 to #1.
* **Mathematical Insight**: Proves that graph topology strongly dictates ranking, demonstrating why commercial search engines require TrustRank seed sets.

### 5.2 Spider Trap & Closed Cycle Absorption
* **Scenario**: A closed 2-cycle loop (`trap_1` $\leftrightarrow$ `trap_2`) contains no outbound links to the rest of the web graph.
* **Result**: Without uniform redistribution ($d \to 1.0$), circulating flow is absorbed by the cycle, trapping $>80\%$ of total network authority. Damping at $d = 0.85$ provides guaranteed escape $(1-d)$, stabilizing legitimate node scores.

### 5.3 Damping Sensitivity Sweep ($d \in [0.10, 0.99]$)
* Sweeping $d$ illustrates the trade-off between uniform redistribution and topological fidelity:
  * For $d \to 0$: Flow degrades to uniform distribution $\frac{1}{N}\mathbf{1}^T$.
  * For $d \to 1$: Flow mirrors graph structure, but convergence slows geometrically ($\mathcal{O}(d^t)$). Standard $d = 0.85$ provides optimal stability.

---

## 6. Academic Significance & Conclusion

This project demonstrates the practical synthesis of discrete mathematics:
* **Graph Theory** formalizes web topology and conservative network flows.
* **Linear Recurrence Relations** govern iterative authority flow with guaranteed geometric convergence.
* **Mathematical Induction** rigorously proves flow invariance across all iterations.
* **Vector Space Modeling** enables principled, metric-based textual relevance evaluation.

By integrating these mathematical disciplines into an interactive web application, the project demonstrates how pure discrete mathematics transformed web search from naive keyword counting into a robust, manipulation-resistant science.
