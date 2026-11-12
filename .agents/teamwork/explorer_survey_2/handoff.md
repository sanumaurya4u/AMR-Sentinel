# Datasets & Knowledge Base Investigation Handoff Report

**Agent**: `explorer_survey_2` (Datasets & Knowledge Base Explorer)  
**Date**: 2026-11-09T20:58:00Z  
**Target Directory**: `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets`  
**Working Directory**: `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2`  
**Parent Orchestrator**: `01b31f9d-d7a9-4fca-9bcc-706835e55498`  

---

## 1. Observation

A comprehensive, non-destructive filesystem survey of `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets` was performed using custom survey scripts (`survey_datasets.py`, `deep_analyze.py`, `inspect_hospital.py`, `inspect_anti.py`, `inspect_package.py`). The dataset directory comprises **74 files** totaling **228.38 MB (239,470,591 bytes)** organized into 11 subdirectories and 4 root files.

### 1.1 Complete Directory Inventory & File Metrics

| Directory / Path | File Count | Size (MB) | Formats | Primary Contents & Description |
|---|---|---|---|---|
| **Root (`data_sets/`)** | 4 files | 72.81 MB | `.csv`, `.md` | `WHO_RELAY_AMR.csv` (72.6 MB, 214,368 rows), `aware-essentialmeds-org-list.md` (145.4 KB), `aware-essentialmeds-org-list-awareGroup-Not-recommended.md` (40.5 KB, 107 banned/not-recommended FDCs), `IND data-who-int-dashboards-amr-antimicrobial-resistance-profile.md` (15.9 KB, India national AMR rates). |
| **`AMR_ANALYZED_DATA_PACKAGE/`** | 11 files | 12.63 MB | `.csv`, `.jsonl` | Cleaned machine-trainable AMR surveillance & ontology corpus: `amr_chatbot_corpus.csv` (22,105 rows), `amr_chatbot_corpus.jsonl` (3,843 records), `ncdc_rag_clean.csv` (19,357 rows), `icmr_surveillance_pages.csv` (1,354 rows), `ncdc_evidence_clean.csv` (5,443 rows), `who_amr_canonical.csv` (1,020 rows), `who_aware_antibiotics.csv` (376 rows), `PACKAGE_MANIFEST.csv`, `amr_data_quality_report.csv`, `amr_surveillance_trend_summary.csv`. |
| **`amr_knowledge_base/`** | 5 files | 8.76 MB | `.md`, `.yaml`, `.csv` | Verified RAG-ready knowledge base: `AMR_KNOWLEDGE_BASE.md` (6.68 MB, 180,379 lines, 3,843 YAML-header records), `AMR_KNOWLEDGE_INDEX.yaml` (2.07 MB, 65,337 lines), `AMR_KNOWLEDGE_VALIDATION.yaml` (43 lines), `AMR_SOURCE_INDEX.yaml` (401 lines, 28 sources), `AMR_KNOWLEDGE_MANIFEST.csv`. |
| **`Tamil/`** | 5 files | 0.20 MB | `.csv`, `.xlsx` | `Hopsital Dataset.csv` (833 clinical prescription rows), `AMRGuard_antibiotic_180_master_clinical_dataset.xlsx` (41.1 KB), `antibiotic_180_usage_symptoms_fda_complete.csv` (181 rows), `antibiotic_usage_side_effects_fda_starter.csv` (41 rows), `uploaded_antibiotic_lookup_3col.csv` (71 rows). |
| **`Tamil/Anti/`** | 6 files | 0.02 MB | `.csv`, `.yaml` | Structured clinical ontology & rules: `brands.csv` (77 Indian brand names), `conditions.csv` (36 condition codes with `SYN_` prefix), `drugs.csv` (80 drugs with AWaRe class & contraindications), `guidelines.csv` (36 ICMR STG 2022 condition guidelines), `regimens.csv` (60 verified empiric regimens), `rules.yaml`. |
| **`Tamil/New folder/`** | 2 files | 0.08 MB | `.csv` | `antibiotic_brand_to_generic_alias_lookup.csv` (405 rows: 403 unique Indian brand aliases mapped to 180 generic antibiotics), `antibiotic_180_with_brand_names_master.csv` (181 rows). |
| **`Tamil/New folder 2/`** | 3 files | 0.32 MB | `.csv` | `AMRGuard_antibiotic_master_180_expanded.csv` (181 rows: FDA indications, adverse effects, mechanisms, precautions), `AMRGuard_antibiotic_180_source_research_queue.csv` (181 rows), `AMRGuard_antibiotic_master_180_research_progress.csv`. |
| **`icmr/`** | 8 files | 95.45 MB | `.pdf` | ICMR Antimicrobial Resistance Surveillance Network (AMRSN) annual reports (2017 to 2024). |
| **`amr/`** | 9 files | 13.13 MB | `.pdf` | National Centre for Disease Control (NCDC) NARS-Net annual surveillance reports (2017 to 2025). |
| **`amrc/`** | 3 files | 4.02 MB | `.pdf` | NCDC National Antibiotic Consumption Network (NAC-NET) annual reports (2022 to 2024). |
| **`india relevant/`** | 5 files | 9.93 MB | `.pdf` | Peer-reviewed genomic studies on Indian isolates: TB WGS (Bhanushali 2024), blaNDM-1/blaNDM-5 in E. coli ST167 (Bhattacharjee 2025), carbapenem-resistant blood isolates (Halder 2024), cephalosporin-resistant S. Typhi (Thirumoorthy 2025), anti-tubercular surveillance (Rao 2023). |
| **`AYUSH_AMR_KNOWLEDGE_BASE_PACKAGE/`** | 2 files | 0.02 MB | `.md`, `.yaml` | `AYUSH_AMR_KNOWLEDGE_BASE.md` (10 curated evidence records on traditional medicine/adjuvants), `AYUSH_AMR_SOURCE_INDEX.yaml`. |
| **`ayur/` & `homeo/`** | 9 files | 4.67 MB | `.pdf`, `.md` | Published reviews and lab studies on Ayurvedic and Homeopathic adjuvant therapies and antimicrobial properties. |
| **`GOV/`** | 2 files | 12.30 MB | `.pdf`, `.md` | `National One Health Mission.pdf` (12.3 MB) and PIB Press Release (PRID 2209331) on One Health AMR governance. |

