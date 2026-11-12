import csv
import json
import os
from collections import Counter
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")
REPORT_PATH = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\deep_analysis_findings.json")

findings = {}

# 1. Hospital Dataset (Tamil/Hopsital Dataset.csv)
hosp_path = BASE / "Tamil" / "Hopsital Dataset.csv"
if hosp_path.exists():
    with open(hosp_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        hosp_rows = list(reader)
    
    diagnoses = Counter(r.get("Diagnosis", "").strip() for r in hosp_rows)
    drugs = Counter(r.get("Name of Drug", "").strip() for r in hosp_rows)
    routes = Counter(r.get("Route", "").strip() for r in hosp_rows)
    frequencies = Counter(r.get("Frequency", "").strip() for r in hosp_rows)
    genders = Counter(r.get("Gender", "").strip() for r in hosp_rows)
    durations = Counter(r.get("Duration (days)", "").strip() for r in hosp_rows)
    
    findings["hospital_dataset"] = {
        "total_records": len(hosp_rows),
        "fields": list(hosp_rows[0].keys()) if hosp_rows else [],
        "sample_records": hosp_rows[:5],
        "top_diagnoses": diagnoses.most_common(15),
        "top_drugs": drugs.most_common(20),
        "routes": routes.most_common(),
        "frequencies": frequencies.most_common(),
        "genders": genders.most_common(),
        "duration_distribution": durations.most_common(10)
    }

# 2. Tamil/Anti/
anti_dir = BASE / "Tamil" / "Anti"
findings["anti_tables"] = {}
for fname in ["brands.csv", "conditions.csv", "drugs.csv", "guidelines.csv", "regimens.csv"]:
    fpath = anti_dir / fname
    if fpath.exists():
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            r = csv.DictReader(f)
            rows = list(r)
            findings["anti_tables"][fname] = {
                "count": len(rows),
                "columns": list(rows[0].keys()) if rows else [],
                "sample": rows[:3]
            }

# 3. Tamil/New folder/ (Brand to Generic)
alias_path = BASE / "Tamil" / "New folder" / "antibiotic_brand_to_generic_alias_lookup.csv"
if alias_path.exists():
    with open(alias_path, "r", encoding="utf-8", errors="ignore") as f:
        r = csv.DictReader(f)
        alias_rows = list(r)
    findings["brand_to_generic_alias"] = {
        "count": len(alias_rows),
        "sample": alias_rows[:5],
        "unique_generics": len(set(r.get("generic_antibiotic_name", "").strip() for r in alias_rows)),
        "unique_brands": len(set(r.get("brand_alias", "").strip() for r in alias_rows))
    }

# 4. AMR_ANALYZED_DATA_PACKAGE (who_aware_antibiotics.csv)
aware_path = BASE / "AMR_ANALYZED_DATA_PACKAGE" / "who_aware_antibiotics.csv"
if aware_path.exists():
    with open(aware_path, "r", encoding="utf-8", errors="ignore") as f:
        r = csv.DictReader(f)
        aware_rows = list(r)
    categories = Counter(r.get("category", "").strip() for r in aware_rows)
    classes = Counter(r.get("antibiotic_class", "").strip() for r in aware_rows)
    findings["who_aware_antibiotics"] = {
        "count": len(aware_rows),
        "columns": list(aware_rows[0].keys()) if aware_rows else [],
        "categories": categories.most_common(),
        "sample": aware_rows[:3]
    }

# 5. AMR_ANALYZED_DATA_PACKAGE (amr_chatbot_corpus.csv)
corpus_path = BASE / "AMR_ANALYZED_DATA_PACKAGE" / "amr_chatbot_corpus.csv"
if corpus_path.exists():
    with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f:
        r = csv.DictReader(f)
        corp_sample = []
        pathogens = Counter()
        antibiotics = Counter()
        record_types = Counter()
        count = 0
        for row in r:
            count += 1
            if count <= 5:
                corp_sample.append(row)
            pathogens[row.get("pathogen", "").strip()] += 1
            antibiotics[row.get("antibiotic", "").strip()] += 1
            record_types[row.get("record_type", "").strip()] += 1
            
    findings["amr_chatbot_corpus"] = {
        "total_records": count,
        "record_types": record_types.most_common(10),
        "top_pathogens": pathogens.most_common(15),
        "top_antibiotics": antibiotics.most_common(15),
        "sample": corp_sample
    }

# 6. amr_knowledge_base (AMR_KNOWLEDGE_VALIDATION.yaml and header of AMR_KNOWLEDGE_BASE.md)
val_path = BASE / "amr_knowledge_base" / "AMR_KNOWLEDGE_VALIDATION.yaml"
if val_path.exists():
    with open(val_path, "r", encoding="utf-8", errors="ignore") as f:
        findings["amr_knowledge_validation"] = f.read()

src_idx_path = BASE / "amr_knowledge_base" / "AMR_SOURCE_INDEX.yaml"
if src_idx_path.exists():
    with open(src_idx_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        findings["amr_source_index_head"] = "".join(lines[:40])

with open(REPORT_PATH, "w", encoding="utf-8") as out:
    json.dump(findings, out, indent=2)

print("Deep analysis complete!")
