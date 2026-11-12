import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path("services/api").resolve()))

from app.engine.engine import DeterministicAuditEngine
import app.engine.evaluator as evaluator

rules_path = Path("services/api/app/rules_data/rules_v1.0.0.json")
with open(rules_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Test with modified banned_pairs
orig_check = evaluator.check_banned_fdc
def mock_check_banned(prescribed_drugs, rule):
    normalized_all = [evaluator.normalize_drug_name(d) for d in prescribed_drugs]
    banned_pairs = [
        ("cefixime", "azithromycin", "Cefixime + Azithromycin"),
        ("ofloxacin", "ornidazole", "Ofloxacin + Ornidazole"),
        ("amoxicillin", "flucloxacillin", "Amoxicillin + Flucloxacillin"),
    ]
    for ing_a, ing_b, display_name in banned_pairs:
        has_combo_line = any(ing_a in d and ing_b in d for d in normalized_all)
        has_separate_lines = any(ing_a in d for d in normalized_all) and any(ing_b in d for d in normalized_all)
        if has_combo_line or has_separate_lines:
            return {
                "Banned FDC Prescribed": display_name,
                "Regulatory Authority": "CDSCO Gazette Notification",
                "Status": "Manufacture, sale and clinical use legally prohibited in India",
            }, []
    return None

evaluator.check_banned_fdc = mock_check_banned

engine = DeterministicAuditEngine(manifest)
p_ctx = {"age_years": 38.0, "gender": "female", "is_pregnant": False, "egfr_ml_min": 92.0, "allergies": []}
lines = [{"drug_name": "Amoxicillin + Flucloxacillin", "dose_text": "500 mg + 500 mg", "frequency_text": "Twice daily (BD)", "duration_days": 5}]
res = engine.evaluate({"patient_context": p_ctx, "indication_code": "SYN_SSTI_UNCOMPLICATED", "prescription_lines": lines})
print("With amox+fluclox added to banned_pairs:", res["status"], [f["rule_id"] for f in res["findings"]])
