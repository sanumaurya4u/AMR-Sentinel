"""High-speed fuzzy entity resolution using RapidFuzz for pharmaceutical brand & generic matching."""
import re
from typing import Any

from rapidfuzz import fuzz, process

# Comprehensive Indian clinical brand-to-generic mappings
PHARMA_BRAND_CATALOG: list[dict[str, Any]] = [
    # Banned Fixed-Dose Combinations (CDSCO Directives)
    {
        "brand_name": "Cefixime + Azithromycin",
        "generic_name": "Cefixime + Azithromycin",
        "aliases": ["cefixime azithromycin", "zifi az", "taxim az", "mahacef az"],
        "default_dose": "200 mg + 250 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": True,
    },
    {
        "brand_name": "Ofloxacin + Ornidazole",
        "generic_name": "Ofloxacin + Ornidazole",
        "aliases": ["oflox oz", "ofloxacin ornidazole", "zanocin oz", "zenflox oz", "o2"],
        "default_dose": "200 mg + 500 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": True,
    },
    {
        "brand_name": "Amoxicillin + Flucloxacillin",
        "generic_name": "Amoxicillin + Flucloxacillin",
        "aliases": ["amoxicillin flucloxacillin", "flumox", "moxikind f"],
        "default_dose": "500 mg + 500 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": True,
    },
    {
        "brand_name": "Ampicillin + Cloxacillin",
        "generic_name": "Ampicillin + Cloxacillin",
        "aliases": ["ampicillin cloxacillin", "ampiclox", "megapen", "novaclox"],
        "default_dose": "250 mg + 250 mg",
        "default_freq": "Four times daily (QID)",
        "default_duration": 5,
        "is_banned_fdc": True,
    },
    {
        "brand_name": "Ciprofloxacin + Tinidazole",
        "generic_name": "Ciprofloxacin + Tinidazole",
        "aliases": ["cifran ct", "ciplox tz", "ciprofloxacin tinidazole"],
        "default_dose": "500 mg + 600 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": True,
    },
    # Common Single-Entity Antimicrobials & Supportive Agents
    {
        "brand_name": "Augmentin",
        "generic_name": "Amoxicillin-Clavulanate",
        "aliases": ["augmentin 625", "clavam", "clavam 625", "moxikind cv", "amoxyclav", "megaclav", "co-amoxiclav"],
        "default_dose": "625 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Amoxil",
        "generic_name": "Amoxicillin",
        "aliases": ["almox", "cipmox", "novamox", "mox 500", "amoxicillin 500"],
        "default_dose": "500 mg",
        "default_freq": "Three times daily (TID)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Niftas",
        "generic_name": "Nitrofurantoin",
        "aliases": ["martifur", "urifast", "nitrofurantoin 100", "niftran"],
        "default_dose": "100 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Cifran",
        "generic_name": "Ciprofloxacin",
        "aliases": ["cifran 500", "cifran 250", "ciplox", "alcipro", "cipro 500"],
        "default_dose": "500 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Azithral",
        "generic_name": "Azithromycin",
        "aliases": ["azithral 500", "azee", "azee 500", "zady", "azibact", "laz 500"],
        "default_dose": "500 mg",
        "default_freq": "Once daily (OD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Taxim-O",
        "generic_name": "Cefixime",
        "aliases": ["taxim-o 200", "zifi", "zifi 200", "mahacef", "cefolac", "omnicef-o"],
        "default_dose": "200 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Doxicip",
        "generic_name": "Doxycycline",
        "aliases": ["doxy-1", "microdox", "doxycycline 100"],
        "default_dose": "100 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Phexin",
        "generic_name": "Cefalexin",
        "aliases": ["sporidex", "ceff", "cefalexin 500"],
        "default_dose": "500 mg",
        "default_freq": "Four times daily (QID)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Meronem",
        "generic_name": "Meropenem",
        "aliases": ["meropenem 1g", "merocrit", "meromac"],
        "default_dose": "1000 mg",
        "default_freq": "Every 8 hours (TDS)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Linospan",
        "generic_name": "Linezolid",
        "aliases": ["zyvox", "lizomac", "linezolid 600"],
        "default_dose": "600 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Genticyn",
        "generic_name": "Gentamicin",
        "aliases": ["gentamicin 80", "genta"],
        "default_dose": "80 mg",
        "default_freq": "Twice daily (BD)",
        "default_duration": 5,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Oral Rehydration Salts (ORS) + Zinc",
        "generic_name": "Oral Rehydration Salts (ORS) + Zinc",
        "aliases": ["ors", "electral", "ors zinc", "pedialyte", "rehydration salts"],
        "default_dose": "1 sachet + 20 mg",
        "default_freq": "As directed",
        "default_duration": 14,
        "is_banned_fdc": False,
    },
    {
        "brand_name": "Calpol",
        "generic_name": "Paracetamol",
        "aliases": ["dolo", "dolo 650", "crocin", "crocin 650", "paracetamol 650", "pacimol"],
        "default_dose": "650 mg",
        "default_freq": "Three times daily (TDS)",
        "default_duration": 3,
        "is_banned_fdc": False,
    },
]


