"""Assistive Intake Extraction Adapter.

Extracts structured clinical facts from prescription images/PDFs with confidence ratings.
SAFETY GUARANTEE: Output is strictly an editable draft. It NEVER triggers an automatic audit.
"""
import re
from typing import Any

from app.config import get_settings


class ExtractionAdapter:
    """Intake adapter with cloud Gemini multimodal extraction and offline heuristic fallback."""

    def __init__(self):
        self.settings = get_settings()

    async def extract_from_bytes(
        self,
        file_bytes: bytes,
        mime_type: str,
        filename: str = "prescription.pdf",
    ) -> dict[str, Any]:
        """Extract draft prescription fields from document bytes."""
        # Check if Gemini API is available and configured
        if self.settings.GEMINI_API_KEY and len(self.settings.GEMINI_API_KEY) > 10:
            try:
                return await self._extract_with_gemini(file_bytes, mime_type)
            except Exception as e:  # noqa: BLE001
                # Log redaction notice and fallback gracefully
                print(f"[ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: {e}")

        # Local offline heuristic fallback
        return self._extract_with_local_heuristics(file_bytes, filename)

    async def _extract_with_gemini(self, file_bytes: bytes, mime_type: str) -> dict[str, Any]:
        """Assistive extraction using Gemini API."""
        import httpx

        prompt = (
            "Extract clinical prescription facts from this synthetic doctor prescription. "
            "Return JSON matching: "
            "{"
            "  patientContext: { ageYears: float, gender: 'female'|'male'|'other', isPregnant: bool, egfrMlMin: float|null, allergies: [string] },"
            "  indicationCode: string,"
            "  prescriptionLines: [{ drugName: string, doseText: string, frequencyText: string, durationDays: int|null }],"
            "  fieldConfidence: { ageYears: 'high'|'medium'|'low', drugs: 'high'|'medium'|'low' }"
            "}"
        )

        # Call Gemini REST API directly with timeout
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.settings.GEMINI_API_KEY}"
        import base64
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

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                result_json = resp.json()
                text_content = result_json["candidates"][0]["content"]["parts"][0]["text"]
                import json
                parsed = json.loads(text_content)
                parsed["extraction_engine"] = "gemini_2.5_flash"
                return parsed

        raise RuntimeError("Gemini extraction non-200 response")

    def _extract_with_local_heuristics(self, file_bytes: bytes, filename: str) -> dict[str, Any]:
        """Offline deterministic heuristic extractor for synthetic demo prescriptions."""
        text_content = file_bytes.decode("utf-8", errors="ignore")

        # Age extraction
        age_match = re.search(r"(?:age|yr|years?)\s*[:=]?\s*(\d{1,3})", text_content, re.IGNORECASE)
        age = float(age_match.group(1)) if age_match else 34.0
        age_conf = "high" if age_match else "low"

        # Gender / Pregnancy
        is_preg = bool(re.search(r"\bpregnant|pregnancy|trimester\b", text_content, re.IGNORECASE))
        gender = "female" if (is_preg or re.search(r"\bfemale\b", text_content, re.IGNORECASE)) else "male"

        # eGFR extraction
        egfr_match = re.search(r"(?:egfr|gfr|creatinine clearance)\s*[:=]?\s*(\d{1,3})", text_content, re.IGNORECASE)
        egfr = float(egfr_match.group(1)) if egfr_match else None

        # Drug detection matching known brands and generics
        detected_lines: list[dict[str, Any]] = []
        brand_mappings = [
            ("cifran", "Ciprofloxacin", "250 mg", "Twice daily (BD)", 5),
            ("ciprofloxacin", "Ciprofloxacin", "250 mg", "Twice daily (BD)", 5),
            ("augmentin", "Amoxicillin-Clavulanate", "625 mg", "Twice daily (BD)", 5),
            ("azithral", "Azithromycin", "500 mg", "Once daily (OD)", 5),
            ("azithromycin", "Azithromycin", "500 mg", "Once daily (OD)", 5),
            ("martifur", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
            ("nitrofurantoin", "Nitrofurantoin", "100 mg", "Twice daily (BD)", 5),
            ("meronem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 7),
            ("meropenem", "Meropenem", "1000 mg", "Every 8 hours (TDS)", 7),
            ("gentamicin", "Gentamicin", "80 mg", "Twice daily (BD)", None),
            ("amoxicillin", "Amoxicillin", "500 mg", "Three times daily (TID)", 5),
        ]

        for token, generic, dose, freq, dur in brand_mappings:
            if token in text_content.lower() or token in filename.lower():
                detected_lines.append({
                    "drugName": generic,
                    "doseText": dose,
                    "frequencyText": freq,
                    "durationDays": dur,
                })
                break

        if not detected_lines:
            detected_lines.append({
                "drugName": "Amoxicillin",
                "doseText": "500 mg",
                "frequencyText": "Three times daily (TID)",
                "durationDays": 5,
            })

        return {
            "patientContext": {
                "ageYears": age,
                "gender": gender,
                "isPregnant": is_preg,
                "egfrMlMin": egfr,
                "allergies": [],
            },
            "indicationCode": "SYN_CAP_MILD",
            "setting": "outpatient",
            "prescriptionLines": detected_lines,
            "fieldConfidence": {
                "ageYears": age_conf,
                "gender": "high" if is_preg else "medium",
                "egfrMlMin": "high" if egfr else "unrecorded",
                "prescriptionLines": "medium",
            },
            "extraction_engine": "offline_heuristic_adapter",
            "clinical_status": "UNTRUSTED_DRAFT_PENDING_CONFIRMATION",
            "disclaimer": "Assistive extraction only. Clinician must verify all fields prior to clinical audit.",
        }