---

### 1.2 Clinical Prescription Dataset (`Tamil/Hopsital Dataset.csv`)

Deep inspection of `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\Tamil\Hopsital Dataset.csv` revealed:
- **Total records**: 833 rows (832 valid patient prescription records, 1 malformed header duplicate row at index 529: `Age='Age', Date of Data Entry='#REF!', Gender='Sex'`).
- **Schema**:
  - `Age` (float/int): Patient age.
  - `Date of Data Entry` (string): Timestamp (e.g. `19/12/2019 14:41:49`).
  - `Gender` (string): `Male` (449 records, 54.0%), `Female` (382 records, 45.9%), corrupt token `Sex` (2 records).
  - `Diagnosis` (string): Unstructured, authentic South Asian clinical free-text co-morbidities.
  - `Name of Drug` (string): Prescribed brand or generic antibiotic.
  - `Dosage (gram)` (float/string): Drug dose expressed in grams (e.g., `1`, `0.5`, `1.2`, `0.2`, `0.625`).
  - `Route` (string): Administration route (`IV`: 534 [64.1%], `Oral`: 293 [35.2%], `IM`: 4 [0.5%], `Route`: 2).
  - `Frequency` (string): Latin clinical frequency abbreviation (`BD`: 430 [51.6%], `TDS`: 283 [34.0%], `OD`: 110 [13.2%], `QID`: 8 [1.0%]).
  - `Duration (days)` (int/string): Treatment duration (`1`: 270, `5`: 151, `2`: 91, `3`: 78, `7`: 74, `4`: 69, `8`: 28, `6`: 25, `10`: 22, `14`: 18).
  - `Indication` (string): Primary infection or symptom warranting antimicrobial therapy.

