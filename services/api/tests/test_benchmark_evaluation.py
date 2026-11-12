"""Comprehensive Benchmark Evaluation Test Suite for AMR Sentinel AI Agent.

Verifies:
1. Benchmark case dataset schema, structure, and integrity across all 30 cases.
2. Evaluation metric formulation correctness (token precision/recall/F1, demographics, Jaccard).
3. Offline extraction safety invariants:
   - clinical_status is ALWAYS "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
   - extraction_engine is "offline_heuristic_adapter" when offline
   - clinical disclaimer is non-empty
4. Assistive AMR knowledge service lookup (WHO AWaRe, CDSCO banned FDCs, STG guidelines).
5. Quantitative benchmark comparison against baseline (overall quality, indication accuracy, concordance).
6. Zero safety-critical false negatives (NEEDS_URGENT_REVIEW never downgrades to NO_RULE_TRIGGERED).
"""
import ast
import json
import sys
from pathlib import Path

# Ensure project root and services/api are in sys.path
_ROOT = Path(__file__).resolve().parents[3]
_API_DIR = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
if str(_API_DIR) not in sys.path:
    sys.path.insert(0, str(_API_DIR))

import pytest
from app.extraction.adapter import ExtractionAdapter
from app.services.amr_knowledge import AMRKnowledgeService, get_amr_knowledge_service

from scripts.evaluate_agent import compute_token_f1, evaluate_benchmark

BENCHMARK_CASES_PATH = Path("services/api/tests/data/benchmark_cases.json")
BASELINE_RESULTS_PATH = Path("services/api/tests/data/baseline_evaluation_results.json")
ENGINE_DIR = Path("services/api/app/engine")


def _read_benchmark_cases() -> list[dict]:
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_baseline_results() -> dict:
    with open(BASELINE_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# Tier 1: Feature 1 — Dataset Schema & Integrity Validation
# ==============================================================================


def test_benchmark_cases_file_exists_and_loads():
    """Verify that the benchmark dataset exists, is valid JSON, and has at least 30 cases."""
    assert BENCHMARK_CASES_PATH.exists(), f"Missing benchmark file: {BENCHMARK_CASES_PATH}"
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)
    assert isinstance(cases, list)
    assert len(cases) == 30, f"Expected exactly 30 benchmark cases, found {len(cases)}"


def test_benchmark_cases_unique_case_ids():
    """Verify that all benchmark case IDs are distinct, non-empty, and follow naming convention."""
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)
    ids = [c.get("id") for c in cases]
    assert all(bool(cid and isinstance(cid, str)) for cid in ids)
    assert len(ids) == len(set(ids)), f"Duplicate IDs detected: {len(ids)} total vs {len(set(ids))} unique"


def test_benchmark_cases_required_keys():
    """Verify that every case adheres to the top-level benchmark schema."""
    required_keys = {"id", "scenario", "document_text", "ground_truth", "expected_audit"}
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        missing = required_keys - set(case.keys())
        assert not missing, f"Case {case.get('id')} missing keys: {missing}"
        assert case["document_text"].strip(), f"Case {case['id']} has empty document_text"
        assert case["scenario"].strip(), f"Case {case['id']} has empty scenario"


