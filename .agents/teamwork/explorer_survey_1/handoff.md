# Architectural Investigation & Baseline Survey Report

**Explorer**: `explorer_survey_1` (Codebase & Agent Architecture Explorer)  
**Parent Orchestrator**: `01b31f9d-d7a9-4fca-9bcc-706835e55498`  
**Date**: 2026-11-09T20:58:00Z  
**Target Repository**: `c:\Seva Sankalp Hackathon\AMR Sentinel`

---

## 1. Observation

### 1.1 AI Agent Implementation (Intake Extraction, Prompts, LLM Client, Assistant Flow)

#### A. Intake Extraction Adapter
- **File**: `services/api/app/extraction/adapter.py`
  - **Class**: `ExtractionAdapter` (lines 12–152)
  - **Method**: `async def extract_from_bytes(self, file_bytes: bytes, mime_type: str, filename: str = "prescription.pdf") -> dict[str, Any]` (lines 18–35):
    ```python
    25: # Check if Gemini API is available and configured
    26: if self.settings.GEMINI_API_KEY and len(self.settings.GEMINI_API_KEY) > 10:
    27:     try:
    28:         return await self._extract_with_gemini(file_bytes, mime_type)
    29:     except Exception as e:
    30:         print(f"[ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: {e}")
    32: 
    33: # Local offline heuristic fallback
    34: return self._extract_with_local_heuristics(file_bytes, filename)
    ```
  - **Method**: `async def _extract_with_gemini(self, file_bytes: bytes, mime_type: str) -> dict[str, Any]` (lines 36–78):
    - Uses `httpx.AsyncClient(timeout=15.0)` to call Gemini REST API:
      `url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.settings.GEMINI_API_KEY}"` (line 52).
    - Base64 encodes `file_bytes` as `inline_data` (lines 53–62).
    - Uses `generationConfig={"response_mime_type": "application/json"}` (line 65).
    - Parses candidate text part as JSON, attaches `"extraction_engine": "gemini_2.5_flash"`, and returns the dictionary (lines 71–76).

#### B. Prompt Template and Few-Shot Status
- **File**: `services/api/app/extraction/adapter.py`, lines 40–49:
  ```python
  prompt = (
      "Extract clinical prescription facts from this synthetic doctor prescription. "
      "Return JSON matching: "
      "{"
      "  patientContext: { ageYears: float, gender: 'female'|'male'|'other', isPregnant: bool, egfrMlMin: float|null, allergies: [string] },"
      "  indicationCode: string,"
      "  prescriptionLines: [{ drugName: string, doseText: string, frequencyText: string, durationDays: int|null }],"
      "  fieldConfidence: { ageYears: 'high'|'medium'|'low', drugs: 'high'|'medium'|'low' }"
      "}"
  )
  ```
- **Direct Observation**:
  - The current prompt is a single zero-shot string.
  - **Zero few-shot examples** exist anywhere in the code.
  - No prompt grounding on Indian antimicrobial brand names or generic active ingredients.
  - No guidance or list of permitted canonical condition codes (e.g., `SYN_CAP_MILD`, `SYN_UNCOMPLICATED_UTI`, `SYN_ACUTE_BRONCHITIS`, `SYN_WATERY_DIARRHEA`).

#### C. Extraction API Route
- **File**: `services/api/app/api/v1/extractions.py`
  - **Endpoint**: `POST /v1/extractions` and `POST /api/v1/extractions` (via `main.py` lines 70–71)
  - **Handler**: `async def extract_prescription(file: UploadFile = File(...))` (lines 22–69)
  - Enforces `ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf", "text/plain"}` (lines 8–14) and `MAX_FILE_BYTES = 10 * 1024 * 1024` (line 15).
  - Invokes `adapter.extract_from_bytes(file_bytes, mime_type, filename)`.
  - Catches general exceptions to return a default template with `"clinical_status": "MANUAL_ENTRY_REQUIRED"` so extraction failures never crash or block the user (lines 50–68).

#### D. Assistant Intake UI Stepper & Clinician Confirmation Flow
- **File**: `apps/web/components/PrescriptionStepper.tsx`
  - Function: `handleFileUpload` (lines 78–126): Uploads document to `POST /api/v1/extractions`, populates form fields, sets `confirmedByClinician = false`, and displays `extractionNotice`.
  - Lines 180: `if (!confirmedByClinician) return;` — blocks submitting to audit endpoint until clinician explicitly confirms.
  - Function: `handleAuditSubmit` (lines 179–226): Posts confirmed payload to `POST /api/v1/audits` and navigates to `/results`.

---

