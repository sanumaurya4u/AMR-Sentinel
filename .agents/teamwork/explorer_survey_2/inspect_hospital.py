import csv
from collections import Counter
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")
hosp_path = BASE / "Tamil" / "Hopsital Dataset.csv"

with open(hosp_path, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in Hospital Dataset: {len(rows)}")
print(f"Columns: {reader.fieldnames}")

# Let's inspect some sample rows across the dataset
print("\n--- First 5 rows ---")
for r in rows[:5]:
    print(r)

print("\n--- Rows 100-105 ---")
for r in rows[100:105]:
    print(r)

# Check invalid / corrupted rows
corrupt_rows = []
for i, r in enumerate(rows):
    try:
        age = float(r.get("Age", ""))
    except ValueError:
        corrupt_rows.append((i, r))

print(f"\nNon-numeric Age rows count: {len(corrupt_rows)}")
for idx, r in corrupt_rows[:5]:
    print(f"Row {idx}: {r}")

# Check age distribution
ages = []
for r in rows:
    try:
        a = float(r.get("Age", ""))
        ages.append(a)
    except ValueError:
        pass

peds = [a for a in ages if a < 18]
geriatric = [a for a in ages if a >= 65]
adult = [a for a in ages if 18 <= a < 65]
print(f"\nAge distribution: Total valid={len(ages)}, Pediatric (<18)={len(peds)}, Adult (18-64)={len(adult)}, Geriatric (>=65)={len(geriatric)}")
print(f"Pediatric sample ages: {peds[:10]}")

# Check unique drugs prescribed
drugs = Counter(r.get("Name of Drug", "").strip().lower() for r in rows)
print(f"\nTotal unique drug names: {len(drugs)}")
print("Top 25 drugs:")
for d, c in drugs.most_common(25):
    print(f"  {d}: {c}")

# Check dosage units / formats
dosages = Counter(r.get("Dosage (gram)", "").strip() for r in rows)
print(f"\nDosage (gram) distribution (top 15):")
for d, c in dosages.most_common(15):
    print(f"  {d}: {c}")

# Check routes
routes = Counter(r.get("Route", "").strip() for r in rows)
print(f"\nRoutes: {routes}")

# Check frequency
freqs = Counter(r.get("Frequency", "").strip() for r in rows)
print(f"\nFrequencies: {freqs}")

# Check durations
durations = Counter(r.get("Duration (days)", "").strip() for r in rows)
print(f"\nDuration (days) distribution (top 15):")
for d, c in durations.most_common(15):
    print(f"  {d}: {c}")
