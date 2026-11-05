# AMR Sentinel AI

> **Clinician-Assistive Antimicrobial Prescription Auditing & Stewardship Platform**  
> *Grounded in ICMR Standard Treatment Guidelines 2022, WHO AWaRe Classification 2023, and CDSCO Banned Fixed-Dose Combination Directives.*

---

## 🏥 Clinical Safety Architecture: Two-Layer Model

AMR Sentinel AI is a clinical decision-support prototype built on a strict two-layer boundary:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ASSISTIVE INTAKE LAYER (Untrusted)                    │
│                 (Gemini Multimodal OCR / Offline Heuristics)                │
│                                                                             │
│  • Ingests synthetic prescription images, PDFs, or manual clinical forms    │
│  • Drafts structured patient context, eGFR, pregnancy, and medications      │
│  • Labels each field with extraction confidence                             │
│  • CRITICAL: AI output is untrusted until explicitly confirmed by clinician │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Human Clinician Confirmation
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DETERMINISTIC CLINICAL AUDIT CORE                       │
│              (Pure Python • Zero Network • Zero LLMs • Zero DB)             │
│                                                                             │
│  • Tier 1: Absolute Contraindications (Pediatric, Pregnancy, Renal eGFR)    │
│  • Tier 2: Indication Legitimacy & CDSCO Banned FDC Checks                  │
│  • Tier 3: WHO AWaRe Spectrum De-escalation Alerts (Access vs Watch/Reserve)│
│  • Tier 4: ICMR Short-Course Treatment Duration Limits                      │
│  • Verified at build-time via Python Abstract Syntax Tree (AST) isolation   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLINICAL AUDIT REPORT                             │
│  [NEEDS URGENT REVIEW (Red) • NEEDS REVIEW (Amber) • NO RULE TRIGGERED]     │
│  • Traceable findings with rule ID, evidence excerpts, and data gaps        │
│  • Non-prescriptive guideline discussion options (never auto-substitutes)   │
│  • Append-only clinician review & override documentation                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Safety Prohibitions (What AMR Sentinel NEVER Does):
1. **Never diagnoses** a patient or condition.
2. **Never issues** or calculates definitive medication prescriptions or doses.
3. **Never auto-substitutes** or discontinues therapy autonomously.
4. **Never describes** a prescription as "safe", "approved", or "correct" (`No Rule Triggered` indicates non-breach of configured rules, not clinical validation).
5. **Never assumes** missing data (e.g. absent eGFR) is normal.

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js 18+ (tested on Node.js v25)

### 1. Clone & Setup Environment
```bash
# Copy root environment template
copy .env.example .env
```

### 2. Start the Backend API (FastAPI)
```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r services/api/requirements-dev.txt

# Run FastAPI local server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir services/api --reload
```
API Documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and Health at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

### 3. Start the Frontend Web App (Next.js)
```bash
cd apps/web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Quality Gates & Automated Verification

Run all test suites and architectural checks with one command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test.ps1
```

Or run targeted verification steps individually:

```bash
# 1. AST Engine Import Isolation Test (Enforces pure Python, 0 network, 0 LLM, 0 DB)
pytest services/api/tests/test_architecture_isolation.py -v

# 2. Clinical Rules Unit Test Suite (24 test scenarios: trigger, non-trigger, boundary, gaps)
pytest services/api/tests/test_rules.py -v

# 3. API Contract & Intake Tests
pytest services/api/tests/test_audits_api.py services/api/tests/test_extractions.py -v

# 4. Ruff Strict Linter & Formatting
ruff check services/api

# 5. Frontend Strict TypeScript Type Check
cd apps/web && npm run type-check
```

---

## 📋 The 6 Golden Synthetic Demonstration Cases

| Case ID | Scenario | Suspected Condition | Prescribed Regimen | Deterministic Outcome | Clinical Rule Evaluated |
|---|---|---|---|---|---|
| **Case 1** | Pediatric Contraindication | Acute Diarrhea | Ciprofloxacin 250mg BD | **`NEEDS_URGENT_REVIEW`** | `SAFETY.PED.FQ_UNDER_18` (Cartilage erosion & arthropathy) |
| **Case 2** | Severe Renal Impairment | Uncomplicated UTI | Nitrofurantoin 100mg BD (eGFR 22) | **`NEEDS_URGENT_REVIEW`** | `SAFETY.RENAL.NITROFURANTOIN_EGFR_LT_30` (Beers Criteria) |
| **Case 3** | Viral Acute Bronchitis | Acute Bronchitis | Azithromycin 500mg OD | **`NEEDS_REVIEW`** | `STEWARDSHIP.VIRAL.ACUTE_BRONCHITIS` (>90% viral etiology) |
| **Case 4** | WHO AWaRe Reserve Escalation | Uncomplicated UTI | Meropenem 1g IV TDS | **`NEEDS_REVIEW`** | `STEWARDSHIP.AWARE.RESERVE_ESCALATION` (Reserve agent protection) |
| **Case 5** | Critical Data Gap | Acute Pyelonephritis | Gentamicin 80mg (eGFR missing) | **`INCOMPLETE_DATA`** | `SAFETY.RENAL.MISSING_EGFR_HOLD` (KDIGO nephrotoxicity hold) |
| **Case 6** | Guideline-Concordant First-Line | Mild CAP | Amoxicillin 500mg TID x 5d | **`NO_RULE_TRIGGERED`** | Concordant with ICMR STG 2022 Mild CAP; Access class |

---

## 🗄️ Supabase Schema & Row Level Security (RLS)

All database tables have Row Level Security enabled:
- **`profiles`**: User profile linked to `auth.users`
- **`organizations`**: Multi-tenant institutional boundary
- **`organization_memberships`**: RBAC (`org_admin`, `clinician`, `clinical_reviewer`)
- **`cases` & `prescription_lines`**: Patient context & entered medication lines
- **`audit_runs` & `audit_findings`**: Immutable, append-only deterministic audit history
- **`acknowledgements`**: Audit trail of clinician review and overrides
- **`rule_set_versions`, `evidence_sources`, `evidence_snapshots`**: Versioned clinical guidelines
- **`document_assets`**: Private object metadata pointing to private storage bucket

Migrations are located in [`supabase/migrations/20261105000000_initial_schema.sql`](supabase/migrations/20261105000000_initial_schema.sql) and [`supabase/seed.sql`](supabase/seed.sql).

---

## ⚠️ Known Limitations & Clinical Validation Roadmap

1. **Hackathon Prototype Status**: This software is an engineering proof-of-concept for antimicrobial stewardship and has not undergone formal clinical trial clearance.
2. **Synthetic Data Policy**: All data shipped or demonstrated is 100% synthetic. Zero Protected Health Information (PHI) is processed or stored.
3. **Local Formulary Customization**: Rules are grounded in ICMR STG 2022 and WHO AWaRe 2023. Real clinical deployment requires institutional review and local hospital antibiogram calibration.