#### Key Demographic & Clinical Subsets
- **Pediatric Patients (<18 years)**: 33 cases (ages 1 to 17). Highlights include:
  - Row 347-353: Ages 13-15 with Dengue Fever / DHF (Dengue Hemorrhagic Fever) prescribed Ceftriaxone 1g BD, Cefixime 0.2g BD, and Metronidazole 0.75g TDS (inappropriate antimicrobial stewardship in viral hemorrahagic fever).
  - Row 403-405, 829-831: Age 15 with "glandular fever, measles, viral encephalitis" prescribed Ceftriaxone 2g BD and Cefixime 0.2g BD.
  - Row 419-420: Age 13 with haematological malignancy prescribed Amikacin 0.25g BD and Cefaziclime (Ceftazidime typo) 1g TDS (nephrotoxic aminoglycoside requiring eGFR monitoring).
  - Row 625: Age 17 with "anaphylaxis (?penicillin)" prescribed Clindamycin 0.3g TDS (appropriate cross-reactivity avoidance).
  - Row 378: Age 1.0 (infant) with "fever with malaena" prescribed Flucloxacillin 0.125g BD.
- **Geriatric Patients (>=65 years)**: 235 cases (28.2%), frequently with Stage 5 CKD, CCF, and severe chest infections.
- **Top Prescribed Antibiotics**:
  1. `ceftriaxone`: 221 (26.5%)
  2. `co-amoxiclav` (including `coamoxiclav`): 171 (20.5%)
  3. `metronidazole`: 59 (7.1%)
  4. `cefixime`: 58 (7.0%)
  5. `septrin` (Co-trimoxazole brand): 37 (4.4%)
  6. `clarithromycin`: 32 (3.8%)
  7. `levofloxacin`: 31 (3.7%)
  8. `amoxicillin+flucloxacillin`: 29 (3.5% - notable WHO Not-Recommended FDC!)
  9. `ceftazidime`: 24 (2.9%)
  10. `cefepime` (including typo `cefipime`): 27 (3.2%)
  11. `clindamycin`: 12 (1.4%)
  12. `rifaximin`: 10 (1.2%)
  13. `amikacin`: 9 (1.1%)
  14. `cefoperazone`: 9 (1.1%)
  15. `meropenem`: 8 (1.0%)
  16. `ciprofloxacin` / `cifran`: 11 (1.3%)

---

### 1.3 Clinical Ontology & Standard Regimens (`Tamil/Anti/`)

The `Tamil/Anti/` directory provides authoritative clinical mapping files:
1. **`conditions.csv` (36 records)**:
   - Contains clinical condition IDs and standardized `SYN_` codes: `SYN_CAP_MILD` (Community-Acquired Pneumonia Mild), `SYN_UNCOMPLICATED_UTI` (Acute Cystitis), `SYN_ACUTE_BRONCHITIS` (Self-Limiting Viral), `SYN_COMMON_COLD` (Rhinopharyngitis), `SYN_VIRAL_URTI` (Upper Respiratory), `SYN_WATERY_DIARRHEA` (Non-Cholera), `SYN_PHARYNGITIS_STREP` (Group A Strep), `SYN_AOM` (Acute Otitis Media).
   - These condition codes **match 1:1** with the condition keys in `services/api/app/rules_data/rules_v1.0.0.json`.
