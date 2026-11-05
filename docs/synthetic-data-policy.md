# AMR Sentinel AI — Synthetic Data & Clinical Safety Policy

## 1. Synthetic Data Mandate
- **100% Synthetic Records**: All patient demographics, clinical scenarios, prescription images, and lab results used across development, automated tests, local seeds, demo presentations, and telemetry are strictly synthetic and generated for demonstration and verification purposes.
- **No Real PHI**: Under no circumstances may real patient names, national identifiers, medical record numbers (MRN), contact information, or authentic identifiable clinical records be committed to source control or ingested into the prototype.
- **Explicit Synthetic Labelling**: All synthetic database records carry `is_synthetic = TRUE` and synthetic UI badges indicate demo status.

## 2. Redaction and Privacy Guardrails
- **Zero-PHI Logging**: API logs and error responses must never dump raw free-text clinical notes, un-redacted document text, patient names, or sensitive identifiers.
- **Traceability via Opaque IDs**: All events are tracked using pseudo-random UUIDs and correlation trace IDs (`trace_id`).
- **Private Storage Isolation**: Uploaded prescription images/PDFs are stored in private, access-controlled buckets with short-lived signed URLs. Public access is forbidden.
- **De-identified Stewardship Analytics**: Aggregate institutional metrics report only anonymized counts, AWaRe percentages, and rule trigger frequencies.

## 3. Clinical Non-Prescriptive Notice
- AMR Sentinel AI is an assistive audit and stewardship exploration tool.
- The platform does not diagnose, does not calculate definitive doses, does not generate prescriptions, and does not replace the clinical judgment of a licensed healthcare practitioner.
- Guideline-concordant options are presented strictly as discussion prompts referencing ICMR STG 2022 and WHO AWaRe 2023 with reminders to verify local antimicrobial stewardship policies.