class DrugEntityMatcher:
    """RapidFuzz-powered brand-to-generic entity resolver."""

    def __init__(self, score_cutoff: float = 72.0):
        self.score_cutoff = score_cutoff
        self._lookup: dict[str, dict[str, Any]] = {}
        self._corpus: list[str] = []
        self._build_index()

    def _build_index(self) -> None:
        """Flatten brand catalog into normalized search corpus."""
        for entry in PHARMA_BRAND_CATALOG:
            # Map canonical brand and generic
            self._add_term(entry["brand_name"].lower(), entry)
            self._add_term(entry["generic_name"].lower(), entry)
            for alias in entry.get("aliases", []):
                self._add_term(alias.lower(), entry)

    def _add_term(self, term: str, entry: dict[str, Any]) -> None:
        clean = re.sub(r"[^\w\s\+]", " ", term).strip()
        if clean and clean not in self._lookup:
            self._lookup[clean] = entry
            self._corpus.append(clean)

    def match_drug(self, text: str) -> tuple[dict[str, Any] | None, float]:
        """Match input string against corpus using RapidFuzz WRatio metric."""
        clean_query = re.sub(r"[^\w\s\+]", " ", text.lower()).strip()
        if not clean_query:
            return None, 0.0

        match = process.extractOne(
            clean_query,
            self._corpus,
            scorer=fuzz.WRatio,
            score_cutoff=self.score_cutoff,
        )

        if match:
            matched_term, score, _ = match
            return self._lookup[matched_term], score

        return None, 0.0

    def resolve_entities_in_text(self, text: str) -> list[dict[str, Any]]:
        """Scan free-form clinical text for multiple drug references."""
        tokens = re.split(r"[\n,;]+", text)
        found: list[dict[str, Any]] = []
        seen_generics = set()

        for token in tokens:
            token = token.strip()
            if len(token) < 2:
                continue
            entry, score = self.match_drug(token)
            if entry and entry["generic_name"] not in seen_generics:
                seen_generics.add(entry["generic_name"])
                found.append({
                    "raw_token": token,
                    "matched_generic": entry["generic_name"],
                    "matched_brand": entry["brand_name"],
                    "default_dose": entry["default_dose"],
                    "default_freq": entry["default_freq"],
                    "default_duration": entry["default_duration"],
                    "is_banned_fdc": entry["is_banned_fdc"],
                    "confidence_score": round(score, 1),
                })

        return found


_matcher_instance: DrugEntityMatcher | None = None


def get_drug_entity_matcher() -> DrugEntityMatcher:
    """Singleton getter for DrugEntityMatcher."""
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = DrugEntityMatcher()
    return _matcher_instance
