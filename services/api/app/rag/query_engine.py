"""Clinical RAG Query Engine combining BM25 sparse search and semantic synthesis."""
import re
from typing import Any

from app.rag.bm25_retriever import BM25ClinicalRetriever
from app.rag.ingest import build_amr_knowledge_corpus


class ClinicalRAGQueryEngine:
    """Retrieval-Augmented Generation query engine grounded in ICMR STG and WHO AWaRe evidence."""

    def __init__(self):
        corpus = build_amr_knowledge_corpus()
        self.retriever = BM25ClinicalRetriever(corpus)
        self.documents = corpus

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Retrieve most relevant clinical guideline chunks."""
        # 1. Sparse BM25 retrieval
        bm25_results = self.retriever.retrieve(query, top_k=top_k * 2)

        if not bm25_results:
            # Fallback substring scoring if BM25 scores 0
            query_tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
            scored = []
            for doc in self.documents:
                text = f"{doc['source_title']} {doc['heading']} {doc['content']}".lower()
                matches = sum(1 for t in query_tokens if t in text)
                if matches > 0:
                    item = doc.copy()
                    item["bm25_score"] = float(matches)
                    scored.append(item)
            scored.sort(key=lambda x: x.get("bm25_score", 0), reverse=True)
            bm25_results = scored[: top_k * 2]

        # 2. Re-ranking: boost official ICMR STG guidelines, CDSCO notices, and heading matches
        ranked_results = []
        clean_q = query.lower()
        query_words = [w for w in re.findall(r"\w+", clean_q) if len(w) > 3]

        for doc in bm25_results:
            base_score = doc.get("bm25_score", 1.0)
            boost = 1.0
            heading_lower = doc.get("heading", "").lower()

            # Boost if key query terms appear in the heading
            heading_matches = sum(1 for w in query_words if w in heading_lower)
            boost += heading_matches * 1.5

            if doc.get("source_category") == "CDSCO_BANNED_FDC":
                if any(w in clean_q for w in ["banned", "fdc", "allowed", "permitted"]) or "+" in clean_q:
                    boost += 3.0
            elif doc.get("source_category") == "ICMR_STG_2022":
                boost += 1.2  # Prioritize national treatment guidelines

            doc["rerank_score"] = round(base_score * boost, 3)
            ranked_results.append(doc)

        ranked_results.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)
        return ranked_results[:top_k]

    def query(self, user_question: str) -> dict[str, Any]:
        """Perform full RAG execution: query -> retrieve -> synthesize answer with citations."""
        evidence_chunks = self.search(user_question, top_k=4)

        if not evidence_chunks:
            return {
                "question": user_question,
                "answer": "No direct matching ICMR STG or WHO AWaRe guidelines found for this query in the local knowledge base.",
                "citations": [],
                "confidence": "low",
            }

        # Build citations list
        citations = []
        for idx, chunk in enumerate(evidence_chunks, 1):
            citations.append({
                "citation_index": idx,
                "source_title": chunk.get("source_title", "Clinical Guidelines"),
                "heading": chunk.get("heading", ""),
                "excerpt": chunk.get("content", "")[:250],
                "score": chunk.get("rerank_score"),
            })

        # Synthesize grounded answer
        top_chunk = evidence_chunks[0]
        synthesis = f"Based on {top_chunk.get('source_title')} ({top_chunk.get('heading')}):\n\n"
        synthesis += f"{top_chunk.get('content')}\n"

        if len(evidence_chunks) > 1:
            second_chunk = evidence_chunks[1]
            if second_chunk.get("source_title") != top_chunk.get("source_title"):
                synthesis += f"\nCorroborating context from {second_chunk.get('source_title')}:\n{second_chunk.get('content')[:200]}..."

        return {
            "question": user_question,
            "answer": synthesis.strip(),
            "citations": citations,
            "confidence": "high" if top_chunk.get("rerank_score", 0) > 2.0 else "medium",
            "disclaimer": "Assistive clinical context only. Does not replace institutional judgment or patient-specific microbiological cultures.",
        }


_rag_engine_instance: ClinicalRAGQueryEngine | None = None


def get_rag_query_engine() -> ClinicalRAGQueryEngine:
    """Singleton getter for ClinicalRAGQueryEngine."""
    global _rag_engine_instance
    if _rag_engine_instance is None:
        _rag_engine_instance = ClinicalRAGQueryEngine()
    return _rag_engine_instance