### 1.2 Configuration & Local Offline Fallback Heuristics

#### A. GEMINI_API_KEY Configuration
- **File**: `services/api/app/config.py` (lines 10–61):
  - Uses `pydantic_settings.BaseSettings` reading `.env`.
  - Line 51: `GEMINI_API_KEY: str = ""`
  - Line 58–61: `@lru_cache def get_settings() -> Settings: return Settings()`
- **Files**: `.env` (line 18) and `services/api/.env` (line 21):
  - `GEMINI_API_KEY=AQ.Ab8RN6LX3V6fgGaHVlts-mIzHEYcCxbBJq9Vg63o_jp1ldtmpA`
  - Configured key length is 56 characters (`> 10`).

#### B. Local Offline Fallback Heuristics Implementation
- **File**: `services/api/app/extraction/adapter.py`, lines 80–152:
  - `def _extract_with_local_heuristics(self, file_bytes: bytes, filename: str) -> dict[str, Any]`
  - Decodes text with `file_bytes.decode("utf-8", errors="ignore")` (line 82).
  - Age regex: `re.search(r"(?:age|yr|years?)\s*[:=]?\s*(\d{1,3})", text_content, re.IGNORECASE)` (line 85); defaults to `34.0`.
  - Pregnancy/Gender: `re.search(r"\bpregnant|pregnancy|trimester\b", text_content, re.IGNORECASE)` (line 90); female if pregnant or `\bfemale\b`, else male.
  - eGFR regex: `re.search(r"(?:egfr|gfr|creatinine clearance)\s*[:=]?\s*(\d{1,3})", text_content, re.IGNORECASE)` (line 94).
  - Drug detection: Scans for 11 hardcoded tuples:
    `("cifran", "Ciprofloxacin", "250 mg", "Twice daily (BD)", 5)`
    `("ciprofloxacin", "Ciprofloxacin", "250 mg", "Twice daily (BD)", 5)`
    `("augmentin", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5)`
    `("azithral", "Azithromycin", "500 mg", "Once daily (OD)", 5)`
    `("azithromycin", "Azithromycin", "500 mg", "Once daily (OD)", 5)`
    `("martifur", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5)`
    `("nitrofurantoin", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5)`
    `("meronem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 7)`
    `("meropenem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 7)`
    `("gentamicin", "Gentamicin", "80 mg", "Twice daily (BD)", None)`
    `("amoxicillin", "Amoxicillin", "500 mg", "Three times daily (TID)", 5)`
  - If no drug matched, defaults to `Amoxicillin 500 mg TID x 5` (lines 123–130).
  - **Indication code is unconditionally hardcoded**: `indicationCode: "SYN_CAP_MILD"` (line 139).
  - Labels returned: `"extraction_engine": "offline_heuristic_adapter"`, `"clinical_status": "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`, `"disclaimer": "Assistive extraction only. Clinician must verify all fields prior to clinical audit."` (lines 148–150).

---

### 1.3 Deterministic Clinical Audit Core & Two-Layer Safety Architecture

#### A. Deterministic Isolation Enforcement
- **File**: `services/api/tests/test_architecture_isolation.py` (lines 1–48):
  - Uses Python `ast.parse` and `ast.walk` to inspect all `.py` files in `services/api/app/engine/`.
  - Asserts that none of the following modules are imported directly or via `from`:
    - Network/HTTP: `requests`, `httpx`, `urllib`, `aiohttp`, `socket`, `http`
    - AI/LLM SDKs: `google`, `google.genai`, `openai`, `anthropic`, `langchain`, `llama_index`
    - Database/ORM: `sqlalchemy`, `asyncpg`, `psycopg2`, `psycopg`, `supabase`, `sqlite3`
    - Process/OS: `subprocess`
  - **Command & Test Output**:
    `powershell -ExecutionPolicy Bypass -Command "$env:PYTHONPATH='services/api'; .\.venv\Scripts\pytest.exe services/api/tests/test_architecture_isolation.py -v"`
    Result: 2 passed in 0.12s.

