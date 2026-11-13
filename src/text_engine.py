"""
Information Retrieval Engine: Tokenization, Inverted Index & TF-IDF Vector Space Model
MFCS Project - Intelligent Search Ranking
"""

import math
import re
from typing import Dict, List, Set, Tuple, Optional
from collections import Counter
from .graph import WebGraph

# Standard English stop words
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
    "cannot", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
    "i", "if", "in", "into", "is", "isn't", "it", "its", "itself", "just", "me", "more", "most", "my", "myself",
    "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves",
    "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who",
    "whom", "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}


class TextRelevanceEngine:
    """
    Implements the classic Vector Space Model (VSM) using TF-IDF weighting
    and Cosine Similarity over an Inverted Index.
    """

    def __init__(self, graph: WebGraph):
        self.graph = graph
        self.inverted_index: Dict[str, Dict[str, int]] = {}  # term -> {doc_id: raw_count}
        self.doc_lengths: Dict[str, int] = {}
        self.doc_vectors: Dict[str, Dict[str, float]] = {}  # doc_id -> {term: tfidf_weight}
        self.doc_norms: Dict[str, float] = {}               # doc_id -> L2 norm
        self.idf: Dict[str, float] = {}                     # term -> idf value
        self.vocabulary: Set[str] = set()

        self.build_index()

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Converts text to lowercase alphanumeric tokens, filtering stop words and single chars."""
        clean_text = text.lower()
        tokens = re.findall(r"\b[a-z0-9_]{2,}\b", clean_text)
        return [tok for tok in tokens if tok not in STOP_WORDS]

    def build_index(self):
        """Indexes all documents currently present in the web graph."""
        self.inverted_index.clear()
        self.doc_lengths.clear()
        self.doc_vectors.clear()
        self.doc_norms.clear()
        self.idf.clear()
        self.vocabulary.clear()

        n_docs = self.graph.num_nodes
        if n_docs == 0:
            return

        doc_tf: Dict[str, Counter] = {}

        for doc_id, page in self.graph.pages.items():
            # Combine title (weighted 2x for importance) and content
            full_text = (page.title + " ") * 2 + page.content
            tokens = self.tokenize(full_text)
            self.doc_lengths[doc_id] = len(tokens)
            tf_counts = Counter(tokens)
            doc_tf[doc_id] = tf_counts

            for term, count in tf_counts.items():
                self.vocabulary.add(term)
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                self.inverted_index[term][doc_id] = count

        # Compute smoothed Inverse Document Frequency: IDF(t) = ln((N + 1) / (df + 1)) + 1
        for term, postings in self.inverted_index.items():
            df = len(postings)
            self.idf[term] = math.log((n_docs + 1.0) / (df + 1.0)) + 1.0

        # Compute Document TF-IDF vectors and their L2 norms
        for doc_id, counts in doc_tf.items():
            vector = {}
            sum_sq = 0.0
            for term, count in counts.items():
                # Sublinear term frequency: 1 + ln(count)
                sublinear_tf = 1.0 + math.log(count)
                weight = sublinear_tf * self.idf[term]
                vector[term] = weight
                sum_sq += weight * weight

            self.doc_vectors[doc_id] = vector
            self.doc_norms[doc_id] = math.sqrt(sum_sq) if sum_sq > 0 else 1.0

    def calculate_relevance(self, query: str) -> Dict[str, dict]:
        """
        Computes Cosine Similarity between the query vector and every document vector:
        CosineSim(d, q) = (v_d . v_q) / (||v_d||_2 * ||v_q||_2)
        
        Returns:
            Dict mapping doc_id -> {
                'raw_score': float,
                'matched_terms': list[str],
                'term_overlap_count': int
            }
        """
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return {doc_id: {"raw_score": 0.0, "matched_terms": [], "term_overlap_count": 0} for doc_id in self.graph.pages}

        query_counts = Counter(query_tokens)
        query_vector = {}
        query_sum_sq = 0.0

        for term, count in query_counts.items():
            if term in self.idf:
                weight = (1.0 + math.log(count)) * self.idf[term]
                query_vector[term] = weight
                query_sum_sq += weight * weight

        query_norm = math.sqrt(query_sum_sq) if query_sum_sq > 0 else 1.0

        # Find candidate documents containing at least one query term
        candidate_scores: Dict[str, float] = {doc_id: 0.0 for doc_id in self.graph.pages}
        matched_terms: Dict[str, List[str]] = {doc_id: [] for doc_id in self.graph.pages}

        for term, q_weight in query_vector.items():
            if term in self.inverted_index:
                for doc_id, d_count in self.inverted_index[term].items():
                    d_weight = self.doc_vectors[doc_id].get(term, 0.0)
                    candidate_scores[doc_id] += d_weight * q_weight
                    matched_terms[doc_id].append(term)

        results = {}
        for doc_id in self.graph.pages:
            dot_product = candidate_scores[doc_id]
            norm_product = self.doc_norms.get(doc_id, 1.0) * query_norm
            similarity = (dot_product / norm_product) if norm_product > 0 else 0.0

            results[doc_id] = {
                "raw_score": round(similarity, 6),
                "matched_terms": matched_terms[doc_id],
                "term_overlap_count": len(matched_terms[doc_id])
            }

        return results

