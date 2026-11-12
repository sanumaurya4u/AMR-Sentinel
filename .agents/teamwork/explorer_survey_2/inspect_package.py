import csv
import json
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\AMR_ANALYZED_DATA_PACKAGE")

print("=== PACKAGE_MANIFEST.csv ===")
with open(BASE / "PACKAGE_MANIFEST.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

print("\n=== amr_data_quality_report.csv ===")
with open(BASE / "amr_data_quality_report.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

print("\n=== amr_surveillance_trend_summary.csv ===")
with open(BASE / "amr_surveillance_trend_summary.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

print("\n=== amr_source_registry.csv (First 6) ===")
with open(BASE / "amr_source_registry.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 7:
            print(line.strip())

print("\n=== who_amr_canonical.csv (First 5) ===")
with open(BASE / "who_amr_canonical.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 6:
            print(line.strip())

print("\n=== ncdc_evidence_clean.csv (First 3) ===")
with open(BASE / "ncdc_evidence_clean.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.strip())

print("\n=== ncdc_rag_clean.csv (First 3) ===")
with open(BASE / "ncdc_rag_clean.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.strip())
