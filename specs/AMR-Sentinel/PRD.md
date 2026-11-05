# AMR Sentinel AI — Product Requirements Document

**Status:** Hackathon prototype specification • **Version:** 0.1 • **Audience:** builders, reviewers, clinicians

## 1. Product definition

AMR Sentinel AI is a **clinical prescription-auditing and antimicrobial-stewardship platform**. It accepts a structured entry or an uploaded prescription, highlights safety and stewardship concerns, and presents evidence-linked review prompts for a qualified clinician.

The product is **not** a diagnostic, prescribing, or autonomous substitution system. It is a demo/prototype until rules and evidence are clinically validated, approved, and governed for the intended setting.

### Scope clarification

A prior sentence about “building websites and services” conflicts with this project’s healthcare scope. For this specification, AMR Sentinel is exclusively a prescription-auditing product. Website-building, web-agency, and unrelated service-delivery features are out of scope unless explicitly confirmed later.

## 2. Problem and users

Antibiotics may be used unnecessarily, too broadly, or despite patient-specific risks. Clinicians need a fast second-check that makes the reasoning visible without replacing their judgement.

| User | Need | Prototype outcome |
|---|---|---|
| Prescriber / clinician | Check an intended prescription quickly | Clear review report and evidence links |
| Stewardship pharmacist | Review patterns and rule hits | Case history and aggregate, de-identified metrics |
| Clinical reviewer / admin | Maintain evidence and rules safely | Versioned, reviewable rule/evidence records |
| Hackathon judge | Understand impact and workflow | Guided sample cases and polished demo flow |

## 3. Goals and success measures

- Audit a structured demo case end-to-end in under 3 seconds locally (excluding OCR).
- Show a plain-language status: **Needs urgent review**, **Needs review**, or **No rule triggered**; never imply clinical approval.
- Explain every finding with rule ID, evidence source/version, input used, and uncertainty.
- Support at least six synthetic cases covering viral indication, broad-spectrum flag, pregnancy/renal/age alerts, allergy/interaction, banned/unsupported fixed-dose combination, and a clean review case.
- Keep clinical decisions deterministic and reproducible for the same structured inputs and evidence version.

## 4. MVP features

1. **Case intake:** manual patient context (age band, pregnancy status, allergies, eGFR/renal status, indication, setting) and prescription-line entry.
2. **Upload/extract:** image/PDF upload; OCR/extraction returns editable, confidence-labelled draft fields. Extraction must not audit until a human confirms inputs.
3. **Deterministic audit:** evaluate configured rules for contraindications, viral/self-limiting indication prompts, allergy/interaction checks, dose/duration completeness, AWaRe class and broad-spectrum stewardship flags, and configured banned/unsupported combinations.
4. **Results:** risk/review level, grouped findings, plain-language reasons, input gaps, evidence provenance, and clinician acknowledgement/notes.
5. **Alternatives:** display only guideline-configured *discussion options*, never an automatic replacement or prescription; show “confirm with current local guidance”.
6. **Demo dashboard:** sample synthetic cases, recent cases for the signed-in demo user, and de-identified rule-hit aggregates.
7. **API:** documented FastAPI endpoints for extraction, audit, cases, evidence, and health checks.

## 5. Non-goals

- Autonomous diagnosis, prescribing, dispensing, dose calculation, or medication substitution.
- Real patient deployment, emergency triage, or reliance as the sole clinical decision-maker.
- Training a clinical ML model, scraping private health data, or importing real patient records for the hackathon.
- Guarantees that a suggestion is correct, complete, locally applicable, or current.

## 6. Core workflow

1. User signs in and selects a synthetic sample or starts a case.
2. User enters data or uploads a document; extraction proposes editable fields with confidence and missing-data prompts.
3. User confirms the structured facts, indication, and medication lines.
4. Backend snapshots the evidence/rule versions and runs the pure deterministic engine.
5. UI shows findings and evidence; clinician records an acknowledgement or correction.
6. Only minimum necessary, access-controlled audit data is retained. The user can delete a demo case.

## 7. Acceptance criteria

- Every audit response contains `audit_id`, `rule_set_version`, `evidence_snapshot_id`, `status`, `findings`, `input_gaps`, and disclaimer metadata.
- A missing or low-confidence value produces an “unknown / needs confirmation” result, never an assumed normal value.
- A hard safety rule cannot be bypassed silently; a clinician may document an override only where the rule policy permits it.
- A failed OCR/AI provider does not block manual entry or the deterministic audit.
- Sample data is conspicuously marked synthetic. Production-like PHI is not included in source control, screenshots, tests, or logs.

## 8. Delivery and cost posture

Use free/open-source local tooling first: Node LTS, Python, Docker optional, Next.js/React/TypeScript/Tailwind, FastAPI/Pydantic/Pytest, and Supabase free tier where available. Deploy frontend to Vercel and API to Railway only after verifying each provider’s current quotas, sleep behavior, database/network limits, and terms. Free tiers can change and are not permanent.

Local-first fallback: run Next.js + FastAPI locally; use seeded synthetic data and a local Postgres/SQLite development adapter when cloud credits or connectivity are unavailable. External OCR/LLM is optional and must degrade to manual entry.

## 9. Reference context

This specification is informed by the public [AMR Sentinel reference repository](https://github.com/amishverma19/amr-sentinel), particularly its separation of AI-assisted intake from a deterministic rules engine. It is not a claim that the reference implementation or its clinical content has been independently validated.