#### B. Audit Engine & Evaluator Logic
- **File**: `services/api/app/engine/engine.py`:
  - Class: `DeterministicAuditEngine` (lines 21–166)
  - `__init__(self, manifest: dict[str, Any])`: Loads immutable rule manifest snapshot and evidence catalog.
  - `evaluate(self, request_data: dict[str, Any]) -> dict[str, Any]`:
    - Normalizes inputs: patient age, pregnancy flag, eGFR, allergies, indication code, prescription lines.
    - Gaps detection: flags missing eGFR or missing treatment duration (lines 67–70).
    - Iterates over `self.rules` and evaluates pure functions in `evaluator.py`:
      - `check_pediatric_contraindication` (`SAFETY.PED.FQ_UNDER_18`, `SAFETY.PED.TETRACYCLINE_UNDER_18`)
      - `check_pregnancy_contraindication` (`SAFETY.PREG.CONTRAINDICATED`)
      - `check_renal_nitrofurantoin` (`SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30`)
      - `check_missing_egfr_hold` (`SAFETY.RENAL.MISSING_EGFR_HOLD`)
      - `check_beta_lactam_allergy` (`SAFETY.ALLERGY.BETA_LACTAM`)
      - `check_banned_fdc` (`REGULATORY.BANNED_FDC`)
      - `check_viral_indication` (`STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS`, `STEWARDSHIP.VIRAL.COMMON_COLD_URTI`)
      - `check_aware_reserve_escalation` (`STEWARDSHIP.AWARE.RESERVE_ESCALATION`)
      - `check_excessive_duration` (`STEWARDSHIP.DURATION.EXCESSIVE`)
    - Computes deterministic aggregate status (lines 142–151):
      - `NEEDS_URGENT_REVIEW` if any finding has `severity == "URGENT_REVIEW"`
      - `INCOMPLETE_DATA` if data gaps exist without urgent/review flags
      - `NEEDS_REVIEW` if any finding has `severity == "NEEDS_REVIEW"`
      - `NO_RULE_TRIGGERED` if clean and complete
    - Attaches mandatory clinical disclaimer (lines 159–164).

#### C. Rule Snapshot & Evidence Catalog
- **File**: `services/api/app/rules_data/rules_v1.0.0.json` (244 lines):
  - Version: `"1.0.0-ICMR-STG-2022"`, Evidence snapshot: `"SNAP-2026-WHO-ICMR-v1"`
  - 10 active rules across 4 safety tiers:
    - Tier 1: Absolute Contraindications (Pediatric, Pregnancy, Renal eGFR <30, Missing eGFR hold, Beta-lactam anaphylaxis)
    - Tier 2: Indication Legitimacy & CDSCO Banned FDCs (`Cefixime + Azithromycin`, `Ofloxacin + Ornidazole`, acute bronchitis, common cold)
    - Tier 3: WHO AWaRe Reserve Escalation (`Meropenem`, `Linezolid`, `Colistin` for mild outpatient infections)
    - Tier 4: ICMR Short-Course Treatment Duration Limits (>5 days for mild CAP or uncomplicated UTI)
  - 10 evidence catalog entries referencing ICMR STG 2022, WHO AWaRe 2023, AGS Beers Criteria 2023, KDIGO AKI guidelines, and CDSCO Gazette bans.

---

### 1.4 Interfaces, Data Models, and Entry Points

#### A. Data Models (`services/api/app/schemas/`)
- `patient.py`:
  - `PatientContext`: `age_years: float`, `gender: Literal["female", "male", "other"]`, `is_pregnant: bool`, `egfr_ml_min: float | None`, `allergies: list[str]`.
- `prescription.py`:
  - `PrescriptionLine`: `drug_name: str`, `dose_text: str`, `frequency_text: str`, `duration_days: int | None`, `route: str`.
- `indication.py`:
  - `ClinicalIndication`: `code: str`, `setting: Literal["outpatient", "inpatient"]`.
- `audit.py`:
  - `AuditRequest`: `patient_context: PatientContext`, `indication_code: str`, `setting: Literal["outpatient", "inpatient"]`, `prescription_lines: list[PrescriptionLine]`, `is_synthetic: bool = True`.
  - `AuditReport`: `audit_id: str`, `status: AuditStatus`, `rule_set_version: str`, `evidence_snapshot_id: str`, `created_at: str`, `findings: list[Finding]`, `input_gaps: list[str]`, `disclaimer: str`.
  - `Finding`: `id: str`, `rule_id: str`, `severity: SeverityLevel`, `title: str`, `explanation: str`, `input_facts_used: dict[str, Any]`, `missing_data_status: list[str]`, `guideline_discussion_prompt: str | None`, `evidence: EvidenceReference`.

#### B. API Entry Points (`services/api/app/main.py`)
- `GET /health` and `/api/v1/health`: Returns service metadata, `engine_mode: "deterministic_isolated"`.
- `POST /v1/extractions` and `/api/v1/extractions`: Accepts prescription file upload, invokes `ExtractionAdapter`, returns confidence-rated draft JSON.
- `POST /v1/audits` and `/api/v1/audits`: Accepts confirmed `AuditRequest`, invokes `DeterministicAuditEngine.evaluate()`, returns `AuditReport`.
- `GET /v1/metrics` and `/api/v1/metrics`: De-identified aggregate stewardship metrics (zero PHI).
- `GET /v1/evidence` and `/v1/evidence/{evidence_id}`: Evidence citations and guideline locators.

