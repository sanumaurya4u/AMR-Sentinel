import os
import json
import csv
from pathlib import Path

DATA_SETS_DIR = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets")
OUTPUT_FILE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_2\dataset_inventory.json")

inventory = {
    "total_files": 0,
    "total_size_bytes": 0,
    "directories": {},
    "root_files": [],
    "file_details": []
}

for root, dirs, files in os.walk(DATA_SETS_DIR):
    rel_root = os.path.relpath(root, DATA_SETS_DIR)
    dir_entry = {
        "rel_path": rel_root,
        "files_count": len(files),
        "subdirs_count": len(dirs),
        "files": []
    }
    
    for f in sorted(files):
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, DATA_SETS_DIR)
        size = os.path.getsize(full_path)
        ext = os.path.splitext(f)[1].lower()
        
        info = {
            "name": f,
            "rel_path": rel_path,
            "size_bytes": size,
            "extension": ext
        }
        
        # Analyze CSV / JSON / JSONL / Markdown / YAML
        if ext == ".csv":
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    reader = csv.reader(fp)
                    header = next(reader, None)
                    row_count = sum(1 for _ in fp) + (1 if header else 0)
                    fp.seek(0)
                    dict_reader = csv.DictReader(fp)
                    sample_rows = []
                    for i, r in enumerate(dict_reader):
                        if i < 3:
                            sample_rows.append(r)
                        else:
                            break
                    info["csv_info"] = {
                        "row_count": row_count,
                        "columns": header if header else [],
                        "num_columns": len(header) if header else 0,
                        "sample_rows": sample_rows
                    }
            except Exception as e:
                info["csv_info"] = {"error": str(e)}
                
        elif ext == ".jsonl":
            try:
                line_count = 0
                sample_lines = []
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    for i, line in enumerate(fp):
                        line_count += 1
                        if i < 3:
                            try:
                                sample_lines.append(json.loads(line))
                            except:
                                sample_lines.append(line.strip())
                info["jsonl_info"] = {
                    "line_count": line_count,
                    "sample_records": sample_lines
                }
            except Exception as e:
                info["jsonl_info"] = {"error": str(e)}

        elif ext in [".md", ".yaml", ".yml", ".txt"]:
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    lines = fp.readlines()
                    info["text_info"] = {
                        "line_count": len(lines),
                        "head": [l.strip() for l in lines[:15] if l.strip()]
                    }
            except Exception as e:
                info["text_info"] = {"error": str(e)}

        inventory["file_details"].append(info)
        dir_entry["files"].append(info)
        inventory["total_files"] += 1
        inventory["total_size_bytes"] += size

    inventory["directories"][rel_root] = dir_entry

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(inventory, out, indent=2)

print(f"Inventory completed: {inventory['total_files']} files, {inventory['total_size_bytes']} bytes.")