2. **`drugs.csv` (80 records)**:
   - Fields: `id`, `generic_name`, `drug_class`, `is_antibiotic`, `aware_class`, `is_fluoroquinolone`, `pregnancy_contraindicated`, `min_age_years`.
   - Examples: Amoxicillin (`Access`, `min_age_years: 0.0`), Ciprofloxacin (`Watch`, `is_fluoroquinolone: True`, `pregnancy_contraindicated: True`, `min_age_years: 18.0`), Doxycycline (`Access`, `pregnancy_contraindicated: True`, `min_age_years: 12.0`).
3. **`guidelines.csv` (36 records)**:
   - Authoritative ICMR STG 2022 guidelines.
   - Distinctly flags `antibiotic_indicated: False` for viral acute bronchitis, common cold, viral URTI, non-strep pharyngitis, and watery diarrhea.
4. **`regimens.csv` (60 records)**:
   - Prescribes exact ICMR-endorsed dosage, frequency, and duration:
     - Mild CAP: Amoxicillin 500mg TID x 5d (ICMR STG CAP 2022).
     - Acute Cystitis: Nitrofurantoin 100mg BID x 5d, or Fosfomycin 3g single dose (ICMR STG UTI 2022).
     - Symptomatic care: Paracetamol 650mg SOS PRN x 3d for viral infections.
5. **`brands.csv` (77 records)**:
   - Primary Indian brand-to-drug mappings with default strengths (e.g., `Augmentin` -> 625mg, `Clavam` -> 625mg, `Taxim-O` -> 200mg, `Monocef` -> 1g, `Cifran` -> 500mg, `Ciplox` -> 500mg, `Azithral` -> 500mg, `Martifur` -> 100mg).

---

### 1.4 Brand-to-Generic Alias Dictionary (`Tamil/New folder/`)

`antibiotic_brand_to_generic_alias_lookup.csv` contains **405 rows** mapping **403 distinct brand names** across Indian, UK, and global pharmaceutical markets to **180 generic antibiotics**.
- Fields: `brand_alias`, `full_brand_display`, `generic_antibiotic_name`.
- Crucial Indian market aliases covered:
  - `Taxim`, `Taxim-O`, `Zifi`, `Mahacef`, `Cefolac` -> `Cefixime`
  - `Monocef`, `Oframax` -> `Ceftriaxone`
  - `Augmentin`, `Clavam`, `Moxikind-CV`, `Amoxyclav`, `Megaclav` -> `Amoxicillin-Clavulanate`
  - `Cifran`, `Ciplox` -> `Ciprofloxacin`
  - `Azithral`, `Azee`, `Zithrox` -> `Azithromycin`
  - `Martifur`, `Furadantin` -> `Nitrofurantoin`
  - `Septrin`, `Bactrim` -> `Co-trimoxazole`
  - `Meronem`, `Meromac` -> `Meropenem`
  - `Mikacin` -> `Amikacin`
  - `Magnex`, `Sulbacin` -> `Cefoperazone-Sulbactam`

---

### 1.5 WHO AWaRe & CDSCO Prohibited FDCs

1. **`aware-essentialmeds-org-list-awareGroup-Not-recommended.md`**:
   - Contains **107 fixed-dose combinations (FDCs)** explicitly listed in the WHO AWaRe **NOT RECOMMENDED** group.
   - Highlights 43 combinations directly relevant to Indian clinical practices, including:
     - `Amoxicillin + flucloxacillin` (prescribed in 29 cases in `Hopsital Dataset.csv`).
     - `Azithromycin + cefixime` (banned by CDSCO Gazette notification, targeted by `REGULATORY.BANNED_FDC` in `rules_v1.0.0.json`).
     - `Ofloxacin + ornidazole` (banned by CDSCO, targeted by `REGULATORY.BANNED_FDC`).
     - `Cefixime + ofloxacin`, `Azithromycin + levofloxacin`, `Cefpodoxime + azithromycin`.
2. **`who_aware_antibiotics.csv` (376 rows)**:
   - Breakdown: 94 `Access`, 145 `Watch`, 30 `Reserve`, 107 `Not Recommended`.
