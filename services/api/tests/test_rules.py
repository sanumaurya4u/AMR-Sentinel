"""Comprehensive unit test suite for pure deterministic clinical rules.

Tests:
1. Trigger condition
2. Non-trigger condition
3. Boundary condition
4. Unknown / data-gap condition
5. Clean prescription outcome
"""
import json
from pathlib import Path

import pytest
from app.engine.engine import DeterministicAuditEngine

RULES_FILE = Path(__file__).parent.parent / "app" / "rules_data" / "rules_v1.0.0.json"


@pytest.fixture
def engine():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return DeterministicAuditEngine(manifest)


# 1. PEDIATRIC CONTRAINDICATION
def test_pediatric_ciprofloxacin_triggers_urgent_review(engine):
    """Child age 8 prescribed Ciprofloxacin must trigger URGENT_REVIEW."""
    payload = {
        "patient_context": {"age_years": 8.0, "is_pregnant": False, "egfr_ml_min": 100},
        "indication_code": "SYN_WATERY_DIARRHEA",
        "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "250mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_URGENT_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.PED.FQ_UNDER_18" in rule_ids


def test_adult_ciprofloxacin_does_not_trigger_pediatric_gate(engine):
    """Adult age 25 prescribed Ciprofloxacin should not trigger pediatric contraindication."""
    payload = {
        "patient_context": {"age_years": 25.0, "is_pregnant": False, "egfr_ml_min": 100},
        "indication_code": "SYN_ENTERIC_FEVER",
        "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "500mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.PED.FQ_UNDER_18" not in rule_ids


def test_pediatric_age_boundary_at_18(engine):
    """Exact age 18.0 should not trigger pediatric gate."""
    payload = {
        "patient_context": {"age_years": 18.0, "is_pregnant": False, "egfr_ml_min": 100},
        "indication_code": "SYN_ENTERIC_FEVER",
        "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "500mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.PED.FQ_UNDER_18" not in rule_ids


# 2. PREGNANCY CONTRAINDICATION
def test_pregnancy_contraindication_triggers_urgent_review(engine):
    """Pregnant patient prescribed Doxycycline must trigger URGENT_REVIEW."""
    payload = {
        "patient_context": {"age_years": 28.0, "is_pregnant": True, "egfr_ml_min": 90},
        "indication_code": "SYN_CAP_MILD",
        "prescription_lines": [{"drug_name": "Doxycycline", "dose_text": "100mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_URGENT_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.PREG.CONTRAINDICATED" in rule_ids


# 3. RENAL NITROFURANTOIN
def test_nitrofurantoin_in_severe_renal_impairment(engine):
    """eGFR 22 mL/min prescribed Nitrofurantoin must trigger URGENT_REVIEW."""
    payload = {
        "patient_context": {"age_years": 74.0, "is_pregnant": False, "egfr_ml_min": 22.0},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [{"drug_name": "Nitrofurantoin", "dose_text": "100mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_URGENT_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30" in rule_ids


def test_nitrofurantoin_normal_renal_function_passes(engine):
    """eGFR 90 mL/min in young patient prescribed Nitrofurantoin passes renal check."""
    payload = {
        "patient_context": {"age_years": 30.0, "is_pregnant": False, "egfr_ml_min": 90.0},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [{"drug_name": "Nitrofurantoin", "dose_text": "100mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30" not in rule_ids


# 4. MANDATORY RENAL HOLD (DATA GAP)
def test_gentamicin_without_egfr_triggers_incomplete_data(engine):
    """Gentamicin prescribed with missing eGFR must trigger data gap."""
    payload = {
        "patient_context": {"age_years": 45.0, "is_pregnant": False, "egfr_ml_min": None},
        "indication_code": "SYN_PYELONEPHRITIS_UNCOMPLICATED",
        "prescription_lines": [{"drug_name": "Gentamicin", "dose_text": "80mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] in ("INCOMPLETE_DATA", "NEEDS_REVIEW")
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.RENAL.MISSING_EGFR_HOLD" in rule_ids
    assert any("eGFR" in gap for gap in report["input_gaps"])


# 5. ALLERGY CROSS-REACTIVITY
def test_penicillin_allergy_triggers_urgent_review_for_amoxicillin(engine):
    """Documented Penicillin allergy prescribed Amoxicillin triggers URGENT_REVIEW."""
    payload = {
        "patient_context": {"age_years": 40.0, "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": ["Penicillin"]},
        "indication_code": "SYN_CAP_MILD",
        "prescription_lines": [{"drug_name": "Amoxicillin", "dose_text": "500mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_URGENT_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "SAFETY.ALLERGY.BETA_LACTAM" in rule_ids


# 6. BANNED FIXED-DOSE COMBINATION
def test_banned_fdc_triggers_urgent_review(engine):
    """Cefixime + Azithromycin banned combination triggers URGENT_REVIEW."""
    payload = {
        "patient_context": {"age_years": 35.0, "is_pregnant": False, "egfr_ml_min": 90.0},
        "indication_code": "SYN_CAP_MILD",
        "prescription_lines": [{"drug_name": "Cefixime + Azithromycin", "dose_text": "1 tab", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_URGENT_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "REGULATORY.BANNED_FDC" in rule_ids


# 7. VIRAL INDICATION STEWARDSHIP
def test_azithromycin_in_acute_bronchitis_triggers_needs_review(engine):
    """Azithromycin prescribed for viral acute bronchitis triggers NEEDS_REVIEW."""
    payload = {
        "patient_context": {"age_years": 32.0, "is_pregnant": False, "egfr_ml_min": 100.0},
        "indication_code": "SYN_ACUTE_BRONCHITIS",
        "prescription_lines": [{"drug_name": "Azithromycin", "dose_text": "500mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS" in rule_ids


# 8. WHO AWARE RESERVE ESCALATION
def test_meropenem_in_mild_uti_triggers_needs_review(engine):
    """Meropenem prescribed for mild outpatient cystitis triggers NEEDS_REVIEW."""
    payload = {
        "patient_context": {"age_years": 28.0, "is_pregnant": False, "egfr_ml_min": 105.0},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [{"drug_name": "Meropenem", "dose_text": "1000mg", "duration_days": 7}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NEEDS_REVIEW"
    rule_ids = [f["rule_id"] for f in report["findings"]]
    assert "STEWARDSHIP.AWARE.RESERVE_ESCALATION" in rule_ids


# 9. CLEAN GUIDELINE-CONCORDANT CASE
def test_clean_guideline_case_triggers_no_rules(engine):
    """Amoxicillin 500mg TID 5d for mild CAP in healthy adult triggers NO_RULE_TRIGGERED."""
    payload = {
        "patient_context": {"age_years": 34.0, "is_pregnant": False, "egfr_ml_min": 98.0, "allergies": []},
        "indication_code": "SYN_CAP_MILD",
        "prescription_lines": [{"drug_name": "Amoxicillin", "dose_text": "500mg", "frequency_text": "TID", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    assert report["status"] == "NO_RULE_TRIGGERED"
    assert len(report["findings"]) == 0
    assert len(report["input_gaps"]) == 0
