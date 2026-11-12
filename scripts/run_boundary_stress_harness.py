"""Standalone Empirical Boundary & Resilience Stress Test Harness.

Executes and logs quantitative empirical verification of:
1. Exact pediatric age boundaries (Ciprofloxacin 18.0 vs 17.9, Doxycycline 12.0 vs 11.9).
2. Exact renal impairment boundaries (Nitrofurantoin eGFR 30.0 vs 29.9, missing eGFR hold).
3. Network circuit breaker resilience (HTTP 429, 500, socket timeout, malformed truncated JSON).
4. Multi-iteration deterministic audit core reproducibility (SHA256 invariance).
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
import time
from unittest.mock import AsyncMock, patch

_ROOT = Path(__file__).resolve().parents[1]
_API_DIR = _ROOT / "services" / "api"
if str(_API_DIR) not in sys.path:
    sys.path.insert(0, str(_API_DIR))

import httpx  # noqa: E402
from app.config import Settings  # noqa: E402
from app.engine.engine import DeterministicAuditEngine  # noqa: E402
from app.extraction.adapter import ExtractionAdapter  # noqa: E402

RULES_FILE = _API_DIR / "app" / "rules_data" / "rules_v1.0.0.json"


def _hash(obj: dict) -> str:
    serialized = json.dumps(obj, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


async def run_stress_suite() -> int:
    print("=" * 80)
    print(" AMR SENTINEL AI — EMPIRICAL BOUNDARY & RESILIENCE STRESS TEST HARNESS")
    print("=" * 80)

    with open(RULES_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    engine = DeterministicAuditEngine(manifest)

    total_checks = 0
    passed_checks = 0

    # --------------------------------------------------------------------------
    # 1. Exact Age Boundaries
    # --------------------------------------------------------------------------
    print("\n[SECTION 1] Pediatric Age Threshold Boundary Stress Tests")
    print("-" * 80)
    print(f"{'Condition':<45} | {'Age':<8} | {'Expected Trigger':<16} | {'Actual Trigger':<16} | {'Status'}")
    print("-" * 80)

    age_tests = [
        # (name, drug, age, should_trigger, rule_id)
        ("Ciprofloxacin adult gate (exact)", "Ciprofloxacin", 18.0, False, "SAFETY.PED.FQ_UNDER_18"),
        ("Ciprofloxacin pediatric gate (exact)", "Ciprofloxacin", 17.9, True, "SAFETY.PED.FQ_UNDER_18"),
        ("Ciprofloxacin micro-upper (18.001)", "Ciprofloxacin", 18.001, False, "SAFETY.PED.FQ_UNDER_18"),
        ("Ciprofloxacin micro-lower (17.999)", "Ciprofloxacin", 17.999, True, "SAFETY.PED.FQ_UNDER_18"),
        ("Levofloxacin pediatric gate", "Levofloxacin", 17.9, True, "SAFETY.PED.FQ_UNDER_18"),
        ("Levofloxacin adult gate", "Levofloxacin", 18.0, False, "SAFETY.PED.FQ_UNDER_18"),
        ("Ofloxacin pediatric gate", "Ofloxacin", 17.9, True, "SAFETY.PED.FQ_UNDER_18"),
        ("Ofloxacin adult gate", "Ofloxacin", 18.0, False, "SAFETY.PED.FQ_UNDER_18"),
        ("Doxycycline pediatric gate (exact)", "Doxycycline", 11.9, True, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
        ("Doxycycline safe boundary (exact)", "Doxycycline", 12.0, False, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
        ("Doxycycline micro-upper (12.001)", "Doxycycline", 12.001, False, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
        ("Doxycycline micro-lower (11.999)", "Doxycycline", 11.999, True, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
        ("Minocycline pediatric gate", "Minocycline", 11.9, True, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
        ("Minocycline safe boundary", "Minocycline", 12.0, False, "SAFETY.PED.TETRACYCLINE_UNDER_18"),
    ]

    for label, drug, age, should_trigger, rule_id in age_tests:
        payload = {
            "patient_context": {"age_years": age, "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []},
            "indication_code": "SYN_ENTERIC_FEVER",
            "prescription_lines": [{"drug_name": drug, "dose_text": "500 mg", "duration_days": 5}],
        }
        res = engine.evaluate(payload)
        actual_trigger = rule_id in [f["rule_id"] for f in res["findings"]]
        ok = actual_trigger == should_trigger
        total_checks += 1
        if ok:
            passed_checks += 1
        status_str = "PASS" if ok else "FAIL"
        print(f"{label:<45} | {age:<8} | {str(should_trigger):<16} | {str(actual_trigger):<16} | {status_str}")

    # --------------------------------------------------------------------------
    # 2. Exact Renal Thresholds
    # --------------------------------------------------------------------------
    print("\n[SECTION 2] Renal Function Threshold Boundary Stress Tests")
    print("-" * 80)
    print(f"{'Condition':<45} | {'eGFR':<8} | {'Expected Trigger':<16} | {'Actual Trigger':<16} | {'Status'}")
    print("-" * 80)

    renal_tests = [
        # (label, drug, age, egfr, should_trigger, rule_id, exp_status)
        ("Nitrofurantoin safe threshold (exact 30.0)", "Nitrofurantoin", 35.0, 30.0, False, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NO_RULE_TRIGGERED"),
        ("Nitrofurantoin impaired (exact 29.9)", "Nitrofurantoin", 35.0, 29.9, True, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NEEDS_URGENT_REVIEW"),
        ("Nitrofurantoin micro-upper (30.001)", "Nitrofurantoin", 35.0, 30.001, False, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NO_RULE_TRIGGERED"),
        ("Nitrofurantoin micro-lower (29.999)", "Nitrofurantoin", 35.0, 29.999, True, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NEEDS_URGENT_REVIEW"),
        ("Nitrofurantoin geriatric (age 65, eGFR 44.9)", "Nitrofurantoin", 65.0, 44.9, True, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NEEDS_URGENT_REVIEW"),
        ("Nitrofurantoin geriatric safe (age 65, eGFR 45.0)", "Nitrofurantoin", 65.0, 45.0, False, "SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30", "NO_RULE_TRIGGERED"),
        ("Gentamicin with missing eGFR (null)", "Gentamicin", 45.0, None, True, "SAFETY.RENAL.MISSING_EGFR_HOLD", "INCOMPLETE_DATA"),
        ("Amikacin with missing eGFR (null)", "Amikacin", 45.0, None, True, "SAFETY.RENAL.MISSING_EGFR_HOLD", "INCOMPLETE_DATA"),
        ("Vancomycin with missing eGFR (null)", "Vancomycin", 45.0, None, True, "SAFETY.RENAL.MISSING_EGFR_HOLD", "INCOMPLETE_DATA"),
        ("Colistin with missing eGFR (null)", "Colistin", 45.0, None, True, "SAFETY.RENAL.MISSING_EGFR_HOLD", "INCOMPLETE_DATA"),
        ("Gentamicin with documented eGFR (80.0)", "Gentamicin", 45.0, 80.0, False, "SAFETY.RENAL.MISSING_EGFR_HOLD", "NO_RULE_TRIGGERED"),
        ("Amikacin with documented eGFR (75.0)", "Amikacin", 45.0, 75.0, False, "SAFETY.RENAL.MISSING_EGFR_HOLD", "NO_RULE_TRIGGERED"),
    ]

    for label, drug, age, egfr, should_trigger, rule_id, exp_status in renal_tests:
        payload = {
            "patient_context": {"age_years": age, "is_pregnant": False, "egfr_ml_min": egfr, "allergies": []},
            "indication_code": "SYN_PYELONEPHRITIS_UNCOMPLICATED" if "Gentamicin" in drug or "Amikacin" in drug or "Vancomycin" in drug or "Colistin" in drug else "SYN_UNCOMPLICATED_UTI",
            "prescription_lines": [{"drug_name": drug, "dose_text": "500 mg", "duration_days": 5}],
        }
        res = engine.evaluate(payload)
        actual_trigger = rule_id in [f["rule_id"] for f in res["findings"]]
        status_ok = res["status"] == exp_status if should_trigger else True
        ok = (actual_trigger == should_trigger) and status_ok
        total_checks += 1
        if ok:
            passed_checks += 1
        status_str = "PASS" if ok else "FAIL"
        egfr_display = str(egfr) if egfr is not None else "null"
        print(f"{label:<45} | {egfr_display:<8} | {str(should_trigger):<16} | {str(actual_trigger):<16} | {status_str}")

    # --------------------------------------------------------------------------
    # 3. Network Resilience Simulation in ExtractionAdapter
    # --------------------------------------------------------------------------
    print("\n[SECTION 3] Network Resilience & Fallback Circuit Breaker Tests")
    print("-" * 80)
    print(f"{'Simulation Scenario':<45} | {'Fallback Engine':<26} | {'Circuit Latched':<15} | {'Status'}")
    print("-" * 80)

    sample_doc = b"Patient: Mrs Sita, 35 yrs Female. Indication: Uncomplicated UTI. Rx: Cap Niftas 100mg BD x 5d."

    # Scenario A: HTTP 429
    with patch("app.extraction.adapter.get_settings") as ms:
        ms.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        ad = ExtractionAdapter()
        mock_resp_429 = httpx.Response(status_code=429, request=httpx.Request("POST", "http://test"))
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp_429):
            t0 = time.perf_counter()
            r429 = await ad.extract_from_bytes(sample_doc, "text/plain")
            dt429 = (time.perf_counter() - t0) * 1000
            ok429 = (
                r429["extraction_engine"] == "offline_heuristic_adapter"
                and r429["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
                and ad._cloud_disabled is True
            )
            total_checks += 1
            if ok429:
                passed_checks += 1
            print(f"{'HTTP 429 Too Many Requests (' + f'{dt429:.1f}ms)':<45} | {r429['extraction_engine']:<26} | {str(ad._cloud_disabled):<15} | {'PASS' if ok429 else 'FAIL'}")

    # Scenario B: HTTP 500
    with patch("app.extraction.adapter.get_settings") as ms:
        ms.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        ad = ExtractionAdapter()
        mock_resp_500 = httpx.Response(status_code=500, request=httpx.Request("POST", "http://test"))
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp_500):
            r500 = await ad.extract_from_bytes(sample_doc, "text/plain")
            ok500 = (
                r500["extraction_engine"] == "offline_heuristic_adapter"
                and ad._cloud_disabled is True
            )
            total_checks += 1
            if ok500:
                passed_checks += 1
            print(f"{'HTTP 500 Internal Server Error':<45} | {r500['extraction_engine']:<26} | {str(ad._cloud_disabled):<15} | {'PASS' if ok500 else 'FAIL'}")

    # Scenario C: Socket Timeout
    with patch("app.extraction.adapter.get_settings") as ms:
        ms.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        ad = ExtractionAdapter()
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, side_effect=httpx.ReadTimeout("Timeout")):
            r_to = await ad.extract_from_bytes(sample_doc, "text/plain")
            ok_to = (
                r_to["extraction_engine"] == "offline_heuristic_adapter"
                and ad._cloud_disabled is True
            )
            total_checks += 1
            if ok_to:
                passed_checks += 1
            print(f"{'Socket Read Timeout (4.0s simulated)':<45} | {r_to['extraction_engine']:<26} | {str(ad._cloud_disabled):<15} | {'PASS' if ok_to else 'FAIL'}")

    # Scenario D: Malformed / Truncated JSON
    with patch("app.extraction.adapter.get_settings") as ms:
        ms.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        ad = ExtractionAdapter()
        bad_json = {"candidates": [{"content": {"parts": [{"text": '{"patientContext": {"ageYears": 42.0,'}]}}]}
        mock_resp_json = httpx.Response(
            status_code=200,
            request=httpx.Request("POST", "http://test"),
            content=json.dumps(bad_json).encode("utf-8"),
        )
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp_json):
            r_bad = await ad.extract_from_bytes(sample_doc, "text/plain")
            ok_bad = (
                r_bad["extraction_engine"] == "offline_heuristic_adapter"
                and ad._cloud_disabled is True
            )
            total_checks += 1
            if ok_bad:
                passed_checks += 1
            print(f"{'Malformed / Truncated JSON Stream':<45} | {r_bad['extraction_engine']:<26} | {str(ad._cloud_disabled):<15} | {'PASS' if ok_bad else 'FAIL'}")

    # Scenario E: Latched Circuit Breaker Zero Network Overhead
    with patch("app.extraction.adapter.get_settings") as ms:
        ms.return_value = Settings(GEMINI_API_KEY="AIzaSyMockKeyForTestingResilience12345")
        ad = ExtractionAdapter()
        ad._cloud_disabled = True
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            t0 = time.perf_counter()
            r_latched = await ad.extract_from_bytes(sample_doc, "text/plain")
            dt_latched = (time.perf_counter() - t0) * 1000
            ok_latched = (
                mock_post.call_count == 0
                and r_latched["extraction_engine"] == "offline_heuristic_adapter"
            )
            total_checks += 1
            if ok_latched:
                passed_checks += 1
            print(f"{'Circuit Latched Call (' + f'{dt_latched:.2f}ms zero I/O)':<45} | {r_latched['extraction_engine']:<26} | {str(ad._cloud_disabled):<15} | {'PASS' if ok_latched else 'FAIL'}")

    # --------------------------------------------------------------------------
    # 4. Deterministic Audit Core Reproducibility (SHA256 Invariance)
    # --------------------------------------------------------------------------
    print("\n[SECTION 4] Deterministic Audit Core Reproducibility (SHA-256 Invariance)")
    print("-" * 80)
    print(f"{'Case Description':<40} | {'Iterations':<10} | {'Unique SHA256 Digests':<22} | {'Status'}")
    print("-" * 80)

    repro_cases = [
        ("Pediatric FQ Contraindication", {
            "patient_context": {"age_years": 8.0, "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []},
            "indication_code": "SYN_WATERY_DIARRHEA",
            "prescription_lines": [{"drug_name": "Ciprofloxacin", "dose_text": "250 mg", "duration_days": 5}],
        }),
        ("Banned FDC Regulatory Breach", {
            "patient_context": {"age_years": 35.0, "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []},
            "indication_code": "SYN_CAP_MILD",
            "prescription_lines": [{"drug_name": "Cefixime + Azithromycin", "dose_text": "200 mg + 250 mg", "duration_days": 5}],
        }),
        ("Nephrotoxic Missing eGFR Hold", {
            "patient_context": {"age_years": 50.0, "is_pregnant": False, "egfr_ml_min": None, "allergies": []},
            "indication_code": "SYN_PYELONEPHRITIS_UNCOMPLICATED",
            "prescription_lines": [{"drug_name": "Gentamicin", "dose_text": "80 mg", "duration_days": 5}],
        }),
        ("Penicillin Anaphylaxis Cross-Reaction", {
            "patient_context": {"age_years": 40.0, "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": ["Penicillin"]},
            "indication_code": "SYN_CAP_MILD",
            "prescription_lines": [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "duration_days": 5}],
        }),
        ("Clean Guideline-Concordant Regimen", {
            "patient_context": {"age_years": 32.0, "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []},
            "indication_code": "SYN_CAP_MILD",
            "prescription_lines": [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "duration_days": 5}],
        }),
    ]

    for label, payload in repro_cases:
        hashes = set()
        for _ in range(100):
            res = engine.evaluate(payload)
            hashes.add(_hash(res))
        ok_repro = len(hashes) == 1
        total_checks += 1
        if ok_repro:
            passed_checks += 1
        print(f"{label:<40} | {'100':<10} | {f'{len(hashes)} unique (deterministic)':<22} | {'PASS' if ok_repro else 'FAIL'}")

    # Concurrent multithreading test
    multi_payload = {
        "patient_context": {"age_years": 16.5, "is_pregnant": True, "egfr_ml_min": 25.0, "allergies": ["Penicillin"]},
        "indication_code": "SYN_UNCOMPLICATED_UTI",
        "prescription_lines": [
            {"drug_name": "Ciprofloxacin", "dose_text": "500 mg", "duration_days": 5},
            {"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "duration_days": 5},
            {"drug_name": "Amoxicillin", "dose_text": "500 mg", "duration_days": 5},
        ],
    }
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(engine.evaluate, multi_payload) for _ in range(50)]
        c_hashes = {_hash(f.result()) for f in futures}
    ok_conc = len(c_hashes) == 1
    total_checks += 1
    if ok_conc:
        passed_checks += 1
    print(f"{'50 Concurrent Worker Threads':<40} | {'50':<10} | {f'{len(c_hashes)} unique (race-free)':<22} | {'PASS' if ok_conc else 'FAIL'}")

    print("\n" + "=" * 80)
    print(f" TOTAL STRESS CHECKS EXECUTED : {total_checks}")
    print(f" TOTAL STRESS CHECKS PASSED   : {passed_checks}")
    print(f" EMPIRICAL INTEGRITY RATE     : {100.0 * passed_checks / total_checks:.2f}%")
    print(f" VERDICT                      : {'APPROVE (100% PASS)' if passed_checks == total_checks else 'REQUEST_CHANGES'}")
    print("=" * 80)

    return 0 if passed_checks == total_checks else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_stress_suite()))
