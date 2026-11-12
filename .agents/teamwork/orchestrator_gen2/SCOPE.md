# Scope: AMR Sentinel AI Agent Enhancement & Calibration (Milestones 4 & 5)

## Architecture
- **Two-Layer Safety Architecture**:
  1. Assistive Intake & Decision-Support Layer (`services/api/app/extraction/`, `services/api/app/services/`):
     - Unstructured prescription extraction with confidence scoring.
     - AMR knowledge retrieval and clinical guidance.
     - Always outputs `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`.
     - Supports Gemini API when available, local offline heuristics when offline.
  2. Deterministic Clinical Audit Core (`services/api/app/engine/`):
     - Pure Python AST isolated: ZERO network, ZERO AI/LLM, ZERO database, ZERO subprocess.
     - 11 clinical rules across 4 safety tiers against `rules_v1.0.0.json`.
     - Authoritative, unaltered, non-bypassed.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Benchmark Test Split & Evaluation Harness | 30 curated clinical cases in `benchmark_cases.json`, evaluation runner `scripts/evaluate_agent.py`. | M1 | Survey |
| 2 | Local Offline Fallback & Brand Resolution Engine | 405-entry brand alias lookup, posology conversion, frequency translation in `ExtractionAdapter`. | M2 | Survey |
| 3 | Few-Shot AI Agent Intake Calibration & Knowledge | Few-shot exemplars in adapter and `AMRKnowledgeService` indexing WHO AWaRe & ICMR STG. | M3 | Survey |
| 4 | E2E Evaluation & Non-Regression Verification | `services/api/tests/test_benchmark_evaluation.py` pytest integration, baseline comparison, `scripts/test.ps1` pass. | M4 | Survey |
| 5 | Adversarial Hardening & Forensic Audit | Stress testing (corrupt inputs, boundary ages, unknown brands) and independent forensic audit. | M5 | Survey |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Benchmark Test Split & Evaluation Harness | Benchmark cases (`benchmark_cases.json`), evaluation runner (`scripts/evaluate_agent.py`), baseline results. | none | DONE |
| M2 | Local Offline Fallback & Brand Resolution Engine | `ExtractionAdapter` offline heuristics, 400+ brand mappings, frequency/unit translation. | M1 | DONE |
| M3 | Few-Shot Prompt Calibration & AMR Knowledge Grounding | Few-shot prompt templates, `AMRKnowledgeService` for resistance evidence and guideline retrieval. | M2 | DONE |
| M4 | E2E Evaluation & Non-Regression Verification | Implement `test_benchmark_evaluation.py` for pytest integration; run evaluation comparing against baseline; verify zero regressions via `pytest services/api/tests` and `scripts/test.ps1`. | M1, M2, M3 | DONE |
| M5 | Adversarial Coverage Hardening & Forensic Audit | Multi-challenger stress testing, forensic integrity checks (AST checks, static analysis, anti-cheating verification). | M4 | DONE |

## Interface Contracts
- Same as defined in PROJECT.md:
  - `ExtractionAdapter.extract_from_bytes` -> dict with `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`, field confidences, and offline fallback.
  - `AMRKnowledgeService.get_clinical_guidance` -> dict with AWaRe category, resistance evidence, and ICMR STG recommendations.
  - `DeterministicAuditEngine.evaluate` -> pure deterministic audit report. AST isolated.
