# Dispatch: Challenger 2 — Milestone 5 Boundary & Resilience Stress Testing

## Task Objective
Empirically stress-test clinical safety boundary thresholds and offline circuit-breaker resilience:
1. Exact age boundaries:
   - Exactly 18.0 years with Ciprofloxacin (must NOT trigger pediatric contraindication).
   - Exactly 17.9 years with Ciprofloxacin (MUST trigger pediatric contraindication `SAFETY.PED.FQ_UNDER_18`).
   - Exactly 12.0 years with Doxycycline (must NOT trigger `SAFETY.PED.TETRACYCLINE_UNDER_18`).
   - Exactly 11.9 years with Doxycycline (MUST trigger `SAFETY.PED.TETRACYCLINE_UNDER_18`).
2. Exact renal thresholds:
   - Exactly eGFR 30.0 mL/min with Nitrofurantoin (must NOT trigger `SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`).
   - Exactly eGFR 29.9 mL/min with Nitrofurantoin (MUST trigger `SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`).
   - eGFR null with nephrotoxic aminoglycosides (Gentamicin/Amikacin) -> triggers `INCOMPLETE_DATA` hold.
3. Network / Cloud resilience simulation:
   - HTTP 429 Too Many Requests, HTTP 500 Internal Error, socket timeout, malformed truncated JSON.
   - Verify immediate, seamless fallback to local heuristics without latency stall or crash.
4. Downstream audit determinism & full test suite clearance (`scripts/test.ps1`).

## Working Directory
`c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\challenger_m5_2\`

## Input Artifacts
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md` (MANDATORY)
- `c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md`
- `services/api/app/extraction/adapter.py`
- `services/api/app/engine/`
- `services/api/tests/`

## Requirements
- Execute an empirical stress testing suite.
- Run `pytest services/api/tests` and `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`.
- Document all tested boundaries, observed behaviors, and verdict (`APPROVE` or `REQUEST_CHANGES`) in `handoff.md`.

## 2026-11-11T17:12:06Z
Received dispatch from parent (993a1695-e727-4162-821a-1cc5b88a100b):
MANDATORY FIRST STEP:
Read c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md before starting work.
Also read:
- c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md
- c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\challenger_m5_2\DISPATCH.md
- services/api/app/extraction/adapter.py
- services/api/app/engine/

TASKS:
1. Write and run an empirical boundary & resilience stress test harness:
   - Exact age thresholds: age 18.0 vs 17.9 for Ciprofloxacin (adult vs pediatric gate); age 12.0 vs 11.9 for Doxycycline (pediatric gate).
   - Exact renal thresholds: eGFR 30.0 vs 29.9 mL/min for Nitrofurantoin; null eGFR for Gentamicin/Amikacin (missing data hold).
   - Network resilience: HTTP 429, HTTP 500, socket timeout, malformed truncated JSON — assert immediate zero-crash fallback to local heuristics.
   - Deterministic audit core reproducibility: verify downstream audit reports are 100% deterministic and reproducible across repeated runs.
2. Run the complete test suite:
   `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`
3. Document all boundary evaluations, resilience tests, outputs, and your verdict (`APPROVE` or `REQUEST_CHANGES`) in `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\challenger_m5_2\handoff.md`.
4. Send a completion message via send_message to recipient 993a1695-e727-4162-821a-1cc5b88a100b.

