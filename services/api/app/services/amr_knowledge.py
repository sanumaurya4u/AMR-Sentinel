"""Assistive AMR Knowledge Retrieval Service.

Grounds assistive intake and clinician decision-support on WHO AWaRe classification,
ICMR Standard Treatment Guidelines (STG 2022), CDSCO regulatory notices, and national
AMR surveillance datasets.

SAFETY GUARANTEE:
This service provides advisory clinical context strictly in the assistive draft layer.
It NEVER executes, mutates, or bypasses the deterministic clinical audit core.
"""
import re
from functools import lru_cache
from typing import Any

# Canonical drug reference profiles
DRUG_CATALOGUE: dict[str, dict[str, Any]] = {
    "amoxicillin": {
        "generic_name": "Amoxicillin",
        "drug_class": "Aminopenicillin",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": True,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
    "amoxicillin-clavulanate": {
        "generic_name": "Amoxicillin-Clavulanate",
        "drug_class": "Beta-lactam + Beta-lactamase Inhibitor",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": True,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
    "nitrofurantoin": {
        "generic_name": "Nitrofurantoin",
        "drug_class": "Nitrofuran",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": True,
        "min_age_years": 1.0,
        "renal_contraindication_egfr": 30.0,
    },
    "cefalexin": {
        "generic_name": "Cefalexin",
        "drug_class": "First-generation Cephalosporin",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": True,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
    "gentamicin": {
        "generic_name": "Gentamicin",
        "drug_class": "Aminoglycoside",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 0.0,
        "requires_egfr": True,
    },
    "amikacin": {
        "generic_name": "Amikacin",
        "drug_class": "Aminoglycoside",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 0.0,
        "requires_egfr": True,
    },
    "doxycycline": {
        "generic_name": "Doxycycline",
        "drug_class": "Tetracycline",
        "aware_class": "Access",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 12.0,
    },
    "ciprofloxacin": {
        "generic_name": "Ciprofloxacin",
        "drug_class": "Fluoroquinolone",
        "aware_class": "Watch",
        "is_antibiotic": True,
        "is_fluoroquinolone": True,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 18.0,
    },
    "levofloxacin": {
        "generic_name": "Levofloxacin",
        "drug_class": "Fluoroquinolone",
        "aware_class": "Watch",
        "is_antibiotic": True,
        "is_fluoroquinolone": True,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 18.0,
    },
    "ofloxacin": {
        "generic_name": "Ofloxacin",
        "drug_class": "Fluoroquinolone",
        "aware_class": "Watch",
        "is_antibiotic": True,
        "is_fluoroquinolone": True,
        "is_beta_lactam": False,
        "pregnancy_safe": False,
        "min_age_years": 18.0,
    },
    "azithromycin": {
        "generic_name": "Azithromycin",
        "drug_class": "Macrolide",
        "aware_class": "Watch",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": True,
        "min_age_years": 0.5,
    },
    "cefixime": {
        "generic_name": "Cefixime",
        "drug_class": "Third-generation Cephalosporin",
        "aware_class": "Watch",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": True,
        "pregnancy_safe": True,
        "min_age_years": 0.5,
    },
    "meropenem": {
        "generic_name": "Meropenem",
        "drug_class": "Carbapenem",
        "aware_class": "Reserve",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": True,
        "pregnancy_safe": True,
        "min_age_years": 0.25,
    },
    "linezolid": {
        "generic_name": "Linezolid",
        "drug_class": "Oxazolidinone",
        "aware_class": "Reserve",
        "is_antibiotic": True,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
    "oral rehydration salts (ors) + zinc": {
        "generic_name": "Oral Rehydration Salts (ORS) + Zinc",
        "drug_class": "Supportive Rehydration & Micronutrient",
        "aware_class": "Access",
        "is_antibiotic": False,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
    "paracetamol": {
        "generic_name": "Paracetamol",
        "drug_class": "Antipyretic Analgesic",
        "aware_class": "Access",
        "is_antibiotic": False,
        "is_fluoroquinolone": False,
        "is_beta_lactam": False,
        "pregnancy_safe": True,
        "min_age_years": 0.0,
    },
}

BANNED_FDCS: list[str] = [
    "cefixime + azithromycin",
    "ofloxacin + ornidazole",
    "amoxicillin + flucloxacillin",
    "ampicillin + cloxacillin",
    "ciprofloxacin + tinidazole",
    "norfloxacin + metronidazole",
    "norfloxacin + tinidazole",
]

ICMR_GUIDELINES: dict[str, dict[str, Any]] = {
    "SYN_CAP_MILD": {
        "condition_name": "Community-Acquired Pneumonia (Mild Outpatient)",
        "source": "ICMR STG 2022 - Respiratory Infections",
        "antibiotic_indicated": True,
        "recommended_regimen": "Amoxicillin 500mg PO TID for 5 days.",
        "rationale": "High-dose amoxicillin provides optimal Streptococcus pneumoniae coverage with minimal collateral resistance pressure.",
    },
    "SYN_UNCOMPLICATED_UTI": {
        "condition_name": "Uncomplicated Acute Cystitis / Lower UTI",
        "source": "ICMR STG 2022 - Urinary Tract Infections",
        "antibiotic_indicated": True,
        "recommended_regimen": "Nitrofurantoin 100mg PO BD x 5 days or Fosfomycin 3g single dose.",
        "rationale": "Empirical fluoroquinolones contraindicated due to >75% E. coli resistance in Indian surveillance networks (NCDC/ICMR).",
    },
    "SYN_ACUTE_BRONCHITIS": {
        "condition_name": "Acute Bronchitis (Self-Limiting Viral)",
        "source": "ICMR STG 2022 - Respiratory Infections",
        "antibiotic_indicated": False,
        "recommended_regimen": "Symptomatic care only. Antibiotics provide zero clinical benefit.",
        "rationale": "Acute bronchitis is >90% viral etiology. Routine antimicrobial therapy drives macrolide and beta-lactam resistance.",
    },
    "SYN_COMMON_COLD": {
        "condition_name": "Common Cold / Rhinopharyngitis (Viral)",
        "source": "ICMR STG 2022 - Upper Respiratory Infections",
        "antibiotic_indicated": False,
        "recommended_regimen": "Supportive hydration, paracetamol for discomfort, saline nasal drops.",
        "rationale": "Viral infection. Antibiotic treatment is strictly contraindicated under national stewardship standards.",
    },
    "SYN_VIRAL_URTI": {
        "condition_name": "Viral Upper Respiratory Tract Infection",
        "source": "ICMR STG 2022 - Upper Respiratory Infections",
        "antibiotic_indicated": False,
        "recommended_regimen": "Symptomatic care, steam inhalation, paracetamol.",
        "rationale": "Self-limiting viral etiology.",
    },
    "SYN_PHARYNGITIS_NON_STREP": {
        "condition_name": "Non-Streptococcal Pharyngitis (Viral Sore Throat)",
        "source": "ICMR STG 2022 - ENT Infections",
        "antibiotic_indicated": False,
        "recommended_regimen": "Warm saline gargles, analgesic throat lozenges, paracetamol.",
        "rationale": "Antibiotics non-indicated unless Centor score >= 3 or positive rapid antigen test for GAS.",
    },
    "SYN_WATERY_DIARRHEA": {
        "condition_name": "Acute Watery Diarrhea (Non-Cholera)",
        "source": "ICMR STG 2022 - Gastrointestinal Infections",
        "antibiotic_indicated": False,
        "recommended_regimen": "Oral Rehydration Salts (ORS) + Zinc (20 mg/day) for 14 days.",
        "rationale": "Non-cholera watery diarrhea is self-limiting viral/osmotic. Antibiotics increase risk of prolonged carriage and toxicity.",
    },
    "SYN_PHARYNGITIS_STREP": {
        "condition_name": "Streptococcal Pharyngitis (Group A Strep)",
        "source": "ICMR STG 2022 - ENT Infections",
        "antibiotic_indicated": True,
        "recommended_regimen": "Amoxicillin 500mg TID for 5-10 days (or Azithromycin for penicillin-allergic patients).",
        "rationale": "Targeted eradication of GAS to prevent acute rheumatic fever.",
    },
    "SYN_AOM": {
        "condition_name": "Acute Otitis Media",
        "source": "ICMR STG 2022 - Pediatric ENT",
        "antibiotic_indicated": True,
        "recommended_regimen": "Amoxicillin 40-45 mg/kg/day in 3 divided doses for 5 days.",
        "rationale": "First-line aminopenicillin monotherapy covers primary middle ear pathogens.",
    },
    "SYN_SSTI_UNCOMPLICATED": {
        "condition_name": "Uncomplicated Skin and Soft Tissue Infection (Cellulitis / Impetigo)",
        "source": "ICMR STG 2022 - Dermatology",
        "antibiotic_indicated": True,
        "recommended_regimen": "Cefalexin 500mg QID for 5 days or Cloxacillin 500mg QID for 5 days.",
        "rationale": "Targets Streptococcus pyogenes and methicillin-sensitive Staphylococcus aureus (MSSA).",
    },
    "SYN_ACUTE_RHINOSINUSITIS": {
        "condition_name": "Acute Bacterial Rhinosinusitis (Persistent >10 Days)",
        "source": "ICMR STG 2022 - ENT Infections",
        "antibiotic_indicated": True,
        "recommended_regimen": "Amoxicillin-Clavulanate 625mg PO BD for 5-7 days.",
        "rationale": "Indicated when symptoms persist >10 days without clinical improvement.",
    },
    "SYN_PYELONEPHRITIS_UNCOMPLICATED": {
        "condition_name": "Acute Uncomplicated Pyelonephritis (Outpatient)",
        "source": "ICMR STG 2022 - Urology",
        "antibiotic_indicated": True,
        "recommended_regimen": "Cefpodoxime 200mg PO BD for 10 days, or initial IV Ceftriaxone 1g dose.",
        "rationale": "Requires prompt upper urinary tract antimicrobial penetration.",
    },
    "SYN_ASYMPTOMATIC_BACTERIURIA_PREGNANCY": {
        "condition_name": "Asymptomatic Bacteriuria in Pregnancy",
        "source": "ICMR STG 2022 - Obstetrics",
        "antibiotic_indicated": True,
        "recommended_regimen": "Cefalexin 500mg PO QID for 5 days or single-dose Fosfomycin 3g.",
        "rationale": "Mandatory treatment in pregnancy to prevent pyelonephritis, preterm labor, and low birth weight.",
    },
}


class AMRKnowledgeService:
    """Service providing grounded antimicrobial resistance knowledge and STG recommendations."""

    def __init__(self):
        self._drug_catalogue = DRUG_CATALOGUE
        self._guidelines = ICMR_GUIDELINES
        self._banned_fdcs = BANNED_FDCS

    def normalize_drug_name(self, name: str) -> str:
        """Normalize drug name string for lookup."""
        clean = re.sub(r"[\s\-_]+", " ", name.strip().lower())
        return clean

    def get_drug_info(self, drug_name: str) -> dict[str, Any]:
        """Look up reference clinical information for an active ingredient."""
        key = self.normalize_drug_name(drug_name)
        if key in self._drug_catalogue:
            return self._drug_catalogue[key]

        # Partial matching
        for k, v in self._drug_catalogue.items():
            if k in key or key in k:
                return v

        return {
            "generic_name": drug_name,
            "drug_class": "Unclassified",
            "aware_class": "Unclassified",
            "is_antibiotic": True,
            "is_fluoroquinolone": False,
            "is_beta_lactam": False,
            "pregnancy_safe": True,
            "min_age_years": 0.0,
        }

    def check_banned_fdc(self, drug_name: str) -> bool:
        """Check if drug represents a banned fixed-dose combination under CDSCO Gazette notifications."""
        norm = self.normalize_drug_name(drug_name)
        for banned in self._banned_fdcs:
            if banned in norm:
                return True
        return False

    def get_guideline(self, indication_code: str | None) -> dict[str, Any] | None:
        """Fetch ICMR Standard Treatment Guideline recommendation for a condition code."""
        if not indication_code:
            return None
        return self._guidelines.get(indication_code)

    def get_resistance_evidence(self, drug_name: str, indication_code: str | None = None) -> str | None:
        """Fetch surveillance resistance evidence from NCDC/ICMR datasets for drug/condition pair."""
        norm = self.normalize_drug_name(drug_name)

        if "ciprofloxacin" in norm or "ofloxacin" in norm or "norfloxacin" in norm:
            if indication_code == "SYN_UNCOMPLICATED_UTI":
                return (
                    "E. coli fluoroquinolone resistance exceeds 75% in Indian surveillance data (NCDC/ICMR). "
                    "Empirical fluoroquinolones are strictly discouraged for lower UTI."
                )
            if indication_code == "SYN_WATERY_DIARRHEA":
                return (
                    "High prevalence of fluoroquinolone resistance in enteric pathogens; "
                    "antimicrobials are not recommended for non-cholera watery diarrhea."
                )

        if "azithromycin" in norm and indication_code in {"SYN_ACUTE_BRONCHITIS", "SYN_COMMON_COLD"}:
            return (
                "Self-limiting viral etiology. Widespread empiric macrolide prescribing fuels "
                "azithromycin resistance in Streptococcus pneumoniae and Mycoplasma species."
            )

        if "meropenem" in norm and indication_code == "SYN_UNCOMPLICATED_UTI":
            return (
                "WHO Reserve antibiotic. Carbapenems should be strictly reserved for multi-drug resistant "
                "infections confirmed by microbiological culture to prevent carbapenemase (NDM/OXA-48) spread."
            )

        return None

    def get_assistive_guidance(
        self,
        prescription_lines: list[dict[str, Any]],
        indication_code: str | None = None,
    ) -> dict[str, Any]:
        """Generate composite assistive clinical guidance for the prescription intake draft."""
        guideline = self.get_guideline(indication_code)
        guidance_lines = []

        for line in prescription_lines:
            d_name = line.get("drugName", "")
            d_info = self.get_drug_info(d_name)
            is_banned = self.check_banned_fdc(d_name)
            res_ev = self.get_resistance_evidence(d_name, indication_code)

            guidance_lines.append({
                "drug_name": d_name,
                "aware_class": d_info.get("aware_class", "Unclassified"),
                "is_banned_fdc": is_banned,
                "resistance_evidence": res_ev,
            })

        return {
            "indication_code": indication_code,
            "guideline_summary": guideline.get("recommended_regimen") if guideline else None,
            "antibiotic_indicated": guideline.get("antibiotic_indicated") if guideline else None,
            "drug_guidance": guidance_lines,
            "disclaimer": "Assistive clinical context only. Does not replace clinician judgment.",
        }


@lru_cache
def get_amr_knowledge_service() -> AMRKnowledgeService:
    """Singleton getter for AMRKnowledgeService."""
    return AMRKnowledgeService()
