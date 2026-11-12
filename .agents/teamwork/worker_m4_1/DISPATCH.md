# Dispatch: Worker M4

## Task Objective
Implement `services/api/tests/test_benchmark_evaluation.py` for comprehensive pytest integration of the benchmark evaluation harness, run the evaluation script `scripts/evaluate_agent.py`, and run the full test suite (`pytest services/api/tests` and `powershell -File scripts/test.ps1`) to verify that all tests pass with zero regressions and demonstrate improved benchmark metrics over baseline.

## Working Directory
`c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\worker_m4_1\`

## Input Artifacts to Read First
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md` (MANDATORY)
- `c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md`
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\spec_miner_m1_3\test_infra_spec.md`
- `services/api/tests/data/benchmark_cases.json`
- `services/api/tests/data/baseline_evaluation_results.json`
- `scripts/evaluate_agent.py`
- `services/api/app/extraction/adapter.py`
- `services/api/app/services/amr_knowledge.py`

## Exclusive File Ownership
`services/api/tests/test_benchmark_evaluation.py`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Requirements
1. Implement `services/api/tests/test_benchmark_evaluation.py`:
   - Test benchmark cases data integrity and schema (all 30 cases have valid structure: id, document_text, ground_truth, expected_audit).
   - Test evaluation metrics calculation (token F1, demographic accuracies, indication match, audit concordance).
   - Test `ExtractionAdapter` offline extraction on benchmark cases, verifying that `clinical_status` is always `UNTRUSTED_DRAFT_PENDING_CONFIRMATION` and `extraction_engine` is `offline_heuristic_adapter` when offline.
   - Test AMR knowledge service lookup (`services/api/app/services/amr_knowledge.py`) for AWaRe classes, banned FDC identification, and guideline recommendations.
   - Test that evaluation metrics achieve or exceed baseline quality metrics.
   - Keep tests fast and self-contained (no external network calls).
2. Execute `scripts/evaluate_agent.py` (via `.venv\Scripts\python.exe scripts/evaluate_agent.py --cases services/api/tests/data/benchmark_cases.json`) and verify extraction accuracy, demographic accuracy, indication accuracy, and audit concordance.
3. Run linter and full test suite:
   - `.venv\Scripts\ruff.exe check services/api`
   - `.venv\Scripts\pytest.exe services/api/tests -v`
   - `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`
4. Document all commands, test results, passing test counts, and verified metrics in `handoff.md`.

## 2026-11-10T12:14:40Z
Implement `services/api/tests/test_benchmark_evaluation.py` for comprehensive pytest integration:
- Benchmark case dataset schema and integrity validation (30 cases, all required keys).
- Evaluation metric formulation tests (token precision/recall/F1, demographics, indication match, concordance).
- Offline extraction validation on benchmark cases: verify `clinical_status` is ALWAYS `UNTRUSTED_DRAFT_PENDING_CONFIRMATION`, `extraction_engine` is `offline_heuristic_adapter` when offline.
- AMR knowledge service validation: AWaRe classification, banned FDC lookup, resistance data, and clinical guidance.
- Quality benchmark comparison: assert that current evaluation against the 30 benchmark cases meets or exceeds baseline performance without regressions.
Run evaluation script and quality gates.
