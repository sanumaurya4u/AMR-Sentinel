import json
from pathlib import Path

BASE = Path(r"c:\Seva Sankalp Hackathon\AMR Sentinel\data_sets\AMR_ANALYZED_DATA_PACKAGE")
jsonl_path = BASE / "amr_chatbot_corpus.jsonl"

resistance_samples = []
obs_samples = []

with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        rtype = data.get("record_type")
        if rtype == "resistance_evidence" and len(resistance_samples) < 5:
            resistance_samples.append(data)
        elif rtype == "structured_observation" and len(obs_samples) < 5:
            obs_samples.append(data)

print("--- RESISTANCE EVIDENCE SAMPLES ---")
for r in resistance_samples:
    print(f"ID: {r.get('record_id')}, Pathogen: {r.get('pathogen')}, Antibiotic: {r.get('antibiotic')}, Metric: {r.get('metric')}, Value: {r.get('value')} {r.get('unit')}, Text: {r.get('text')[:120]}")

print("\n--- STRUCTURED OBSERVATION SAMPLES ---")
for r in obs_samples:
    print(f"ID: {r.get('record_id')}, Country: {r.get('country')}, Organism: {r.get('organism')}, Year: {r.get('year')}, Value: {r.get('value_percent')}%, Def: {r.get('definition')[:100]}")
