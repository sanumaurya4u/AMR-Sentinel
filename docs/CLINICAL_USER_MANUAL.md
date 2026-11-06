# AMR Sentinel AI — Clinician & Practitioner User Manual
**A Practice Guide for Antimicrobial Stewardship and Safe Prescription Auditing**  
*Grounded in ICMR Standard Treatment Guidelines 2022, WHO AWaRe Classification 2023, and CDSCO Safety Directives*

---

## 1. Introduction & Clinical Safety Boundary

**AMR Sentinel AI** is an assistive antimicrobial stewardship second-check platform designed to support physicians, resident medical officers, clinical pharmacists, and healthcare practitioners during clinical decision-making. 

### Core Operating Principles for Clinicians
1. **Assistive, Not Autonomous:** AMR Sentinel AI does **not** diagnose conditions, prescribe medications, calculate final doses, or autonomously alter therapy.
2. **Preserver of Clinical Autonomy:** The tool provides deterministic, evidence-backed cross-checks against national and international clinical guidelines. All therapeutic decisions remain the sole responsibility of the treating clinician.
3. **Absence of Proof ≠ Proof of Absence:** A status of `NO RULE TRIGGERED` indicates that the entered regimen does not violate configured safety gates in the guideline database; it does **not** constitute an endorsement of clinical efficacy or patient safety.
4. **Explicit Handling of Unknowns:** If vital parameters (such as renal function or pregnancy status) are not provided, the platform **never assumes they are normal**. It actively flags them as **Clinical Data Gaps**.

---

## 2. Platform Architecture: The Two-Layer Safety Model

Understanding how AMR Sentinel processes your data guarantees safe and efficient usage:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   STEP 1: ASSISTIVE INTAKE LAYER                       │
│        (Optical Character Recognition / Digital Form Processing)       │
│                                                                        │
│ • Drafts patient profile, symptoms, and prescribed antibiotics.        │
│ • Labels low-confidence or ambiguous fields.                          │
│ • UNTRUSTED UNTIL CONFIRMED: Never triggers clinical rules automatically.│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ 
                 [ Mandatory Clinician Review & Edit ]
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               STEP 2: DETERMINISTIC CLINICAL AUDIT CORE                │
│    (Zero LLM Hallucinations • Pure Guideline Logic • ISO/ICMR Grounded) │
│                                                                        │
│ • Tier 1: Absolute Safety Gates (Pregnancy, Pediatric, Renal eGFR)     │
│ • Tier 2: CDSCO Banned Fixed-Dose Combinations (FDCs)                  │
│ • Tier 3: Indication Legitimacy (Viral / Self-limiting syndromes)      │
│ • Tier 4: WHO AWaRe Spectrum Optimization (Access vs Watch / Reserve)  │
│ • Tier 5: Duration of Therapy & Dose Completeness                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               STEP 3: ACTIONABLE CLINICAL AUDIT REPORT                 │
│                                                                        │
│ • Immediate Traffic-Light Risk Stratification                          │
│ • Rule IDs with linked ICMR / WHO guideline excerpts                   │
│ • Guideline-endorsed non-prescriptive discussion options               │
│ • Append-only clinician rationale override documentation               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Clinical Workflow Guide

### Step 1: Entering Patient Demographics and Physiological Context
Navigate to **New Prescription Audit** (`/new-audit`). Accurately enter the physiological parameters:

* **Age:** Critical for pediatric and geriatric safety limits (e.g., Fluoroquinolones under 18 years, Tetracyclines under 8 years).
* **Biological Sex & Pregnancy Status:** Toggle "Pregnant / Gestational" if applicable. Many antimicrobials (e.g., Doxycycline, Fluoroquinolones, Aminoglycosides) carry strict contraindications due to fetal chondrotoxicity, tooth discoloration, or ototoxicity.
* **Estimated GFR (eGFR in mL/min/1.73m²):** 
  * If known, enter the calculated creatinine clearance.
  * *Clinical Pearl:* Drugs like Nitrofurantoin are contraindicated at eGFR < 30 mL/min due to lack of therapeutic urinary concentration and high risk of peripheral neuropathy.
  * If eGFR is unmeasured, leave blank; the engine will alert you to verify renal reserve before nephrotoxic drug administration.
