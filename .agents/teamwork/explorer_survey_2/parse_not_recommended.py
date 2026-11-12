import re
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")
md_path = BASE / "aware-essentialmeds-org-list-awareGroup-Not-recommended.md"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Pattern: ##### <Name>
names = re.findall(r"#####\s+([^\n]+)", text)
print(f"Total Not Recommended antibiotics/combinations found: {len(names)}")
print("First 20 Not Recommended combinations:")
for n in names[:20]:
    print(" -", n.strip())

# Check for notable Indian FDCs
indian_fdcs = [n for n in names if any(k in n.lower() for k in ["cefixime", "ofloxacin", "ciprofloxacin", "azithromycin", "ornidazole", "clavulanic", "cefpodoxime"])]
print(f"\nNotable Not Recommended FDCs relevant to India ({len(indian_fdcs)} found):")
for n in indian_fdcs[:20]:
    print(" -", n.strip())
