"""Audit evaluation route."""
import json
import uuid
from pathlib import Path

from app.engine.engine import DeterministicAuditEngine
from app.schemas.audit import AuditReport, AuditRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["Audits"])

# Load rule manifest snapshot once at module load
RULES_PATH = Path(__file__).parent.parent.parent / "rules_data" / "rules_v1.0.0.json"

if not RULES_PATH.exists():
    raise RuntimeError(f"Critical Clinical Failure: Rule snapshot missing at {RULES_PATH}")

with open(RULES_PATH, "r", encoding="utf-8") as f:
    ACTIVE_MANIFEST = json.load(f)

ENGINE = DeterministicAuditEngine(ACTIVE_MANIFEST)


@router.post(
    "/audits",
    response_model=AuditReport,
    status_code=status.HTTP_200_OK,
    summary="Evaluate prescription with deterministic rules engine",
)
async def evaluate_audit(request: AuditRequest):
    """Run deterministic clinical audit on confirmed prescription data."""
    try:
        # Convert request model to dictionary
        request_dict = request.model_dump()

        # Pure deterministic evaluation
        result = ENGINE.evaluate(request_dict)

        audit_id = f"AUD-{uuid.uuid4().hex[:8].upper()}"

        return AuditReport(
            audit_id=audit_id,
            status=result["status"],
            rule_set_version=result["rule_set_version"],
            evidence_snapshot_id=result["evidence_snapshot_id"],
            findings=result["findings"],
            input_gaps=result["input_gaps"],
            disclaimer=result["disclaimer"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deterministic evaluation error: {e!s}",
        ) from e