* **Known Drug Allergies:** Type known hypersensitivities (e.g., Penicillin, Cephalosporins, Sulfa drugs).

---

### Step 2: Specifying Indication and Care Setting
Select the primary clinical working diagnosis from the standardized dropdown:

* **Indication Categorization:**
  * **Bacterial Infections:** e.g., *Community-Acquired Pneumonia (CAP)*, *Acute Uncomplicated Cystitis (UTI)*, *Streptococcal Pharyngitis*.
  * **Self-Limiting / Viral Syndromes:** e.g., *Acute Bronchitis*, *Viral Rhinopharyngitis (Common Cold)*, *Acute Watery Diarrhea*.
* **Clinical Setting:** Select **Outpatient (OPD)** or **Inpatient (Ward / ICU)**. Outpatient settings are held to strict oral de-escalation guidelines under WHO AWaRe standards.

---

### Step 3: Prescribed Regimen Entry (Two Methods)

#### Option A: Direct Digital Selection (Recommended for OPD E-Prescribing)
1. Select the medication from the generic formulary catalog (e.g., *Amoxicillin-Clavulanate*, *Azithromycin*, *Ciprofloxacin*).
2. Enter the intended dosage (e.g., `500 mg`, `625 mg`).
3. Specify dosing frequency (e.g., `TDS`, `BD`, `OD`).
4. Enter the planned duration in days (e.g., `5 days`).
5. Click **+ Add Drug** if evaluating multi-drug polypharmacy regimens.

#### Option B: Digital Prescription Upload (OCR Assist)
1. Click **Upload Prescription (PDF / Image)**.
2. The AI assistant extracts draft fields and fills in the stepper form.
3. **Mandatory Step:** Review every extracted item. Hand-written prescription ambiguity must be corrected manually before continuing.

---

### Step 4: Clinician Review & Confirmation
At the base of the intake form, verify the summary card and check the required clinical affirmation:
> ☑ **"I confirm that I have verified the extracted/entered patient context, clinical indication, and medication regimen."**

Click **Execute Deterministic Audit**. The engine processes all 5 tiers of safety rules in less than 3 seconds.

---

## 4. Understanding Audit Results & Actionable Findings

The **Clinical Audit Summary** (`/results`) organizes feedback into clear, unambiguous sections:

### 1. Triage Status Badges
| Badge | Clinical Meaning | Recommended Action |
|:---|:---|:---|
| <span style="color:#DC2626; font-weight:bold;">● NEEDS URGENT REVIEW</span> | **Critical Safety Contraindication:** High likelihood of patient harm, teratogenicity, severe organ toxicity, or banned drug combination. | **Withhold / Re-evaluate:** Review clinical contraindication immediately; explore guideline-recommended alternatives. |
| <span style="color:#D97706; font-weight:bold;">● NEEDS REVIEW</span> | **Antimicrobial Stewardship Alert:** Broad-spectrum agent used where narrow-spectrum is standard, self-limiting viral illness, or prolonged duration. | **De-escalation Review:** Review culture sensitivity, de-escalate to WHO Access group, or shorten therapy course. |
| <span style="color:#059669; font-weight:bold;">● NO RULE TRIGGERED</span> | **Guideline Concordant:** Regimen aligns with configured baseline ICMR STG 2022 / WHO AWaRe criteria. | **Proceed with Clinical Judgement:** Continue monitoring clinical response and organ function. |

---

### 2. Deconstructing a Finding Card
Each flagged item provides transparent clinical reasoning:
* **Rule Identifier:** Stable reference (e.g., `SAFETY.PEDIATRIC.CIPROFLOXACIN.AGE_LT_18`).
* **Clinical Alert:** Clear rationale explaining the pathological or pharmacological hazard.
* **Facts Evaluated:** Shows the exact values that triggered the alert (e.g., `Patient Age: 8 years`, `Drug: Ciprofloxacin`).
* **Guideline Discussion Prompt:** Suggests standard first-line options for discussion (e.g., *"Consider Oral Amoxicillin 500 mg TDS or supportive oral rehydration under ICMR Pediatric Guidelines"*).
* **Evidence Source Button:** Click **View Guideline Citation** to open the evidence drawer with the exact chapter, table number, and verbatim excerpt from ICMR STG or WHO.

