import json
from pathlib import Path

findings_path = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\deep_analysis_findings.json")
with open(findings_path, "r", encoding="utf-8") as f:
    d = json.load(f)

print("--- HOSPITAL DATASET ---")
h = d.get("hospital_dataset", {})
print("Total records:", h.get("total_records"))
print("Fields:", h.get("fields"))
print("Sample record 0:", h.get("sample_records", [])[0] if h.get("sample_records") else None)
print("Top Diagnoses:", h.get("top_diagnoses")[:8])
print("Top Drugs:", h.get("top_drugs")[:10])
print("Routes:", h.get("routes"))
print("Frequencies:", h.get("frequencies"))
print("Genders:", h.get("genders"))

print("\n--- ANTI TABLES ---")
for k, v in d.get("anti_tables", {}).items():
    print(f"Table {k}: count={v['count']}, columns={v['columns']}")

print("\n--- BRAND TO GENERIC ---")
bg = d.get("brand_to_generic_alias", {})
print("Count:", bg.get("count"), "Unique Brands:", bg.get("unique_brands"), "Unique Generics:", bg.get("unique_generics"))
print("Sample:", bg.get("sample")[:3])

print("\n--- WHO AWARE ---")
aw = d.get("who_aware_antibiotics", {})
print("Count:", aw.get("count"), "Categories:", aw.get("categories"))
print("Sample:", aw.get("sample")[:2])

print("\n--- CHATBOT CORPUS ---")
cb = d.get("amr_chatbot_corpus", {})
print("Total records:", cb.get("total_records"))
print("Record types:", cb.get("record_types"))
print("Top pathogens:", cb.get("top_pathogens")[:8])
print("Top antibiotics:", cb.get("top_antibiotics")[:8])
