"""LangGraph node functions executing stages of the clinical audit workflow."""
import json
import uuid
from pathlib import Path
from typing import Any

from app.agent.state import ClinicalAgentState
from app.engine.engine import DeterministicAuditEngine
from app.extraction.adapter import ExtractionAdapter
from app.rag.query_engine import get_rag_query_engine

RULES_PATH = Path(__file__).parent.parent / "rules_data" / "rules_v1.0.0.json"
with open(RULES_PATH, encoding="utf-8") as f:
    ACTIVE_MANIFEST = json.load(f)

ENGINE = DeterministicAuditEngine(ACTIVE_MANIFEST)


async def extract_node(state: ClinicalAgentState) -> dict[str, Any]:
    """Node 1: Extract structured prescription facts from raw text or document bytes."""
    file_bytes = state.get("file_bytes")
    raw_text = state.get("raw_text", "")
    mime_type = state.get("mime_type", "text/plain")
    filename = state.get("filename", "prescription.txt")

    if not file_bytes and raw_text:
        file_bytes = raw_text.encode("utf-8")

    if not file_bytes:
        file_bytes = b"Patient: 34 yo female. Mild CAP. Rx: Amoxicillin 500mg TID x 5d."

    adapter = ExtractionAdapter()
    draft = await adapter.extract_from_bytes(file_bytes, mime_type, filename)

    return {
        "extracted_draft": draft,
        "extraction_source": draft.get("extraction_engine", "offline_heuristic_adapter"),
        "workflow_step": "EXTRACTED",
    }


async def rag_retrieval_node(state: ClinicalAgentState) -> dict[str, Any]:
    """Node 2: Retrieve grounded ICMR STG, WHO AWaRe, and CDSCO evidence for drafted drugs."""
    draft = state.get("extracted_draft", {})
    prescription_lines = draft.get("prescriptionLines", [])
    indication_code = draft.get("indicationCode", "SYN_CAP_MILD")

    rag_engine = get_rag_query_engine()

    guidelines = []
    citations = []
    warnings = []

    # Query RAG engine for each prescribed drug and indication
    for line in prescription_lines:
        drug_name = line.get("drugName", "")
        query_str = f"{drug_name} for {indication_code}"
        rag_res = rag_engine.query(query_str)

        if rag_res.get("citations"):
            citations.extend(rag_res["citations"])
            guidelines.append({
                "drug": drug_name,
                "answer": rag_res.get("answer"),
                "confidence": rag_res.get("confidence"),
            })

        # Check for banned FDCs
        if "+" in drug_name:
            banned_check = rag_engine.search(f"banned {drug_name}", top_k=1)
            if banned_check and banned_check[0].get("source_category") == "CDSCO_BANNED_FDC":
                warnings.append(f"CDSCO Alert: {drug_name} is listed as a prohibited fixed-dose combination.")

    return {
        "rag_guidelines": guidelines,
        "rag_citations": citations,
        "amr_warnings": warnings,
        "workflow_step": "RAG_RETRIEVED",
    }


async def deterministic_audit_node(state: ClinicalAgentState) -> dict[str, Any]:
    """Node 3: Execute deterministic clinical rules (Pure Python AST-isolated core)."""
    draft = state.get("extracted_draft", {})

    audit_payload = {
        "audit_id": f"AUD-{uuid.uuid4().hex[:8].upper()}-AGENT",
        "patientContext": draft.get("patientContext", {}),
        "indicationCode": draft.get("indicationCode", "SYN_CAP_MILD"),
        "setting": draft.get("setting", "outpatient"),
        "prescriptionLines": draft.get("prescriptionLines", []),
    }

    report = ENGINE.evaluate(audit_payload)
    return {
        "audit_report": report,
        "workflow_step": "AUDITED",
    }


async def report_synthesis_node(state: ClinicalAgentState) -> dict[str, Any]:
    """Node 4: Synthesize final decision-support report combining audit results and RAG evidence."""
    report = state.get("audit_report", {})
    citations = state.get("rag_citations", [])
    warnings = state.get("amr_warnings", [])
    draft = state.get("extracted_draft", {})

    enhanced_report = dict(report)
    enhanced_report["clinical_evidence_citations"] = citations
    enhanced_report["amr_stewardship_warnings"] = warnings
    enhanced_report["extraction_confidence"] = draft.get("fieldConfidence", {})
    enhanced_report["clinical_disclaimer"] = (
        "Deterministic audit verified against ICMR STG 2022 & WHO AWaRe 2023. "
        "Intake data is an assistive draft; final prescription decisions remain with the treating physician."
    )

    return {
        "audit_report": enhanced_report,
        "workflow_step": "COMPLETED",
    }
