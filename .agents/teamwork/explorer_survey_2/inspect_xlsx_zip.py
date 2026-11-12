import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\Tamil")
xlsx_path = BASE / "AMRGuard_antibiotic_180_master_clinical_dataset.xlsx"

with zipfile.ZipFile(xlsx_path, "r") as z:
    print("Files in xlsx archive:")
    for name in z.namelist():
        print(" ", name)
    
    # Read shared strings if present
    shared_strings = []
    if "xl/sharedStrings.xml" in z.namelist():
        tree = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in tree.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
            t = si.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
            shared_strings.append(t.text if t is not None else "")
    print(f"Total shared strings: {len(shared_strings)}")
    print("Sample shared strings:", shared_strings[:15])

    # Read workbook.xml to get sheet names
    if "xl/workbook.xml" in z.namelist():
        tree = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = tree.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet")
        for s in sheets:
            print("Sheet name:", s.attrib.get("name"), "sheetId:", s.attrib.get("sheetId"))
