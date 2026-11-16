"""Standalone script to index AMR datasets into the clinical RAG engine."""
import sys
from pathlib import Path

# Add services/api to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "services" / "api"))

from app.rag.ingest import build_amr_knowledge_corpus
from app.rag.query_engine import get_rag_query_engine


def main():
    print("=" * 60)
    print("  AMR Sentinel — Clinical Knowledge Ingestion & Indexing")
    print("=" * 60)

    corpus = build_amr_knowledge_corpus(workspace_root=root_dir)
    print(f"Loaded {len(corpus)} clinical evidence & guideline chunks.")

    categories = {}
    for doc in corpus:
        cat = doc.get("source_category", "OTHER")
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in categories.items():
        print(f" - {cat}: {count} chunks")

    print("\nInitializing BM25 Sparse Index and Reranker...")
    rag = get_rag_query_engine()

    test_queries = [
        "What is the first-line antibiotic for mild community acquired pneumonia?",
        "Is cefixime with azithromycin permitted under CDSCO?",
        "What is the recommended treatment for acute watery diarrhea?",
    ]

    print("\nVerifying RAG Query Retrieval:")
    for q in test_queries:
        res = rag.query(q)
        print(f"\nQ: {q}")
        print(f"A: {res['answer'][:120]}...")
        print(f"Citations: {len(res['citations'])} sources")

    print("\n[SUCCESS] Knowledge ingestion and retrieval verification completed!")


if __name__ == "__main__":
    main()