3. **`IND data-who-int-dashboards-amr-antimicrobial-resistance-profile.md`**:
   - Confirms national Indian surveillance benchmarks:
     - Bloodstream infections due to MRSA: **53.58%**.
     - Bloodstream infections due to E. coli resistant to 3rd-generation cephalosporins (ESBL): **80.1%**.

---

### 1.6 Current State of Repository Extraction & Decision Support

Examination of `services/api/app/extraction/adapter.py`:
- Line 40-49: Prompt for Gemini is brief and ungrounded:
  ```python
  prompt = (
      "Extract clinical prescription facts from this synthetic doctor prescription. "
      "Return JSON matching: { patientContext: ..., indicationCode: ..., prescriptionLines: ..., fieldConfidence: ... }"
  )
  ```
- Lines 99-111: Offline heuristic extractor relies on a crude hardcoded list of only **11 tokens** (`cifran`, `ciprofloxacin`, `augmentin`, `azithral`, `azithromycin`, `martifur`, `nitrofurantoin`, `meronem`, `meropenem`, `gentamicin`, `amoxicillin`).
- Line 139: Hardcoded `"indicationCode": "SYN_CAP_MILD"` for all offline fallback extractions!
- No utilization of the 405-entry alias lookup, no parsing of gram dosages into mg, no translation of BD/TDS/OD/QID into standard frequencies, and no mapping of co-morbidities to `SYN_` condition codes.

---

## 2. Logic Chain

```
[Observation 1.2: Hopsital Dataset.csv (833 real cases, gram dosages, BD/TDS/OD, complex diagnoses)]
  + [Observation 1.3 & 1.4: conditions.csv, brands.csv, 405-entry brand alias lookup]
      │
      ▼ (Step 1: Few-Shot Intake Prompt & Regex Calibration)
The Gemini intake extraction prompt and the local heuristic fallback can be calibrated using authentic clinical Indian prescription patterns.
      │
      ▼ (Step 2: Grounded Knowledge Retrieval / RAG)
[Observation 1.1 & 1.5: amr_knowledge_base (3,843 records), guidelines.csv, WHO AWaRe Not-Recommended]
  + [Observation 1.6: Existing two-layer architecture (assistive intake draft -> deterministic rules core)]
      │
The AI assistant can query amr_knowledge_base and guidelines.csv to generate evidence-backed rationale, pathogen resistance context (e.g. 80.1% ESBL E. coli in India), and ICMR STG suggestions for clinician review, without contaminating or bypassing the deterministic rules engine.
      │
      ▼ (Step 3: Benchmark Test Split & Evaluation Pipeline)
[Observation 1.2 & 1.3: 832 valid clinical records, diverse age/pediatric/geriatric cases, viral vs bacterial]
      │
A rigorous 100-case stratified test split can be synthesized from Hopsital Dataset.csv and Anti/ reference standards. An automated evaluation harness can execute against this benchmark to quantitatively prove improved extraction accuracy, brand resolution recall, and clinical safety detection over baseline.
```

### Detailed Logic Steps:

1. **Intake Extraction Calibration (Addressing R1 & R3)**:
   - *Observation*: Current prompt in `services/api/app/extraction/adapter.py` lacks Indian clinical context, dosage units, frequency mappings, and brand-name disambiguation. The offline heuristic handles only 11 drugs and hardcodes `SYN_CAP_MILD`.
   - *Inference*: By injecting few-shot exemplars derived from `Tamil/Hopsital Dataset.csv` (e.g. showing how `"Rx: Taxim-O 200mg BD x 5d, Dx: Acute cystitis"` maps to `drugName: "Cefixime"`, `doseText: "200 mg"`, `frequencyText: "Twice daily (BD)"`, `durationDays: 5`, `indicationCode: "SYN_UNCOMPLICATED_UTI"`), Gemini's extraction accuracy and adherence to schema will improve significantly.
   - *Offline Heuristic Enhancement*: The offline fallback can ingest `antibiotic_brand_to_generic_alias_lookup.csv` (405 entries) and regex patterns for `(gram)` conversion ($1.2\text{ g} \to 1200\text{ mg}$, $0.625\text{ g} \to 625\text{ mg}$), and match diagnosis keywords to `conditions.csv` (`"cough", "sputum", "fever"` $\to$ `SYN_CAP_MILD`, `"dysuria", "burning micturition"` $\to$ `SYN_UNCOMPLICATED_UTI`, `"cold", "coryza", "runny nose"` $\to$ `SYN_COMMON_COLD`, `"bronchitis"` $\to$ `SYN_ACUTE_BRONCHITIS`).

