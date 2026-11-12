"""Milestone 5 Adversarial Verification: Boundary & Resilience Stress Test Suite.

Stress tests:
1. Exact age boundaries (Ciprofloxacin 18.0 vs 17.9, Doxycycline 12.0 vs 11.9, micro-thresholds).
2. Exact renal boundaries (Nitrofurantoin eGFR 30.0 vs 29.9, Beers criteria interaction, null eGFR holds).
3. Network resilience & circuit breaker (HTTP 429, HTTP 500, socket timeout, malformed truncated JSON).
4. Deterministic audit core reproducibility (100-run SHA256 invariance, concurrency, key-order invariance).
"""
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import AsyncMock, patch

_API_DIR = Path(__file__).resolve().parents[1]
if str(_API_DIR) not in sys.path:
    sys.path.insert(0, str(_API_DIR))

import httpx
import pytest
from app.config import Settings
from app.engine.engine import DeterministicAuditEngine
from app.extraction.adapter import ExtractionAdapter

RULES_FILE = Path(__file__).parent.parent / "app" / "rules_data" / "rules_v1.0.0.json"




@pytest.fixture
def engine():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return DeterministicAuditEngine(manifest)


# ==============================================================================
# 1. Exact Age Boundaries
# ==============================================================================


@pytest.mark.parametrize(
    "age,drug_name,should_trigger,expected_status",
    [
        (18.0, "Ciprofloxacin", False, "NO_RULE_TRIGGERED"),
        (18.1, "Ciprofloxacin", False, "NO_RULE_TRIGGERED"),
        (17.9, "Ciprofloxacin", True, "NEEDS_URGENT_REVIEW"),
        (17.999, "Ciprofloxacin", True, "NEEDS_URGENT_REVIEW"),
        (18.001, "Ciprofloxacin", False, "NO_RULE_TRIGGERED"),
        (17.9, "Levofloxacin", True, "NEEDS_URGENT_REVIEW"),
        (18.0, "Levofloxacin", False, "NO_RULE_TRIGGERED"),
        (17.9, "Ofloxacin", True, "NEEDS_URGENT_REVIEW"),
        (18.0, "Ofloxacin", False, "NO_RULE_TRIGGERED"),
        (17.9, "Norfloxacin", True, "NEEDS_URGENT_REVIEW"),
        (18.0, "Norfloxacin", False, "NO_RULE_TRIGGERED"),
        (17.9, "Moxifloxacin", True, "NEEDS_URGENT_REVIEW"),
        (18.0, "Moxifloxacin", False, "NO_RULE_TRIGGERED"),
    ],
)
def test_ciprofloxacin_and_fq_pediatric_age_boundaries(engine, age, drug_name, should_trigger, expected_status):
    """Stress-test exact age boundary for Fluoroquinolones (min_age_years = 18.0)."""
    payload = {
        "patient_context": {"age_years": age, "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []},
        "indication_code": "SYN_ENTERIC_FEVER",
        "prescription_lines": [{"drug_name": drug_name, "dose_text": "500 mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    triggered_rules = [f["rule_id"] for f in report["findings"]]

    if should_trigger:
        assert "SAFETY.PED.FQ_UNDER_18" in triggered_rules, (
            f"Expected SAFETY.PED.FQ_UNDER_18 for {drug_name} at age {age}"
        )
        assert report["status"] == expected_status
    else:
        assert "SAFETY.PED.FQ_UNDER_18" not in triggered_rules, (
            f"Did not expect SAFETY.PED.FQ_UNDER_18 for {drug_name} at age {age}"
        )


@pytest.mark.parametrize(
    "age,drug_name,should_trigger,expected_status",
    [
        (12.0, "Doxycycline", False, "NO_RULE_TRIGGERED"),
        (12.1, "Doxycycline", False, "NO_RULE_TRIGGERED"),
        (11.9, "Doxycycline", True, "NEEDS_URGENT_REVIEW"),
        (11.999, "Doxycycline", True, "NEEDS_URGENT_REVIEW"),
        (12.001, "Doxycycline", False, "NO_RULE_TRIGGERED"),
        (11.9, "Tetracycline", True, "NEEDS_URGENT_REVIEW"),
        (12.0, "Tetracycline", False, "NO_RULE_TRIGGERED"),
        (11.9, "Minocycline", True, "NEEDS_URGENT_REVIEW"),
        (12.0, "Minocycline", False, "NO_RULE_TRIGGERED"),
    ],
)
def test_doxycycline_and_tetracycline_pediatric_age_boundaries(engine, age, drug_name, should_trigger, expected_status):
    """Stress-test exact age boundary for Tetracyclines (min_age_years = 12.0)."""
    payload = {
        "patient_context": {"age_years": age, "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []},
        "indication_code": "SYN_CAP_MILD",
        "prescription_lines": [{"drug_name": drug_name, "dose_text": "100 mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    triggered_rules = [f["rule_id"] for f in report["findings"]]

    if should_trigger:
        assert "SAFETY.PED.TETRACYCLINE_UNDER_18" in triggered_rules, (
            f"Expected SAFETY.PED.TETRACYCLINE_UNDER_18 for {drug_name} at age {age}"
        )
        assert report["status"] == expected_status
    else:
        assert "SAFETY.PED.TETRACYCLINE_UNDER_18" not in triggered_rules, (
            f"Did not expect SAFETY.PED.TETRACYCLINE_UNDER_18 for {drug_name} at age {age}"
        )


# ==============================================================================
# 2. Exact Renal Thresholds
# ==============================================================================


@pytest.mark.parametrize(
    "egfr,age,should_trigger,expected_status",
    [
        (30.0, 35.0, False, "NO_RULE_TRIGGERED"),
        (30.1, 35.0, False, "NO_RULE_TRIGGERED"),
        (29.9, 35.0, True, "NEEDS_URGENT_REVIEW"),
        (29.999, 35.0, True, "NEEDS_URGENT_REVIEW"),
        (30.001, 35.0, False, "NO_RULE_TRIGGERED"),
        (15.0, 35.0, True, "NEEDS_URGENT_REVIEW"),
        (0.0, 35.0, True, "NEEDS_URGENT_REVIEW"),
        # Geriatric Beers interaction (age >= 65 and (egfr < 45 or egfr is None))
        (44.9, 65.0, True, "NEEDS_URGENT_REVIEW"),
        (45.0, 65.0, False, "NO_RULE_TRIGGERED"),
        (45.1, 65.0, False, "NO_RULE_TRIGGERED"),
        (35.0, 64.9, False, "NO_RULE_TRIGGERED"),  # Not geriatric, eGFR > 30.0
    ],
)
def test_nitrofurantoin_renal_boundaries(engine, egfr, age, should_trigger, expected_status):
    """Stress-test exact eGFR boundary for Nitrofurantoin (threshold = 30.0 mL/min)."""
    payload = {
        "patient_context": {"age_years": age, "is_pregnant": False, "egfr_ml_min": egfr, "allergies": []},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [{"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    triggered_rules = [f["rule_id"] for f in report["findings"]]

    if should_trigger:
        assert "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30" in triggered_rules, (
            f"Expected Nitrofurantoin renal alert at eGFR {egfr}, age {age}"
        )
        assert report["status"] == expected_status
    else:
        assert "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30" not in triggered_rules, (
            f"Did not expect Nitrofurantoin renal alert at eGFR {egfr}, age {age}"
        )


@pytest.mark.parametrize(
    "drug_name,egfr,should_hold",
    [
        ("Gentamicin", None, True),
        ("Amikacin", None, True),
        ("Vancomycin", None, True),
        ("Colistin", None, True),
        ("Gentamicin", 80.0, False),
        ("Amikacin", 75.0, False),
        ("Vancomycin", 90.0, False),
        ("Colistin", 65.0, False),
        ("Amoxicillin", None, False),  # Not a narrow-therapeutic nephrotoxic target
    ],
)
def test_missing_egfr_hold_aminoglycosides_and_nephrotoxics(engine, drug_name, egfr, should_hold):
    """Stress-test missing eGFR hold for Gentamicin, Amikacin, and other nephrotoxics."""
    payload = {
        "patient_context": {"age_years": 45.0, "is_pregnant": False, "egfr_ml_min": egfr, "allergies": []},
        "indication_code": "SYN_PYELONEPHRITIS_UNCOMPLICATED",
        "prescription_lines": [{"drug_name": drug_name, "dose_text": "500 mg", "duration_days": 5}],
    }
    report = engine.evaluate(payload)
    triggered_rules = [f["rule_id"] for f in report["findings"]]

    if should_hold:
        assert "SAFETY.RENAL.MISSING_EGFR_HOLD" in triggered_rules
        assert report["status"] == "INCOMPLETE_DATA"
        assert any("eGFR" in gap for gap in report["input_gaps"])
    else:
        assert "SAFETY.RENAL.MISSING_EGFR_HOLD" not in triggered_rules


# ==============================================================================
# 3. Network Resilience Simulation & Circuit Breaker in ExtractionAdapter
# ==============================================================================


@pytest.fixture
def adapter():
    with patch("app.extraction.adapter.get_settings") as mock_settings:
        mock_settings.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        yield ExtractionAdapter()


@pytest.mark.asyncio
async def test_network_resilience_http_429_too_many_requests(adapter):
    """Verify immediate graceful fallback to local heuristics on HTTP 429 Too Many Requests."""
    mock_resp = httpx.Response(
        status_code=429,
        request=httpx.Request("POST", "https://generativelanguage.googleapis.com"),
        content=b'{"error": {"code": 429, "message": "Resource has been exhausted (rate limit)"}}',
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp):
        sample_doc = b"Patient: Mrs Sita, 35 yrs Female. Indication: Uncomplicated UTI. Rx: Cap Niftas 100mg BD x 5d."
        result = await adapter.extract_from_bytes(sample_doc, "text/plain")

        assert result is not None
        assert result["extraction_engine"] == "offline_heuristic_adapter"
        assert result["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
        assert result["patientContext"]["ageYears"] == 35.0
        assert result["patientContext"]["gender"] == "female"
        assert any(line["drugName"] == "Nitrofurantoin" for line in result["prescriptionLines"])
        assert adapter._cloud_disabled is True, "Circuit breaker should latch closed (_cloud_disabled=True)"


@pytest.mark.asyncio
async def test_network_resilience_http_500_internal_error(adapter):
    """Verify immediate graceful fallback to local heuristics on HTTP 500 Internal Error."""
    mock_resp = httpx.Response(
        status_code=500,
        request=httpx.Request("POST", "https://generativelanguage.googleapis.com"),
        content=b'{"error": {"code": 500, "message": "Internal Server Error"}}',
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp):
        sample_doc = b"Patient: Ramesh, 48 yrs Male. Cough and fever. Rx: Tab Augmentin 625mg BD x 5d."
        result = await adapter.extract_from_bytes(sample_doc, "text/plain")

        assert result is not None
        assert result["extraction_engine"] == "offline_heuristic_adapter"
        assert result["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
        assert any(line["drugName"] == "Amoxicillin-Clavulanate" for line in result["prescriptionLines"])
        assert adapter._cloud_disabled is True


@pytest.mark.asyncio
async def test_network_resilience_socket_timeout(adapter):
    """Verify immediate graceful fallback on socket / network timeout."""
    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ReadTimeout("Socket timeout after 4.0s"),
    ):
        sample_doc = b"Patient: Anita, 28 yrs Female. Ear pain. Rx: Tab Azithral 500mg OD x 3d."
        result = await adapter.extract_from_bytes(sample_doc, "text/plain")

        assert result is not None
        assert result["extraction_engine"] == "offline_heuristic_adapter"
        assert result["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
        assert any(line["drugName"] == "Azithromycin" for line in result["prescriptionLines"])
        assert adapter._cloud_disabled is True


@pytest.mark.asyncio
async def test_network_resilience_malformed_truncated_json(adapter):
    """Verify immediate graceful fallback when API returns truncated / invalid JSON."""
    truncated_payload = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": '{"patientContext": {"ageYears": 42.0, "gender": "female", "incomplete_json...'}
                    ]
                }
            }
        ]
    }
    mock_resp = httpx.Response(
        status_code=200,
        request=httpx.Request("POST", "https://generativelanguage.googleapis.com"),
        content=json.dumps(truncated_payload).encode("utf-8"),
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp):
        sample_doc = b"Patient: Deepa, 42 yrs Female. Burning micturition. Rx: Cap Niftas 100mg BD x 5 days."
        result = await adapter.extract_from_bytes(sample_doc, "text/plain")

        assert result is not None
        assert result["extraction_engine"] == "offline_heuristic_adapter"
        assert result["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
        assert any(line["drugName"] == "Nitrofurantoin" for line in result["prescriptionLines"])
        assert adapter._cloud_disabled is True


@pytest.mark.asyncio
async def test_network_resilience_circuit_breaker_latch_prevents_subsequent_network_calls(adapter):
    """Verify that once circuit breaker trips, subsequent requests bypass network entirely."""
    adapter._cloud_disabled = True  # Circuit breaker already latched

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        sample_doc = b"Patient: Vikram, 22 yrs Male. Pharyngitis. Rx: Cap Almox 500mg TID x 5d."
        result = await adapter.extract_from_bytes(sample_doc, "text/plain")

        assert result["extraction_engine"] == "offline_heuristic_adapter"
        mock_post.assert_not_called()  # Confirms zero network overhead on subsequent calls


# ==============================================================================
# 4. Deterministic Audit Core Reproducibility
# ==============================================================================


def _compute_audit_hash(report: dict) -> str:
    """Compute deterministic SHA-256 digest over normalized audit report."""
    serialized = json.dumps(report, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def test_audit_core_100_percent_reproducibility_across_iterations(engine):
    """Stress-test that audit report hashes are 100% deterministic over 100 repeated runs."""
    payloads = [
        # Case 1: Pediatric FQ violation
        {
            "patient_context": {"age_years": 8.0, "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []},
            "indication_code": "SYN_WATERY_DIARRHEA",
            "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "250 mg", "duration_days": 5}],
        },
        # Case 2: Banned FDC
        {
            "patient_context": {"age_years": 35.0, "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []},
            "indication_code": "SYN_CAP_MILD",
            "prescription_lines": [
                {"drug_name": "Cefixime + Azithromycin", "dose_text": "200 mg + 250 mg", "duration_days": 5}
            ],
        },
        # Case 3: Missing renal hold
        {
            "patient_context": {"age_years": 50.0, "is_pregnant": False, "egfr_ml_min": None, "allergies": []},
            "indication_code": "SYN_PYELONEPHRITIS_UNCOMPLICATED",
            "prescription_lines": [{"drug_name": "Gentamicin", "dose_text": "80 mg", "duration_days": 5}],
        },
        # Case 4: Clean guideline case
        {
            "patient_context": {"age_years": 32.0, "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []},
            "indication_code": "SYN_CAP_MILD",
            "prescription_lines": [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "duration_days": 5}],
        },
    ]

    for case_idx, payload in enumerate(payloads):
        hashes = set()
        for _ in range(100):
            report = engine.evaluate(payload)
            h = _compute_audit_hash(report)
            hashes.add(h)

        assert len(hashes) == 1, f"Case {case_idx + 1} produced non-deterministic output across 100 runs! Found: {hashes}"


def test_audit_core_multithreaded_concurrency_reproducibility(engine):
    """Verify that concurrent thread execution produces identical output to sequential execution."""
    payload = {
        "patient_context": {"age_years": 16.5, "is_pregnant": True, "egfr_ml_min": 25.0, "allergies": ["Penicillin"]},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [
            {"drug_name": "Ciprofloxacin", "dose_text": "500 mg", "duration_days": 5},
            {"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "duration_days": 5},
            {"drug_name": "Amoxicillin", "dose_text": "500 mg", "duration_days": 5},
        ],
    }

    baseline_hash = _compute_audit_hash(engine.evaluate(payload))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(engine.evaluate, payload) for _ in range(50)]
        results = [f.result() for f in futures]

    result_hashes = {_compute_audit_hash(r) for r in results}
    assert result_hashes == {baseline_hash}, "Thread race condition detected: divergent audit report hashes!"


def test_audit_core_key_order_invariance(engine):
    """Verify that scrambled dictionary key ordering in JSON payload does not affect evaluation."""
    payload_a = {
        "patient_context": {"age_years": 10.0, "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []},
        "indication_code": "SYN_WATERY_DIARRHEA",
        "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "250 mg", "duration_days": 5}],
    }
    payload_b = {
        "prescription_lines": [{"duration_days": 5, "dose_text": "250 mg", "drug_name": "Ciprofloxacin"}],
        "indication_code": "SYN_WATERY_DIARRHEA",
        "patient_context": {"allergies": [], "egfr_ml_min": 90.0, "is_pregnant": False, "age_years": 10.0},
    }

    report_a = engine.evaluate(payload_a)
    report_b = engine.evaluate(payload_b)

    assert _compute_audit_hash(report_a) == _compute_audit_hash(report_b)
