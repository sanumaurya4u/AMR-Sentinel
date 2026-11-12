# Dispatch: Worker M4 — Iteration 2 (Remediation of Reviewer Findings)

## Task Objective
Remediate the specific mathematical and token extraction defects identified by `reviewer_m4_1` in Milestone 4:
1. Fix `compute_token_f1` in `scripts/evaluate_agent.py` to use multiset intersection (`collections.Counter`), strictly bounding $Precision, Recall, F1 \in [0.0, 1.0]$.
2. Fix compound drug over-extraction in `services/api/app/extraction/adapter.py` by masking matched tokens (`lowered = lowered.replace(token, " " * len(token))`) to eliminate spurious extra lines for FDC combinations like `Cefixime + Azithromycin`.
3. Add a unit test in `services/api/tests/test_benchmark_evaluation.py` explicitly asserting that duplicate prediction tokens never produce Recall > 1.0 or F1 > 1.0.
4. Re-record baseline / update benchmark evaluation comparison so the output displays mathematically valid scores ($P, R, F1 \le 100.0\%$).
5. Run full test suites:
   - `.venv\Scripts\ruff.exe check services/api`
   - `.venv\Scripts\pytest.exe services/api/tests -v`
   - `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`
   - `.venv\Scripts\python.exe scripts/evaluate_agent.py --cases services/api/tests/data/benchmark_cases.json --compare-baseline`

## Working Directory
`c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\worker_m4_2\`

## Input Artifacts
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md` (MANDATORY)
- `c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md`
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\reviewer_m4_1\handoff.md` (Contains exact code snippets and rationale)
- `scripts/evaluate_agent.py`
- `services/api/app/extraction/adapter.py`
- `services/api/tests/test_benchmark_evaluation.py`

## Exclusive Write Ownership
- `scripts/evaluate_agent.py`
- `services/api/app/extraction/adapter.py`
- `services/api/tests/test_benchmark_evaluation.py`
- `services/api/tests/data/baseline_evaluation_results.json`

## 2026-11-11T16:49:13Z
You are worker_m4_2, a teamwork_worker implementing Milestone 4 Iteration 2 (Remediation) for AMR Sentinel AI.
Working directory: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\worker_m4_2\
Parent orchestrator conversation ID: 993a1695-e727-4162-821a-1cc5b88a100b
Task: Fix compute_token_f1, fix compound drug over-extraction in adapter.py, update test_benchmark_evaluation.py, re-record baseline evaluation data, run full quality gates and write handoff report.
