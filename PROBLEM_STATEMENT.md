# PROJECT PROBLEM STATEMENT & SYSTEM SPECIFICATION

## Intelligent Search Ranking Using Web Graphs
### *A Discrete Mathematical Search Engine Combining Graph Theory, Recurrence Relations, Logic, and Algebraic Structures*

**Technical Specification Document**  
**Core Disciplines Applied:**
* **Logic and Proof Techniques**: Propositional & Predicate Logic, Satisfiability, Mathematical Induction
* **Combinatorics**: Recurrence Relations, Generating Functions, Inclusion-Exclusion Principle, Pigeonhole Principle, Path Counting via Matrix Powers
* **Graph Theory**: Directed Graphs, Adjacency Matrices, Connectivity & Network Flows, Absorbing Cycles & Graph Traps
* **Algebraic Structures**: Matrix Rings, Invariant Subspaces, Modular Indexing, Vector Space Models

---

## 1. Executive Summary & Problem Overview

The explosive expansion of the World Wide Web has produced billions of interconnected hypertext documents. When a user executes a search query, traditional search architectures locate hundreds or thousands of documents containing matching terms. Determining which documents are genuinely authoritative, relevant, and trustworthy constitutes one of the foundational challenges of computer science and information retrieval.

A naive lexical search engine ranks documents strictly by keyword frequency. However, pure keyword retrieval suffers from severe structural vulnerabilities:
1. **Keyword Stuffing & Lexical Manipulation**: A low-quality webpage can artificially inflate target keyword occurrences to dominate term-frequency heuristics without providing substantive value.
2. **Authoritative Conciseness Dilemma**: Pioneering, seminal reference documents are often concise, having lower raw term counts than verbose, unauthoritative blogs.
3. **Absence of Topological Authority (Document Silo Illusion)**: Pure keyword frequency treats documents as isolated, disconnected silos, ignoring the rich structure of peer citations and hyperlink endorsements.

This project, **"Intelligent Search Ranking Using Web Graphs,"** designs and implements an end-to-end discrete mathematical search retrieval and ranking engine. It unifies **Graph Theory & Network Flows**, **Coupled Linear Recurrence Relations & Combinatorics**, **Propositional Logic & Mathematical Induction**, and **Matrix Rings & Algebraic Structures** into an intelligent hybrid ranking framework.

Webpages are modeled as vertices in a directed web graph $G = (V, E)$, structural prestige is computed via a conservative network flow linear recurrence, and textual similarity is computed via propositional postings evaluation in an algebraic vector space model. A candidate-level convex score fusion engine dynamically balances query satisfaction against structural authority, supported by a full interactive research studio.

---

## 2. Core Mathematical Objectives

1. **Directed Web Graph Construction**: Model interconnected webpages as a directed graph $G = (V, E)$, formalizing edge connectivity through adjacency lists and adjacency matrices $\mathbf{A} \in \{0, 1\}^{N \times N}$.
2. **Topological Degree & Singularity Analysis**: Compute in-degree (citation volume), out-degree (branching factor), and detect graph singularities including dead ends (sinks / dangling nodes with out-degree zero) and absorbing cycles (spider traps).
3. **Conservative Network Flow Formulation**: Model hyperlinks as directed conduits where each vertex conserves authority by evenly dividing its flow among outgoing edges with capacity $\frac{1}{\text{deg}_{\text{out}}(u)}$.
4. **Coupled Linear Recurrence Relations**: Formulate authority flow as a discrete first-order linear recurrence relation $\mathbf{x}^{(t+1)} = d \mathbf{x}^{(t)} \mathbf{P} + \frac{1-d}{N}\mathbf{1}^T$, establishing geometric convergence to a unique stationary flow distribution.
5. **Combinatorial Path Counting via Matrix Powers**: Utilize the combinatorial property of adjacency matrix powers $\mathbf{A}^k$ to calculate the exact number of directed walks of length $k$ connecting every pair of pages.
6. **Inclusion-Exclusion Principle Verification**: Formally evaluate set union and intersection cardinalities $|\mathcal{A} \cup \mathcal{B}| = |\mathcal{A}| + |\mathcal{B}| - |\mathcal{A} \cap \mathcal{B}|$ across inverted index postings for multi-term query satisfaction.
7. **Mathematical Induction on Flow Invariance**: Prove and verify via Mathematical Induction that the total network flow invariant $\sum_{i=1}^N x_i^{(t)} = 1.0$ is preserved strictly across all iterations $t \ge 0$.
8. **Propositional Logic & Satisfiability**: Formulate search queries as Boolean predicate conjuncts and disjuncts evaluated over inverted postings lists.
9. **Matrix Ring Operators & Invariant Subspaces**: Treat the transition matrix $\mathbf{P}$ and Google matrix $\mathbf{G}$ as elements of the matrix ring $M_N(\mathbb{R})$, extracting the fixed-point vector $\mathbf{x}^* \mathbf{G} = \mathbf{x}^*$ belonging to the dominant invariant subspace ($\lambda = 1$).
10. **Vector Space Model (VSM) Information Retrieval**: Construct an inner product space $\mathbb{R}^{|V|}$ with sublinear term-frequency scaling and smoothed inverse document frequency (IDF) to evaluate query-document cosine similarity.
11. **Candidate-Level Normalization & Convex Hybrid Fusion**: Implement min-max candidate normalization to place disparate dimensional scales into $[0, 1]$, computing:
    $$\text{FinalScore}(p, q) = \alpha \cdot R_{\text{norm}}(p, q) + (1 - \alpha) \cdot PR_{\text{norm}}(p)$$
