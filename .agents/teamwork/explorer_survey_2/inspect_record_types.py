import json
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\AMR_ANALYZED_DATA_PACKAGE")
jsonl_path = BASE / "amr_chatbot_corpus.jsonl"

types_seen = {}

with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        rtype = data.get("record_type")
        if rtype not in types_seen:
            types_seen[rtype] = data

for rtype, sample in types_seen.items():
    print(f"\n================ Type: {rtype} ================")
    print(f"Keys: {list(sample.keys())}")
    for k in ["record_id", "source_id", "publisher", "network", "data_layer", "report_year", "pathogen", "antibiotic", "specimen", "metric", "value", "unit"]:
        if k in sample:
            print(f"  {k}: {sample[k]}")
    print(f"  text snippet: {repr(sample.get('text', ''))[:150]}")
