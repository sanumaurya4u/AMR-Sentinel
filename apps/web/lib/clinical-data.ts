/**
 * Canonical Antimicrobial and Clinical Indication Reference Data
 * Grounded in ICMR Standard Treatment Guidelines 2022 & WHO AWaRe Classification 2023.
 */

export interface DrugCatalogItem {
  id: number;
  genericName: string;
  drugClass: string;
  isAntibiotic: boolean;
  awareClass: "Access" | "Watch" | "Reserve";
  isFluoroquinolone: boolean;
  pregnancyContraindicated: boolean;
  minAgeYears: number;
  commonBrands?: string[];
}

export interface ConditionCatalogItem {
  id: number;
  code: string;
  displayName: string;
  isSelfLimitingOrViral: boolean;
  icmrCategory: string;
}

export const DRUG_CATALOG: DrugCatalogItem[] = [
  { id: 1, genericName: "Amoxicillin", drugClass: "Aminopenicillin", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Mox", "Novamox", "Amoxil"] },
  { id: 2, genericName: "Amoxicillin-Clavulanate", drugClass: "Beta-lactam + Inhibitor", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Augmentin", "Clavam", "Moxikind-CV"] },
  { id: 3, genericName: "Nitrofurantoin", drugClass: "Nitrofuran", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 1, commonBrands: ["Martifur", "Niftran", "Furadantin"] },
  { id: 4, genericName: "Fosfomycin", drugClass: "Phosphonic acid", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 12, commonBrands: ["Monurol", "Fosfocin"] },
  { id: 5, genericName: "Cefalexin", drugClass: "First-gen Cephalosporin", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Sporidex", "Phexin"] },
  { id: 6, genericName: "Cefixime", drugClass: "Third-gen Cephalosporin", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.5, commonBrands: ["Zifi", "Taxim-O", "Cefolac"] },
  { id: 7, genericName: "Azithromycin", drugClass: "Macrolide", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.5, commonBrands: ["Azithral", "Azee", "Zithromax"] },
  { id: 8, genericName: "Ciprofloxacin", drugClass: "Fluoroquinolone", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: true, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["Cifran", "Ciplox"] },
  { id: 9, genericName: "Levofloxacin", drugClass: "Fluoroquinolone", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: true, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["Levomac", "Levaquin"] },
  { id: 10, genericName: "Ofloxacin", drugClass: "Fluoroquinolone", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: true, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["Zenflox", "Oflox"] },
  { id: 11, genericName: "Norfloxacin", drugClass: "Fluoroquinolone", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: true, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["Norflox"] },
  { id: 12, genericName: "Doxycycline", drugClass: "Tetracycline", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["Doxicip", "Doxt"] },
  { id: 13, genericName: "Meropenem", drugClass: "Carbapenem", isAntibiotic: true, awareClass: "Reserve", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.25, commonBrands: ["Meronem", "Mero"] },
  { id: 14, genericName: "Linezolid", drugClass: "Oxazolidinone", isAntibiotic: true, awareClass: "Reserve", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Lizomac", "Linid"] },
  { id: 15, genericName: "Colistin", drugClass: "Polymyxin", isAntibiotic: true, awareClass: "Reserve", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Coly-Mycin"] },
  { id: 16, genericName: "Amikacin", drugClass: "Aminoglycoside", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: true, minAgeYears: 0, commonBrands: ["Mikacin"] },
  { id: 17, genericName: "Gentamicin", drugClass: "Aminoglycoside", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: true, minAgeYears: 0, commonBrands: ["Garamycin"] },
  { id: 18, genericName: "Oral Rehydration Salts (ORS) + Zinc", drugClass: "Supportive Rehydration", isAntibiotic: false, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Electral", "Prolyte"] },
  { id: 19, genericName: "Paracetamol", drugClass: "Antipyretic Analgesic", isAntibiotic: false, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Dolo 650", "Calpol", "Crocin"] },
  { id: 20, genericName: "Ceftriaxone", drugClass: "Third-gen Cephalosporin", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.05, commonBrands: ["Monocef", "Rocephin"] },
  { id: 21, genericName: "Cefuroxime Axetil", drugClass: "Second-gen Cephalosporin", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.25, commonBrands: ["Ceftum", "Zinacef"] },
  { id: 22, genericName: "Piperacillin-Tazobactam", drugClass: "Antipseudomonal Penicillin + BLI", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0.15, commonBrands: ["Pipzo", "Tazomac"] },
  { id: 23, genericName: "Vancomycin", drugClass: "Glycopeptide", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 0, commonBrands: ["Vancocin"] },
  { id: 24, genericName: "Co-trimoxazole", drugClass: "Folate Pathway Inhibitor", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: true, minAgeYears: 0.15, commonBrands: ["Bactrim", "Septran"] },
  { id: 25, genericName: "Metronidazole", drugClass: "Nitroimidazole", isAntibiotic: true, awareClass: "Access", isFluoroquinolone: false, pregnancyContraindicated: true, minAgeYears: 0, commonBrands: ["Flagyl", "Metrogyl"] },
  // Banned Fixed-Dose Combinations (CDSCO & WHO Not Recommended)
  { id: 90, genericName: "Cefixime + Azithromycin", drugClass: "Banned FDC (Cephalosporin + Macrolide)", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: false, pregnancyContraindicated: false, minAgeYears: 18, commonBrands: ["Zifi-AZ", "Cefolac-AZ"] },
  { id: 91, genericName: "Ofloxacin + Ornidazole", drugClass: "Banned FDC (Fluoroquinolone + Nitroimidazole)", isAntibiotic: true, awareClass: "Watch", isFluoroquinolone: true, pregnancyContraindicated: true, minAgeYears: 18, commonBrands: ["O2", "Zenflox-OZ"] },
];

export const CONDITION_CATALOG: ConditionCatalogItem[] = [
  { id: 1, code: "SYN_CAP_MILD", displayName: "Community-Acquired Pneumonia (Mild Outpatient)", isSelfLimitingOrViral: false, icmrCategory: "Respiratory" },
  { id: 2, code: "SYN_UNCOMPLICATED_UTI", displayName: "Uncomplicated Acute Cystitis / Lower UTI", isSelfLimitingOrViral: false, icmrCategory: "Urinary Tract" },
  { id: 3, code: "SYN_ACUTE_BRONCHITIS", displayName: "Acute Bronchitis (Self-Limiting Viral)", isSelfLimitingOrViral: true, icmrCategory: "Respiratory" },
  { id: 4, code: "SYN_COMMON_COLD", displayName: "Common Cold / Viral Rhinopharyngitis", isSelfLimitingOrViral: true, icmrCategory: "Upper Respiratory" },
  { id: 5, code: "SYN_VIRAL_URTI", displayName: "Viral Upper Respiratory Tract Infection (URTI)", isSelfLimitingOrViral: true, icmrCategory: "Upper Respiratory" },
  { id: 6, code: "SYN_PHARYNGITIS_NON_STREP", displayName: "Non-Streptococcal Pharyngitis (Viral Sore Throat)", isSelfLimitingOrViral: true, icmrCategory: "ENT" },
  { id: 7, code: "SYN_WATERY_DIARRHEA", displayName: "Acute Watery Diarrhea (Non-Cholera)", isSelfLimitingOrViral: true, icmrCategory: "Gastrointestinal" },
  { id: 8, code: "SYN_PHARYNGITIS_STREP", displayName: "Streptococcal Pharyngitis (Group A Strep Confirmed)", isSelfLimitingOrViral: false, icmrCategory: "ENT" },
  { id: 9, code: "SYN_AOM", displayName: "Acute Otitis Media (AOM)", isSelfLimitingOrViral: false, icmrCategory: "ENT" },
  { id: 10, code: "SYN_SSTI_UNCOMPLICATED", displayName: "Uncomplicated Skin Infection (Cellulitis / Impetigo)", isSelfLimitingOrViral: false, icmrCategory: "Dermatology" },
  { id: 11, code: "SYN_PYELONEPHRITIS_UNCOMPLICATED", displayName: "Acute Pyelonephritis (Outpatient)", isSelfLimitingOrViral: false, icmrCategory: "Urology" },
  { id: 12, code: "SYN_ENTERIC_FEVER", displayName: "Enteric Fever / Typhoid", isSelfLimitingOrViral: false, icmrCategory: "Infectious Diseases" },
];
