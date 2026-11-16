"""Integration and unit tests for RAG engine, RapidFuzz entity matching, and LangGraph agent."""
import pytest
from app.agent.graph import get_clinical_agent
from app.extraction.fuzzy_match import get_drug_entity_matcher
from app.rag.query_engine import get_rag_query_engine


def test_rapidfuzz_brand_matching():
    """Verify RapidFuzz accurately maps brand names to canonical generics."""
    matcher = get_drug_entity_matcher()

    entry, score = matcher.match_drug("augmentin 625")
    assert entry is not None
    assert entry["generic_name"] == "Amoxicillin-Clavulanate"
    assert score >= 80.0

    entry2, score2 = matcher.match_drug("cifran 500")
    assert entry2 is not None
    assert entry2["generic_name"] == "Ciprofloxacin"
    assert score2 >= 80.0

    entry3, _ = matcher.match_drug("zifi az")
    assert entry3 is not None
    assert entry3["is_banned_fdc"] is True


def test_rag_query_engine_retrieval():
    """Verify BM25 sparse retrieval and evidence ranking."""
    rag = get_rag_query_engine()

    res = rag.query("What is the first-line treatment for acute cystitis / uncomplicated UTI?")
    assert res is not None
    assert len(res["citations"]) > 0
    assert "Nitrofurantoin" in res["answer"] or "Fosfomycin" in res["answer"]


def test_rag_banned_fdc_detection():
    """Verify RAG correctly flags CDSCO banned fixed-dose combinations."""
    rag = get_rag_query_engine()

    res = rag.query("Is cefixime with azithromycin allowed?")
    assert res is not None
    assert "BANNED" in res["answer"] or "Prohibited" in res["answer"]


@pytest.mark.asyncio
async def test_langgraph_clinical_agent_execution():
    """Verify end-to-end execution of LangGraph clinical workflow agent."""
    agent = get_clinical_agent()
    clinical_note = "Master Aarav, 8 yo male. Acute watery diarrhea. Rx: Tab Cifran 250mg BD x 5d."

    report = await agent.run(raw_text=clinical_note)
    assert report is not None
    assert report.get("status") == "NEEDS_URGENT_REVIEW"
    assert len(report.get("findings", [])) >= 1
    # Check that pediatric FQ rule triggered
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.PED.FQ_UNDER_18" in rule_ids
    assert len(report.get("clinical_evidence_citations", [])) > 0
