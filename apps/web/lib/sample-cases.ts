/**
 * Pre-configured Synthetic Golden Test Cases for AMR Sentinel AI Hackathon Evaluation.
 * Conspicuously labelled synthetic; zero PHI.
 */

export interface SyntheticCase {
  id: string;
  title: string;
  scenarioSubtitle: string;
  clinicalObjective: string;
  expectedStatus: "NEEDS_URGENT_REVIEW" | "NEEDS_REVIEW" | "NO_RULE_TRIGGERED" | "INCOMPLETE_DATA";
  patientContext: {
    ageYears: number;
    gender: "female" | "male" | "other";
    isPregnant: boolean;
    egfrMlMin?: number;
    weightKg?: number;
    allergies: string[];
  };
  indicationCode: string;
  indicationName: string;
  setting: "outpatient" | "inpatient";
  prescriptionLines: Array<{
    drugName: string;
    doseText: string;
    frequencyText: string;
    durationDays?: number;
  }>;
}

export const SYNTHETIC_SAMPLE_CASES: SyntheticCase[] = [
  {
    id: "SYN_CASE_01_PEDIATRIC_CQ",
    title: "Case 1: Pediatric Fluoroquinolone Contraindication",
    scenarioSubtitle: "8-year-old child prescribed Ciprofloxacin for uncomplicated diarrhea",
    clinicalObjective: "Trigger Tier 1 Pediatric Contraindication (FDA Black Box & ICMR Pediatric Guidelines warning for arthropathy / cartilage erosion in patients <18).",
    expectedStatus: "NEEDS_URGENT_REVIEW",
    patientContext: {
      ageYears: 8,
      gender: "male",
      isPregnant: false,
      egfrMlMin: 95,
      weightKg: 25,
      allergies: [],
    },
    indicationCode: "SYN_WATERY_DIARRHEA",
    indicationName: "Acute Watery Diarrhea (Non-Cholera)",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Ciprofloxacin",
        doseText: "250 mg",
        frequencyText: "Twice daily (BD)",
        durationDays: 5,
      },
    ],
  },
  {
    id: "SYN_CASE_02_GERIATRIC_RENAL",
    title: "Case 2: Geriatric Severe Renal Impairment (Nitrofurantoin)",
    scenarioSubtitle: "74-year-old patient with eGFR 22 mL/min prescribed Nitrofurantoin",
    clinicalObjective: "Trigger Tier 1 Renal Safety Gate (Beers Criteria & ICMR Geriatric: inadequate urinary concentrations and peripheral neurotoxicity when eGFR <30 mL/min).",
    expectedStatus: "NEEDS_URGENT_REVIEW",
    patientContext: {
      ageYears: 74,
      gender: "female",
      isPregnant: false,
      egfrMlMin: 22,
      allergies: [],
    },
    indicationCode: "SYN_UNCOMPLICATED_UTI",
    indicationName: "Uncomplicated Acute Cystitis / Lower UTI",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Nitrofurantoin",
        doseText: "100 mg",
        frequencyText: "Twice daily (BD)",
        durationDays: 5,
      },
    ],
  },
  {
    id: "SYN_CASE_03_VIRAL_BRONCHITIS",
    title: "Case 3: Inappropriate Antibiotic in Viral Acute Bronchitis",
    scenarioSubtitle: "32-year-old adult prescribed Azithromycin for self-limiting viral bronchitis",
    clinicalObjective: "Trigger Tier 2 Viral Indication Flag (ICMR STG 2022 & WHO: acute bronchitis in healthy adults is >90% viral; antibiotic therapy confers zero clinical benefit).",
    expectedStatus: "NEEDS_REVIEW",
    patientContext: {
      ageYears: 32,
      gender: "female",
      isPregnant: false,
      egfrMlMin: 110,
      allergies: [],
    },
    indicationCode: "SYN_ACUTE_BRONCHITIS",
    indicationName: "Acute Bronchitis (Self-Limiting Viral)",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Azithromycin",
        doseText: "500 mg",
        frequencyText: "Once daily (OD)",
        durationDays: 5,
      },
    ],
  },
  {
    id: "SYN_CASE_04_AWARE_RESERVE",
    title: "Case 4: Severe AWaRe Escalation (Reserve Carbapenem for Mild UTI)",
    scenarioSubtitle: "28-year-old with uncomplicated cystitis prescribed IV Meropenem",
    clinicalObjective: "Trigger Tier 3 WHO AWaRe Reserve Escalation (Meropenem is a Reserve-group antibiotic reserved for multidrug-resistant life-threatening pathogens; first-line is Access-group Nitrofurantoin/Fosfomycin).",
    expectedStatus: "NEEDS_REVIEW",
    patientContext: {
      ageYears: 28,
      gender: "female",
      isPregnant: false,
      egfrMlMin: 105,
      allergies: [],
    },
    indicationCode: "SYN_UNCOMPLICATED_UTI",
    indicationName: "Uncomplicated Acute Cystitis / Lower UTI",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Meropenem",
        doseText: "1000 mg",
        frequencyText: "Every 8 hours (TDS)",
        durationDays: 7,
      },
    ],
  },
  {
    id: "SYN_CASE_05_INCOMPLETE_DATA",
    title: "Case 5: Critical Missing Data Gap (Gentamicin without eGFR)",
    scenarioSubtitle: "45-year-old prescribed nephrotoxic Aminoglycoside with undocumented renal function",
    clinicalObjective: "Trigger Tier 1 Mandatory Renal Function Hold (KDIGO Guidelines: narrow-therapeutic aminoglycosides require confirmed eGFR prior to initiation to prevent acute tubular necrosis).",
    expectedStatus: "INCOMPLETE_DATA",
    patientContext: {
      ageYears: 45,
      gender: "male",
      isPregnant: false,
      // egfrMlMin intentionally omitted!
      allergies: [],
    },
    indicationCode: "SYN_PYELONEPHRITIS_UNCOMPLICATED",
    indicationName: "Acute Pyelonephritis (Outpatient)",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Gentamicin",
        doseText: "80 mg",
        frequencyText: "Twice daily (BD)",
        // durationDays intentionally omitted!
      },
    ],
  },
  {
    id: "SYN_CASE_06_CLEAN_GUIDELINE",
    title: "Case 6: Guideline-Concordant First-Line Prescription",
    scenarioSubtitle: "34-year-old with mild CAP prescribed Amoxicillin 500mg TID for 5 days",
    clinicalObjective: "Demonstrate clean audit run with zero triggered safety or stewardship rules (Concordant with ICMR STG 2022 Mild CAP; Access class; duration <= 5 days).",
    expectedStatus: "NO_RULE_TRIGGERED",
    patientContext: {
      ageYears: 34,
      gender: "male",
      isPregnant: false,
      egfrMlMin: 98,
      allergies: [],
    },
    indicationCode: "SYN_CAP_MILD",
    indicationName: "Community-Acquired Pneumonia (Mild Outpatient)",
    setting: "outpatient",
    prescriptionLines: [
      {
        drugName: "Amoxicillin",
        doseText: "500 mg",
        frequencyText: "Three times daily (TID)",
        durationDays: 5,
      },
    ],
  },
];
