"""LangGraph clinical workflow graph assembly."""
import uuid
from typing import Any

from app.agent.nodes import (
    deterministic_audit_node,
    extract_node,
    rag_retrieval_node,
    report_synthesis_node,
)
from app.agent.state import ClinicalAgentState
from langgraph.graph import END, StateGraph


def build_clinical_graph() -> StateGraph:
    """Build and compile stateful clinical audit workflow graph."""
    builder = StateGraph(ClinicalAgentState)

    # Add workflow nodes
    builder.add_node("extract", extract_node)
    builder.add_node("rag_retrieve", rag_retrieval_node)
    builder.add_node("deterministic_audit", deterministic_audit_node)
    builder.add_node("synthesize_report", report_synthesis_node)

    # Set linear edges with safety checkpoints
    builder.set_entry_point("extract")
    builder.add_edge("extract", "rag_retrieve")
    builder.add_edge("rag_retrieve", "deterministic_audit")
    builder.add_edge("deterministic_audit", "synthesize_report")
    builder.add_edge("synthesize_report", END)

    return builder.compile()


class ClinicalWorkflowAgent:
    """High-level facade for executing the LangGraph clinical workflow agent."""

    def __init__(self):
        self._compiled_graph = build_clinical_graph()

    async def run(
        self,
        raw_text: str = "",
        file_bytes: bytes | None = None,
        mime_type: str = "text/plain",
        filename: str = "prescription.txt",
    ) -> dict[str, Any]:
        """Execute stateful graph from clinical input."""
        initial_state: ClinicalAgentState = {
            "raw_text": raw_text,
            "file_bytes": file_bytes or b"",
            "mime_type": mime_type,
            "filename": filename,
            "trace_id": str(uuid.uuid4()),
            "errors": [],
            "workflow_step": "INITIALIZED",
        }

        final_state = await self._compiled_graph.ainvoke(initial_state)
        return final_state.get("audit_report", {})


_clinical_agent_instance: ClinicalWorkflowAgent | None = None


def get_clinical_agent() -> ClinicalWorkflowAgent:
    """Singleton getter for ClinicalWorkflowAgent."""
    global _clinical_agent_instance
    if _clinical_agent_instance is None:
        _clinical_agent_instance = ClinicalWorkflowAgent()
    return _clinical_agent_instance
