"""Automated Benchmark Evaluation Runner for AMR Sentinel AI Agent.

Evaluates extraction quality, medication entity recognition (P/R/F1),
demographic accuracy, indication classification, and downstream audit concordance.
Supports recording baseline and comparative delta reporting.
"""
import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# Ensure services/api is on sys.path
sys.path.insert(0, str(Path("services/api").resolve()))

from app.engine.engine import DeterministicAuditEngine
from app.extraction.adapter import ExtractionAdapter


def _load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_token_f1(pred_tokens: list[str], truth_tokens: list[str]) -> tuple[float, float, float]:
    """Compute precision, recall, and F1 over lists of string tokens (case-insensitive multiset)."""
    p_set = [t.lower().strip() for t in pred_tokens if t]
    t_set = [t.lower().strip() for t in truth_tokens if t]

    if not p_set and not t_set:
        return 1.0, 1.0, 1.0
    if not p_set or not t_set:
        return 0.0, 0.0, 0.0

    p_counts = Counter(p_set)
    t_counts = Counter(t_set)
    tp = sum((p_counts & t_counts).values())
    precision = tp / len(p_set) if p_set else 0.0
    recall = tp / len(t_set) if t_set else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


async def evaluate_benchmark(
    cases_path: Path,
    use_cloud_if_available: bool = False,
) -> dict[str, Any]:
    """Execute evaluation over all benchmark cases."""
    cases = _load_json(cases_path)
    rules_path = Path("services/api/app/rules_data/rules_v1.0.0.json")
    rules_manifest = _load_json(rules_path)

    audit_engine = DeterministicAuditEngine(rules_manifest)
    adapter = ExtractionAdapter()

    total_cases = len(cases)
    age_correct = 0
    gender_correct = 0
    pregnancy_correct = 0
    egfr_correct = 0
    indication_correct = 0
    audit_status_correct = 0

    all_pred_drugs: list[str] = []
    all_truth_drugs: list[str] = []
    rule_jaccards: list[float] = []

    case_results = []

    for c in cases:
        case_id = c["id"]
        doc_text = c["document_text"]
        gt = c["ground_truth"]
        exp_audit = c["expected_audit"]

        # Run extraction
        file_bytes = doc_text.encode("utf-8")
        extracted = await adapter.extract_from_bytes(file_bytes, "text/plain", filename=f"{case_id}.txt")

        # Patient Context
        p_ctx = extracted.get("patientContext", {})
        gt_ctx = gt.get("patientContext", {})

        # Age
        ext_age = p_ctx.get("ageYears")
        gt_age = gt_ctx.get("ageYears")
        if ext_age is not None and gt_age is not None and abs(float(ext_age) - float(gt_age)) < 0.5:
            age_correct += 1

        # Gender
        if str(p_ctx.get("gender", "")).lower() == str(gt_ctx.get("gender", "")).lower():
            gender_correct += 1

        # Pregnancy
        if bool(p_ctx.get("isPregnant")) == bool(gt_ctx.get("isPregnant")):
            pregnancy_correct += 1

        # eGFR
        ext_egfr = p_ctx.get("egfrMlMin")
        gt_egfr = gt_ctx.get("egfrMlMin")
        if (ext_egfr is None and gt_egfr is None) or (
            ext_egfr is not None and gt_egfr is not None and abs(float(ext_egfr) - float(gt_egfr)) < 2.0
        ):
            egfr_correct += 1

        # Indication Code
        ext_ind = extracted.get("indicationCode", "")
        gt_ind = gt.get("indicationCode", "")
        if ext_ind == gt_ind:
            indication_correct += 1

        # Drug entities
        ext_lines = extracted.get("prescriptionLines", [])
        gt_lines = gt.get("prescriptionLines", [])
        ext_drugs = [line.get("drugName", "") for line in ext_lines]
        gt_drugs = [line.get("drugName", "") for line in gt_lines]

        all_pred_drugs.extend(ext_drugs)
        all_truth_drugs.extend(gt_drugs)

        # Downstream Clinical Audit Concordance
        audit_payload = {
            "patient_context": {
                "age_years": p_ctx.get("ageYears"),
                "gender": p_ctx.get("gender", "unknown"),
                "is_pregnant": p_ctx.get("isPregnant", False),
                "egfr_ml_min": p_ctx.get("egfrMlMin"),
                "allergies": p_ctx.get("allergies", []),
            },
            "indication_code": ext_ind,
            "prescription_lines": [
                {
                    "drug_name": line.get("drugName", ""),
                    "dose_text": line.get("doseText", ""),
                    "frequency_text": line.get("frequencyText", ""),
                    "duration_days": line.get("durationDays"),
                }
                for line in ext_lines
            ],
        }

        audit_result = audit_engine.evaluate(audit_payload)
        pred_status = audit_result.get("status")
        pred_rules = {f["rule_id"] for f in audit_result.get("findings", [])}
        exp_rules = set(exp_audit.get("rules", []))

        if pred_status == exp_audit.get("status"):
            audit_status_correct += 1

        # Rule Jaccard
        if not pred_rules and not exp_rules:
            jaccard = 1.0
        elif not pred_rules or not exp_rules:
            jaccard = 0.0
        else:
            jaccard = len(pred_rules & exp_rules) / len(pred_rules | exp_rules)
        rule_jaccards.append(jaccard)

        case_results.append({
            "id": case_id,
            "scenario": c["scenario"],
            "pred_drugs": ext_drugs,
            "truth_drugs": gt_drugs,
            "pred_indication": ext_ind,
            "truth_indication": gt_ind,
            "pred_status": pred_status,
            "exp_status": exp_audit.get("status"),
            "status_match": pred_status == exp_audit.get("status"),
            "engine": extracted.get("extraction_engine"),
        })

    drug_p, drug_r, drug_f1 = compute_token_f1(all_pred_drugs, all_truth_drugs)

    metrics = {
        "total_cases": total_cases,
        "demographics": {
            "age_accuracy": round(age_correct / total_cases * 100, 2),
            "gender_accuracy": round(gender_correct / total_cases * 100, 2),
            "pregnancy_accuracy": round(pregnancy_correct / total_cases * 100, 2),
            "egfr_accuracy": round(egfr_correct / total_cases * 100, 2),
        },
        "medication_extraction": {
            "drug_precision": round(drug_p * 100, 2),
            "drug_recall": round(drug_r * 100, 2),
            "drug_f1": round(drug_f1 * 100, 2),
        },
        "indication_classification": {
            "indication_accuracy": round(indication_correct / total_cases * 100, 2),
        },
        "audit_concordance": {
            "status_concordance": round(audit_status_correct / total_cases * 100, 2),
            "mean_rule_jaccard": round(sum(rule_jaccards) / len(rule_jaccards) * 100, 2) if rule_jaccards else 0.0,
        },
        "overall_quality_score": round(
            (
                (age_correct / total_cases)
                + (gender_correct / total_cases)
                + (pregnancy_correct / total_cases)
                + (egfr_correct / total_cases)
                + drug_f1
                + (indication_correct / total_cases)
                + (audit_status_correct / total_cases)
            )
            / 7
            * 100,
            2,
        ),
    }

    return {
        "summary": metrics,
        "details": case_results,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate AMR Sentinel AI Agent on Benchmark Cases.")
    parser.add_argument("--cases", default="services/api/tests/data/benchmark_cases.json", help="Path to benchmark cases")
    parser.add_argument("--record-baseline", action="store_true", help="Record current results as baseline")
    parser.add_argument("--compare-baseline", action="store_true", help="Compare against recorded baseline")
    args = parser.parse_args()

    cases_path = Path(args.cases)
    if not cases_path.exists():
        print(f"Error: {cases_path} does not exist. Run scripts/generate_benchmark_cases.py first.")
        sys.exit(1)

    print("==================================================================")
    print("  AMR Sentinel AI — Benchmark Evaluation Runner")
    print(f"  Cases: {cases_path}")
    print("==================================================================")

    res = asyncio.run(evaluate_benchmark(cases_path))
    summary = res["summary"]

    print("\n--- Summary Metrics ---")
    print(f"Total Cases: {summary['total_cases']}")
    print(f"Age Accuracy:        {summary['demographics']['age_accuracy']}%")
    print(f"Gender Accuracy:     {summary['demographics']['gender_accuracy']}%")
    print(f"Pregnancy Accuracy:  {summary['demographics']['pregnancy_accuracy']}%")
    print(f"eGFR Accuracy:       {summary['demographics']['egfr_accuracy']}%")
    print(f"Drug Precision:      {summary['medication_extraction']['drug_precision']}%")
    print(f"Drug Recall:         {summary['medication_extraction']['drug_recall']}%")
    print(f"Drug F1 Score:       {summary['medication_extraction']['drug_f1']}%")
    print(f"Indication Accuracy: {summary['indication_classification']['indication_accuracy']}%")
    print(f"Audit Concordance:   {summary['audit_concordance']['status_concordance']}%")
    print(f"Rule Jaccard:        {summary['audit_concordance']['mean_rule_jaccard']}%")
    print(f"\n>> OVERALL QUALITY SCORE: {summary['overall_quality_score']} / 100 <<")

    baseline_path = Path("services/api/tests/data/baseline_evaluation_results.json")

    if args.record_baseline:
        with open(baseline_path, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print(f"\n[Baseline Recorded] Successfully saved baseline results to {baseline_path}")

    if args.compare_baseline:
        if not baseline_path.exists():
            print(f"\n[Warning] Baseline file not found at {baseline_path}. Recording baseline now.")
            with open(baseline_path, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
        else:
            with open(baseline_path, "r", encoding="utf-8") as f:
                base_data = json.load(f)
            b_sum = base_data["summary"]

            print("\n==================================================================")
            print("  BASELINE COMPARISON REPORT (Pre-Enhancement vs Post-Enhancement)")
            print("==================================================================")
            fmt = "{:<30} {:<15} {:<15} {:<15}"
            print(fmt.format("Metric", "Baseline", "Current", "Delta"))
            print("-" * 75)

            def print_row(name, b_val, c_val):
                delta = round(c_val - b_val, 2)
                d_str = f"+{delta}%" if delta > 0 else f"{delta}%"
                print(fmt.format(name, f"{b_val}%", f"{c_val}%", d_str))

            print_row("Age Accuracy", b_sum["demographics"]["age_accuracy"], summary["demographics"]["age_accuracy"])
            print_row("Gender Accuracy", b_sum["demographics"]["gender_accuracy"], summary["demographics"]["gender_accuracy"])
            print_row("Pregnancy Accuracy", b_sum["demographics"]["pregnancy_accuracy"], summary["demographics"]["pregnancy_accuracy"])
            print_row("eGFR Accuracy", b_sum["demographics"]["egfr_accuracy"], summary["demographics"]["egfr_accuracy"])
            print_row("Drug Precision", b_sum["medication_extraction"]["drug_precision"], summary["medication_extraction"]["drug_precision"])
            print_row("Drug Recall", b_sum["medication_extraction"]["drug_recall"], summary["medication_extraction"]["drug_recall"])
            print_row("Drug F1 Score", b_sum["medication_extraction"]["drug_f1"], summary["medication_extraction"]["drug_f1"])
            print_row("Indication Accuracy", b_sum["indication_classification"]["indication_accuracy"], summary["indication_classification"]["indication_accuracy"])
            print_row("Audit Status Concordance", b_sum["audit_concordance"]["status_concordance"], summary["audit_concordance"]["status_concordance"])
            print_row("Mean Rule Jaccard", b_sum["audit_concordance"]["mean_rule_jaccard"], summary["audit_concordance"]["mean_rule_jaccard"])
            print("-" * 75)
            print_row("OVERALL QUALITY SCORE", b_sum["overall_quality_score"], summary["overall_quality_score"])
            print("==================================================================")


if __name__ == "__main__":
    main()
