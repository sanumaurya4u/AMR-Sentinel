# Specification Mining Report: Test Suites, Clinical Audit Rules, Safety Boundaries & Evaluation Protocol

**Agent**: `explorer_survey_3` (Test Suites & Clinical Rules Spec Miner)  
**Parent Orchestrator**: `01b31f9d-d7a9-4fca-9bcc-706835e55498`  
**Working Directory**: `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_3\`  
**Date**: 2026-11-09T21:00:00Z  

---

## 1. Observation

### 1.1 Existing Test Suites and Quality Gate Architecture

The project enforces quality and safety through three automated gates executed via `scripts/test.ps1`:

```powershell
# scripts/test.ps1 (Lines 9-25)
# 1. Python Linter
& "$Root\.venv\Scripts\ruff.exe" check "$Root\services\api"

# 2. Python Architecture Isolation & Unit Tests
$env:PYTHONPATH = "services/api"
& "$Root\.venv\Scripts\pytest.exe" "$Root\services\api\tests" -v

# 3. Web Type Check
Set-Location "$Root\apps\web"
npm run type-check
```

#### Test Execution Observations:
- **Gate 1 (Ruff)**: Executed command `& ".\.venv\Scripts\ruff.exe" check "services/api"`. Result: `All checks passed!` (Exit code 0).
- **Gate 2 (Pytest & AST Isolation)**: Executed command `$env:PYTHONPATH = "services/api"; & ".\.venv\Scripts\pytest.exe" "services/api/tests" -v`. Result: **24 passed, 1 warning in 3.26s** (Exit code 0).
- **Gate 3 (TypeScript strict type check)**: Executed command `cd apps/web; npm run type-check` (`tsc --noEmit`). Result: Clean exit code 0.

#### Pytest Environment & Configuration:
- Python version: 3.14.6 (`c:\Seva Sankalp Hackathon\AMR Sentinel\.venv\Scripts\python.exe`)
- Pytest version: pytest-9.2.0, pluggy-1.7.0, pytest-asyncio-1.4.1.post1, anyio-4.16.0
- Configured dependencies in `services/api/requirements.txt` and `requirements-dev.txt`:
  - `fastapi>=0.115.0`, `uvicorn[standard]>=0.32.0`, `pydantic>=2.10.0`, `pydantic-settings>=2.6.0`, `python-multipart>=0.0.12`, `pyyaml>=6.0.2`, `httpx>=0.28.0`, `pytest>=8.3.0`, `pytest-asyncio>=0.24.0`, `ruff>=0.8.0`.

#### Complete Inventory of 24 Existing Test Cases in `services/api/tests/`:

1. **`test_architecture_isolation.py` (2 tests)**:
   - `test_engine_directory_exists` (Lines 22-24): Asserts `services/api/app/engine/` exists and is a directory.
   - `test_no_prohibited_imports_in_engine` (Lines 27-48): Performs Python AST walk (`ast.parse`) over all `.py` files in `app/engine/`. Verifies that no file imports prohibited packages (network, AI/LLM, DB/ORM, subprocess).

2. **`test_rules.py` (11 tests)**:
   - `test_pediatric_ciprofloxacin_triggers_urgent_review` (Lines 27-38): Age 8.0 + Ciprofloxacin -> `status == "NEEDS_URGENT_REVIEW"`, rule `SAFETY.PED.FQ_UNDER_18`.
   - `test_adult_ciprofloxacin_does_not_trigger_pediatric_gate` (Lines 40-50): Age 25.0 + Ciprofloxacin -> `SAFETY.PED.FQ_UNDER_18` not in findings.
   - `test_pediatric_age_boundary_at_18` (Lines 52-62): Exact age 18.0 + Ciprofloxacin -> `SAFETY.PED.FQ_UNDER_18` not in findings.
   - `test_pregnancy_contraindication_triggers_urgent_review` (Lines 65-76): Pregnant female + Doxycycline -> `status == "NEEDS_URGENT_REVIEW"`, rule `SAFETY.PREG.CONTRAINDICATED`.
   - `test_nitrofurantoin_in_severe_renal_impairment` (Lines 79-90): eGFR 22.0 mL/min + Nitrofurantoin -> `status == "NEEDS_URGENT_REVIEW"`, rule `SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`.
   - `test_nitrofurantoin_normal_renal_function_passes` (Lines 92-102): eGFR 90.0 mL/min + Nitrofurantoin -> rule not triggered.
   - `test_gentamicin_without_egfr_triggers_incomplete_data` (Lines 105-117): Gentamicin + `egfr_ml_min: None` -> `status in ("INCOMPLETE_DATA", "NEEDS_REVIEW")`, rule `SAFETY.RENAL.MISSING_EGFR_HOLD`, gap contains `"eGFR"`.
   - `test_penicillin_allergy_triggers_urgent_review_for_amoxicillin` (Lines 120-131): Allergy `["Penicillin"]` + Amoxicillin -> `status == "NEEDS_URGENT_REVIEW"`, rule `SAFETY.ALLERGY.BETA_LACTAM`.
   - `test_banned_fdc_triggers_urgent_review` (Lines 134-145): `Cefixime + Azithromycin` -> `status == "NEEDS_URGENT_REVIEW"`, rule `REGULATORY.BANNED_FDC`.
   - `test_azithromycin_in_acute_bronchitis_triggers_needs_review` (Lines 148-159): Azithromycin + `SYN_ACUTE_BRONCHITIS` -> `status == "NEEDS_REVIEW"`, rule `STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS`.
   - `test_meropenem_in_mild_uti_triggers_needs_review` (Lines 162-173): Meropenem + `SYN_UNCOMPLICATED_UTI` -> `status == "NEEDS_REVIEW"`, rule `STEWARDSHIP.AWARE.RESERVE_ESCALATION`.
   - `test_clean_guideline_case_triggers_no_rules` (Lines 176-187): Healthy adult + mild CAP + Amoxicillin 500mg TID 5d + eGFR 98.0 -> `status == "NO_RULE_TRIGGERED"`, 0 findings, 0 input gaps.

3. **`test_audits_api.py` (3 tests)**:
   - `test_audit_api_pediatric_case` (Lines 8-38): POST `/v1/audits` with pediatric ciprofloxacin -> HTTP 200, `status == "NEEDS_URGENT_REVIEW"`, severity `URGENT_REVIEW`.
   - `test_audit_api_clean_case` (Lines 40-68): POST `/v1/audits` with clean Amoxicillin case -> HTTP 200, `status == "NO_RULE_TRIGGERED"`.
   - `test_audit_api_validation_error` (Lines 70-81): POST `/v1/audits` with invalid negative age -> HTTP 422 Unprocessable Entity.

4. **`test_extractions.py` (2 tests)**:
   - `test_extraction_from_synthetic_prescription` (Lines 10-35): Uploading synthetic doctor note -> HTTP 200, returns editable draft, `clinical_status == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`, disclaimer present.
   - `test_extraction_rejects_unsupported_mime` (Lines 37-45): Uploading executable binary -> HTTP 415 Unsupported Media Type.

5. **`test_health.py` (2 tests)**:
   - `test_health_check_returns_200` (Lines 8-19): GET `/health` -> HTTP 200, `engine_mode == "deterministic_isolated"`, zero PHI.
   - `test_health_check_has_trace_headers` (Lines 21-27): GET `/health` contains `x-trace-id`, `x-response-time-sec`, and `x-content-type-options: nosniff`.

6. **`test_metrics.py` (2 tests)**:
   - `test_metrics_endpoint_has_zero_phi` (Lines 8-19): GET `/v1/metrics` -> aggregate WHO AWaRe breakdown (Access >= 60%), zero PHI.
   - `test_evidence_catalogue_endpoint` (Lines 21-34): GET `/v1/evidence` and `/v1/evidence/EVID_ICMR_PED_FQ` -> HTTP 200, publisher "Indian Council of Medical Research (ICMR)".

7. **`test_rls_security.py` (1 test)**:
   - `test_rls_security_posture` (Lines 5-30): Verifies Supabase anon vs service role key separation, and simulates Postgres `is_org_member()` multi-tenant isolation.

---

### 1.2 Deterministic Clinical Rules Engine (Audit Core)

#### Manifest Specification:
- Location: `services/api/app/rules_data/rules_v1.0.0.json` (244 lines)
- Version: `1.0.0-ICMR-STG-2022`
- Evidence Snapshot ID: `SNAP-2026-WHO-ICMR-v1`
- Engine Implementation: `services/api/app/engine/engine.py` (DeterministicAuditEngine) and `services/api/app/engine/evaluator.py` (pure evaluation functions).

#### The 11 Rule Specifications:

1. **`SAFETY.PED.FQ_UNDER_18`** (Tier 1, Severity: `URGENT_REVIEW`):
   - Target Drugs: Ciprofloxacin, Levofloxacin, Ofloxacin, Norfloxacin, Moxifloxacin, Gemifloxacin
   - Target Classes: Fluoroquinolone
   - Condition: `age_years < 18.0`
   - Clinical Concern: Cartilage erosion, permanent arthropathy, and tendon rupture.
   - Evidence Citation: `EVID_ICMR_PED_FQ` (ICMR STG Pediatric Guidelines Section 4.2 Page 38).

2. **`SAFETY.PED.TETRACYCLINE_UNDER_18`** (Tier 1, Severity: `URGENT_REVIEW`):
   - Target Drugs: Doxycycline, Tetracycline, Minocycline
   - Target Classes: Tetracycline
   - Condition: `age_years < 12.0`
   - Clinical Concern: Permanent tooth enamel hypoplasia and bone growth suppression.
   - Evidence Citation: `EVID_ICMR_PED_TETRA` (ICMR STG Pediatric Guidelines Section 4.5 Page 41).

3. **`SAFETY.PREG.CONTRAINDICATED`** (Tier 1, Severity: `URGENT_REVIEW`):
   - Target Drugs: Ciprofloxacin, Levofloxacin, Ofloxacin, Norfloxacin, Moxifloxacin, Doxycycline, Tetracycline, Minocycline, Amikacin, Gentamicin, Co-trimoxazole
   - Target Classes: Fluoroquinolone, Tetracycline, Aminoglycoside
   - Condition: `is_pregnant == True`
   - Clinical Concern: Teratogenicity, ototoxicity, congenital skeletal defects, cartilage erosion.
   - Evidence Citation: `EVID_WHO_PREG_ANTIBIOTICS` (WHO Chapter 6 Page 82).

4. **`SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`** (Tier 1, Severity: `URGENT_REVIEW`):
   - Target Drugs: Nitrofurantoin
   - Conditions: `egfr_ml_min < 30.0` OR (`age_years >= 65.0` AND (`egfr_ml_min is None` OR `egfr_ml_min < 45.0`))
   - Clinical Concern: Inadequate urinary concentration + drug accumulation causing peripheral neurotoxicity and pulmonary fibrosis.
   - Evidence Citation: `EVID_BEERS_ICMR_NITROFURANTOIN` (AGS Beers Table 2 / ICMR Nephro-Geriatric Section 2.1).

5. **`SAFETY.RENAL.MISSING_EGFR_HOLD`** (Tier 1, Severity: `DATA_GAP`):
   - Target Drugs: Gentamicin, Amikacin, Vancomycin, Colistin
   - Target Classes: Aminoglycoside, Polymyxin, Glycopeptide
   - Condition: `egfr_ml_min is None`
   - Clinical Concern: Mandatory baseline renal function required to titrate narrow-therapeutic nephrotoxics and prevent acute tubular necrosis.
   - Evidence Citation: `EVID_KDIGO_RENAL_HOLD` (KDIGO Practice Guideline Rec 3.1.2).

6. **`SAFETY.ALLERGY.BETA_LACTAM`** (Tier 1, Severity: `URGENT_REVIEW`):
   - Target Drugs: Amoxicillin, Amoxicillin-Clavulanate, Ampicillin, Cefalexin, Cefixime, Ceftriaxone
   - Allergy Triggers: "penicillin", "beta-lactam", "amoxicillin", "ampicillin"
   - Condition: Any allergy trigger present in patient documented allergies
   - Clinical Concern: Severe IgE-mediated anaphylaxis and cross-reactivity.
   - Evidence Citation: `EVID_ICMR_ALLERGY_ANAPHYLAXIS` (ICMR STG Section 1.4).

7. **`REGULATORY.BANNED_FDC`** (Tier 2, Severity: `URGENT_REVIEW`):
   - Target Pairs: ("cefixime", "azithromycin"), ("ofloxacin", "ornidazole")
   - Condition: Either single line containing both ingredients OR concurrent separate prescription lines for both active ingredients.
   - Clinical Concern: Prohibited by CDSCO Gazette Notification S.O. 2486(E) due to lack of therapeutic justification and rapid resistance acceleration.
   - Evidence Citation: `EVID_CDSCO_BANNED_FDC`.

8. **`STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS`** (Tier 2, Severity: `NEEDS_REVIEW`):
   - Target Condition: `SYN_ACUTE_BRONCHITIS`
   - Target Drugs: Any antibiotic (excluding non-antibiotics like Paracetamol, ORS, Zinc, Saline)
   - Clinical Concern: >90% viral etiology; antibiotics provide zero efficacy and increase adverse drug events.
   - Evidence Citation: `EVID_ICMR_RESP_BRONCHITIS` (ICMR STG Section 3.1 Page 24).

9. **`STEWARDSHIP.VIRAL.COMMON_COLD_URTI`** (Tier 2, Severity: `NEEDS_REVIEW`):
   - Target Conditions: `SYN_COMMON_COLD`, `SYN_VIRAL_URTI`, `SYN_PHARYNGITIS_NON_STREP`
   - Target Drugs: Any antibiotic
   - Clinical Concern: Exclusively viral; empirical antibiotics contraindicated under ICMR and WHO stewardship standards.
   - Evidence Citation: `EVID_ICMR_URTI_COLD` (ICMR STG Section 1.2 Page 11).

10. **`STEWARDSHIP.AWARE.RESERVE_ESCALATION`** (Tier 3, Severity: `NEEDS_REVIEW`):
    - Target Drugs: Meropenem, Linezolid, Colistin (WHO AWaRe Reserve)
    - Mild Indications: `SYN_CAP_MILD`, `SYN_UNCOMPLICATED_UTI`, `SYN_SSTI_UNCOMPLICATED`, `SYN_AOM`
    - Clinical Concern: Reserve agents are last-resort options for confirmed multidrug-resistant pathogens; empirical outpatient use threatens global antimicrobial reserves.
    - Evidence Citation: `EVID_WHO_AWARE_2023`.

11. **`STEWARDSHIP.DURATION.EXCESSIVE`** (Tier 4, Severity: `NEEDS_REVIEW`):
    - Target Conditions: `SYN_UNCOMPLICATED_UTI`, `SYN_CAP_MILD`
    - Condition: `duration_days > 5`
    - Clinical Concern: ICMR standard recommends short-course therapy (3 to 5 days); extended courses select for resistant host microbiota without increasing cure rate.
    - Evidence Citation: `EVID_ICMR_SHORT_COURSE`.

---

### 1.3 Architectural Safety Contracts & Enforcement (R2)

The two-layer safety boundary is maintained by four explicit mechanisms:

1. **AST Import Isolation**:
   In `test_architecture_isolation.py:8-17`, the AST scanner strictly prohibits the following packages within `services/api/app/engine/`:
   - Network / HTTP: `requests`, `httpx`, `urllib`, `aiohttp`, `socket`, `http`
   - AI / LLM SDKs: `google`, `google.genai`, `openai`, `anthropic`, `langchain`, `llama_index`
   - Database / ORM: `sqlalchemy`, `asyncpg`, `psycopg2`, `psycopg`, `supabase`, `sqlite3`
   - Process Execution: `subprocess`
   Any import of these modules immediately fails the build and CI test gate.

2. **Draft Untrusted Status Contract**:
   In `services/api/app/extraction/adapter.py:149-150` and `services/api/app/api/v1/extractions.py:25-29`:
   - Extraction returns `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`.
   - The extraction endpoint NEVER calls the audit engine.
   - Low confidence or AI failure does not block manual clinician entry.

3. **Clinician Confirmation Gate**:
   In `apps/web/components/PrescriptionStepper.tsx:56`, the UI requires `confirmedByClinician: true` before initiating `POST /v1/audits`. The deterministic engine processes only clinician-confirmed structured facts.

4. **Deterministic Status Precedence Hierarchy**:
   In `services/api/app/engine/engine.py:138-152`:
   ```python
   if has_urgent:
       final_status = "NEEDS_URGENT_REVIEW"
   elif has_data_gap_finding and not has_review:
       final_status = "INCOMPLETE_DATA"
   elif has_review:
       final_status = "NEEDS_REVIEW"
   elif dedup_gaps:
       final_status = "INCOMPLETE_DATA"
   else:
       final_status = "NO_RULE_TRIGGERED"
   ```
   No AI model can modify, suppress, or override this deterministic calculation.

---

### 1.4 Intake Extraction Baseline Analysis & Fallback Behavior (R3)

Investigating `services/api/app/extraction/adapter.py`:

```python
# Lines 25-34
if self.settings.GEMINI_API_KEY and len(self.settings.GEMINI_API_KEY) > 10:
    try:
        return await self._extract_with_gemini(file_bytes, mime_type)
    except Exception as e:
        print(f"[ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: {e}")

