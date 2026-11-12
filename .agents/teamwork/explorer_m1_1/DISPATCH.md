## 2026-11-09T20:57:59Z
You are explorer_m1_1 (role: Benchmark Cases & Ground Truth Specialist).
Your working directory is: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_m1_1\
Your parent orchestrator is conversation ID: 01b31f9d-d7a9-4fca-9bcc-706835e55498

MANDATORY FIRST STEP:
Read the authoritative user request at:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md
and the project roadmap at:
c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md

TASK:
For Milestone 1 (Benchmark Test Split & Evaluation Harness):
1. Design the exact schema and clinical cases for a 25-30 case benchmark test split to be saved in services/api/tests/data/benchmark_cases.json.
2. The benchmark cases must be derived from authentic data in c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets (including Tamil/Hopsital Dataset.csv, Tamil/Anti/, and apps/web/lib/sample-cases.ts).
3. Ensure comprehensive coverage across:
   - 4 Pediatric cases (Ciprofloxacin under 18, Doxycycline under 12, Amoxicillin guideline pass, Azithromycin)
   - 4 Renal/Geriatric cases (Nitrofurantoin eGFR 22, Nitrofurantoin eGFR 85, Gentamicin missing eGFR, Amikacin normal eGFR)
   - 3 Pregnancy cases (Doxycycline pregnant, Ciprofloxacin pregnant, Cefalexin pregnant pass)
   - 3 Allergy cases (Penicillin allergy + Amoxicillin, Penicillin allergy + Azithromycin, no allergy)
   - 3 Banned FDC cases (Cefixime + Azithromycin, Ofloxacin + Ornidazole, Amoxicillin + Flucloxacillin)
   - 4 Viral self-limiting cases (Acute bronchitis + Azithromycin, Common cold + Amoxicillin, Viral URTI + Paracetamol only, Non-strep pharyngitis + Cefixime)
   - 2 AWaRe Reserve cases (Meropenem for mild UTI, Linezolid for mild SSTI)
   - 2 Excessive Duration cases (Amoxicillin 14d for CAP, Nitrofurantoin 10d for cystitis)
   - 5 Clean Guideline-concordant cases (Amoxicillin 5d CAP, Nitrofurantoin 5d UTI, ORS + Zinc diarrhea, Cefalexin 5d SSTI, Paracetamol viral)
4. For each case, specify:
   - `id`: unique identifier
   - `clinical_scenario`: realistic prescription text (simulating real doctor's note or OCR output with authentic Indian brands/abbreviations)
   - `ground_truth`: expected patientContext (age, gender, isPregnant, egfrMlMin, allergies), indicationCode (canonical SYN_*), prescriptionLines (generic drugName, doseText, frequencyText, durationDays)
   - `expected_audit`: expected status (NEEDS_URGENT_REVIEW, NEEDS_REVIEW, INCOMPLETE_DATA, NO_RULE_TRIGGERED) and triggered rule IDs.
5. Provide the complete JSON template and recommended implementation plan for the worker.
