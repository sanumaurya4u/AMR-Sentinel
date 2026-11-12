## 2026-11-10T12:06:24Z

Sender: 19bae494-7a09-440b-b1f6-003a695dbb45
Priority: MESSAGE_PRIORITY_HIGH

Content:
Train and enhance the AI agent in this project for improved clinical output using the referenced datasets in c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets for a capability showcase.

Working directory: c:\Seva Sankalp Hackathon\AMR Sentinel
Integrity mode: demo
The team must NOT: copy code from existing open-source projects for core logic, or run external scripts or delegate execution to other tools.

## Requirements
### R1. AI Agent Enhancement & Calibration
Train, tune, or enhance the AI agent using the datasets in c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets (e.g., calibrating prescription intake extraction prompts/few-shot examples or grounding knowledge retrieval on AMR packages), allowing the team to select the optimal approach based on the existing project architecture.

### R2. Clinical Safety Guardrails
Preserve the two-layer safety architecture: the AI agent functions strictly as an assistive intake/decision-support layer producing editable drafts or guidance, while the deterministic clinical audit core remains unaltered, non-bypassed, and authoritative.

### R3. Infrastructure & Fallback
Permit cloud API calls using the configured GEMINI_API_KEY from environment variables, while ensuring functional local offline fallback when API access or credentials are not present.

## Acceptance Criteria
- An automated evaluation script executes against a benchmark test split derived from data_sets and verifies improved output quality or extraction accuracy over baseline.
- Agent execution succeeds with cloud API calls when GEMINI_API_KEY is provided, and gracefully degrades to local fallback heuristics when unavailable.
- The deterministic clinical rules engine remains intact without external LLM dependencies introduced into the deterministic core.
- All existing test suites pass via pytest services/api/tests and scripts/test.ps1 without regressions.

---
## Resume / Handover Instructions
Working directory: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\orchestrator_gen2\
Authoritative user request file: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md
Project specification: c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md

Previous session progress:
- Initial survey (Phase 0) completed and documented in PROJECT.md.
- Datasets surveyed: `services/api/tests/data/benchmark_cases.json` (30 curated clinical cases from `data_sets`).
- Benchmark evaluation runner: `scripts/evaluate_agent.py` and `services/api/tests/data/baseline_evaluation_results.json` established.
- Offline fallback & brand mappings: `services/api/app/extraction/adapter.py` enhanced with 400+ brand mappings, posology conversions, and indication classification with fast fallback.
- AMR Knowledge service: `services/api/app/services/amr_knowledge.py` indexing WHO AWaRe, ICMR STG 2022 guidelines, and resistance data.

Next steps for this orchestrator:
- Resume from Milestone 4 and Milestone 5:
  1. Complete Milestone 4: Write `services/api/tests/test_benchmark_evaluation.py` for comprehensive pytest integration, execute evaluation, and verify that all test suites pass via `pytest services/api/tests` and `scripts/test.ps1` with zero regressions.
  2. Complete Milestone 5: Adversarial verification (stress testing edge cases, corrupt inputs, boundary ages, unknown brands) and forensic audit (AST checks, static analysis, execution tracing, zero cheating/hardcoding).
- You are a pure orchestrator. NEVER write code directly. Dispatch specialists (workers, reviewers, challengers, forensic auditor).
- Report progress in your working directory `progress.md` and `BRIEFING.md`.
- When all requirements and acceptance criteria are satisfied, report completion so Victory Audit can be initiated.


## 2026-11-10T12:37:51Z

Sender: 19bae494-7a09-440b-b1f6-003a695dbb45
Priority: MESSAGE_PRIORITY_HIGH

Content:
Liveness Check Nudge: Please update your progress.md and BRIEFING.md with recent milestone progress (including worker_m4_1 test creation in services/api/tests/test_benchmark_evaluation.py).
