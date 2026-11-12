import csv
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")
hosp_path = BASE / "Tamil" / "Hopsital Dataset.csv"

with open(hosp_path, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

fq_drugs = ["ciprofloxacin", "cifran", "ofloxacin", "levofloxacin", "norfloxacin", "moxifloxacin"]

print("--- PEDIATRIC CASES (<18) WITH POTENTIAL AMR CONCERNS ---")
for i, r in enumerate(rows):
    try:
        age = float(r.get("Age", ""))
    except ValueError:
        continue
    if age < 18:
        drug = r.get("Name of Drug", "").strip().lower()
        print(f"Row {i} (Age {age}, {r.get('Gender')}): Diagnosis='{r.get('Diagnosis')}', Drug='{drug}', Dose='{r.get('Dosage (gram)')}g', Freq='{r.get('Frequency')}', Dur='{r.get('Duration (days)')}d'")
