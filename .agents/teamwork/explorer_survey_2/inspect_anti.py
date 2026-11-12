import csv
import json
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")

# Let's inspect Tamil/Anti/
print("=== Tamil/Anti/conditions.csv ===")
with open(BASE / "Tamil" / "Anti" / "conditions.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 10:
            print(line.strip())

print("\n=== Tamil/Anti/drugs.csv (First 5) ===")
with open(BASE / "Tamil" / "Anti" / "drugs.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 6:
            print(line.strip())

print("\n=== Tamil/Anti/guidelines.csv (First 5) ===")
with open(BASE / "Tamil" / "Anti" / "guidelines.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 6:
            print(line.strip())

print("\n=== Tamil/Anti/regimens.csv (First 5) ===")
with open(BASE / "Tamil" / "Anti" / "regimens.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 6:
            print(line.strip())

print("\n=== Tamil/Anti/brands.csv (First 10) ===")
with open(BASE / "Tamil" / "Anti" / "brands.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 11:
            print(line.strip())
