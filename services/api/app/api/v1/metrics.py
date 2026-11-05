"""De-identified stewardship metrics and evidence catalogue endpoints."""
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["Metrics & Stewardship"])

RULES_PATH = Path(__file__).parent.parent.parent / "rules_data" / "rules_v1.0.0.json"

with open(RULES_PATH, "r", encoding="utf-8") as f:
    ACTIVE_MANIFEST = json.load(f)


@router.get(
    "/metrics",
    summary="De-identified institutional antimicrobial stewardship analytics",
)
async def get_stewardship_metrics() -> dict[str, Any]:
    """Return de-identified aggregate stewardship metrics.

    SAFETY MANDATE: Zero PHI is contained in aggregate metrics.
    """
    return {
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "organization_name": "National Antimicrobial Stewardship Initiative",
        "period": "Last 30 Days (Demo Aggregate)",
        "who_aware_distribution": {
            "access_percentage": 64.2,
            "watch_percentage": 31.8,
            "reserve_percentage": 4.0,
            "target_met": True,
            "benchmark_reference": "WHO AWaRe 2023 Target: >=60% Access group",
        },
        "safety_interceptions": {
            "total_audits_evaluated": 1284,
            "urgent_contraindications_flagged": 42,
            "viral_inappropriate_prevented": 89,
            "reserve_escapes_intercepted": 18,
            "missing_data_holds": 31,
        },
        "top_triggered_rules": [
            {
                "rule_id": "STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS",
                "category": "Viral Indication Review",
                "trigger_count": 52,
                "percentage_of_alerts": 34.0,
            },
            {
                "rule_id": "SAFETY.PED.FQ_UNDER_18",
                "category": "Pediatric Safety Gate",
                "trigger_count": 43,
                "percentage_of_alerts": 28.1,
            },
            {
                "rule_id": "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30",
                "category": "Renal & Geriatric Safety",
                "trigger_count": 29,
                "percentage_of_alerts": 19.0,
            },
            {
                "rule_id": "STEWARDSHIP.AWARE.RESERVE_ESCALATION",
                "category": "AWaRe Reserve Escalation",
                "trigger_count": 18,
                "percentage_of_alerts": 11.8,
            },
        ],
        "active_rule_set_version": ACTIVE_MANIFEST.get("version"),
        "evidence_snapshot_id": ACTIVE_MANIFEST.get("evidence_snapshot_id"),
    }


@router.get(
    "/evidence",
    summary="List official evidence sources and citations",
)
async def list_evidence_sources() -> dict[str, Any]:
    """Return catalogue of all active ICMR and WHO guideline citations."""
    return {
        "rule_set_version": ACTIVE_MANIFEST.get("version"),
        "evidence_snapshot_id": ACTIVE_MANIFEST.get("evidence_snapshot_id"),
        "sources": ACTIVE_MANIFEST.get("evidence_catalog", {}),
    }


@router.get(
    "/evidence/{evidence_id}",
    summary="Get single evidence source locator by ID",
)
async def get_evidence_source(evidence_id: str) -> dict[str, Any]:
    """Return specific evidence citation metadata."""
    catalog = ACTIVE_MANIFEST.get("evidence_catalog", {})
    if evidence_id not in catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence source '{evidence_id}' not found in active snapshot.",
        )
    return catalog[evidence_id]
