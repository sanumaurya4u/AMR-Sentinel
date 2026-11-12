import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path("services/api").resolve()))

from app.engine.engine import DeterministicAuditEngine

rules_path = Path("services/api/app/rules_data/rules_v1.0.0.json")
with open(rules_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

engine = DeterministicAuditEngine(manifest)

test_cases = [
    ("case_01", {"age_years": 8.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_WATERY_DIARRHEA", [{"drug_name": "Ciprofloxacin", "dose_text": "250 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_02", {"age_years": 9.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []}, "SYN_CAP_MILD", [{"drug_name": "Doxycycline", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_03", {"age_years": 5.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []}, "SYN_AOM", [{"drug_name": "Amoxicillin", "dose_text": "250 mg", "frequency_text": "Three times daily (TID)", "duration_days": 5}]),
    ("case_04", {"age_years": 10.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_PHARYNGITIS_STREP", [{"drug_name": "Azithromycin", "dose_text": "250 mg", "frequency_text": "Once daily (OD)", "duration_days": 3}]),
    ("case_05", {"age_years": 74.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 22.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_06", {"age_years": 42.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 85.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_07", {"age_years": 52.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": None, "allergies": []}, "SYN_PYELONEPHRITIS_UNCOMPLICATED", [{"drug_name": "Gentamicin", "dose_text": "80 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_08", {"age_years": 38.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_PYELONEPHRITIS_UNCOMPLICATED", [{"drug_name": "Amikacin", "dose_text": "500 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_09", {"age_years": 27.0, "gender": "female", "is_pregnant": True, "egfr_ml_min": 100.0, "allergies": []}, "SYN_CAP_MILD", [{"drug_name": "Doxycycline", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_10", {"age_years": 29.0, "gender": "female", "is_pregnant": True, "egfr_ml_min": 105.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Ciprofloxacin", "dose_text": "500 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_11", {"age_years": 26.0, "gender": "female", "is_pregnant": True, "egfr_ml_min": 110.0, "allergies": []}, "SYN_ASYMPTOMATIC_BACTERIURIA_PREGNANCY", [{"drug_name": "Cefalexin", "dose_text": "500 mg", "frequency_text": "Four times daily (QID)", "duration_days": 5}]),
    ("case_12", {"age_years": 45.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": ["Penicillin"]}, "SYN_CAP_MILD", [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "frequency_text": "Three times daily (TID)", "duration_days": 5}]),
    ("case_13", {"age_years": 36.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 98.0, "allergies": ["Penicillin"]}, "SYN_CAP_MILD", [{"drug_name": "Azithromycin", "dose_text": "500 mg", "frequency_text": "Once daily (OD)", "duration_days": 5}]),
    ("case_14", {"age_years": 50.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 92.0, "allergies": []}, "SYN_ACUTE_RHINOSINUSITIS", [{"drug_name": "Amoxicillin-Clavulanate", "dose_text": "625 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_15", {"age_years": 34.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_CAP_MILD", [{"drug_name": "Cefixime + Azithromycin", "dose_text": "200 mg + 250 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_16", {"age_years": 42.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []}, "SYN_WATERY_DIARRHEA", [{"drug_name": "Ofloxacin + Ornidazole", "dose_text": "200 mg + 500 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_17", {"age_years": 38.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 92.0, "allergies": []}, "SYN_SSTI_UNCOMPLICATED", [{"drug_name": "Amoxicillin + Flucloxacillin", "dose_text": "500 mg + 500 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_18", {"age_years": 31.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 105.0, "allergies": []}, "SYN_ACUTE_BRONCHITIS", [{"drug_name": "Azithromycin", "dose_text": "500 mg", "frequency_text": "Once daily (OD)", "duration_days": 5}]),
    ("case_19", {"age_years": 25.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 110.0, "allergies": []}, "SYN_COMMON_COLD", [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "frequency_text": "Three times daily (TID)", "duration_days": 5}]),
    ("case_20", {"age_years": 28.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []}, "SYN_VIRAL_URTI", [{"drug_name": "Paracetamol", "dose_text": "650 mg", "frequency_text": "Three times daily (TDS)", "duration_days": 3}]),
    ("case_21", {"age_years": 33.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 98.0, "allergies": []}, "SYN_PHARYNGITIS_NON_STREP", [{"drug_name": "Cefixime", "dose_text": "200 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_22", {"age_years": 28.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 105.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Meropenem", "dose_text": "1000 mg", "frequency_text": "Every 8 hours (TDS)", "duration_days": 5}]),
    ("case_23", {"age_years": 35.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_SSTI_UNCOMPLICATED", [{"drug_name": "Linezolid", "dose_text": "600 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_24", {"age_years": 40.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 95.0, "allergies": []}, "SYN_CAP_MILD", [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "frequency_text": "Three times daily (TID)", "duration_days": 14}]),
    ("case_25", {"age_years": 33.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 90.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 10}]),
    ("case_26", {"age_years": 34.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 98.0, "allergies": []}, "SYN_CAP_MILD", [{"drug_name": "Amoxicillin", "dose_text": "500 mg", "frequency_text": "Three times daily (TID)", "duration_days": 5}]),
    ("case_27", {"age_years": 29.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 102.0, "allergies": []}, "SYN_UNCOMPLICATED_UTI", [{"drug_name": "Nitrofurantoin", "dose_text": "100 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]),
    ("case_28", {"age_years": 24.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 105.0, "allergies": []}, "SYN_WATERY_DIARRHEA", [{"drug_name": "Oral Rehydration Salts (ORS) + Zinc", "dose_text": "1 sachet + 20 mg", "frequency_text": "As directed", "duration_days": 14}]),
    ("case_29", {"age_years": 44.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 92.0, "allergies": []}, "SYN_SSTI_UNCOMPLICATED", [{"drug_name": "Cefalexin", "dose_text": "500 mg", "frequency_text": "Four times daily (QID)", "duration_days": 5}]),
    ("case_30", {"age_years": 30.0, "gender": "male", "is_pregnant": False, "egfr_ml_min": 100.0, "allergies": []}, "SYN_COMMON_COLD", [{"drug_name": "Paracetamol", "dose_text": "650 mg", "frequency_text": "Three times daily (TDS)", "duration_days": 3}]),
]

for cid, p_ctx, ind, lines in test_cases:
    res = engine.evaluate({"patient_context": p_ctx, "indication_code": ind, "prescription_lines": lines})
    rules = [f["rule_id"] for f in res["findings"]]
    print(f"{cid}: status={res['status']}, rules={rules}")
