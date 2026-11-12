"""Adversarial stress-testing script for reviewer_m4_2."""
import asyncio
import json
import sys
from pathlib import Path

# Add services/api
sys.path.insert(0, str(Path("services/api").resolve()))

from app.engine.engine import DeterministicAuditEngine
from app.extraction.adapter import ExtractionAdapter


async def run_stress_test():
    adapter = ExtractionAdapter()
    manifest_path = Path("services/api/app/rules_data/rules_v1.0.0.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    engine = DeterministicAuditEngine(manifest)

    scenarios = [
        ("Empty payload", b"", "text/plain"),
        ("Whitespace only", b"   \n\t\r   ", "text/plain"),
        ("Corrupted binary bytes", b"\x00\xff\xfe\x01\x02\x03\x80\x90\xaa\xbb", "application/octet-stream"),
        ("Extreme geriatric age 150", b"Patient: Ram, 150 yrs Male. Rx: Tab Cifran 500mg BD x 5d", "text/plain"),
        ("Pediatric neonate age 0", b"Neonate Baby, 0 yrs Male. Rx: Tab Cifran 100mg BD x 5d", "text/plain"),
        ("Contradictory pregnant male", b"Patient: Mr. Suresh, 30 yrs Male, Pregnant. Rx: Tab Doxicip 100mg BD x 5d", "text/plain"),
        ("Severe zero eGFR renal failure", b"Patient: Sita, 50 yrs Female, eGFR: 0. Rx: Cap Martifur 100mg BD x 5d", "text/plain"),
        ("Massive dose and duration", b"Patient: Anita, 35 yrs Female. Rx: Tab Augmentin 50000mg BD x 50d", "text/plain"),
        ("Unknown novel drug", b"Patient: Ravi, 25 yrs Male. Rx: Tab WonderDrugZ 999mg OD x 3d", "text/plain"),
        ("Mixed case and noisy punctuation", b"!!!PATIENT: 45 YR FEMALE; eGFR=22 mL/min; RX: Cap NIFTAS 100mg bid x 7 days...", "text/plain"),
    ]

    print("==================================================================")
    print("  ADVERSARIAL STRESS TEST RESULTS")
    print("==================================================================")
    all_passed = True
    for label, payload, mime in scenarios:
        try:
            extracted = await adapter.extract_from_bytes(payload, mime, "stress_case.txt")
            
            # Clinical safety invariant checks
            assert extracted["clinical_status"] == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION", (
                f"{label}: Violated clinical_status invariant!"
            )
            assert extracted["extraction_engine"] == "offline_heuristic_adapter"
            assert "disclaimer" in extracted and len(extracted["disclaimer"]) > 0
            assert isinstance(extracted["patientContext"], dict)
            assert isinstance(extracted["prescriptionLines"], list)
            assert len(extracted["prescriptionLines"]) > 0

            # Deterministic engine execution on extracted draft
            audit = engine.evaluate(extracted)
            assert "status" in audit
            assert audit["status"] in {"NEEDS_URGENT_REVIEW", "NEEDS_REVIEW", "INCOMPLETE_DATA", "NO_RULE_TRIGGERED"}
            
            print(f"[PASS] {label:35} -> Engine: {extracted['extraction_engine']:26} | Audit: {audit['status']:20} | Findings: {len(audit['findings'])}")
        except Exception as e:
            print(f"[FAIL] {label:35} -> Error: {e}")
            all_passed = False

    print("==================================================================")
    print(f"Overall Stress Test Status: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_stress_test())
    sys.exit(0 if success else 1)
