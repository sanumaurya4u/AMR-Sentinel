"""Audit request and report canonical schemas."""
from datetime import UTC, datetime
from typing import Any, Literal

from app.schemas.patient import PatientContext
from app.schemas.prescription import PrescriptionLine
from pydantic import BaseModel, ConfigDict, Field

AuditStatus = Literal[
    "NEEDS_URGENT_REVIEW",
    "NEEDS_REVIEW",
    "NO_RULE_TRIGGERED",
    "INCOMPLETE_DATA",
    "UNAVAILABLE",
]

SeverityLevel = Literal["URGENT_REVIEW", "NEEDS_REVIEW", "DATA_GAP", "INFO"]


class EvidenceReference(BaseModel):
    """Evidence source citation and locator."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    publisher: str
    jurisdiction: str
    published_on: str
    section_ref: str
    excerpt: str
    url: str | None = None


class Finding(BaseModel):
    """Structured clinical finding from deterministic evaluation."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    rule_id: str
    severity: SeverityLevel
    title: str
    explanation: str
    input_facts_used: dict[str, Any]
    missing_data_status: list[str] = Field(default_factory=list)
    guideline_discussion_prompt: str | None = None
    evidence: EvidenceReference


class AuditRequest(BaseModel):
    """Confirmed audit request payload."""
    model_config = ConfigDict(populate_by_name=True)

    patient_context: PatientContext = Field(..., alias="patientContext")
    indication_code: str = Field(..., alias="indicationCode")
    setting: Literal["outpatient", "inpatient"] = "outpatient"
    prescription_lines: list[PrescriptionLine] = Field(..., alias="prescriptionLines")
    is_synthetic: bool = Field(True, alias="isSynthetic")


class AuditReport(BaseModel):
    """Deterministic audit result report."""
    model_config = ConfigDict(populate_by_name=True)

    audit_id: str
    status: AuditStatus
    rule_set_version: str
    evidence_snapshot_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    findings: list[Finding] = Field(default_factory=list)
    input_gaps: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "AMR Sentinel AI is an assistive decision-support prototype. "
        "It does not diagnose, prescribe, or validate medical therapy. "
        "No Rule Triggered indicates non-breach of configured safety rules, not clinical approval. "
        "Clinicians retain sole clinical responsibility."
    )