2. **Knowledge Retrieval Grounding on AMR Packages (Addressing R1 & R2)**:
   - *Observation*: `amr_knowledge_base/AMR_KNOWLEDGE_BASE.md` contains 3,843 structured, verified records covering ICMR surveillance, NCDC resistance evidence, and WHO GLASS metrics. `Tamil/Anti/guidelines.csv` contains exact ICMR STG 2022 treatment pathways.
   - *Inference*: When the user or clinician reviews a prescription draft, the AI assistant can retrieve relevant evidence:
     - If `Ciprofloxacin` is prescribed for acute cystitis in an adult, the agent retrieves Record `ICMR STG UTI 2022` from `guidelines.csv` and local resistance surveillance from `amr_knowledge_base` noting that empiric fluoroquinolones have >75% resistance in *E. coli* in India, and recommends first-line Nitrofurantoin 100mg BD x 5d or Fosfomycin 3g.
     - If `Amoxicillin+Flucloxacillin` is prescribed (found 29 times in `Hopsital Dataset.csv`), the agent retrieves WHO AWaRe classification noting it is in the `Not Recommended` group and suggests standard Amoxicillin-Clavulanate or Cefalexin.
   - *Safety Invariance*: This decision-support retrieval operates strictly in the assistive draft layer. The deterministic audit core (`app/engine/engine.py` evaluating `rules_v1.0.0.json`) remains completely untouched, maintaining the two-layer safety guarantee.

3. **Formulating the Benchmark Evaluation Split (Addressing Acceptance Criteria)**:
   - *Observation*: Acceptance Criteria requires: *"An automated evaluation script executes against a benchmark test split derived from data_sets and verifies improved output quality or extraction accuracy over baseline."*
   - *Inference*: A dedicated evaluation test suite (`services/api/tests/test_benchmark_evaluation.py` or `scripts/evaluate_agent_benchmark.py`) can be built utilizing a curated benchmark dataset of 50-100 golden cases sampled from `Tamil/Hopsital Dataset.csv` and cross-referenced with `Tamil/Anti/`.
   - *Evaluation Metrics*:
     1. **Field-level Extraction Accuracy**: Accuracy of `patientContext.ageYears`, `patientContext.gender`, `prescriptionLines.drugName` (generic name resolution), `prescriptionLines.doseText`, `prescriptionLines.frequencyText`, `prescriptionLines.durationDays`, `indicationCode`.
     2. **Brand-to-Generic Resolution Recall**: Proportion of Indian brand names (Taxim-O, Monocef, Augmentin, Cifran, Septrin, Mirox) correctly resolved to generic antimicrobial names.
     3. **Clinical Safety / AMR Violation Detection Rate**: Percentage of unsafe prescriptions (pediatric FQ, viral respiratory illness with antibiotics, banned FDC) correctly audited by the pipeline after extraction.
     4. **Baseline Comparison**: Clear quantitative improvement of Enhanced Agent over Baseline (Baseline: 11 drugs, 0% brand resolution on unmapped brands, hardcoded `SYN_CAP_MILD`; Enhanced Agent: >90% brand resolution, accurate dosage in mg, correct condition classification).

---

## 3. Caveats

