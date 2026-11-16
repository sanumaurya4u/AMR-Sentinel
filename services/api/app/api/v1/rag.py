"""API router for clinical RAG knowledge query and guidelines search."""
from typing import Any

from app.rag.query_engine import get_rag_query_engine
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["RAG Knowledge Engine"])


class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="Clinical query or antibiotic question")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of guideline citations to retrieve")


class RAGCitation(BaseModel):
    citation_index: int
    source_title: str
    heading: str
    excerpt: str
    score: float | None = None


class RAGQueryResponse(BaseModel):
    question: str
    answer: str
    citations: list[RAGCitation]
    confidence: str
    disclaimer: str


@router.post(
    "/rag/query",
    response_model=RAGQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query AMR clinical knowledge base with RAG",
)
async def query_rag_knowledge(request: RAGQueryRequest) -> dict[str, Any]:
    """Execute hybrid BM25 + semantic clinical guideline retrieval for a user question."""
    rag_engine = get_rag_query_engine()
    result = rag_engine.query(request.query)
    return result


@router.get(
    "/rag/sources",
    status_code=status.HTTP_200_OK,
    summary="List indexed guideline datasets in knowledge corpus",
)
async def list_rag_sources() -> dict[str, Any]:
    """List indexed clinical guidelines and evidence collections."""
    rag_engine = get_rag_query_engine()
    categories: dict[str, int] = {}
    for doc in rag_engine.documents:
        cat = doc.get("source_category", "OTHER")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total_chunks_indexed": len(rag_engine.documents),
        "source_breakdown": categories,
        "standards": [
            "ICMR Standard Treatment Guidelines (STG 2022)",
            "WHO AWaRe Classification 2023 (Access, Watch, Reserve)",
            "CDSCO Banned Fixed-Dose Combination Gazette Directives",
        ],
    }