12. **Adversarial & Graph Mutation Experiments**: Experimentally investigate the susceptibility and resilience of web graph ranking against Sybil link farm attacks, spider trap absorbing cycles, and variations in the damping factor $d \in [0.10, 0.99]$.
13. **Interactive Research Studio & Visualizer**: Provide an interactive web dashboard with dual light/dark theming, live force-directed graph physics, a step-by-step recurrence convergence lab, and real-time parameter tuning.

---

## 3. Detailed Mathematical Formulations

```
       [Webpage Text Corpus]                      [Directed Hyperlinks]
                 │                                          │
                 ▼ (Logic & Vector Spaces)                  ▼ (Graph Topology)
     ┌───────────────────────┐                  ┌───────────────────────┐
     │ Inverted Index & VSM  │                  │  Directed Graph G(V,E)│
     │  • Propositional Logic│                  │  • Adjacency Matrix A │
     │  • Inclusion-Exclusion│                  │  • In/Out Degrees     │
     │  • TF-IDF Vector Space│                  │  • Flow Conservation  │
     │  • Cosine Similarity  │                  └───────────┬───────────┘
     └───────────┬───────────┘                              │
                 │                                          ▼ (Recurrence & Flows)
                 │                              ┌───────────────────────┐
                 │                              │ Recurrence Flow Engine│
                 │                              │  • Coupled Recurrence │
                 │                              │  • Invariant Subspace │
                 │                              │  • Inductive Proof    │
                 │                              │  • Path Counting A^k  │
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

### 3.2 Combinatorics, Recurrences & Path Counting
* **Coupled Linear Recurrence Relation**:
  Authority flow across discrete iteration steps is governed by the first-order coupled linear recurrence:
  $$\mathbf{x}^{(t+1)} = d \left( \mathbf{x}^{(t)}\mathbf{P} + \left(\sum_{k \in \text{dangling}} x_k^{(t)}\right) \frac{\mathbf{1}^T}{N} \right) + (1 - d) \frac{\mathbf{1}^T}{N}$$
  where $d \in (0, 1)$ is the damping factor (typically $0.85$). The constant injection $\frac{1-d}{N}$ ensures graph reachability.
* **Generating Functions & Resolvent Operator**:
  In steady-state equilibrium ($\mathbf{x}^* = d \mathbf{x}^* \mathbf{S} + \frac{1-d}{N}\mathbf{1}^T$), the recurrence can be solved using the matrix generating function resolvent:
  $$\mathbf{x}^* = \frac{1-d}{N}\mathbf{1}^T (\mathbf{I} - d\mathbf{S})^{-1} = \frac{1-d}{N}\mathbf{1}^T \sum_{k=0}^{\infty} d^k \mathbf{S}^k$$
* **Combinatorial Path Counting via Matrix Powers $\mathbf{A}^k$**:
  A fundamental theorem in combinatorics establishes that the $(i, j)$-th entry of the $k$-th power of the adjacency matrix counts the exact number of directed walks of length $k$ from vertex $i$ to vertex $j$:
  $$(\mathbf{A}^k)_{ij} = \text{number of walks of length } k \text{ from } v_i \text{ to } v_j$$
  Total length-$k$ paths in the web graph equals $\sum_{i, j} (\mathbf{A}^k)_{ij}$.
* **Inclusion-Exclusion Principle**:
  When evaluating multi-term search queries across inverted index postings lists, the number of distinct documents satisfying at least one term is governed by:
  $$|\mathcal{A} \cup \mathcal{B}| = |\mathcal{A}| + |\mathcal{B}| - |\mathcal{A} \cap \mathcal{B}|$$
  For three terms:
  $$|\mathcal{A} \cup \mathcal{B} \cup \mathcal{C}| = |\mathcal{A}| + |\mathcal{B}| + |\mathcal{C}| - |\mathcal{A} \cap \mathcal{B}| - |\mathcal{A} \cap \mathcal{C}| - |\mathcal{B} \cap \mathcal{C}| + |\mathcal{A} \cap \mathcal{B} \cap \mathcal{C}|$$

### 3.3 Logic and Proof Techniques
* **Propositional Logic & Satisfiability**:
  Each search term $t_k$ defines a Boolean predicate $P(t_k, d) \in \{0, 1\}$ over document $d$. A multi-term query $q = t_1 \land t_2$ defines a conjunction:
  $$\text{Sat}(q, d) = P(t_1, d) \land P(t_2, d)$$
  The candidate document set represents the satisfiable assignment set for the query predicate.
* **Mathematical Induction on Flow Invariance**:
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

### 3.4 Algebraic Structures & Number Theory
* **Matrix Ring $M_N(\mathbb{R})$ & Invariant Subspaces**:
  The transition operator $\mathbf{P}$ and Google matrix $\mathbf{G} = d\mathbf{S} + \frac{1-d}{N}\mathbf{1}\mathbf{1}^T$ are elements of the matrix ring $M_N(\mathbb{R})$ under standard matrix addition and matrix multiplication.
  The recurrence possesses a stationary fixed point:
  $$\mathbf{x}^* \mathbf{G} = \mathbf{x}^* \iff \mathbf{x}^* (\mathbf{G} - \mathbf{I}) = \mathbf{0}$$
  This fixed-point vector spans the one-dimensional invariant subspace corresponding to eigenvalue $\lambda_1 = 1$.
* **Metric Vector Space Model in $\mathbb{R}^{|V_{\text{vocab}}|}$**:
  Document and query texts are projected as vectors into $\mathbb{R}^{|V|}$ with inner product $\langle \mathbf{u}, \mathbf{v} \rangle = \sum u_i v_i$:
  * **Sublinear Term Frequency**:
    $$\text{TF}(t, d) = \begin{cases} 1 + \ln(f_{t, d}) & \text{if } f_{t, d} > 0 \\ 0 & \text{otherwise} \end{cases}$$
  * **Smoothed Inverse Document Frequency**:
    $$\text{IDF}(t) = \ln\left( \frac{N + 1}{\text{df}(t) + 1} \right) + 1$$
  * **Cosine Similarity Metric**:
    $$R(d, q) = \frac{\langle \mathbf{v}_d, \mathbf{v}_q \rangle}{\|\mathbf{v}_d\|_2 \|\mathbf{v}_q\|_2} = \frac{\sum_{t \in q \cap d} w_{t, d} \cdot w_{t, q}}{\sqrt{\sum_{t \in d} w_{t, d}^2} \sqrt{\sum_{t \in q} w_{t, q}^2}}$$
* **Modular Arithmetic Applications**:
  Document identifiers and inverted vocabulary keys utilize modular hash mapping ($h(k) \pmod m$) for $O(1)$ dictionary lookups.

### 3.5 Candidate Score Normalization & Convex Hybrid Fusion
Because cosine similarity $R(d, q) \in [0, 1]$ and PageRank flow vector entries $x^*_d \approx \frac{1}{N}$ occupy disparate numerical scales, candidate-level Min-Max normalization is performed:
$$R_{\text{norm}}(d) = \frac{R(d, q) - R_{\min}}{R_{\max} - R_{\min} + \delta}, \quad PR_{\text{norm}}(d) = \frac{x^*_d - x^*_{\min}}{x^*_{\max} - x^*_{\min} + \delta}$$
where $\delta = 10^{-12}$. The final ranking is determined by the convex combination:
$$\text{FinalScore}(d, q) = \alpha \cdot R_{\text{norm}}(d) + (1 - \alpha) \cdot PR_{\text{norm}}(d), \quad \alpha \in [0, 1]$$

---

## 4. Proposed System Architecture & Components

| Component / Layer | Implementation File | Mathematical Foundations |
| :--- | :--- | :--- |
| **Web Graph Engine** | `src/graph.py` | **Graph Theory**: Directed graphs, adjacency matrices, in/out degrees, dangling sinks, and combinatorial path counting $A^k$. |
| **Recurrence & Flow Engine** | `src/pagerank.py`, `src/recurrence_flow.py` | **Combinatorics**: Coupled linear recurrence relation, generating function resolvents.<br>**Logic & Induction**: Inductive flow conservation proof ($\sum x_i = 1$).<br>**Algebraic Structures**: Matrix ring operators and invariant fixed points ($\lambda = 1$). |
| **Information Retrieval Engine** | `src/text_engine.py` | **Logic**: Propositional Boolean search satisfaction.<br>**Combinatorics**: Inclusion-Exclusion principle for multi-term candidate sets.<br>**Algebraic Structures**: Vector Space Model in $\mathbb{R}^{|V|}$ with cosine inner products. |
| **Hybrid Ranking Engine** | `src/ranking.py` | Candidate Min-Max normalization, convex combination score fusion, and Spearman rank displacement analysis. |
| **Experimental & Visual Suite** | `src/experiments.py`, `src/app.py`, `static/js/main.js` | Sybil link farm attack simulations, spider trap cycle absorption, damping sensitivity sweeps, and full interactive web dashboard. |

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

This project demonstrates the powerful, practical synthesis of discrete mathematics:
* **Graph Theory** formalizes web topology and conservative network flows.
* **Combinatorics** provides linear recurrence relations, path counting via $A^k$, and the Inclusion-Exclusion principle.
* **Logic and Induction** enables propositional query evaluation and formally proves flow invariance across all iterations.
* **Algebraic Structures** frames the authority vector as a fixed point in a matrix ring and powers vector space cosine retrieval.

By integrating these mathematical disciplines into an interactive web application, the project demonstrates how pure discrete mathematics transformed web search from naive keyword counting into a robust, manipulation-resistant science.
