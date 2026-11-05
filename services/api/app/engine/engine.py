"""AMR Sentinel Pure Deterministic Audit Engine.

Evaluates confirmed clinical prescriptions against an immutable rule manifest and evidence catalog.
CRITICAL CONSTRAINT: No external I/O, database, or network calls.
"""
from typing import Any

from app.engine.evaluator import (
    check_aware_reserve_escalation,
    check_banned_fdc,
    check_beta_lactam_allergy,
    check_excessive_duration,
    check_missing_egfr_hold,
    check_pediatric_contraindication,
    check_pregnancy_contraindication,
    check_renal_nitrofurantoin,
    check_viral_indication,
)


class DeterministicAuditEngine:
    """Pure, side-effect-free clinical audit engine."""

    def __init__(self, manifest: dict[str, Any]):
        """Initialize with an immutable rule manifest snapshot."""
        self.manifest = manifest
        self.version = manifest.get("version", "1.0.0")
        self.evidence_snapshot_id = manifest.get("evidence_snapshot_id", "SNAP-001")
        self.rules: list[dict[str, Any]] = manifest.get("rules", [])
        self.evidence_catalog: dict[str, Any] = manifest.get("evidence_catalog", {})

    def evaluate(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Run deterministic audit on confirmed input data.

        Returns a dictionary representation of AuditReport.
        """
        patient_ctx = request_data.get("patient_context") or request_data.get("patientContext", {})
        age_years = float(patient_ctx.get("age_years") or patient_ctx.get("ageYears", 0.0))
        is_pregnant = bool(patient_ctx.get("is_pregnant") or patient_ctx.get("isPregnant", False))
        egfr = patient_ctx.get("egfr_ml_min") if "egfr_ml_min" in patient_ctx else patient_ctx.get("egfrMlMin")
        egfr_val = float(egfr) if egfr is not None else None
        allergies: list[str] = patient_ctx.get("allergies", [])

        indication_code = str(request_data.get("indication_code") or request_data.get("indicationCode", ""))
        lines = request_data.get("prescription_lines") or request_data.get("prescriptionLines", [])

        prescribed_drugs = [
            line.get("drug_name") or line.get("drugName", "")
            for line in lines
            if line.get("drug_name") or line.get("drugName")
        ]

        normalized_lines = [
            {
                "drug_name": line.get("drug_name") or line.get("drugName", ""),
                "dose_text": line.get("dose_text") or line.get("doseText", ""),
                "frequency_text": line.get("frequency_text") or line.get("frequencyText", ""),
                "duration_days": line.get("duration_days") if "duration_days" in line else line.get("durationDays"),
            }
            for line in lines
        ]

        findings: list[dict[str, Any]] = []
        input_gaps: list[str] = []

        # Check for general input gaps
        if egfr_val is None:
            input_gaps.append("Patient eGFR / renal function unrecorded")
        if any(line.get("duration_days") is None for line in normalized_lines):
            input_gaps.append("Medication duration (days) missing on one or more lines")

        # Evaluate rules
        finding_counter = 1
        for rule in self.rules:
            rule_id = rule.get("rule_id", "")
            severity = rule.get("severity", "NEEDS_REVIEW")
            ev_ref_id = rule.get("evidence_ref", "")
            evidence_data = self.evidence_catalog.get(ev_ref_id, {
                "id": ev_ref_id,
                "title": "Clinical Guideline Reference",
                "publisher": "Clinical Guideline Source",
                "jurisdiction": "National / International",
                "published_on": "2022-01-01",
                "section_ref": "Standard Treatment Guidelines",
                "excerpt": "Evidence guidance applies.",
                "url": None,
            })

            result: Any = None

            if rule_id == "SAFETY.PED.FQ_UNDER_18" or rule_id == "SAFETY.PED.TETRACYCLINE_UNDER_18":
                result = check_pediatric_contraindication(age_years, prescribed_drugs, rule)

            elif rule_id == "SAFETY.PREG.CONTRAINDICATED":
                result = check_pregnancy_contraindication(is_pregnant, prescribed_drugs, rule)

            elif rule_id == "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30":
                result = check_renal_nitrofurantoin(age_years, egfr_val, prescribed_drugs, rule)

            elif rule_id == "SAFETY.RENAL.MISSING_EGFR_HOLD":
                result = check_missing_egfr_hold(egfr_val, prescribed_drugs, rule)

            elif rule_id == "SAFETY.ALLERGY.BETA_LACTAM":
                result = check_beta_lactam_allergy(allergies, prescribed_drugs, rule)

            elif rule_id == "REGULATORY.BANNED_FDC":
                result = check_banned_fdc(prescribed_drugs, rule)

            elif rule_id in ("STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS", "STEWARDSHIP.VIRAL.COMMON_COLD_URTI"):
                result = check_viral_indication(indication_code, prescribed_drugs, rule)

            elif rule_id == "STEWARDSHIP.AWARE.RESERVE_ESCALATION":
                result = check_aware_reserve_escalation(indication_code, prescribed_drugs, rule)

            elif rule_id == "STEWARDSHIP.DURATION.EXCESSIVE":
                result = check_excessive_duration(indication_code, normalized_lines, rule)

            if result is not None:
                facts, rule_gaps = result
                input_gaps.extend(rule_gaps)
                findings.append({
                    "id": f"FND-{finding_counter:03d}",
                    "rule_id": rule_id,
                    "severity": severity,
                    "title": rule.get("title", ""),
                    "explanation": rule.get("explanation", ""),
                    "input_facts_used": facts,
                    "missing_data_status": rule_gaps,
                    "guideline_discussion_prompt": rule.get("guideline_discussion_prompt"),
                    "evidence": evidence_data,
                })
                finding_counter += 1

        # Deduplicate gaps
        dedup_gaps = list(dict.fromkeys(input_gaps))

        # Calculate final audit status deterministically
        has_urgent = any(f["severity"] == "URGENT_REVIEW" for f in findings)
        has_review = any(f["severity"] == "NEEDS_REVIEW" for f in findings)
        has_data_gap_finding = any(f["severity"] == "DATA_GAP" for f in findings)

        if has_urgent:
            final_status = "NEEDS_URGENT_REVIEW"
        elif has_data_gap_finding and not has_review:
            final_status = "INCOMPLETE_DATA"
        elif has_review:
            final_status = "NEEDS_REVIEW"
        elif dedup_gaps:
            final_status = "INCOMPLETE_DATA"
        else:
            final_status = "NO_RULE_TRIGGERED"

        return {
            "status": final_status,
            "rule_set_version": self.version,
            "evidence_snapshot_id": self.evidence_snapshot_id,
            "findings": findings,
            "input_gaps": dedup_gaps,
            "disclaimer": (
                "AMR Sentinel AI is an assistive decision-support prototype. "
                "It does not diagnose, prescribe, or validate medical therapy. "
                "No Rule Triggered indicates non-breach of configured safety rules, not clinical approval. "
                "Clinicians retain sole clinical responsibility."
            ),
        }
