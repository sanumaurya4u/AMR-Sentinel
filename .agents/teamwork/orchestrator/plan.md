# Plan: AI Agent Enhancement & Calibration

## Phase 0: Survey & Discovery (Current)
- Dispatch 3 Explorers in parallel to survey:
  1. `explorer_arch`: Codebase architecture, AI agent implementation, prompt structure, local fallback heuristics, and integration points.
  2. `explorer_data`: Datasets in `data_sets` (`AMR_ANALYZED_DATA_PACKAGE`, `amr_knowledge_base`, formats, schemas, benchmark extraction opportunities).
  3. `explorer_tests`: Existing test suites in `services/api/tests`, `scripts/test.ps1`, deterministic clinical audit core rules and verification boundaries.
- Synthesize findings into `PROJECT.md` with full Feature Inventory, module boundaries, and milestone roadmap.

## Phase 1: Test Infrastructure & Baseline Benchmark
- Create E2E / automated evaluation benchmark split derived from `data_sets`.
- Run baseline evaluation to record pre-enhancement performance.
- Verify deterministic core test non-regression baseline.

## Phase 2: AI Agent Enhancement & Grounding
- Calibrate intake extraction prompts/few-shot examples using dataset split.
- Ground knowledge retrieval on AMR packages and guidelines.
- Ensure robust fallback to local heuristics when `GEMINI_API_KEY` is absent.
- Ensure clinical audit core remains unaltered and authoritative.

## Phase 3: Automated Evaluation, Review, Adversarial Hardening & Audit
- Run evaluation script against benchmark test split; verify improved accuracy.
- Run `pytest services/api/tests` and `scripts/test.ps1` to ensure zero regressions.
- Independent Reviewers, Challengers, and Forensic Auditor verification.
- Final victory audit and report to parent.