---

### 1.5 Referenced Datasets in `data_sets/`

- **Directory**: `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets`:
  - `AMR_ANALYZED_DATA_PACKAGE/who_aware_antibiotics.csv` (38,537 bytes, 378 records):
    Full WHO AWaRe classification mapping antibiotics and combinations into `Access`, `Watch`, `Reserve`, and `Not Recommended`. Contains banned fixed-dose combinations and indication recommendations.
  - `AMR_ANALYZED_DATA_PACKAGE/amr_chatbot_corpus.jsonl` (4,940,992 bytes, 3,844 records):
    Verified surveillance records and clinical excerpts from NCDC NARS-Net, ICMR, and WHO reports.
  - `AMR_ANALYZED_DATA_PACKAGE/icmr_surveillance_pages.csv` (2,175,630 bytes) & `ncdc_evidence_clean.csv` (390,507 bytes).
  - `amr_knowledge_base/AMR_KNOWLEDGE_BASE.md` (6,839,612 bytes) & `AMR_KNOWLEDGE_INDEX.yaml` (2,117,620 bytes):
    Comprehensive knowledge base covering Indian AMR patterns, ICMR treatment guidelines, antibiograms, and pathogen-drug pairings.
  - `aware-essentialmeds-org-list-awareGroup-Not-recommended.md` (41,442 bytes) & `aware-essentialmeds-org-list.md` (148,863 bytes):
    Lists unrecommended antimicrobial formulations and rationales.
  - `apps/web/lib/sample-cases.ts`:
    6 synthetic golden test cases covering:
    1. `SYN_CASE_01_PEDIATRIC_CQ` -> `NEEDS_URGENT_REVIEW`
    2. `SYN_CASE_02_GERIATRIC_RENAL` -> `NEEDS_URGENT_REVIEW`
    3. `SYN_CASE_03_VIRAL_BRONCHITIS` -> `NEEDS_REVIEW`
    4. `SYN_CASE_04_AWARE_RESERVE` -> `NEEDS_REVIEW`
    5. `SYN_CASE_05_INCOMPLETE_DATA` -> `INCOMPLETE_DATA`
    6. `SYN_CASE_06_CLEAN_GUIDELINE` -> `NO_RULE_TRIGGERED`

---

## 2. Logic Chain

1. **AI Intake Boundary Integrity**:
   - From Section 1.1, the AI agent is confined strictly to `services/api/app/extraction/adapter.py` and returns only editable drafts to `PrescriptionStepper.tsx`.
   - From Section 1.3A, the AST import isolation test (`test_architecture_isolation.py`) strictly forbids importing any AI, LLM, HTTP, or DB modules into `services/api/app/engine/`.
   - *Deduction*: Enhancing the AI agent (e.g. prompt calibration, few-shot examples, dictionary grounding) in `app/extraction/` will not violate the deterministic safety boundary or break AST isolation as long as all LLM/extraction code remains isolated within `app/extraction/`.

2. **Root Causes of Extraction Inaccuracy**:
   - In `_extract_with_gemini` (Section 1.1B), the prompt is a generic single-sentence instruction without any few-shot examples.
   - The model is not informed about standard Indian prescription conventions (BD, TID, OD, Q8H) or brand-to-generic mappings (Augmentin -> Amoxicillin-Clavulanate, Cifran -> Ciprofloxacin, Martifur -> Nitrofurantoin, Zifi-AZ -> Cefixime + Azithromycin).
   - The model has no list of canonical indication codes (`SYN_CAP_MILD`, `SYN_UNCOMPLICATED_UTI`, `SYN_ACUTE_BRONCHITIS`, `SYN_WATERY_DIARRHEA`, etc.), leading to hallucinated or non-standard indication strings that will fail downstream schema validation or miss rule triggers.
   - *Deduction*: Calibrating the prompt with structured few-shot examples and condition code mappings derived from `apps/web/lib/sample-cases.ts` and `data_sets/AMR_ANALYZED_DATA_PACKAGE/who_aware_antibiotics.csv` will directly improve extraction precision and grounding.

