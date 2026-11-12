# Project: AMR Sentinel AI Agent Enhancement & Calibration

## Architecture
- **Two-Layer Safety Architecture**:
  1. **Assistive Intake & Decision-Support Layer (`services/api/app/extraction/`, `services/api/app/services/`)**:
     - Extracts unstructured prescription documents into structured draft JSON with field confidence ratings.
     - Grounds on AMR knowledge packages and ICMR STG guidelines for clinical context and resistance guidance.
     - Always emits `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`.
     - Operates with live Gemini API when `GEMINI_API_KEY` is present; degrades gracefully to local offline heuristics when absent or invalid.
  2. **Deterministic Clinical Audit Core (`services/api/app/engine/`)**:
     - Strict AST import isolation: ZERO network, ZERO AI/LLM SDKs, ZERO database, ZERO subprocess.
     - Evaluates 11 clinical rules across 4 safety tiers against immutable `rules_v1.0.0.json`.
     - Authoritative, unaltered, non-bypassed. Only evaluates clinician-confirmed facts.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Benchmark Test Split & Evaluation Harness | Curated test split of 20-30 clinical cases from `data_sets` and automated evaluation script computing field accuracy, drug Precision/Recall/F1, brand resolution, indication match, and audit concordance with baseline comparison. | M1 | Survey (explorer_2 & 3) |
| 2 | Local Offline Fallback & Brand Resolution Engine | Upgraded offline extractor in `ExtractionAdapter` utilizing 405-entry brand alias lookup, gram-to-mg conversion, clinical frequency translation, and condition keyword classification. | M2 | Survey (explorer_1 & 2) |
| 3 | Few-Shot AI Agent Intake Calibration | Calibrated prompt template for `ExtractionAdapter._extract_with_gemini` incorporating authentic Indian clinical few-shot exemplars, canonical `SYN_` condition codes, and brand-to-generic mappings. | M3 | Survey (explorer_1 & 2) |
| 4 | Assistive AMR Knowledge Retrieval Grounding | Lightweight knowledge retrieval service (`services/api/app/services/amr_knowledge.py`) indexing `amr_knowledge_base`, `who_aware_antibiotics.csv`, and `guidelines.csv` for resistance evidence and ICMR STG guidance strictly in the draft layer. | M3 | Survey (explorer_1 & 2) |
| 5 | Deterministic Safety Core Non-Regression | Verification that AST import isolation remains intact, deterministic core rules remain unaltered, and all existing 24 tests and `scripts/test.ps1` pass without regression. | M4 | Survey (explorer_1 & 3) |
| 6 | Adversarial Hardening & Forensic Audit | Stress testing edge cases (corrupted input, extreme dosages, unknown brands, boundary ages) and independent forensic audit verifying zero cheating/hardcoding and authentic model execution. | M5 | Survey (all) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Benchmark Test Split & Evaluation Harness | Curate 20-30 case benchmark split in `services/api/tests/data/benchmark_cases.json`; build `scripts/evaluate_agent.py` and `services/api/tests/test_benchmark_evaluation.py`; record baseline evaluation metrics. | none | PLANNED |
| M2 | Local Offline Fallback & Brand Resolution Engine | Upgrade `_extract_with_local_heuristics` in `ExtractionAdapter` using 405 brand aliases, gram-to-mg unit conversion, frequency regex, and condition classification; verify offline execution without API key. | M1 | PLANNED |
| M3 | Few-Shot Prompt Calibration & AMR Knowledge Grounding | Calibrate `_extract_with_gemini` in `ExtractionAdapter` with few-shot exemplars; implement assistive knowledge retrieval (`amr_knowledge.py`) referencing `amr_knowledge_base` and WHO AWaRe data. | M2 | PLANNED |
| M4 | E2E Evaluation & Non-Regression Verification | Execute automated evaluation against benchmark test split; verify quantitative improvement over baseline; verify live API and offline fallback modes; run `scripts/test.ps1` to ensure zero regressions across all 24 tests. | M1, M2, M3 | PLANNED |
| M5 | Adversarial Coverage Hardening & Forensic Audit | Adversarial verification with Challengers; run full forensic integrity checks (AST checks, static analysis, execution tracing, zero cheating/hardcoding); final victory gate. | M4 | PLANNED |

## Interface Contracts
### `ExtractionAdapter` ↔ API Route (`POST /v1/extractions`)
- Method: `async def extract_from_bytes(file_bytes: bytes, mime_type: str, filename: str) -> dict[str, Any]`
- Input: `file_bytes` (up to 10MB), `mime_type` (image/pdf/text), `filename` (str)
- Output:
  ```json
  {
    "patientContext": {
      "ageYears": 34.0,
      "gender": "female",
      "isPregnant": false,
      "egfrMlMin": 95.0,
      "allergies": []
    },
    "indicationCode": "SYN_CAP_MILD",
    "prescriptionLines": [
      {
        "drugName": "Amoxicillin",
        "doseText": "500 mg",
        "frequencyText": "Three times daily (TID)",
        "durationDays": 5
      }
    ],
    "fieldConfidence": { "ageYears": "high", "drugs": "high" },
    "extraction_engine": "gemini_2.5_flash" | "offline_heuristic_adapter",
    "clinical_status": "UNTRUSTED_DRAFT_PENDING_CONFIRMATION",
    "disclaimer": "Assistive extraction only. Clinician must verify all fields prior to clinical audit."
  }
  ```
- Error behavior: Catches any LLM or network exception; falls back to offline heuristic; never throws 500.

### `AMRKnowledgeService` ↔ Assistive Guidance
- Module: `services/api/app/services/amr_knowledge.py`
- Method: `get_clinical_guidance(drug_name: str, indication_code: str | None) -> dict[str, Any]`
- Output:
  ```json
  {
    "drug_name": "Ciprofloxacin",
    "aware_class": "Watch",
    "is_banned_fdc": false,
    "resistance_evidence": "E. coli resistance to fluoroquinolones exceeds 75% in Indian surveillance data.",
    "guideline_recommendation": "First-line empiric treatment for uncomplicated UTI is Nitrofurantoin 100mg BD x 5d.",
    "evidence_citations": ["EVID_WHO_AWARE_2023", "ICMR STG UTI 2022"]
  }
  ```

### Deterministic Audit Core ↔ Confirmed Prescription
- Unaltered contract: `DeterministicAuditEngine.evaluate(audit_request: dict) -> dict`
- Input: Clinician-confirmed `AuditRequest`
- Output: `AuditReport` with deterministic status (`NEEDS_URGENT_REVIEW`, `NEEDS_REVIEW`, `INCOMPLETE_DATA`, `NO_RULE_TRIGGERED`)
- Pure Python AST isolation: No network, No AI, No DB, No subprocess in `app/engine/`.

## Code Layout
- `services/api/app/extraction/adapter.py`: AI intake extraction adapter (Gemini API + local fallback).
- `services/api/app/services/amr_knowledge.py`: Assistive AMR knowledge retrieval service.
- `services/api/app/engine/`: Deterministic clinical audit core (IMMUTABLE, AST ISOLATED).
- `services/api/app/rules_data/rules_v1.0.0.json`: Clinical rules manifest (IMMUTABLE).
- `services/api/tests/data/benchmark_cases.json`: Benchmark evaluation dataset derived from `data_sets`.
- `services/api/tests/test_benchmark_evaluation.py`: Pytest evaluation suite against benchmark split.
- `scripts/evaluate_agent.py`: Standalone automated evaluation & baseline comparison script.