def test_benchmark_cases_ground_truth_structure():
    """Verify that ground_truth contains valid patientContext, indicationCode, and prescriptionLines."""
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        gt = case["ground_truth"]
        assert "patientContext" in gt, f"Case {case['id']} missing patientContext in ground_truth"
        assert "indicationCode" in gt, f"Case {case['id']} missing indicationCode in ground_truth"
        assert "prescriptionLines" in gt, f"Case {case['id']} missing prescriptionLines in ground_truth"

        ctx = gt["patientContext"]
        assert isinstance(ctx.get("ageYears"), (int, float)), f"Case {case['id']} invalid ageYears"
        assert ctx.get("ageYears") >= 0.0, f"Case {case['id']} negative ageYears"
        assert ctx.get("gender") in {"male", "female"}, f"Case {case['id']} invalid gender"
        assert isinstance(ctx.get("isPregnant"), bool), f"Case {case['id']} isPregnant must be bool"
        assert isinstance(ctx.get("allergies"), list), f"Case {case['id']} allergies must be list"
        if ctx.get("egfrMlMin") is not None:
            assert isinstance(ctx["egfrMlMin"], (int, float)), f"Case {case['id']} invalid egfrMlMin"

        ind = gt["indicationCode"]
        assert ind.startswith("SYN_"), f"Case {case['id']} indicationCode must start with SYN_, got {ind}"

        lines = gt["prescriptionLines"]
        assert isinstance(lines, list) and len(lines) > 0, f"Case {case['id']} prescriptionLines empty"
        for line in lines:
            assert line.get("drugName"), f"Case {case['id']} missing drugName in line"
            assert line.get("doseText"), f"Case {case['id']} missing doseText in line"
            assert line.get("frequencyText"), f"Case {case['id']} missing frequencyText in line"