3. **Weakness in Offline Fallback Heuristics**:
   - In `_extract_with_local_heuristics` (Section 1.2B), only 11 drug keywords are recognized. Common antibiotics (e.g., Cefalexin, Ceftriaxone/Monocef, Doxycycline, Linezolid, Colistin, banned FDCs like Cefixime + Azithromycin) are unrecognized and default to Amoxicillin.
   - The condition code in offline fallback is unconditionally hardcoded to `"SYN_CAP_MILD"`. If a synthetic prescription clearly states "acute diarrhea" or "uncomplicated cystitis", the offline fallback erroneously labels it as mild pneumonia.
   - *Deduction*: Expanding the offline heuristic regex and keyword dictionary using `DRUG_CATALOG` (`apps/web/lib/clinical-data.ts`) and `CONDITION_CATALOG` will allow the offline extractor to accurately parse all 6 golden synthetic cases and common clinical variants without external network access.

4. **Missing Automated Benchmark Evaluation Suite**:
   - From Section 1.5 and inspection of `scripts/`, there is currently no benchmark evaluation script that executes against a test split derived from `data_sets` and quantitatively compares extraction accuracy between baseline and enhanced agent.
   - *Deduction*: An automated evaluation runner (e.g. `scripts/evaluate_agent.py`) must be created to satisfy Acceptance Criterion 1 of the original request (`ORIGINAL_REQUEST.md`, lines 29–31).

---

## 3. Caveats

- **No Caveats on Codebase Exploration**: The entire backend (`services/api`), frontend (`apps/web`), specifications (`specs/AMR-Sentinel`), and data packages (`data_sets`) were inspected directly.
- **External Network Dependency for Gemini**: While `GEMINI_API_KEY` is present in `.env`, actual network calls to `generativelanguage.googleapis.com` depend on internet connectivity and Google API quota. The fallback to local offline heuristics is tested and verified to operate seamlessly when the key or network is unavailable.
- **Read-Only Scope**: In adherence to explorer role rules, no source files were modified during this investigation.

---

## 4. Conclusion

1. **Architecture Status**: The existing two-layer clinical safety architecture is robustly designed and verified by build-time AST checks. The deterministic clinical audit core in `app/engine/` is completely decoupled from the assistive intake layer in `app/extraction/`.
2. **Current Agent Limitations**: The AI extraction agent currently relies on a minimal zero-shot prompt with zero few-shot demonstrations, no brand-to-generic dictionary grounding, and an offline fallback that hardcodes condition codes to `SYN_CAP_MILD`.
3. **Enhancement Vector**:
   - Calibrate `ExtractionAdapter._extract_with_gemini` with few-shot synthetic prescription examples and schema-grounded condition code guidance.
   - Expand `ExtractionAdapter._extract_with_local_heuristics` with brand-to-generic matching from `data_sets/AMR_ANALYZED_DATA_PACKAGE/who_aware_antibiotics.csv` and regex condition classification from `apps/web/lib/clinical-data.ts`.
   - Develop an automated evaluation benchmark script (`scripts/evaluate_agent.py`) running against a benchmark split of synthetic cases to measure precision, recall, and exact match accuracy across cloud API and offline fallback modes.

---

## 5. Verification Method

To independently verify the findings in this report, execute the following commands:

1. **Verify AST Isolation of Engine (Pure Python, Zero LLM, Zero Network, Zero DB)**:
   ```powershell
   powershell -ExecutionPolicy Bypass -Command "$env:PYTHONPATH = 'services/api'; .\.venv\Scripts\pytest.exe services/api/tests/test_architecture_isolation.py -v"
   ```
   *Expected outcome*: 2 passed (verifying zero prohibited imports in `services/api/app/engine/`).

2. **Verify Full Existing Test Suite**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/test.ps1
   ```
   *Expected outcome*: Ruff passes, 24 pytest tests pass, Next.js TypeScript type check passes.

3. **Inspect AI Agent Files**:
   - `services/api/app/extraction/adapter.py`: Lines 40–49 (prompt) and 80–152 (fallback heuristics).
   - `services/api/app/config.py`: Line 51 (`GEMINI_API_KEY`).
   - `services/api/app/engine/engine.py`: Lines 21–166 (deterministic audit evaluation).
   - `services/api/app/rules_data/rules_v1.0.0.json`: Rules manifest and evidence catalog.

4. **Invalidation Conditions**:
   - If any prohibited module (e.g. `google`, `httpx`, `supabase`) is imported inside `services/api/app/engine/`, `test_architecture_isolation.py` fails immediately.
   - If `GEMINI_API_KEY` is revoked or offline, `ExtractionAdapter.extract_from_bytes` must catch the exception and fall back to `_extract_with_local_heuristics` without raising a 500 error to the client.
