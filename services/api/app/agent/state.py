"""State definition for LangGraph clinical stewardship agent."""
from typing import Any, TypedDict


class ClinicalAgentState(TypedDict, total=False):
    """Clinical agent workflow state tracked across nodes."""
    # Input payloads
    raw_text: str
    file_bytes: bytes
    mime_type: str
    filename: str

    # Extracted clinical intake draft (untrusted until confirmed)
    extracted_draft: dict[str, Any]
    extraction_source: str  # "gemini", "openrouter", "offline_heuristics"

    # Grounded RAG knowledge and evidence citations
    rag_guidelines: list[dict[str, Any]]
    rag_citations: list[dict[str, Any]]
    amr_warnings: list[str]

    # Deterministic evaluation (Pure Python Core)
    audit_report: dict[str, Any]

    # Execution telemetry and errors
    workflow_step: str
    trace_id: str
    errors: list[str]
