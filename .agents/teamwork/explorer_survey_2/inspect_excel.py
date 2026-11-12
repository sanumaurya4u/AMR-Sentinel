import openpyxl
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\Tamil")
xlsx_path = BASE / "AMRGuard_antibiotic_180_master_clinical_dataset.xlsx"

try:
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    print("Sheet names:", wb.sheetnames)
    for sname in wb.sheetnames:
        sheet = wb[sname]
        rows = list(sheet.iter_rows(values_only=True))
        print(f"\nSheet '{sname}': {len(rows)} rows")
        if rows:
            print("Header:", rows[0])
            for r in rows[1:4]:
                print("Row:", r)
except Exception as e:
    print("Error reading excel:", e)
