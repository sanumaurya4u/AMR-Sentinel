"""Ingestion and document chunking service for AMR knowledge assets and clinical guidelines."""
import csv
from pathlib import Path
from typing import Any


def load_icmr_guidelines(csv_path: Path) -> list[dict[str, Any]]:
    """Load ICMR Standard Treatment Guidelines from guidelines.csv."""
    chunks = []
    if not csv_path.exists():
        return chunks

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sec_ref = row.get("section_ref", "")
            summary = row.get("summary", "")
            indicated = row.get("antibiotic_indicated", "True") == "True"

            chunks.append({
                "source_title": row.get("source", "ICMR STG 2022"),
                "source_category": "ICMR_STG_2022",
                "heading": sec_ref,
                "content": f"Condition: {sec_ref}\nGuideline Recommendation: {summary}\nAntibiotic Indicated: {'Yes' if indicated else 'No, Contraindicated/Not Recommended'}",
                "metadata": {
                    "condition_id": row.get("condition_id"),
                    "antibiotic_indicated": indicated,
                    "section_ref": sec_ref,
                },
            })
    return chunks


def load_who_aware_antibiotics(csv_path: Path) -> list[dict[str, Any]]:
    """Load WHO AWaRe classification & Essential Medicines recommendations."""
    chunks = []
    if not csv_path.exists():
        return chunks

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            drug = row.get("antibiotic", "")
            group = row.get("aware_group", "Unclassified")
            recs = row.get("recommendations", "")

            content = f"Antimicrobial: {drug}\nWHO AWaRe Group: {group}"
            if recs:
                content += f"\nWHO Indication Recommendations: {recs}"

            chunks.append({
                "source_title": "WHO AWaRe Classification 2023",
                "source_category": "WHO_AWARE_2023",
                "heading": f"{drug} ({group})",
                "content": content,
                "metadata": {
                    "drug_name": drug,
                    "aware_group": group,
                    "source": row.get("source", "WHO EML 2023"),
                },
            })
    return chunks


def load_cdsco_banned_fdcs() -> list[dict[str, Any]]:
    """Codify CDSCO Indian Gazette Banned Fixed-Dose Combinations."""
    banned_list = [
        ("Cefixime + Azithromycin", "Dual broad-spectrum cephalosporin and macrolide fixed-dose combination banned due to irrational antimicrobial spectrum and lack of therapeutic synergy."),
        ("Ofloxacin + Ornidazole", "Fluoroquinolone + Nitroimidazole FDC widely prescribed for diarrhea; banned for empiric acute gastroenteritis due to rampant fluoroquinolone resistance."),
        ("Amoxicillin + Flucloxacillin", "Irrational penicillin combination prohibited under CDSCO Gazette notifications."),
        ("Ampicillin + Cloxacillin", "Oral combination with variable bio-availabilities and no proven therapeutic superiority over monotherapy."),
        ("Ciprofloxacin + Tinidazole", "Empiric combination banned for routine outpatient diarrheal illness."),
        ("Norfloxacin + Metronidazole", "Prohibited fixed-dose combination; monotherapy with oral rehydration is standard of care."),
    ]
    chunks = []
    for drug, rationale in banned_list:
        chunks.append({
            "source_title": "CDSCO Gazette Directives",
            "source_category": "CDSCO_BANNED_FDC",
            "heading": f"BANNED FDC: {drug}",
            "content": f"Prohibited Formulation: {drug}\nRegulatory Status: BANNED by CDSCO Gazette.\nClinical Rationale: {rationale}",
            "metadata": {
                "drug_name": drug,
                "is_banned_fdc": True,
            },
        })
    return chunks


def build_amr_knowledge_corpus(workspace_root: Path | None = None) -> list[dict[str, Any]]:
    """Assemble all structured clinical chunks across available datasets."""
    if workspace_root is None:
        workspace_root = Path(__file__).resolve().parents[4]

    corpus: list[dict[str, Any]] = []

    # 1. ICMR STG Guidelines
    icmr_csv = workspace_root / "data_sets" / "Tamil" / "Anti" / "guidelines.csv"
    corpus.extend(load_icmr_guidelines(icmr_csv))

    # 2. WHO AWaRe Classifications
    who_csv = workspace_root / "data_sets" / "AMR_ANALYZED_DATA_PACKAGE" / "who_aware_antibiotics.csv"
    corpus.extend(load_who_aware_antibiotics(who_csv))

    # 3. CDSCO Banned FDCs
    corpus.extend(load_cdsco_banned_fdcs())

    return corpus