---

### 3. Addressing Clinical Data Gaps
If an alert indicates **"Data Gap: Renal Function (eGFR) Unspecified"** or **"Pregnancy Status Unconfirmed"**:
* The system refuses to assume normal organ reserve.
* Order necessary baseline laboratory tests (Serum Creatinine, Urine Pregnancy Test) before dispensing high-risk antimicrobial agents.

---

## 5. Clinician Overrides & Chart Documentation

Clinical medicine frequently requires individualized deviations based on microbiology cultures, patient intolerance, or secondary bacterial infection.

### How to Record a Guideline Override:
1. If your clinical assessment warrants maintaining the prescribed regimen despite an alert, click **Document Clinical Review & Override**.
2. Select your clinical rationale:
   * *Culture & Susceptibility Guided Therapy* (e.g., organism resistant to first-line Access agents).
   * *Specialist / Infectious Disease Consultation Completed*.
   * *Patient Intolerance or Documented Allergy to First-Line Regimen*.
   * *Severe or Complicated Clinical Presentation*.
3. Enter your clinical justification notes and GMC / Medical Council Registration details.
4. Click **Submit & Record Override**. 
5. The system stores an immutable, timestamped audit log and generates a printable summary for the patient's physical case sheet or hospital pharmacy record.

---

## 6. Antimicrobial Stewardship Best Practices for Prescribers

To maximize patient safety and combat antimicrobial resistance (AMR), apply the **Five Rights of Antimicrobial Stewardship**:

1. **Right Indication:** Do not prescribe antibiotics for common colds, viral upper respiratory infections, or uncomplicated acute watery diarrhea. Rehydration and symptomatic therapy are the cornerstones of care.
2. **Right Drug (WHO AWaRe Categorization):**
   * 🟢 **Access Group (Target: ≥ 60% of total hospital use):** First- or second-line narrow spectrum agents (Amoxicillin, Cefalexin, Nitrofurantoin). Lower resistance potential.
   * 🟡 **Watch Group:** Broad-spectrum agents with high resistance selection risk (Fluoroquinolones, 3rd Gen Cephalosporins, Macrolides). Reserve for specific, documented indications.
   * 🔴 **Reserve Group:** Last-resort antibiotics (Colistin, Meropenem, Linezolid). Protect for multi-drug resistant (MDR) infections with microbiological confirmation.
3. **Right Dose & Frequency:** Tailor dosage based on patient renal function (eGFR) and therapeutic targets.
4. **Right Duration:** Prefer shorter, guideline-directed courses (e.g., 5 days for mild CAP or uncomplicated cystitis) to minimize collateral microbial damage and adverse reactions.
5. **Right Re-evaluation (48-hour Antibiotic Time-out):** Review microbiological cultures at 48 to 72 hours; de-escalate from empiric broad-spectrum coverage to directed narrow-spectrum therapy as soon as sensitivities return.

---

## 7. Frequently Asked Questions (FAQ) for Physicians

**Q: Can AMR Sentinel AI automatically change my prescription in the hospital EMR?**  
*No.* AMR Sentinel is an assistive clinical decision-support tool. It has no authority to alter, suspend, or cancel your orders. Only the licensed prescriber can modify or confirm therapy.

**Q: Why does the system flag Fixed-Dose Combinations like Cefixime + Azithromycin or Ofloxacin + Ornidazole?**  
*Reason:* The Central Drugs Standard Control Organisation (CDSCO) and ICMR have explicitly banned or discouraged dual-broad-spectrum oral FDCs because they lack synergistic therapeutic evidence, accelerate multi-drug resistance, and induce dysbiosis.

**Q: What should I do if a patient has normal renal function but the system flags a data gap?**  
*Solution:* Ensure the eGFR field is filled out in the patient context panel during Step 1. If left blank, the platform safely flags unverified renal clearance.

**Q: Are patient identifiers or clinical records shared externally?**  
*No.* AMR Sentinel AI is engineered with zero-leakage privacy gates. It operates locally or over secure institutional channels without sending protected health information (PHI) to public LLMs.

---

*AMR Sentinel AI Platform — Promoting rational antimicrobial use to preserve life-saving medicines for future generations.*