1. **Hospital Dataset Quality Artifacts**:
   - `Tamil/Hopsital Dataset.csv` contains one corrupted header row at index 529 (`Age='Age', Date of Data Entry='#REF!', Gender='Sex'`). The benchmark loader and extraction pipeline must filter out or clean non-numeric age rows.
   - Minor spelling errors exist in free-text clinical entries: e.g. `cefipime` (Cefepime), `coamoxiclav` (Co-amoxiclav), `cefaziclime` (Ceftazidime), `ca buffalo mucosa` (oral cancer - buccal mucosa), `ospiration pneumonia` (aspiration pneumonia). Normalization fuzzy matching or alias mapping is essential.
2. **WHO_RELAY_AMR.csv Size & Scope**:
   - `WHO_RELAY_AMR.csv` is 72.6 MB and contains 214,368 global health indicators across hundreds of countries and non-AMR domains. Direct runtime querying of this 72MB file is unnecessary; `AMR_ANALYZED_DATA_PACKAGE/who_amr_canonical.csv` (1,020 rows) and `amr_knowledge_base/AMR_KNOWLEDGE_BASE.md` already contain the cleaned, canonicalized AMR indicators (specifically E. coli 3GC and MRSA rates).
3. **Strict Two-Layer Safety Boundary**:
   - The deterministic clinical rules engine in `services/api/app/engine/` and `app/rules_data/rules_v1.0.0.json` must NOT be replaced with LLM prompting. All AI enhancements (prompts, few-shots, RAG retrieval) belong strictly in the assistive extraction and decision-support guidance layer (`app/extraction/` or dedicated recommendation service).
4. **Read-Only Investigation Compliance**:
   - No code or data files inside `data_sets/` or `services/api/` were modified during this investigation. All analysis scripts and artifacts were authored exclusively within `.agents/teamwork/explorer_survey_2/`.

---

## 4. Conclusion & Recommendations

The datasets in `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets` provide a complete, verified foundation for training, calibrating, and evaluating the AMR Sentinel AI agent:

### 4.1 Calibration & Prompt Enhancement Strategy
1. **Calibrated Extraction Prompt with Few-Shot Indian Clinical Exemplars**:
   - Update `ExtractionAdapter._extract_with_gemini` with 3-4 diverse few-shot prescription examples extracted directly from `Hopsital Dataset.csv` and `Tamil/Anti/` (e.g. pediatric viral bronchitis where antibiotics should be withheld, adult lower UTI with brand name Martifur, outpatient pneumonia with Augmentin).
   - Instruct Gemini to resolve local Indian brand names to generics using the 405-alias dictionary, normalize gram dosages to standard metric units (e.g. $1\text{ g} \to 1000\text{ mg}$), and infer standard `SYN_` indication codes from clinical diagnoses.
2. **Upgraded Offline Fallback Heuristics**:
   - Replace the 11-item hardcoded array in `_extract_with_local_heuristics` with the loaded 405-entry alias lookup (`antibiotic_brand_to_generic_alias_lookup.csv`).
   - Implement regex parsing for gram dosages (`(\d+(?:\.\d+)?)\s*(?:g|gm|gram)` $\to \times 1000\text{ mg}$) and Indian frequency tokens (`\bBD\b` $\to$ Twice daily, `\bTDS\b|\bTID\b` $\to$ Three times daily, `\bOD\b` $\to$ Once daily, `\bQID\b` $\to$ Four times daily).
   - Add condition keyword detection matching `Tamil/Anti/conditions.csv` instead of hardcoding `SYN_CAP_MILD`.