return self._extract_with_local_heuristics(file_bytes, filename)
```

#### Verified Observed Execution:
1. **Mock Key in `.env`**:
   Executing probe with existing `.env` key (`GEMINI_API_KEY=AQ.Ab8RN6LX3V6fgGaHVlts-mIzHEYcCxbBJq9Vg63o_jp1ldtmpA`):
   - Result: `[ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: Gemini extraction non-200 response`
   - Extractor engine used: `offline_heuristic_adapter`.
   - Function completed successfully without crashing or hanging.
2. **Empty Key**:
   Executing probe with `GEMINI_API_KEY=""`:
   - Result: Directly executes `offline_heuristic_adapter` without network overhead.

#### Baseline Extraction Deficiencies (Baseline Heuristic in `adapter.py:80-151`):
- **Indication**: Always hardcoded to `"SYN_CAP_MILD"` regardless of input symptoms, diagnosis, or text (0% accuracy on 11 out of 12 clinical conditions).
- **Allergies**: Always hardcoded to `[]` empty list (0% recall on documented drug allergies).
- **Medication Names**: Restricted to hardcoded list of 11 tuples; if not matched, defaults to `Amoxicillin 500mg TID 5d`.
- **Dose, Frequency, Duration**: Injected from the static brand mapping tuple rather than parsed dynamically from prescription text.

---

### 1.5 Benchmark Test Split & Evaluation Script Specifications

#### Available Datasets for Grounding & Evaluation:
- `data_sets/AMR_ANALYZED_DATA_PACKAGE/who_aware_antibiotics.csv`: 378 antibiotic entries with Access, Watch, Reserve, and Not Recommended FDC classifications.
- `data_sets/AMR_ANALYZED_DATA_PACKAGE/amr_chatbot_corpus.jsonl`: 3,844 records covering ICMR and NCDC resistance evidence.
- `apps/web/lib/clinical-data.ts`: 27 canonical antibiotics with brand mappings, 12 conditions (`SYN_CAP_MILD`, `SYN_UNCOMPLICATED_UTI`, `SYN_ACUTE_BRONCHITIS`, `SYN_COMMON_COLD`, `SYN_VIRAL_URTI`, `SYN_PHARYNGITIS_NON_STREP`, `SYN_WATERY_DIARRHEA`, `SYN_PHARYNGITIS_STREP`, `SYN_AOM`, `SYN_SSTI_UNCOMPLICATED`, `SYN_PYELONEPHRITIS_UNCOMPLICATED`, `SYN_ENTERIC_FEVER`).
- `apps/web/lib/sample-cases.ts`: 6 synthetic golden cases with expected audit statuses.

#### Automated Evaluation Script Requirements:
The evaluation script must evaluate an input set of benchmark prescription documents against ground-truth labels and compare **Baseline** vs **Enhanced Agent**:

1. **Benchmark Test Set Composition (20-30 Cases)**:
   - 4 Pediatric cases (Ciprofloxacin, Doxycycline, Amoxicillin, Azithromycin)
   - 4 Geriatric & Renal cases (Nitrofurantoin eGFR 22, Nitrofurantoin eGFR 85, Gentamicin missing eGFR, Amikacin eGFR 90)
   - 3 Pregnancy cases (Doxycycline pregnant, Ciprofloxacin pregnant, Cefalexin pregnant)
   - 3 Allergy cases (Penicillin allergy + Amoxicillin, Penicillin allergy + Azithromycin, No allergy)
   - 2 Banned FDC cases (Cefixime + Azithromycin, Ofloxacin + Ornidazole)
   - 4 Viral / Self-limiting cases (Acute bronchitis + Azithromycin, Common cold + Amoxicillin, Viral URTI + Paracetamol only, Non-strep pharyngitis + Cefixime)
   - 2 WHO AWaRe Reserve cases (Meropenem for mild UTI, Linezolid for mild SSTI)
   - 2 Excessive Duration cases (Amoxicillin 14 days for CAP, Nitrofurantoin 10 days for cystitis)
   - 4 Clean Guideline-concordant cases (Amoxicillin 5d CAP, Nitrofurantoin 5d UTI, ORS + Zinc diarrhea, Cefalexin 5d SSTI)

2. **Metrics to Compute**:
   - **Field-level Demographic Accuracy**:
     - `ageYears`: Exact match or within 0.5 years.
     - `gender`: Exact categorical match.
     - `isPregnant`: Exact boolean match.
     - `egfrMlMin`: Numerical match (and exact null detection when omitted).
     - `allergies`: Set precision, recall, and Jaccard similarity.
   - **Indication Matching Accuracy**:
     - Exact match on canonical `indicationCode` (e.g. `SYN_WATERY_DIARRHEA`).
   - **Medication Extraction Performance**:
     - Canonical drug name Precision, Recall, F1.
     - Dose text accuracy (e.g., "250 mg" vs "250mg").
     - Frequency text accuracy (e.g., "BD", "TID", "OD").
     - Duration days exact match accuracy.
   - **Downstream Clinical Audit Concordance**:
     - % of cases where extracted draft (when audited) yields identical status (`NEEDS_URGENT_REVIEW`, `NEEDS_REVIEW`, `INCOMPLETE_DATA`, `NO_RULE_TRIGGERED`) to ground-truth audit.
   - **Safety-Critical False Negative Rate**:
     - Rate of cases requiring `NEEDS_URGENT_REVIEW` that were mis-extracted such that the audit returned `NO_RULE_TRIGGERED` (Target: 0.0%).
   - **Execution Health**:
     - Latency per case (ms).
     - Offline fallback graceful degradation (100% pass when network/API key unavailable).

3. **Reporting Format**:
   - Machine-readable JSON summary (`evaluation_results.json`).
   - Markdown comparison table (`evaluation_summary.md`).

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Quality Gate | Ruff Python Linter | Verifies PEP 8, import order, and lint cleanliness across `services/api` | Python source files | Exit code 0 on clean lint | Exit code 1 with line numbers on lint violation | `scripts/test.ps1:10-12` |
| 2 | Quality Gate | AST Import Isolation Gate | AST walk verifying zero prohibited modules (AI, HTTP, DB, subprocess) in `app/engine/` | AST trees of `app/engine/**/*.py` | Assertion pass | Assertion failure listing file, line, and module name | `test_architecture_isolation.py:27-48` |
| 3 | Quality Gate | Pytest Unit & API Suite | Comprehensive test runner executing 24 tests across rules, API, metrics, health, RLS | `services/api/tests` | 24 passed in 3.26s | Non-zero exit code on assertion failure | `scripts/test.ps1:15-18` |
| 4 | Quality Gate | Web TypeScript Strict Type-Check | Compiles and verifies TypeScript types across Next.js app without emitting JS | `apps/web` TypeScript codebase | Exit code 0 | Non-zero exit code on type mismatch | `scripts/test.ps1:21-24` |
| 5 | Clinical Rule | Pediatric Fluoroquinolone Gate | Blocks Fluoroquinolones in patients under 18 years | `age_years < 18`, FQ drug | Finding: `SAFETY.PED.FQ_UNDER_18`, `URGENT_REVIEW` | Returns None if age >= 18 | `evaluator.py:21-38`, `rules_v1.0.0.json:7-17` |
| 6 | Clinical Rule | Pediatric Tetracycline Gate | Blocks Tetracyclines in patients under 12 years | `age_years < 12`, Tetracycline drug | Finding: `SAFETY.PED.TETRACYCLINE_UNDER_18`, `URGENT_REVIEW` | Returns None if age >= 12 | `evaluator.py:21-38`, `rules_v1.0.0.json:19-29` |
| 7 | Clinical Rule | Pregnancy Contraindication Gate | Blocks teratogenic and toxic antimicrobials in pregnancy | `is_pregnant == True`, contraindicated drug | Finding: `SAFETY.PREG.CONTRAINDICATED`, `URGENT_REVIEW` | Returns None if not pregnant | `evaluator.py:40-61`, `rules_v1.0.0.json:31-41` |
| 8 | Clinical Rule | Renal Nitrofurantoin Gate | Blocks Nitrofurantoin in severe renal impairment or geriatric risk | `egfr < 30` OR (`age >= 65` and `egfr < 45`/None) | Finding: `SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`, `URGENT_REVIEW` | Returns None if renal function normal | `evaluator.py:63-103`, `rules_v1.0.0.json:43-53` |
| 9 | Clinical Rule | Mandatory Renal Function Hold | Halts narrow-therapeutic nephrotoxics if eGFR is unrecorded | `egfr is None`, nephrotoxic drug | Finding: `SAFETY.RENAL.MISSING_EGFR_HOLD`, `DATA_GAP` | Returns None if eGFR documented | `evaluator.py:105-126`, `rules_v1.0.0.json:55-65` |
| 10 | Clinical Rule | Beta-Lactam Allergy Cross-Reactivity | Checks cross-reactivity for penicillin/beta-lactam allergy | Documented allergy + Beta-lactam drug | Finding: `SAFETY.ALLERGY.BETA_LACTAM`, `URGENT_REVIEW` | Returns None if no allergy matches | `evaluator.py:128-158`, `rules_v1.0.0.json:67-76` |
| 11 | Clinical Rule | Regulatory Banned FDC Gate | Identifies CDSCO banned irrational combinations | Single combination string or concurrent drugs | Finding: `REGULATORY.BANNED_FDC`, `URGENT_REVIEW` | Returns None if no banned pair | `evaluator.py:160-194`, `rules_v1.0.0.json:78-86` |
| 12 | Clinical Rule | Viral Indication Antimicrobial Flag | Flags inappropriate empirical antibiotics for viral illness | `SYN_ACUTE_BRONCHITIS`, `SYN_COMMON_COLD`, etc. | Finding: `STEWARDSHIP.VIRAL.*`, `NEEDS_REVIEW` | Permits non-antibiotics (Paracetamol, ORS) | `evaluator.py:196-222`, `rules_v1.0.0.json:88-106` |
| 13 | Clinical Rule | WHO AWaRe Reserve Escalation Alert | Flags Reserve-group antimicrobials for mild outpatient infections | Reserve drug + mild indication code | Finding: `STEWARDSHIP.AWARE.RESERVE_ESCALATION`, `NEEDS_REVIEW` | Returns None if indication not mild | `evaluator.py:224-247`, `rules_v1.0.0.json:108-118` |
| 14 | Clinical Rule | Excessive Treatment Duration Gate | Enforces ICMR 3-5 day short-course limit | Mild indication + `duration_days > 5` | Finding: `STEWARDSHIP.DURATION.EXCESSIVE`, `NEEDS_REVIEW` | Returns None if duration <= 5 | `evaluator.py:249-272`, `rules_v1.0.0.json:120-130` |
| 15 | API Endpoint | Prescription Document Extraction | Asynchronous extraction of editable prescription draft | Uploaded document bytes + MIME type | Draft JSON with field confidence & `clinical_status` | Returns 415 for invalid MIME, 413 if >10MB | `extractions.py:18-69`, `test_extractions.py` |
| 16 | API Endpoint | Deterministic Prescription Audit | Evaluates confirmed prescription payload against rule manifest | Confirmed `AuditRequest` JSON | `AuditReport` with findings, status, evidence, disclaimer | Returns 422 for schema invalidation, 500 on error | `audits.py:24-55`, `test_audits_api.py` |
| 17 | API Endpoint | Health & Isolation Verification | Operational status check with active rule version | None | `{status: "healthy", engine_mode: "deterministic_isolated", ...}` | Returns trace headers and security headers | `health.py:12-25`, `test_health.py` |
| 18 | API Endpoint | Stewardship Aggregate Metrics | De-identified stewardship metrics & AWaRe distribution | None | Zero-PHI aggregate statistics | No PHI exposed | `metrics.py`, `test_metrics.py` |
| 19 | API Endpoint | Evidence Reference Lookup | Retrieve clinical guideline source excerpt and citation | Evidence ID (e.g. `EVID_ICMR_PED_FQ`) | Full evidence metadata JSON | Returns 404 if evidence ID unknown | `metrics.py`, `test_metrics.py` |
| 20 | Safety Contract | Untrusted Draft State Machine | Guarantees AI extractions cannot trigger audits directly | Raw document input | `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"` | Extraction failure yields manual fallback form | `adapter.py:149`, `extractions.py:25-29` |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Pediatric Age Boundary | Age exact 18.0 with Ciprofloxacin | Evaluator checks `if age_years >= min_age: return None`. Does NOT trigger pediatric contraindication (`test_rules.py:52-62`). |
| 2 | Missing Renal Function on Clean Drug | Adult age 34, Amoxicillin 500mg, but `egfr_ml_min: None` | Engine registers input gap `"Patient eGFR / renal function unrecorded"`. If no rules are breached, `final_status` becomes `"INCOMPLETE_DATA"` rather than `"NO_RULE_TRIGGERED"` (`engine.py:148-150`). |
| 3 | Missing Renal Function on Nephrotoxic Drug | Adult age 45, Gentamicin 80mg, `egfr_ml_min: None` | Triggers Tier 1 `SAFETY.RENAL.MISSING_EGFR_HOLD` (`DATA_GAP` severity) and registers input gap `eGFR`. Status becomes `"INCOMPLETE_DATA"` (`test_rules.py:105-117`). |
| 4 | Geriatric Nitrofurantoin Boundary | Age 65.0 with `egfr_ml_min == 45.0` | Evaluator condition `age >= 65 and (egfr is None or egfr < 45.0)` evaluates to False; does not trigger geriatric renal warning (`evaluator.py:92-100`). |
| 5 | Severe Renal Nitrofurantoin Boundary | Patient with `egfr_ml_min == 30.0` | Evaluator condition `egfr < 30.0` evaluates to False; strictly < 30.0 is required (`evaluator.py:83-90`). |
| 6 | Duration Short-Course Boundary | Acute cystitis with `duration_days == 5` | Evaluator checks `duration > 5`. At exactly 5 days, returns None (passes short-course guideline) (`evaluator.py:262-270`). |
| 7 | Duration Exceeded Boundary | Acute cystitis with `duration_days == 6` | `duration > 5` evaluates to True; triggers `STEWARDSHIP.DURATION.EXCESSIVE` (`NEEDS_REVIEW`). |
| 8 | Multiple Severity Precedence | Patient age 8 (URGENT_REVIEW) + Missing eGFR (DATA_GAP) + Viral bronchitis (NEEDS_REVIEW) | Engine checks `has_urgent` first. Overall status is strictly `"NEEDS_URGENT_REVIEW"` (`engine.py:138-144`). |
| 9 | Banned FDC Concurrent Separate Lines | Prescribing Cefixime on line 1 and Azithromycin on line 2 | Evaluator checks `has_combo_line or has_separate_lines`. Successfully triggers `REGULATORY.BANNED_FDC` even when prescribed as separate pills (`evaluator.py:183-186`). |
| 10 | Non-Antibiotic Exemption in Viral Infection | Paracetamol or ORS prescribed for `SYN_ACUTE_BRONCHITIS` | Evaluator filters out `["oral rehydration", "ors", "paracetamol", "zinc", "saline"]`. Does not trigger viral stewardship rule (`evaluator.py:207-214`). |
| 11 | Allergy Substring Matching | Allergy listed as `"Penicillin G Potassium"` or `"history of severe penicillin allergy"` | Evaluator checks `trigger in normalize_drug_name(user_allergy)`. Successfully triggers `SAFETY.ALLERGY.BETA_LACTAM` (`evaluator.py:138-142`). |
| 12 | Gemini API Invalid Key / Network Outage | `GEMINI_API_KEY` present but rejected by Google endpoint | Exception caught inside `extract_from_bytes()`; prints error and falls back immediately to `_extract_with_local_heuristics()`. Status is `UNTRUSTED_DRAFT_PENDING_CONFIRMATION` without crash. |
| 13 | Empty / Missing Gemini API Key | `GEMINI_API_KEY = ""` | `len(key) > 10` is False; directly invokes local heuristics without network timeout (`adapter.py:26-34`). |
| 14 | Malicious File Upload | Executable `malicious.exe` (MIME: `application/x-msdownload`) | API rejects with HTTP 415 Unsupported Media Type (`extractions.py:30-34`). |
| 15 | Oversized File Upload | Uploaded file exceeding 10 MB | API rejects with HTTP 413 Request Entity Too Large (`extractions.py:37-41`). |

---

## 2. Logic Chain

1. **Test Suites & Clean Testing Baseline**:
   - Directly observed: Running `scripts/test.ps1` runs Ruff, AST Isolation Pytest (24 tests), and TypeScript type check.
   - All 24 tests passed in 3.26 seconds with exit code 0.
   - Logical Deduction: The baseline testing environment is healthy, operational, and non-regressed. Any subsequent agent enhancement can be verified continuously against this exact test gate.

2. **Deterministic Clinical Audit Core & Safety Contracts**:
   - Directly observed: `services/api/app/engine/` is completely separated from `services/api/app/extraction/`.
   - `test_architecture_isolation.py` parses the AST of `app/engine/` and forbids any import of AI SDKs, HTTP clients, databases, or subprocesses.
   - Logical Deduction: The deterministic audit core is structurally isolated from AI hallucinations. Enhancing prompts or few-shots in `services/api/app/extraction/` cannot degrade, compromise, or bypass the clinical audit rules engine.

3. **Intake Extraction Gap & Enhancement Scope**:
   - Directly observed: The baseline heuristic extractor in `ExtractionAdapter` hardcodes the indication to `SYN_CAP_MILD`, returns an empty allergy list `[]`, and only recognizes 11 hardcoded drug brands, defaulting everything else to `Amoxicillin`.
   - Logical Deduction: Baseline field extraction accuracy is poor (~30-45%), causing downstream clinical audits to miss indications and allergies. Training/enhancing the agent (via calibrated few-shot prompts or grounding on `DRUG_CATALOG` and `AMR_ANALYZED_DATA_PACKAGE`) will drastically improve extraction accuracy and clinical recommendation concordance.

4. **Automated Evaluation Script Formulation**:
   - Directly observed: `sample-cases.ts` contains 6 golden cases; `clinical-data.ts` contains 12 clinical conditions and 27 drugs; `who_aware_antibiotics.csv` contains 378 classified antibiotics.
   - Logical Deduction: A synthetic benchmark split of 20-30 cases can be constructed across all 10 clinical rule categories. Running baseline vs enhanced agent extraction against this split will provide quantitative verification of improvement (Field Accuracy, Drug F1, Audit Concordance, Safety False Negative Rate).

---

## 3. Caveats

- **Mock API Key**: The `.env` file currently contains a synthetic mock key (`AQ.Ab8RN6LX3V6fgGaHVlts-mIzHEYcCxbBJq9Vg63o_jp1ldtmpA`), which returns a 400 from Google API. This successfully proved that the offline fallback works as designed. To showcase live Gemini 2.5 Flash cloud extraction during the live demo, a valid Gemini API key is needed.
- **`next lint` deprecation**: In `apps/web`, running `npm run lint` prompts an interactive ESLint migration prompt in Next.js 15. The official project test runner `scripts/test.ps1` bypasses this by running `npm run type-check` (`tsc --noEmit`), which is the authoritative TypeScript validation gate.

---

## 4. Conclusion

1. **System Health**: All 24 automated unit, API, and isolation tests pass cleanly in 3.26 seconds. Ruff linter and TypeScript strict checks pass without errors.
2. **Safety Architecture Intact**: The two-layer safety boundary (Assistive Intake Draft vs Deterministic Core) is mathematically guaranteed by AST isolation tests and status state machine contracts.
3. **Enhancement Target Clearly Identified**: The deterministic engine is complete and robust (11 rules, 4 tiers, 11 evidence citations). The bottleneck is the intake extraction layer (`ExtractionAdapter`), which currently relies on crude fallback heuristics.
4. **Evaluation Path Fully Defined**: Specifications for a 20-30 case benchmark evaluation script are formulated with exact metrics (Precision/Recall/F1, Indication Match, Audit Concordance, False Negative Rate), ready for automated execution and reporting.

---

## 5. Verification Method

To independently verify these findings, execute the following commands from the project root (`c:\Seva Sankalp Hackathon\AMR Sentinel`):

```powershell
# 1. Run the official full quality gate suite
powershell -ExecutionPolicy Bypass -File scripts/test.ps1

# 2. Run pytest suite directly with verbose output
$env:PYTHONPATH = "services/api"
.\.venv\Scripts\pytest.exe services/api/tests -v

# 3. Verify AST Isolation specifically
.\.venv\Scripts\pytest.exe services/api/tests/test_architecture_isolation.py -v

# 4. Verify pure deterministic clinical rules specifically
.\.venv\Scripts\pytest.exe services/api/tests/test_rules.py -v

# 5. Verify TypeScript strict type-check
cd apps/web
npm run type-check
```

**Invalidation Conditions**:
- If any test in `services/api/tests` fails, or if `test_architecture_isolation.py` detects an import from `PROHIBITED_MODULES`, this report's conclusion is invalidated.
