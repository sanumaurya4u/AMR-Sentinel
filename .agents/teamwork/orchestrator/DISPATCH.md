## 2026-11-09T20:41:38Z
Train and enhance the AI agent in this project for improved clinical output using the referenced datasets in c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets for a capability showcase.

Working directory: c:\Seva Sankalp Hackathon\AMR Sentinel
Integrity mode: demo
The team must NOT: copy code from existing open-source projects for core logic, or run external scripts or delegate execution to other tools.

## Requirements

### R1. AI Agent Enhancement & Calibration
Train, tune, or enhance the AI agent using the datasets in `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets` (e.g., calibrating prescription intake extraction prompts/few-shot examples or grounding knowledge retrieval on AMR packages), allowing the team to select the optimal approach based on the existing project architecture.

### R2. Clinical Safety Guardrails
Preserve the two-layer safety architecture: the AI agent functions strictly as an assistive intake/decision-support layer producing editable drafts or guidance, while the deterministic clinical audit core remains unaltered, non-bypassed, and authoritative.

### R3. Infrastructure & Fallback
Permit cloud API calls using the configured `GEMINI_API_KEY` from environment variables, while ensuring functional local offline fallback when API access or credentials are not present.

## Verification Resources

- Datasets: `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets` (including `AMR_ANALYZED_DATA_PACKAGE` and `amr_knowledge_base`)
- Existing test suites: `services/api/tests` and `scripts/test.ps1`

## Acceptance Criteria

### Automated Evaluation & Quality
- [ ] An automated evaluation script executes against a benchmark test split derived from `data_sets` and verifies improved output quality or extraction accuracy over baseline.
- [ ] Agent execution succeeds with cloud API calls when `GEMINI_API_KEY` is provided, and gracefully degrades to local fallback heuristics when unavailable.

### Architecture & Non-regression
- [ ] The deterministic clinical rules engine remains intact without external LLM dependencies introduced into the deterministic core.
- [ ] All existing test suites pass via `pytest services/api/tests` and `scripts/test.ps1` without regressions.
