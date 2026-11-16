"""Assistive Intake Extraction Adapter.

Extracts structured clinical facts from prescription images/PDFs with confidence ratings.
SAFETY GUARANTEE: Output is strictly an editable draft. It NEVER triggers an automatic audit.
"""
import base64
import json
import re
from typing import Any

from app.config import get_settings
from app.extraction.fuzzy_match import get_drug_entity_matcher
from app.services.amr_knowledge import get_amr_knowledge_service

# Comprehensive brand-to-generic catalog derived from Indian pharmaceutical records
# (including data_sets/Tamil/Anti/brands.csv and antibiotic_brand_to_generic_alias_lookup.csv)
BRAND_MAPPINGS: list[tuple[str, str, str, str, int | None]] = [
    # Banned FDCs (checked first to match compound phrases before single tokens)
    ("cefixime + azithromycin", "Cefixime + Azithromycin", "200 mg + 250 mg", "Twice daily (BD)", 5),
    ("ofloxacin + ornidazole", "Ofloxacin + Ornidazole", "200 mg + 500 mg", "Twice daily (BD)", 5),
    ("amoxicillin + flucloxacillin", "Amoxicillin + Flucloxacillin", "500 mg + 500 mg", "Twice daily (BD)", 5),
    ("ampicillin + cloxacillin", "Ampicillin + Cloxacillin", "250 mg + 250 mg", "Four times daily (QID)", 5),
    ("ciprofloxacin + tinidazole", "Ciprofloxacin + Tinidazole", "500 mg + 600 mg", "Twice daily (BD)", 5),
    # Supportive & Non-antibiotics
    ("oral rehydration salts", "Oral Rehydration Salts (ORS) + Zinc", "1 sachet + 20 mg", "As directed", 14),
    ("ors + zinc", "Oral Rehydration Salts (ORS) + Zinc", "1 sachet + 20 mg", "As directed", 14),
    ("ors", "Oral Rehydration Salts (ORS) + Zinc", "1 sachet + 20 mg", "As directed", 14),
    ("paracetamol", "Paracetamol", "650 mg", "Three times daily (TDS)", 3),
    ("calpol", "Paracetamol", "650 mg", "Three times daily (TDS)", 3),
    ("dolo", "Paracetamol", "650 mg", "Three times daily (TDS)", 3),
    ("crocin", "Paracetamol", "650 mg", "Three times daily (TDS)", 3),
    # Aminopenicillins & BLIs
    ("augmentin", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("clavam", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("moxikind-cv", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("amoxyclav", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("megaclav", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("amoxicillin-clavulanate", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("co-amoxiclav", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
    ("amoxil", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    ("almox", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    ("cipmox", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    ("novamox", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    ("mox", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    ("amoxicillin", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
    # Nitrofurans
    ("martifur", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
    ("niftas", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
    ("urifast", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
    ("nitrofurantoin", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
    # Macrolides
    ("azithral", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("azee", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("zady", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("azibact", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("laz", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("azithromycin", "Azithromycin", "500 mg", "Once daily (OD)", 5),
    ("clarithromycin", "Clarithromycin", "500 mg", "Twice daily (BD)", 5),
    # Fluoroquinolones
    ("cifran", "Ciprofloxacin", "500 mg", "Twice daily (BD)", 5),
    ("ciplox", "Ciprofloxacin", "500 mg", "Twice daily (BD)", 5),
    ("alcipro", "Ciprofloxacin", "500 mg", "Twice daily (BD)", 5),
    ("ciprofloxacin", "Ciprofloxacin", "500 mg", "Twice daily (BD)", 5),
    ("levomac", "Levofloxacin", "500 mg", "Once daily (OD)", 5),
    ("l-cin", "Levofloxacin", "500 mg", "Once daily (OD)", 5),
    ("glevo", "Levofloxacin", "500 mg", "Once daily (OD)", 5),
    ("levofloxacin", "Levofloxacin", "500 mg", "Once daily (OD)", 5),
    ("oflox", "Ofloxacin", "200 mg", "Twice daily (BD)", 5),
    ("zanocin", "Ofloxacin", "200 mg", "Twice daily (BD)", 5),
    ("zenflox", "Ofloxacin", "200 mg", "Twice daily (BD)", 5),
    ("ofloxacin", "Ofloxacin", "200 mg", "Twice daily (BD)", 5),
    ("norflox", "Norfloxacin", "400 mg", "Twice daily (BD)", 5),
    ("norbactin", "Norfloxacin", "400 mg", "Twice daily (BD)", 5),
    ("norfloxacin", "Norfloxacin", "400 mg", "Twice daily (BD)", 5),
    # Tetracyclines
    ("doxicip", "Doxycycline", "100 mg", "Twice daily (BD)", 5),
    ("doxy-1", "Doxycycline", "100 mg", "Twice daily (BD)", 5),
    ("microdox", "Doxycycline", "100 mg", "Twice daily (BD)", 5),
    ("doxycycline", "Doxycycline", "100 mg", "Twice daily (BD)", 5),
    # Cephalosporins
    ("phexin", "Cefalexin", "500 mg", "Four times daily (QID)", 5),
    ("sporidex", "Cefalexin", "500 mg", "Four times daily (QID)", 5),
    ("ceff", "Cefalexin", "500 mg", "Four times daily (QID)", 5),
    ("cefalexin", "Cefalexin", "500 mg", "Four times daily (QID)", 5),
    ("taxim-o", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("zifi", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("mahacef", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("cefolac", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("omnicef-o", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("cefixime", "Cefixime", "200 mg", "Twice daily (BD)", 5),
    ("monocef", "Ceftriaxone", "1000 mg", "Once daily (OD)", 5),
    ("c-tri", "Ceftriaxone", "1000 mg", "Once daily (OD)", 5),
    ("xone", "Ceftriaxone", "1000 mg", "Once daily (OD)", 5),
    ("ceftriaxone", "Ceftriaxone", "1000 mg", "Once daily (OD)", 5),
    ("ceftum", "Cefuroxime", "500 mg", "Twice daily (BD)", 5),
    ("cetil", "Cefuroxime", "500 mg", "Twice daily (BD)", 5),
    ("cefuroxime", "Cefuroxime", "500 mg", "Twice daily (BD)", 5),
    ("gudcef", "Cefpodoxime", "200 mg", "Twice daily (BD)", 10),
    ("doxcef", "Cefpodoxime", "200 mg", "Twice daily (BD)", 10),
    ("macpod", "Cefpodoxime", "200 mg", "Twice daily (BD)", 10),
    ("cefpodoxime", "Cefpodoxime", "200 mg", "Twice daily (BD)", 10),
    # Carbapenems & Reserve
    ("meronem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 5),
    ("meropenem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 5),
    ("linospan", "Linezolid", "600 mg", "Twice daily (BD)", 5),
    ("zyvox", "Linezolid", "600 mg", "Twice daily (BD)", 5),
    ("lizomac", "Linezolid", "600 mg", "Twice daily (BD)", 5),
    ("linezolid", "Linezolid", "600 mg", "Twice daily (BD)", 5),
    ("colistin", "Colistin", "150 mg", "Twice daily (BD)", 7),
    # Aminoglycosides
    ("gentamicin", "Gentamicin", "80 mg", "Twice daily (BD)", 5),
    ("genticyn", "Gentamicin", "80 mg", "Twice daily (BD)", 5),
    ("amikacin", "Amikacin", "500 mg", "Twice daily (BD)", 5),
    ("amicip", "Amikacin", "500 mg", "Twice daily (BD)", 5),
    # Antipseudomonals
    ("pipzo", "Piperacillin-Tazobactam", "4500 mg", "Every 6 hours (QID)", 7),
    ("piperacillin-tazobactam", "Piperacillin-Tazobactam", "4500 mg", "Every 6 hours (QID)", 7),
]

# Indication Keyword Rule Table mapped to ICMR canonical condition codes
INDICATION_KEYWORDS: list[tuple[list[str], str]] = [
    (["asymptomatic bacteriuria"], "SYN_ASYMPTOMATIC_BACTERIURIA_PREGNANCY"),
    (["watery diarrhea", "diarrhea", "loose motion", "cholera", "gastroenteritis"], "SYN_WATERY_DIARRHEA"),
    (["streptococcal pharyngitis", "strep pharyngitis", "exudative tonsillitis"], "SYN_PHARYNGITIS_STREP"),
    (["non-streptococcal pharyngitis", "viral sore throat", "sore throat", "non-strep"], "SYN_PHARYNGITIS_NON_STREP"),
    (["otitis media", "aom", "ear pain", "ear discharge"], "SYN_AOM"),
    (["acute bronchitis", "bronchitis"], "SYN_ACUTE_BRONCHITIS"),
    (["common cold", "rhinopharyngitis", "rhinorrhea", "coryza", "sneezing"], "SYN_COMMON_COLD"),
    (["viral urti", "upper respiratory", "urti"], "SYN_VIRAL_URTI"),
    (["pyelonephritis", "flank pain", "costovertebral"], "SYN_PYELONEPHRITIS_UNCOMPLICATED"),
    (["cystitis", "lower uti", "dysuria", "burning micturition", "uti"], "SYN_UNCOMPLICATED_UTI"),
    (["cellulitis", "impetigo", "ssti", "skin infection", "furuncle", "soft tissue"], "SYN_SSTI_UNCOMPLICATED"),
    (["rhinosinusitis", "sinusitis", "facial pain", "nasal purulence"], "SYN_ACUTE_RHINOSINUSITIS"),
    (["pneumonia", "cap", "consolidation", "rales", "chest infection"], "SYN_CAP_MILD"),
]


class ExtractionAdapter:
    """Intake adapter with calibrated Gemini multimodal extraction and offline heuristic fallback."""

    def __init__(self):
        self.settings = get_settings()
        self.knowledge_service = get_amr_knowledge_service()
        self._cloud_disabled = False

    async def extract_from_bytes(
        self,
        file_bytes: bytes,
        mime_type: str,
        filename: str = "prescription.pdf",
    ) -> dict[str, Any]:
        """Extract draft prescription fields from document bytes."""
        # Attempt cloud extraction if key configured and circuit breaker open
        if (
            not self._cloud_disabled
            and self.settings.GEMINI_API_KEY
            and len(self.settings.GEMINI_API_KEY) > 10
        ):
            try:
                return await self._extract_with_gemini(file_bytes, mime_type)
            except Exception as e:  # noqa: BLE001
                # If credentials invalid or non-200, disable cloud calls for fast offline processing
                self._cloud_disabled = True
                print(f"[ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: {e}")

        # Local offline heuristic fallback
        return self._extract_with_local_heuristics(file_bytes, filename)

    async def _extract_with_gemini(self, file_bytes: bytes, mime_type: str) -> dict[str, Any]:
        """Assistive extraction using Gemini API calibrated with Indian clinical exemplars."""
        import httpx

        prompt = (
            "You are an expert clinical intake assistant for the AMR Sentinel Stewardship System. "
            "Extract structured clinical facts from this doctor prescription into strictly valid JSON.\n\n"
            "SCHEMA SPECIFICATION:\n"
            "{\n"
            '  "patientContext": {\n'
            '    "ageYears": float,\n'
            '    "gender": "female" | "male" | "other",\n'
            '    "isPregnant": bool,\n'
            '    "egfrMlMin": float | null,\n'
            '    "allergies": [string]\n'
            "  },\n"
            '  "indicationCode": "SYN_CAP_MILD" | "SYN_UNCOMPLICATED_UTI" | "SYN_ACUTE_BRONCHITIS" | "SYN_COMMON_COLD" | "SYN_VIRAL_URTI" | "SYN_PHARYNGITIS_NON_STREP" | "SYN_WATERY_DIARRHEA" | "SYN_PHARYNGITIS_STREP" | "SYN_AOM" | "SYN_SSTI_UNCOMPLICATED" | "SYN_ACUTE_RHINOSINUSITIS" | "SYN_PYELONEPHRITIS_UNCOMPLICATED" | "SYN_ASYMPTOMATIC_BACTERIURIA_PREGNANCY",\n'
            '  "prescriptionLines": [\n'
            "    {\n"
            '      "drugName": string (canonical generic active ingredient or banned FDC, e.g. "Amoxicillin", "Ciprofloxacin", "Amoxicillin-Clavulanate", "Nitrofurantoin", "Azithromycin", "Cefixime + Azithromycin", "Oral Rehydration Salts (ORS) + Zinc"),\n'
            '      "doseText": string (e.g. "500 mg", "100 mg", "250 mg", "625 mg", "1 sachet + 20 mg"),\n'
            '      "frequencyText": string (e.g. "Twice daily (BD)", "Three times daily (TID)", "Once daily (OD)", "Four times daily (QID)", "As directed"),\n'
            '      "durationDays": integer | null\n'
            "    }\n"
            "  ],\n"
            '  "fieldConfidence": {\n'
            '    "ageYears": "high" | "medium" | "low",\n'
            '    "drugs": "high" | "medium" | "low"\n'
            "  }\n"
            "}\n\n"
            "FEW-SHOT CLINICAL EXAMPLES:\n"
            "Example 1 (Pediatric Diarrhea):\n"
            "Input: Patient: Master Aarav, 8 yrs Male. Watery diarrhea. Rx: Tab Cifran 250mg BD x 5d.\n"
            'Output: {"patientContext": {"ageYears": 8.0, "gender": "male", "isPregnant": false, "egfrMlMin": null, "allergies": []}, "indicationCode": "SYN_WATERY_DIARRHEA", "prescriptionLines": [{"drugName": "Ciprofloxacin", "doseText": "250 mg", "frequencyText": "Twice daily (BD)", "durationDays": 5}], "fieldConfidence": {"ageYears": "high", "drugs": "high"}}\n\n'
            "Example 2 (Cystitis with Brand Resolution):\n"
            "Input: Priya, 42 F. Burning micturition. Rx: Cap Niftas 100mg BD x 5 days.\n"
            'Output: {"patientContext": {"ageYears": 42.0, "gender": "female", "isPregnant": false, "egfrMlMin": null, "allergies": []}, "indicationCode": "SYN_UNCOMPLICATED_UTI", "prescriptionLines": [{"drugName": "Nitrofurantoin", "doseText": "100 mg", "frequencyText": "Twice daily (BD)", "durationDays": 5}], "fieldConfidence": {"ageYears": "high", "drugs": "high"}}\n\n'
            "Example 3 (Banned Fixed Dose Combination):\n"
            "Input: Manoj, 34 M. Mild CAP. Rx: Tab Cefixime + Azithromycin 200mg+250mg BD x 5d.\n"
            'Output: {"patientContext": {"ageYears": 34.0, "gender": "male", "isPregnant": false, "egfrMlMin": null, "allergies": []}, "indicationCode": "SYN_CAP_MILD", "prescriptionLines": [{"drugName": "Cefixime + Azithromycin", "doseText": "200 mg + 250 mg", "frequencyText": "Twice daily (BD)", "durationDays": 5}], "fieldConfidence": {"ageYears": "high", "drugs": "high"}}\n'
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.settings.GEMINI_API_KEY}"
        b64_data = base64.b64encode(file_bytes).decode("utf-8")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": mime_type, "data": b64_data}},
                    ]
                }
            ],
            "generationConfig": {"response_mime_type": "application/json"},
        }

        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                result_json = resp.json()
                text_content = result_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_content)
                parsed["extraction_engine"] = "gemini_2.5_flash"
                parsed["clinical_status"] = "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"
                parsed["disclaimer"] = "Assistive extraction only. Clinician must verify all fields prior to clinical audit."
                # Attach assistive AMR knowledge
                parsed["amr_guidance"] = self.knowledge_service.get_assistive_guidance(
                    parsed.get("prescriptionLines", []),
                    parsed.get("indicationCode"),
                )
                return parsed

        raise RuntimeError(f"Gemini API returned status {resp.status_code}")

    def _extract_with_local_heuristics(self, file_bytes: bytes, filename: str) -> dict[str, Any]:
        """Offline deterministic heuristic extractor calibrated against Indian AMR datasets."""
        text_content = file_bytes.decode("utf-8", errors="ignore")
        lowered = f"{text_content.lower()} {filename.lower()}"

        # 1. Demographics: Age
        age_match = re.search(r"(?:age|yr|years?)\s*[:=]?\s*(\d{1,3}(?:\.\d+)?)", text_content, re.IGNORECASE)
        if not age_match:
            # Fallback patterns like "8 yrs", "8 yo", "8 year old"
            age_match = re.search(r"\b(\d{1,3})\s*(?:yrs?|yo|year(?:\s*old)?)\b", text_content, re.IGNORECASE)
        age = float(age_match.group(1)) if age_match else 34.0
        age_conf = "high" if age_match else "low"

        # 2. Demographics: Pregnancy & Gender
        is_preg = bool(re.search(r"\b(?:pregnant|pregnancy|trimester|antenatal|gestation)\b", text_content, re.IGNORECASE))
        if is_preg or re.search(r"\b(?:female|woman|girl|mrs|ms)\b", text_content, re.IGNORECASE):
            gender = "female"
            gender_conf = "high"
        elif re.search(r"\b(?:male|man|boy|mr|master)\b", text_content, re.IGNORECASE):
            gender = "male"
            gender_conf = "high"
        else:
            gender = "female"
            gender_conf = "medium"

        # 3. Demographics: eGFR
        egfr = None
        egfr_conf = "unrecorded"
        # Check if explicitly not recorded
        if not re.search(r"(?:egfr|gfr)\s*[:=]?\s*(?:not recorded|pending|unknown|none|nil)", text_content, re.IGNORECASE):
            egfr_match = re.search(r"(?:egfr|gfr|creatinine clearance)\s*[:=]?\s*(\d{1,3}(?:\.\d+)?)", text_content, re.IGNORECASE)
            if egfr_match:
                egfr = float(egfr_match.group(1))
                egfr_conf = "high"

        # 4. Demographics: Allergies
        allergies: list[str] = []
        allergy_match = re.search(r"(?:allergy|allergies|allergic to)\s*[:=]?\s*([a-zA-Z\s,]+)", text_content, re.IGNORECASE)
        if allergy_match:
            allergy_str = allergy_match.group(1).lower()
            if "none" not in allergy_str and "nil" not in allergy_str and "no known" not in allergy_str:
                if "penicillin" in allergy_str:
                    allergies.append("Penicillin")
                elif "sulfa" in allergy_str:
                    allergies.append("Sulfa")
                elif "aspirin" in allergy_str:
                    allergies.append("Aspirin")

        # 5. Indication Code Classification
        detected_indication = "SYN_CAP_MILD"  # Default fallback
        ind_conf = "low"
        for kw_list, ind_code in INDICATION_KEYWORDS:
            if any(kw in lowered for kw in kw_list):
                detected_indication = ind_code
                ind_conf = "high"
                break

        # 6. Prescription Line Extraction (Drug, Posology, Frequency, Duration)
        detected_lines: list[dict[str, Any]] = []

        # Parse specific duration in text
        duration_days: int | None = None
        dur_match = re.search(r"(?:for|x)\s*(\d{1,2})\s*(?:days?|d\b)", text_content, re.IGNORECASE)
        if not dur_match:
            dur_match = re.search(r"\b(\d{1,2})\s*/\s*7\b", text_content)
        if dur_match:
            duration_days = int(dur_match.group(1))

        # Check for specific compound dosages (e.g. 200mg+250mg, 200mg+500mg, 500mg+500mg)
        combo_dose_match = re.search(r"(\d+\s*mg\s*\+\s*\d+\s*mg)", text_content, re.IGNORECASE)
        custom_combo_dose = combo_dose_match.group(1).replace(" ", "") if combo_dose_match else None
        if custom_combo_dose:
            custom_combo_dose = re.sub(r"(\d+mg)\+(\d+mg)", r"\1 + \2", custom_combo_dose)

        # Scan for brand and generic entities
        matched_drugs_seen = set()
        for token, generic, def_dose, def_freq, def_dur in BRAND_MAPPINGS:
            # Word boundary check or substring in text
            if token in lowered:
                if generic in matched_drugs_seen:
                    continue
                matched_drugs_seen.add(generic)
                lowered = lowered.replace(token, " " * len(token))

                # Posology detection for this drug
                dose_text = def_dose
                if custom_combo_dose and "+" in generic:
                    dose_text = custom_combo_dose
                else:
                    # Check for gram dosages: e.g. 1g, 0.5g, 0.25g, 0.4g, 0.125g, 1.5g, 4.5g
                    g_match = re.search(r"\b(\d+(?:\.\d+)?)\s*g\b", text_content, re.IGNORECASE)
                    mg_match = re.search(r"\b(\d{2,4})\s*mg\b", text_content, re.IGNORECASE)
                    if mg_match:
                        dose_text = f"{mg_match.group(1)} mg"
                    elif g_match:
                        grams = float(g_match.group(1))
                        mg_val = int(grams * 1000) if grams.is_integer() else round(grams * 1000, 1)
                        dose_text = f"{mg_val} mg"

                # Frequency detection
                freq_text = def_freq
                if re.search(r"\b(?:qid|four times daily)\b", text_content, re.IGNORECASE):
                    freq_text = "Four times daily (QID)"
                elif re.search(r"\b(?:tid|tds|three times daily)\b", text_content, re.IGNORECASE):
                    freq_text = "Three times daily (TID)" if "tds" not in lowered else "Three times daily (TDS)"
                elif re.search(r"\b(?:bd|bid|twice daily)\b", text_content, re.IGNORECASE):
                    freq_text = "Twice daily (BD)"
                elif re.search(r"\b(?:od|once daily)\b", text_content, re.IGNORECASE):
                    freq_text = "Once daily (OD)"
                elif re.search(r"\b(?:every 8 hours|q8h)\b", text_content, re.IGNORECASE):
                    freq_text = "Every 8 hours (TDS)"
                elif re.search(r"\b(?:as directed)\b", text_content, re.IGNORECASE):
                    freq_text = "As directed"

                final_dur = duration_days if duration_days is not None else def_dur

                detected_lines.append({
                    "drugName": generic,
                    "doseText": dose_text,
                    "frequencyText": freq_text,
                    "durationDays": final_dur,
                })

        # RapidFuzz fallback if no exact brand token matched
        if not detected_lines:
            fuzzy_matcher = get_drug_entity_matcher()
            fuzzy_entities = fuzzy_matcher.resolve_entities_in_text(text_content)
            for fe in fuzzy_entities:
                detected_lines.append({
                    "drugName": fe["matched_generic"],
                    "doseText": fe["default_dose"],
                    "frequencyText": fe["default_freq"],
                    "durationDays": fe["default_duration"],
                })

        # Default fallback if still nothing detected
        if not detected_lines:
            detected_lines.append({
                "drugName": "Amoxicillin",
                "doseText": "500 mg",
                "frequencyText": "Three times daily (TID)",
                "durationDays": 5,
            })

        # Generate assistive AMR knowledge guidance
        amr_guidance = self.knowledge_service.get_assistive_guidance(detected_lines, detected_indication)

        return {
            "patientContext": {
                "ageYears": age,
                "gender": gender,
                "isPregnant": is_preg,
                "egfrMlMin": egfr,
                "allergies": allergies,
            },
            "indicationCode": detected_indication,
            "setting": "outpatient",
            "prescriptionLines": detected_lines,
            "fieldConfidence": {
                "ageYears": age_conf,
                "gender": gender_conf,
                "isPregnant": "high",
                "egfrMlMin": egfr_conf,
                "indicationCode": ind_conf,
                "prescriptionLines": "high" if len(matched_drugs_seen) > 0 else "low",
            },
            "extraction_engine": "offline_heuristic_adapter",
            "clinical_status": "UNTRUSTED_DRAFT_PENDING_CONFIRMATION",
            "disclaimer": "Assistive extraction only. Clinician must verify all fields prior to clinical audit.",
            "amr_guidance": amr_guidance,
        }