### 4.2 AMR Knowledge Retrieval Grounding Architecture
- Implement a lightweight retrieval utility (`services/api/app/services/amr_knowledge.py`) that indexes `amr_knowledge_base/AMR_KNOWLEDGE_BASE.md` and `Tamil/Anti/guidelines.csv`.
- When an audit is performed or when a prescription draft is presented, the assistant queries the index for:
  1. The drug's WHO AWaRe classification (`who_aware_antibiotics.csv`).
  2. Banned FDC status (`aware-essentialmeds-org-list-awareGroup-Not-recommended.md` and CDSCO bans).
  3. ICMR STG guideline summary for the detected indication code (`guidelines.csv` and `regimens.csv`).
  4. Relevant national pathogen resistance evidence (e.g. MRSA 53.6%, E. coli 3GC 80.1%).

### 4.3 Benchmark Evaluation Test Split Blueprint
- Create a benchmark dataset of **60 stratified test cases** derived from `Tamil/Hopsital Dataset.csv` and `Tamil/Anti/` covering:
  - 15 Pediatric cases (including FQ contraindications and viral infections).
  - 15 Adult respiratory cases (CAP mild vs viral bronchitis/common cold).
  - 15 Urinary tract cases (Acute cystitis, eGFR variations, nitrofurantoin thresholds).
  - 15 Regulatory & FDC cases (banned combinations: Cefixime+Azithromycin, Ofloxacin+Ornidazole, Amoxicillin+Flucloxacillin).
- Build an automated evaluation script `scripts/evaluate_agent_benchmark.py` that computes:
  - **Baseline vs Enhanced Extraction Field F1 Score** (Target: $>90\%$ on Enhanced vs $\sim 45\%$ Baseline).
  - **Brand Resolution Accuracy** (Target: $>95\%$ on Enhanced vs $15\%$ Baseline).
  - **Clinical Safety Guardrail Conformance** (100% adherence to deterministic audit rules).

---

## 5. Verification Method

To independently verify the observations, statistics, and findings detailed in this report:

1. **Verify Dataset File Counts & Integrity**:
   Run the survey script in this folder:
   ```powershell
   python "c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\survey_datasets.py"
   ```
   *Expected Output*: `Inventory completed: 74 files, 239470591 bytes.`

2. **Verify Hospital Dataset Statistics & Demographics**:
   Run the hospital dataset inspection script:
   ```powershell
   python "c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\inspect_hospital.py"
   ```
   *Expected Output*: 833 rows, 832 valid rows, 33 pediatric (<18), 564 adult, 235 geriatric, row 529 malformed header duplicate.

3. **Verify Anti Guideline & Brand Mapping Tables**:
   Run the Anti inspection script:
   ```powershell
   python "c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\inspect_anti.py"
   ```
   *Expected Output*: `conditions.csv` (36 rows with `SYN_` codes matching `rules_v1.0.0.json`), `drugs.csv` (80 rows), `guidelines.csv` (36 rows), `regimens.csv` (60 rows), `brands.csv` (77 rows).

4. **Verify WHO AWaRe Not-Recommended Combinations**:
   Run the not-recommended parser script:
   ```powershell
   python "c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\parse_not_recommended.py"
   ```
   *Expected Output*: 107 Not-Recommended combinations, 43 Indian FDCs including `Amoxicillin + flucloxacillin`, `Azithromycin + cefixime`, and `Ofloxacin + ornidazole`.

5. **Verify Knowledge Base Validation & Manifest**:
   Inspect `c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\amr_knowledge_base\AMR_KNOWLEDGE_VALIDATION.yaml`:
   *Expected Output*: Confirms 3,843 records, `unique_record_ids: true`, `all_source_ids_resolve: true`, layer counts matching `AMR_KNOWLEDGE_BASE.md`.

6. **Verify Non-Regression on Existing Test Suites**:
   Run the existing project tests:
   ```powershell
   Set-Location 'c:\Seva Sankalp Hackathon\AMR Sentinel\services\api'
   & 'c:\Seva Sankalp Hackathon\AMR Sentinel\.venv\Scripts\python.exe' -m pytest tests -v
   ```
   *Expected Output*: All 24 tests across 7 test files pass (`24 passed in 2.15s`).
