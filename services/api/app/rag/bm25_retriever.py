"""BM25 sparse retrieval engine for clinical guidelines and antimicrobial surveillance."""
import re
from typing import Any

from rank_bm25 import BM25Okapi

CLINICAL_STOPWORDS = {
    "what", "is", "the", "for", "of", "and", "to", "in", "a", "an", "with",
    "are", "as", "by", "this", "that", "it", "from", "at", "on", "or", "be",
    "how", "can", "allowed", "do", "does", "did", "tell", "me", "about", "which",
}


def tokenize_clinical_text(text: str) -> list[str]:
    """Tokenize and normalize medical text for BM25 indexing."""
    # Retain alphanumeric tokens and medical dashes (e.g. amoxicillin-clavulanate)
    cleaned = re.sub(r"[^\w\-\+]", " ", text.lower())
    return [t for t in cleaned.split() if len(t) > 1 and t not in CLINICAL_STOPWORDS]


class BM25ClinicalRetriever:
    """Fast in-memory BM25 index over clinical evidence and ICMR guideline chunks."""

    def __init__(self, documents: list[dict[str, Any]] | None = None):
        self.documents: list[dict[str, Any]] = documents or []
        self._corpus_tokens: list[list[str]] = []
        self._bm25: BM25Okapi | None = None
        if self.documents:
            self._build_index()

    def _build_index(self) -> None:
        """Tokenize all indexed documents and initialize BM25Okapi."""
        self._corpus_tokens = [
            tokenize_clinical_text(f"{doc.get('source_title', '')} {doc.get('heading', '')} {doc.get('content', '')}")
            for doc in self.documents
        ]
        if self._corpus_tokens:
            self._bm25 = BM25Okapi(self._corpus_tokens)

    def add_documents(self, new_docs: list[dict[str, Any]]) -> None:
        """Add new documents and re-index."""
        self.documents.extend(new_docs)
        self._build_index()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Retrieve top-K most relevant chunks using BM25 scoring."""
        if not self._bm25 or not self.documents:
            return []

        tokens = tokenize_clinical_text(query)
        if not tokens:
            return []

        scores = self._bm25.get_scores(tokens)
        scored_pairs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scored_pairs[:top_k]:
            if score > 0.0:
                doc = self.documents[idx].copy()
                doc["bm25_score"] = round(float(score), 4)
                results.append(doc)

        return results
