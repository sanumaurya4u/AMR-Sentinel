"""Pure Python Clinical Rule Evaluators.

CRITICAL ARCHITECTURAL CONSTRAINTS:
- Pure functions only.
- Zero network, database, AI/LLM, or OS environment imports.
- Completely deterministic output for identical inputs and rule manifests.
"""
from typing import Any


def normalize_drug_name(name: str) -> str:
    """Normalize drug name for exact and substring matching."""
    return name.strip().lower()


def check_pediatric_contraindication(
    age_years: float,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check if any prescribed drug is contraindicated in pediatric age group."""
    min_age = rule.get("min_age_years", 18.0)
    if age_years >= min_age:
        return None

    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    for drug in prescribed_drugs:
        drug_norm = normalize_drug_name(drug)
        if any(t in drug_norm for t in target_drugs):
            facts = {
                "Patient Age": f"{age_years} years",
                "Minimum Safe Age Threshold": f"{min_age} years",
                "Triggering Drug": drug,
            }
            return facts, []

    return None


def check_pregnancy_contraindication(
    is_pregnant: bool,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check if any prescribed drug is contraindicated in pregnancy."""
    if not is_pregnant:
        return None

    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    for drug in prescribed_drugs:
        drug_norm = normalize_drug_name(drug)
        if any(t in drug_norm for t in target_drugs):
            facts = {
                "Pregnancy Documented": True,
                "Triggering Agent": drug,
                "Clinical Risk": "FDA Category D/X or proven fetal toxicity",
            }
            return facts, []

    return None


def check_renal_nitrofurantoin(
    age_years: float,
    egfr_ml_min: float | None,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check Nitrofurantoin contraindication in severe renal impairment or geriatric age."""
    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    has_nitro = any(
        any(t in normalize_drug_name(drug) for t in target_drugs)
        for drug in prescribed_drugs
    )

    if not has_nitro:
        return None

    egfr_thresh = rule.get("egfr_threshold", 30.0)
    geriatric_thresh = rule.get("geriatric_age_threshold", 65.0)

    # Check triggering conditions
    if egfr_ml_min is not None and egfr_ml_min < egfr_thresh:
        facts = {
            "Prescribed Drug": "Nitrofurantoin",
            "Patient eGFR": f"{egfr_ml_min} mL/min",
            "Threshold Limit": f"<{egfr_thresh} mL/min",
            "Failure Mechanism": "Inadequate urinary clearance and severe peripheral neurotoxicity risk",
        }
        return facts, []

    if age_years >= geriatric_thresh and (egfr_ml_min is None or egfr_ml_min < 45.0):
        facts = {
            "Prescribed Drug": "Nitrofurantoin",
            "Patient Age": f"{age_years} years",
            "Patient eGFR": f"{egfr_ml_min if egfr_ml_min is not None else 'Unrecorded'}",
            "Beers Criteria Alert": "Geriatric renal risk with high adverse event profile",
        }
        gaps = ["eGFR unrecorded in geriatric patient"] if egfr_ml_min is None else []
        return facts, gaps

    return None


def check_missing_egfr_hold(
    egfr_ml_min: float | None,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check if nephrotoxic agents are prescribed without documented renal function."""
    if egfr_ml_min is not None:
        return None  # eGFR is documented, safety hold not triggered

    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    for drug in prescribed_drugs:
        drug_norm = normalize_drug_name(drug)
        if any(t in drug_norm for t in target_drugs):
            facts = {
                "Nephrotoxic Agent Prescribed": drug,
                "Documented eGFR": "Missing / Unrecorded",
                "KDIGO Protocol": "Baseline renal function required prior to administration",
            }
            return facts, ["eGFR (Estimated Glomerular Filtration Rate)"]

    return None


def check_beta_lactam_allergy(
    allergies: list[str],
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check for beta-lactam allergy cross-reactivity."""
    if not allergies:
        return None

    allergy_triggers = [a.lower() for a in rule.get("allergy_triggers", [])]
    has_allergy = any(
        any(trigger in normalize_drug_name(user_allergy) for trigger in allergy_triggers)
        for user_allergy in allergies
    )

    if not has_allergy:
        return None

    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    for drug in prescribed_drugs:
        drug_norm = normalize_drug_name(drug)
        if any(t in drug_norm for t in target_drugs):
            facts = {
                "Documented Allergy": ", ".join(allergies),
                "Prescribed Beta-Lactam": drug,
                "Risk": "Severe IgE-mediated anaphylaxis or cross-reactivity",
            }
            return facts, []

    return None


def check_banned_fdc(
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check for CDSCO / WHO banned fixed-dose combinations.

    Matches either:
    1. A single prescription line containing both ingredients (e.g. 'Cefixime + Azithromycin')
    2. Concurrent prescription of both separate active ingredients.
    """
    normalized_all = [normalize_drug_name(d) for d in prescribed_drugs]

    # Recognized banned pairs: (ingredient_a, ingredient_b, display_title)
    banned_pairs = [
        ("cefixime", "azithromycin", "Cefixime + Azithromycin"),
        ("ofloxacin", "ornidazole", "Ofloxacin + Ornidazole"),
    ]

    for ing_a, ing_b, display_name in banned_pairs:
        # Check single line with both
        has_combo_line = any(ing_a in d and ing_b in d for d in normalized_all)

        # Check concurrent separate lines
        has_separate_lines = any(ing_a in d for d in normalized_all) and any(ing_b in d for d in normalized_all)

        if has_combo_line or has_separate_lines:
            facts = {
                "Banned FDC Prescribed": display_name,
                "Regulatory Authority": "CDSCO Gazette Notification",
                "Status": "Manufacture, sale and clinical use legally prohibited in India",
            }
            return facts, []

    return None


def check_viral_indication(
    indication_code: str,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check inappropriate antibiotic prescription for viral self-limiting indications."""
    target_conditions = rule.get("target_conditions", [])
    if indication_code not in target_conditions:
        return None

    # Exclude non-antibiotics (e.g. Paracetamol, ORS)
    non_antibiotics = ["oral rehydration", "ors", "paracetamol", "zinc", "saline"]
    antibiotic_drugs = [
        d for d in prescribed_drugs
        if not any(na in normalize_drug_name(d) for na in non_antibiotics)
    ]

    if not antibiotic_drugs:
        return None

    facts = {
        "Suspected Indication": indication_code,
        "Prescribed Antibiotic": ", ".join(antibiotic_drugs),
        "Clinical Evidence": "Etiology is >90% viral; antibiotics confer zero efficacy and induce resistance",
    }
    return facts, []


def check_aware_reserve_escalation(
    indication_code: str,
    prescribed_drugs: list[str],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check empirical use of Reserve-group antimicrobials for mild outpatient indications."""
    mild_indications = rule.get("mild_indications", [])
    if indication_code not in mild_indications:
        return None

    target_drugs = [d.lower() for d in rule.get("target_drugs", [])]
    for drug in prescribed_drugs:
        drug_norm = normalize_drug_name(drug)
        if any(t in drug_norm for t in target_drugs):
            facts = {
                "Prescribed Agent": drug,
                "WHO AWaRe Classification": "Reserve (Last-Resort)",
                "Indication": indication_code,
                "Stewardship Concern": "Reserve agents must be protected for confirmed MDR life-threatening infections",
            }
            return facts, []

    return None


def check_excessive_duration(
    indication_code: str,
    prescription_lines: list[dict[str, Any]],
    rule: dict[str, Any],
) -> tuple[dict[str, Any], list[str]] | None:
    """Check if prescribed treatment duration exceeds ICMR short-course recommendations."""
    target_conditions = rule.get("target_conditions", [])
    if indication_code not in target_conditions:
        return None

    max_days = rule.get("max_duration_days", 5)
    for line in prescription_lines:
        duration = line.get("duration_days")
        if duration is not None and duration > max_days:
            facts = {
                "Prescribed Drug": line.get("drug_name"),
                "Prescribed Duration": f"{duration} days",
                "ICMR Recommended Max Duration": f"{max_days} days",
                "Clinical Concern": "Extended courses select for resistant flora without improving clinical cure",
            }
            return facts, []

    return None
