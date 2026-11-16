"""API router for executing the LangGraph clinical workflow agent."""
from typing import Annotated, Any

from app.agent.graph import get_clinical_agent
from fastapi import APIRouter, File, Form, UploadFile, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["Clinical Agent"])


class AgentTextRequest(BaseModel):
    prescription_text: str = Field(..., min_length=5, description="Raw doctor prescription or clinical note")


@router.post(
    "/agent/run-text",
    status_code=status.HTTP_200_OK,
    summary="Execute full clinical workflow agent from raw prescription text",
)
async def run_agent_from_text(request: AgentTextRequest) -> dict[str, Any]:
    """Run full LangGraph agent: Intake -> RAG Knowledge Lookup -> Deterministic Audit -> Synthesized Report."""
    agent = get_clinical_agent()
    result = await agent.run(raw_text=request.prescription_text)
    return result


@router.post(
    "/agent/run-document",
    status_code=status.HTTP_200_OK,
    summary="Execute full clinical workflow agent from uploaded prescription document/image",
)
async def run_agent_from_document(
    file: Annotated[UploadFile, File(...)],
    notes: Annotated[str, Form()] = "",
) -> dict[str, Any]:
    """Run full LangGraph agent from uploaded PDF or image prescription."""
    file_bytes = await file.read()
    agent = get_clinical_agent()
    result = await agent.run(
        raw_text=notes,
        file_bytes=file_bytes,
        mime_type=file.content_type or "application/octet-stream",
        filename=file.filename or "prescription.bin",
    )
    return result