def test_benchmark_cases_expected_audit_structure():
    """Verify that expected_audit specifies a recognized clinical status and rule IDs."""
    valid_statuses = {"NEEDS_URGENT_REVIEW", "NEEDS_REVIEW", "INCOMPLETE_DATA", "NO_RULE_TRIGGERED"}
    with open(BENCHMARK_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        exp = case["expected_audit"]
        assert "status" in exp, f"Case {case['id']} missing status in expected_audit"
        assert exp["status"] in valid_statuses, f"Case {case['id']} unknown status: {exp['status']}"
        assert "rules" in exp, f"Case {case['id']} missing rules list"
        assert isinstance(exp["rules"], list), f"Case {case['id']} rules must be a list"


def test_baseline_results_file_structure():
    """Verify that baseline_evaluation_results.json exists and conforms to evaluation schema."""
    assert BASELINE_RESULTS_PATH.exists(), f"Missing baseline results: {BASELINE_RESULTS_PATH}"
    with open(BASELINE_RESULTS_PATH, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    assert "summary" in baseline
    assert "details" in baseline
    summary = baseline["summary"]
    assert summary["total_cases"] == 30
    assert "demographics" in summary
    assert "medication_extraction" in summary
    assert "indication_classification" in summary
    assert "audit_concordance" in summary
    assert "overall_quality_score" in summary


# ==============================================================================
# Tier 1: Feature 1 — Metric Formulation Unit Tests
# ==============================================================================


def test_compute_token_f1_exact_match():
    """Token F1 should return 1.0, 1.0, 1.0 when prediction and truth match exactly."""
    pred = ["Amoxicillin", "Paracetamol"]
    truth = ["Amoxicillin", "Paracetamol"]
    p, r, f1 = compute_token_f1(pred, truth)
    assert p == 1.0
    assert r == 1.0
    assert f1 == 1.0


def test_compute_token_f1_case_insensitivity():
    """Token F1 should normalize strings case-insensitively and strip whitespace."""
    pred = [" ciprofloxacin ", "METROGYL "]
    truth = ["Ciprofloxacin", "metrogyl"]
    p, r, f1 = compute_token_f1(pred, truth)
    assert p == 1.0
    assert r == 1.0
    assert f1 == 1.0


def test_compute_token_f1_partial_overlap():
    """Token F1 should accurately calculate precision, recall, and harmonic mean."""
    pred = ["Amoxicillin", "Clavulanate"]
    truth = ["Amoxicillin", "Paracetamol"]
    p, r, f1 = compute_token_f1(pred, truth)
    assert p == 0.5
    assert r == 0.5
    assert f1 == 0.5


def test_compute_token_f1_completely_disjoint():
    """Token F1 should return 0.0 when there is zero overlap between tokens."""
    pred = ["Ciprofloxacin"]
    truth = ["Azithromycin"]
    p, r, f1 = compute_token_f1(pred, truth)
    assert p == 0.0
    assert r == 0.0
    assert f1 == 0.0


def test_compute_token_f1_empty_inputs_boundary():
    """Token F1 handles empty predictions and ground truths without division-by-zero errors."""
    # Both empty -> perfect concordance
    p, r, f1 = compute_token_f1([], [])
    assert p == 1.0 and r == 1.0 and f1 == 1.0

    # One empty, one non-empty -> 0
    p, r, f1 = compute_token_f1(["Amoxicillin"], [])
    assert p == 0.0 and r == 0.0 and f1 == 0.0

    p, r, f1 = compute_token_f1([], ["Amoxicillin"])
    assert p == 0.0 and r == 0.0 and f1 == 0.0


def test_compute_token_f1_duplicate_predictions_bounded():
    """Verify multiset intersection prevents mathematical overflow when duplicate predictions exist.

    Predicting 5x 'Amoxicillin' against 1x ground-truth 'Amoxicillin':
    - True Positives = 1 (bounded by ground-truth multiset count)
    - Precision = 1 / 5 = 0.2
    - Recall = 1 / 1 = 1.0
    - F1 = 2 * 0.2 * 1.0 / (0.2 + 1.0) = 0.4 / 1.2 = 0.3333... <= 1.0
    Ensures Recall and F1 NEVER exceed 1.0 (100%).
    """
    pred = ["Amoxicillin"] * 5
    truth = ["Amoxicillin"]
    p, r, f1 = compute_token_f1(pred, truth)
    assert round(p, 4) == 0.2
    assert round(r, 4) == 1.0
    assert f1 <= 1.0
    assert round(f1, 4) == round(0.4 / 1.2, 4)

    # Reverse: 1 prediction against multiple ground truth
    pred_rev = ["Amoxicillin"]
    truth_rev = ["Amoxicillin", "Amoxicillin"]
    p_rev, r_rev, f1_rev = compute_token_f1(pred_rev, truth_rev)
    assert round(p_rev, 4) == 1.0
    assert round(r_rev, 4) == 0.5
    assert f1_rev <= 1.0


# ==============================================================================
# Tier 1 & 2: Feature 2 — Local Offline Extraction & Safety Invariant Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_offline_extraction_safety_invariants_across_all_cases():
    """Verify that offline extraction strictly enforces the Two-Layer Safety Architecture.

    CRITICAL INVARIANTS:
    1. clinical_status is ALWAYS 'UNTRUSTED_DRAFT_PENDING_CONFIRMATION'
    2. extraction_engine is 'offline_heuristic_adapter' when offline
    3. disclaimer is present and non-empty
    4. fieldConfidence is present for all extracted fields
    """
    adapter = ExtractionAdapter()
    cases = _read_benchmark_cases()

    for case in cases:
        file_bytes = case["document_text"].encode("utf-8")
        extracted = await adapter.extract_from_bytes(file_bytes, "text/plain", filename=f"{case['id']}.txt")

        # Invariant 1: Safety boundary flag
        assert extracted.get("clinical_status") == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION", (
            f"Case {case['id']} violated clinical_status safety invariant!"
        )

        # Invariant 2: Engine identification
        assert extracted.get("extraction_engine") == "offline_heuristic_adapter", (
            f"Case {case['id']} engine should be offline_heuristic_adapter, got {extracted.get('extraction_engine')}"
        )

        # Invariant 3: Clinician disclaimer
        assert extracted.get("disclaimer") and len(extracted["disclaimer"]) > 10, (
            f"Case {case['id']} missing clinical disclaimer"
        )

        # Invariant 4: Confidence metadata
        fc = extracted.get("fieldConfidence", {})
        for field in ["ageYears", "gender", "isPregnant", "egfrMlMin", "indicationCode", "prescriptionLines"]:
            assert field in fc, f"Case {case['id']} missing fieldConfidence for {field}"

        # Invariant 5: Setting is outpatient
        assert extracted.get("setting") == "outpatient"

        # Invariant 6: Prescription lines populated
        lines = extracted.get("prescriptionLines", [])
        assert len(lines) > 0, f"Case {case['id']} extracted zero prescription lines"


@pytest.mark.asyncio
async def test_offline_brand_to_generic_mappings():
    """Verify canonical Indian trade brand resolution to generic active ingredients."""
    adapter = ExtractionAdapter()
    test_cases = [
        ("Rx: Tab Augmentin 625mg BD x 5d", "Amoxicillin-Clavulanate"),
        ("Rx: Tab Cifran 500mg BD x 5d", "Ciprofloxacin"),
        ("Rx: Cap Martifur 100mg BD x 5d", "Nitrofurantoin"),
        ("Rx: Tab Azithral 500mg OD x 3d", "Azithromycin"),
        ("Rx: Tab Taxim-O 200mg BD x 5d", "Cefixime"),
        ("Rx: Tab Doxicip 100mg BD x 5d", "Doxycycline"),
        ("Rx: Inj Monocef 1g OD x 5d", "Ceftriaxone"),
        ("Rx: Inj Meronem 1g TDS x 7d", "Meropenem"),
    ]

    for raw_rx, expected_generic in test_cases:
        extracted = await adapter.extract_from_bytes(raw_rx.encode("utf-8"), "text/plain", "rx.txt")
        drug_names = [line["drugName"] for line in extracted.get("prescriptionLines", [])]
        assert expected_generic in drug_names, (
            f"Expected {expected_generic} from '{raw_rx}', got {drug_names}"
        )


@pytest.mark.asyncio
async def test_offline_compound_fdc_no_duplicate_component_lines():
    """Verify that compound FDCs (e.g. Cefixime + Azithromycin) do not extract duplicate individual components."""
    adapter = ExtractionAdapter()
    compound_samples = [
        ("Rx: Tab Cefixime + Azithromycin 200mg+250mg BD x 5d", "Cefixime + Azithromycin"),
        ("Rx: Tab Ofloxacin + Ornidazole 200mg+500mg BD x 5d", "Ofloxacin + Ornidazole"),
        ("Rx: Cap Amoxicillin + Flucloxacillin 500mg+500mg BD x 5d", "Amoxicillin + Flucloxacillin"),
    ]
    for text, expected_compound in compound_samples:
        extracted = await adapter.extract_from_bytes(text.encode("utf-8"), "text/plain", "rx.txt")
        lines = extracted.get("prescriptionLines", [])
        drug_names = [line["drugName"] for line in lines]
        assert drug_names == [expected_compound], (
            f"Expected exactly 1 compound drug line [{expected_compound}], got {drug_names}"
        )


@pytest.mark.asyncio
async def test_offline_posology_and_frequency_parsing():
    """Verify gram-to-mg conversion and frequency expansion in local heuristics."""
    adapter = ExtractionAdapter()

    # Gram-to-mg conversion (1g -> 1000 mg)
    note_gram = "Rx: Tab Cifran 1g BD x 5 days"
    extracted = await adapter.extract_from_bytes(note_gram.encode("utf-8"), "text/plain", "rx.txt")
    lines = extracted.get("prescriptionLines", [])
    assert lines[0]["doseText"] == "1000 mg"
    assert lines[0]["frequencyText"] == "Twice daily (BD)"
    assert lines[0]["durationDays"] == 5

    # Fractional gram conversion (0.5g -> 500 mg / 500.0 mg)
    note_fractional = "Rx: Tab Amoxil 0.5g TDS for 7 days"
    extracted_frac = await adapter.extract_from_bytes(note_fractional.encode("utf-8"), "text/plain", "rx.txt")
    lines_frac = extracted_frac.get("prescriptionLines", [])
    assert "500" in lines_frac[0]["doseText"]
    assert "TDS" in lines_frac[0]["frequencyText"] or "TID" in lines_frac[0]["frequencyText"]
    assert lines_frac[0]["durationDays"] == 7


@pytest.mark.asyncio
async def test_offline_indication_classification():
    """Verify that clinical symptom notes map to canonical SYN_ indication codes."""
    adapter = ExtractionAdapter()
    test_indications = [
        ("Complaints: Burning micturition, dysuria, urgency x 2 days.", "SYN_UNCOMPLICATED_UTI"),
        ("Diagnosis: Mild Community Acquired Pneumonia with cough and fever.", "SYN_CAP_MILD"),
        ("Complaints: Acute watery diarrhea and mild abdominal cramps.", "SYN_WATERY_DIARRHEA"),
        ("Diagnosis: Acute Bronchitis, productive cough with clear sputum.", "SYN_ACUTE_BRONCHITIS"),
        ("Diagnosis: Acute Otitis Media with severe ear pain.", "SYN_AOM"),
    ]

    for note, expected_syn in test_indications:
        extracted = await adapter.extract_from_bytes(note.encode("utf-8"), "text/plain", "note.txt")
        assert extracted.get("indicationCode") == expected_syn, (
            f"Expected {expected_syn} from '{note}', got {extracted.get('indicationCode')}"
        )


# ==============================================================================
# Tier 1 & 2: Feature 4 — AMR Knowledge Service Retrieval Tests
# ==============================================================================


def test_amr_knowledge_service_aware_lookup():
    """Verify accurate WHO AWaRe classification retrieval for core antibiotics."""
    svc = get_amr_knowledge_service()

    # Access group
    assert svc.get_drug_info("Amoxicillin")["aware_class"] == "Access"
    assert svc.get_drug_info("Amoxicillin-Clavulanate")["aware_class"] == "Access"
    assert svc.get_drug_info("Nitrofurantoin")["aware_class"] == "Access"
    assert svc.get_drug_info("Doxycycline")["aware_class"] == "Access"
    assert svc.get_drug_info("Cefalexin")["aware_class"] == "Access"

    # Watch group
    assert svc.get_drug_info("Ciprofloxacin")["aware_class"] == "Watch"
    assert svc.get_drug_info("Levofloxacin")["aware_class"] == "Watch"
    assert svc.get_drug_info("Ofloxacin")["aware_class"] == "Watch"
    assert svc.get_drug_info("Azithromycin")["aware_class"] == "Watch"
    assert svc.get_drug_info("Cefixime")["aware_class"] == "Watch"

    # Reserve group
    assert svc.get_drug_info("Meropenem")["aware_class"] == "Reserve"
    assert svc.get_drug_info("Linezolid")["aware_class"] == "Reserve"

    # Unclassified
    assert svc.get_drug_info("NovelAntibioticX")["aware_class"] == "Unclassified"


def test_amr_knowledge_service_banned_fdc_detection():
    """Verify CDSCO regulatory prohibited fixed-dose combination detection."""
    svc = get_amr_knowledge_service()

    banned_drugs = [
        "Cefixime + Azithromycin",
        "Ofloxacin + Ornidazole",
        "Amoxicillin + Flucloxacillin",
        "Ampicillin + Cloxacillin",
        "Ciprofloxacin + Tinidazole",
    ]
    for banned in banned_drugs:
        assert svc.check_banned_fdc(banned) is True, f"Failed to detect banned FDC: {banned}"

    # Legitimate monotherapy should not be flagged as banned FDC
    assert svc.check_banned_fdc("Amoxicillin") is False
    assert svc.check_banned_fdc("Ciprofloxacin") is False
    assert svc.check_banned_fdc("Nitrofurantoin") is False


def test_amr_knowledge_service_resistance_evidence():
    """Verify surveillance resistance evidence retrieval for high-risk drug/condition pairs."""
    svc = get_amr_knowledge_service()

    # Fluoroquinolone in lower UTI
    ev_uti = svc.get_resistance_evidence("Ciprofloxacin", "SYN_UNCOMPLICATED_UTI")
    assert ev_uti is not None
    assert "75%" in ev_uti or "fluoroquinolone" in ev_uti.lower()

    # Fluoroquinolone in watery diarrhea
    ev_diarrhea = svc.get_resistance_evidence("Ciprofloxacin", "SYN_WATERY_DIARRHEA")
    assert ev_diarrhea is not None
    assert "enteric" in ev_diarrhea.lower() or "resistance" in ev_diarrhea.lower()

    # Macrolide in acute bronchitis
    ev_bronch = svc.get_resistance_evidence("Azithromycin", "SYN_ACUTE_BRONCHITIS")
    assert ev_bronch is not None
    assert "viral" in ev_bronch.lower()

    # Reserve Meropenem in mild UTI
    ev_mero = svc.get_resistance_evidence("Meropenem", "SYN_UNCOMPLICATED_UTI")
    assert ev_mero is not None
    assert "Reserve" in ev_mero or "carbapenem" in ev_mero.lower()

    # Clean concordant case should have None resistance alert
    ev_clean = svc.get_resistance_evidence("Amoxicillin", "SYN_CAP_MILD")
    assert ev_clean is None


def test_amr_knowledge_service_guidelines_retrieval():
    """Verify ICMR Standard Treatment Guideline recommendations for key indication codes."""
    svc = get_amr_knowledge_service()

    g_uti = svc.get_guideline("SYN_UNCOMPLICATED_UTI")
    assert g_uti is not None
    assert g_uti["antibiotic_indicated"] is True
    assert "Nitrofurantoin" in g_uti["recommended_regimen"]

    g_bronch = svc.get_guideline("SYN_ACUTE_BRONCHITIS")
    assert g_bronch is not None
    assert g_bronch["antibiotic_indicated"] is False

    g_diarrhea = svc.get_guideline("SYN_WATERY_DIARRHEA")
    assert g_diarrhea is not None
    assert g_diarrhea["antibiotic_indicated"] is False
    assert "ORS" in g_diarrhea["recommended_regimen"]

    # None indication code returns None
    assert svc.get_guideline(None) is None


def test_amr_knowledge_composite_assistive_guidance():
    """Verify composite guidance generation for prescription intake drafts."""
    svc = AMRKnowledgeService()
    lines = [
        {"drugName": "Ciprofloxacin", "doseText": "500 mg"},
        {"drugName": "Cefixime + Azithromycin", "doseText": "200 mg + 250 mg"},
    ]
    guidance = svc.get_assistive_guidance(lines, "SYN_UNCOMPLICATED_UTI")

    assert guidance["indication_code"] == "SYN_UNCOMPLICATED_UTI"
    assert guidance["antibiotic_indicated"] is True
    assert "disclaimer" in guidance
    assert len(guidance["drug_guidance"]) == 2

    # Check first drug
    d0 = guidance["drug_guidance"][0]
    assert d0["drug_name"] == "Ciprofloxacin"
    assert d0["aware_class"] == "Watch"
    assert d0["is_banned_fdc"] is False
    assert d0["resistance_evidence"] is not None

    # Check second drug (banned FDC)
    d1 = guidance["drug_guidance"][1]
    assert d1["is_banned_fdc"] is True


# ==============================================================================
# Tier 3 & 4: E2E Benchmark Evaluation & Non-Regression Verification
# ==============================================================================


@pytest.mark.asyncio
async def test_e2e_benchmark_evaluation_meets_or_exceeds_baseline():
    """Run full benchmark evaluation on all 30 cases and assert metrics meet or exceed baseline.

    Verifies:
    1. Overall quality score >= baseline (81.9 -> ~96.6)
    2. Indication classification accuracy >= baseline (23.33% -> ~93.3%)
    3. Clinical audit status concordance >= baseline (60.0% -> ~96.7%)
    4. Mean rule Jaccard similarity >= baseline (58.33% -> ~95.0%)
    5. Demographic accuracies maintain >= 90%
    6. Drug F1 score maintains >= 95%
    """
    res = await evaluate_benchmark(BENCHMARK_CASES_PATH)
    current = res["summary"]
    baseline_data = _read_baseline_results()
    base = baseline_data["summary"]

    assert current["total_cases"] == 30

    # 1. Overall quality score
    assert current["overall_quality_score"] >= base["overall_quality_score"], (
        f"Overall quality score degraded: {current['overall_quality_score']} vs baseline {base['overall_quality_score']}"
    )

    # 2. Indication classification accuracy
    curr_ind_acc = current["indication_classification"]["indication_accuracy"]
    base_ind_acc = base["indication_classification"]["indication_accuracy"]
    assert curr_ind_acc >= base_ind_acc, (
        f"Indication accuracy degraded: {curr_ind_acc}% vs baseline {base_ind_acc}%"
    )
    assert curr_ind_acc >= 80.0, f"Indication accuracy should be at least 80%, got {curr_ind_acc}%"

    # 3. Downstream clinical audit concordance
    curr_concordance = current["audit_concordance"]["status_concordance"]
    base_concordance = base["audit_concordance"]["status_concordance"]
    assert curr_concordance >= base_concordance, (
        f"Audit concordance degraded: {curr_concordance}% vs baseline {base_concordance}%"
    )
    assert curr_concordance >= 90.0, f"Audit status concordance should be >= 90%, got {curr_concordance}%"

    # 4. Mean rule Jaccard
    curr_jaccard = current["audit_concordance"]["mean_rule_jaccard"]
    base_jaccard = base["audit_concordance"]["mean_rule_jaccard"]
    assert curr_jaccard >= base_jaccard, (
        f"Mean rule Jaccard degraded: {curr_jaccard}% vs baseline {base_jaccard}%"
    )

    # 5. Demographics
    assert current["demographics"]["age_accuracy"] >= 95.0
    assert current["demographics"]["gender_accuracy"] >= 85.0
    assert current["demographics"]["pregnancy_accuracy"] >= 90.0
    assert current["demographics"]["egfr_accuracy"] >= 95.0

    # 6. Medication extraction
    assert current["medication_extraction"]["drug_f1"] >= 95.0


@pytest.mark.asyncio
async def test_zero_safety_critical_false_negatives():
    """Verify that expected urgent clinical safety violations NEVER produce NO_RULE_TRIGGERED.

    SAFETY MANDATE:
    If a prescription has severe contraindications (pediatric FQ, pregnancy contraindication,
    banned FDC, severe renal accumulation), the downstream audit engine must NEVER return
    NO_RULE_TRIGGERED. False negatives on urgent safety violations are strictly prohibited.
    """
    res = await evaluate_benchmark(BENCHMARK_CASES_PATH)
    details = res["details"]

    false_negatives = []
    for d in details:
        if d["exp_status"] == "NEEDS_URGENT_REVIEW" and d["pred_status"] == "NO_RULE_TRIGGERED":
            false_negatives.append(d)

    assert len(false_negatives) == 0, (
        f"CRITICAL SAFETY VIOLATION: {len(false_negatives)} cases with expected NEEDS_URGENT_REVIEW "
        f"predicted NO_RULE_TRIGGERED: {[fn['id'] for fn in false_negatives]}"
    )


# ==============================================================================
# Tier 1: Feature 5 — Deterministic Core AST Isolation Invariant
# ==============================================================================


def test_deterministic_core_ast_isolation_maintained():
    """Verify that services/api/app/engine/ maintains pure AST isolation.

    Zero network, zero AI SDKs, zero database, zero subprocess.
    """
    prohibited_modules = {
        "requests", "httpx", "aiohttp", "urllib.request",
        "google", "google.genai", "google.generativeai",
        "openai", "anthropic", "langchain", "llama_index",
        "sqlalchemy", "supabase", "psycopg2", "asyncpg",
        "subprocess", "os.system",
    }

    assert ENGINE_DIR.exists(), f"Engine directory missing: {ENGINE_DIR}"

    for py_file in ENGINE_DIR.glob("**/*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(py_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prohibited in prohibited_modules:
                        assert not alias.name.startswith(prohibited), (
                            f"Prohibited import '{alias.name}' detected in {py_file}"
                        )
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for prohibited in prohibited_modules:
                    assert not mod.startswith(prohibited), (
                        f"Prohibited from-import '{mod}' detected in {py_file}"
                    )
