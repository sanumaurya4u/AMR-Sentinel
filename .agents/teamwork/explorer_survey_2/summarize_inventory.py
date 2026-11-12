import json
from pathlib import Path

INVENTORY_FILE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\dataset_inventory.json")

with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total files: {data['total_files']}, Total size: {data['total_size_bytes'] / (1024*1024):.2f} MB\n")

# Group files by directory
for dir_name, dir_info in data["directories"].items():
    print(f"=== Directory: {dir_name} ({dir_info['files_count']} files) ===")
    for f in dir_info["files"]:
        size_kb = f["size_bytes"] / 1024
        print(f"  - {f['name']} ({size_kb:.1f} KB, ext: {f['extension']})")
        if "csv_info" in f:
            cinfo = f["csv_info"]
            print(f"    Rows: {cinfo.get('row_count')}, Cols ({cinfo.get('num_columns')}): {cinfo.get('columns')}")
        elif "jsonl_info" in f:
            jinfo = f["jsonl_info"]
            print(f"    JSONL Lines: {jinfo.get('line_count')}")
        elif "text_info" in f:
            tinfo = f["text_info"]
            print(f"    Text Lines: {tinfo.get('line_count')}, Preview: {tinfo.get('head')[:3]}")
    print()
