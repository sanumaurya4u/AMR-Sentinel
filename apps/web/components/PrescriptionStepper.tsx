"use client";

import React, { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import {
  User,
  Activity,
  Pill,
  CheckCircle,
  Sparkles,
  AlertCircle,
  Plus,
  Trash2,
  ArrowRight,
  ArrowLeft,
  ShieldCheck,
  UploadCloud,
  FileCheck2,
  AlertTriangle,
  HeartPulse,
  BookOpen,
  Info,
} from "lucide-react";
import { DRUG_CATALOG, CONDITION_CATALOG, DrugCatalogItem, ConditionCatalogItem } from "@/lib/clinical-data";
import { SYNTHETIC_SAMPLE_CASES, SyntheticCase } from "@/lib/sample-cases";
import { SyntheticDataNotice } from "./DisclaimerBanner";

export interface PrescriptionLineForm {
  id: string;
  drugName: string;
  doseText: string;
  frequencyText: string;
  durationDays: string;
}

export function PrescriptionStepper() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<number>(1);

  // Form State
  const [ageYears, setAgeYears] = useState<string>("34");
  const [gender, setGender] = useState<"female" | "male" | "other">("male");
  const [isPregnant, setIsPregnant] = useState<boolean>(false);
  const [egfrMlMin, setEgfrMlMin] = useState<string>("98");
  const [allergies, setAllergies] = useState<string>("");

  const [indicationCode, setIndicationCode] = useState<string>("SYN_CAP_MILD");
  const [setting, setSetting] = useState<"outpatient" | "inpatient">("outpatient");

  const [prescriptionLines, setPrescriptionLines] = useState<PrescriptionLineForm[]>([
    {
      id: "line-1",
      drugName: "Amoxicillin",
      doseText: "500 mg",
      frequencyText: "Three times daily (TID)",
      durationDays: "5",
    },
  ]);

  const [confirmedByClinician, setConfirmedByClinician] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isExtracting, setIsExtracting] = useState<boolean>(false);
  const [extractionNotice, setExtractionNotice] = useState<string | null>(null);
  const [selectedCaseId, setSelectedCaseId] = useState<string>("");

  // Auto-load case from URL query parameter (e.g. ?case=SYN_CASE_02_GERIATRIC_RENAL)
  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const caseParam = params.get("case");
      if (caseParam) {
        const found = SYNTHETIC_SAMPLE_CASES.find((c) => c.id === caseParam);
        if (found) {
          setSelectedCaseId(found.id);
          loadSyntheticCase(found);
        }
      }
    }
  }, []);

  // Compute live age band
  const ageNumber = parseFloat(ageYears) || 0;
  const ageBand = useMemo(() => {
    if (ageNumber < 18) return { label: "Pediatric (<18y)", color: "text-urgent bg-urgent-subtle border-urgent-border" };
    if (ageNumber >= 65) return { label: "Geriatric (≥65y)", color: "text-amber-800 bg-amber-50 border-amber-300" };
    return { label: "Adult (18-64y)", color: "text-slate-clinical bg-slate-100 border-slate-200" };
  }, [ageNumber]);

  // Compute live CKD Stage based on eGFR
  const ckdStage = useMemo(() => {
    if (!egfrMlMin || egfrMlMin.trim() === "") {
      return { stage: "eGFR Unrecorded", color: "text-info bg-info-subtle border-info/30", alert: "Safety holds on nephrotoxic drugs" };
    }
    const val = parseFloat(egfrMlMin);
    if (isNaN(val)) return { stage: "Invalid eGFR", color: "text-slate-clinical bg-slate-100 border-slate-200", alert: "" };
    if (val >= 90) return { stage: "Stage 1 (Normal / High: ≥90)", color: "text-emerald-800 bg-emerald-50 border-emerald-300", alert: "Normal renal filtration" };
    if (val >= 60) return { stage: "Stage 2 (Mild Reduction: 60-89)", color: "text-emerald-800 bg-emerald-50 border-emerald-300", alert: "Adequate clearance for most agents" };
    if (val >= 30) return { stage: "Stage 3 (Moderate CKD: 30-59)", color: "text-amber-800 bg-amber-50 border-amber-300", alert: "Requires dosage adjustment" };
    if (val >= 15) return { stage: "Stage 4 (Severe CKD: 15-29)", color: "text-urgent bg-urgent-subtle border-urgent-border", alert: "Strict contraindication for Nitrofurantoin" };
    return { stage: "Stage 5 (Kidney Failure: <15)", color: "text-urgent bg-urgent-subtle border-urgent-border", alert: "Severe nephrotoxicity alert" };
  }, [egfrMlMin]);

  // Lookup active condition object
  const activeCondition = useMemo(() => {
    return CONDITION_CATALOG.find((c) => c.code === indicationCode) || CONDITION_CATALOG[0];
  }, [indicationCode]);

  // Assistive document extraction handler
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsExtracting(true);
    setExtractionNotice(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/extractions`, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        if (data.patientContext) {
          if (data.patientContext.ageYears !== undefined) setAgeYears(String(data.patientContext.ageYears));
          if (data.patientContext.gender) setGender(data.patientContext.gender);
          if (data.patientContext.isPregnant !== undefined) setIsPregnant(data.patientContext.isPregnant);
          if (data.patientContext.egfrMlMin !== undefined && data.patientContext.egfrMlMin !== null) {
            setEgfrMlMin(String(data.patientContext.egfrMlMin));
          }
        }
        if (data.indicationCode) setIndicationCode(data.indicationCode);
        if (data.prescriptionLines && data.prescriptionLines.length > 0) {
          setPrescriptionLines(
            data.prescriptionLines.map((l: { drugName?: string; doseText?: string; frequencyText?: string; durationDays?: number }, i: number) => ({
              id: `ext-line-${i}`,
              drugName: l.drugName || "Amoxicillin",
              doseText: l.doseText || "500 mg",
              frequencyText: l.frequencyText || "Twice daily (BD)",
              durationDays: l.durationDays ? String(l.durationDays) : "",
            }))
          );
        }
        setExtractionNotice(`Document draft extracted successfully using ${data.extraction_engine || "assistive adapter"}. Please review and confirm each field.`);
        setConfirmedByClinician(false);
      }
    } catch (err) {
      console.warn("Upload failed, manual entry remains available:", err);
      setExtractionNotice("Extraction service unavailable. Please enter clinical facts manually.");
    } finally {
      setIsExtracting(false);
    }
  };

  // Load a synthetic sample case
  const loadSyntheticCase = (c: SyntheticCase) => {
    setSelectedCaseId(c.id);
    setAgeYears(c.patientContext.ageYears.toString());
    setGender(c.patientContext.gender);
    setIsPregnant(c.patientContext.isPregnant);
    setEgfrMlMin(c.patientContext.egfrMlMin !== undefined ? c.patientContext.egfrMlMin.toString() : "");
    setAllergies(c.patientContext.allergies.join(", "));
    setIndicationCode(c.indicationCode);
    setSetting(c.setting);
    setPrescriptionLines(
      c.prescriptionLines.map((line, idx) => ({
        id: `line-${idx + 1}`,
        drugName: line.drugName,
        doseText: line.doseText,
        frequencyText: line.frequencyText,
        durationDays: line.durationDays ? line.durationDays.toString() : "",
      }))
    );
    setConfirmedByClinician(false);
  };

  // Add line
  const addPrescriptionLine = () => {
    setPrescriptionLines((prev) => [
      ...prev,
      {
        id: `line-${Date.now()}`,
        drugName: "Amoxicillin",
        doseText: "500 mg",
        frequencyText: "Twice daily (BD)",
        durationDays: "5",
      },
    ]);
  };

  // Remove line
  const removePrescriptionLine = (id: string) => {
    if (prescriptionLines.length > 1) {
      setPrescriptionLines((prev) => prev.filter((l) => l.id !== id));
    }
  };

  // Update line
  const updatePrescriptionLine = (id: string, field: keyof PrescriptionLineForm, value: string) => {
    setPrescriptionLines((prev) =>
      prev.map((l) => (l.id === id ? { ...l, [field]: value } : l))
    );
  };

  // Submit to audit endpoint
  const handleAuditSubmit = async () => {
    if (!confirmedByClinician) return;
    setIsSubmitting(true);

    const payload = {
      patientContext: {
        ageYears: parseFloat(ageYears) || 0,
        gender,
        isPregnant: gender === "female" ? isPregnant : false,
        egfrMlMin: egfrMlMin ? parseFloat(egfrMlMin) : null,
        allergies: allergies
          ? allergies.split(",").map((s) => s.trim()).filter(Boolean)
          : [],
      },
      indicationCode,
      setting,
      prescriptionLines: prescriptionLines.map((line) => ({
        drugName: line.drugName,
        doseText: line.doseText,
        frequencyText: line.frequencyText,
        durationDays: line.durationDays ? parseInt(line.durationDays, 10) : null,
      })),
      isSynthetic: true,
    };

    // Store in sessionStorage for results page
    sessionStorage.setItem("amr_active_audit_payload", JSON.stringify(payload));

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/audits`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const auditResult = await res.json();
        sessionStorage.setItem("amr_active_audit_result", JSON.stringify(auditResult));
      }
    } catch {
      console.warn("Backend unavailable, client will evaluate deterministic offline fallback");
    } finally {
      setIsSubmitting(false);
      router.push("/results");
    }
  };

  const steps = [
    { num: 1, title: "Patient Context", short: "1. Patient", icon: User },
    { num: 2, title: "Indication & Setting", short: "2. Indication", icon: Activity },
    { num: 3, title: "Prescription Lines", short: "3. Medications", icon: Pill },
    { num: 4, title: "Confirm Facts", short: "4. Verify", icon: CheckCircle },
  ];

  return (
    <div className="space-y-6">
      {/* Quick Load Synthetic Golden Case Ribbon */}
      <div className="rounded-xl border border-primary/20 bg-primary-subtle/20 p-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <Sparkles className="h-5 w-5 text-primary shrink-0" />
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-primary">
                Quick-Load Synthetic Golden Case
              </h3>
              <p className="text-[11px] text-slate-clinical">
                Instantly populate clinical facts for verified ICMR / WHO demonstration scenarios
              </p>
            </div>
          </div>
          <select
            value={selectedCaseId}
            onChange={(e) => {
              const selected = SYNTHETIC_SAMPLE_CASES.find((c) => c.id === e.target.value);
              if (selected) loadSyntheticCase(selected);
            }}
            className="w-full sm:w-auto rounded-lg border border-border bg-white px-3 py-2 text-xs font-bold text-ink shadow-xs focus:border-primary focus:outline-hidden"
          >
            <option value="" disabled>
              -- Select a Synthetic Demonstration Case --
            </option>
            {SYNTHETIC_SAMPLE_CASES.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Assistive Document Upload Card */}
      <div className="rounded-xl border border-border bg-surface p-4 shadow-xs">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <UploadCloud className="h-5 w-5 text-primary shrink-0" />
            <div>
              <h4 className="text-xs font-bold text-ink">Upload Synthetic Prescription (Image or PDF)</h4>
              <p className="text-[11px] text-slate-clinical">
                Assistive extraction drafts editable fields. Output is untrusted until confirmed by clinician.
              </p>
            </div>
          </div>
          <div>
            <label className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-white px-3.5 py-2 text-xs font-semibold text-ink hover:bg-canvas shadow-xs cursor-pointer">
              <UploadCloud className="h-3.5 w-3.5 text-primary" />
              <span>{isExtracting ? "Extracting Draft..." : "Upload Document"}</span>
              <input
                type="file"
                accept="image/*,application/pdf,text/plain"
                onChange={handleFileUpload}
                disabled={isExtracting}
                className="hidden"
              />
            </label>
          </div>
        </div>

        {extractionNotice && (
          <div className="mt-3 flex items-center gap-2 rounded-lg bg-primary-subtle/40 p-2.5 text-xs text-primary border border-primary/20">
            <FileCheck2 className="h-4 w-4 shrink-0" />
            <span>{extractionNotice}</span>
          </div>
        )}
      </div>

      <SyntheticDataNotice />

      {/* Stepper Navigation Tabs (Responsive & Untruncated) */}
      <nav aria-label="Progress">
        <ol className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          {steps.map((s) => {
            const Icon = s.icon;
            const isActive = currentStep === s.num;
            const isCompleted = currentStep > s.num;

            return (
              <li key={s.num}>
                <button
                  type="button"
                  onClick={() => setCurrentStep(s.num)}
                  className={`flex w-full items-center gap-2.5 rounded-xl border p-3 text-left transition-all ${
                    isActive
                      ? "border-primary bg-primary-subtle/30 text-primary font-semibold shadow-xs"
                      : isCompleted
                      ? "border-border bg-surface text-slate-clinical hover:bg-canvas"
                      : "border-border/60 bg-surface/50 text-slate-subtle"
                  }`}
                >
                  <span
                    className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                      isActive
                        ? "bg-primary text-white"
                        : isCompleted
                        ? "bg-emerald-600 text-white"
                        : "bg-slate-200 text-slate-600"
                    }`}
                  >
                    {isCompleted ? "✓" : s.num}
                  </span>
                  <div className="min-w-0">
                    <p className="text-xs font-bold truncate hidden sm:block">{s.title}</p>
                    <p className="text-xs font-bold truncate sm:hidden">{s.short}</p>
                  </div>
                </button>
              </li>
            );
          })}
        </ol>
      </nav>

      {/* 2-Column Clinical Prescription Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (60% ~ 7 cols): Active Stepper Form */}
        <div className="lg:col-span-7 rounded-2xl border border-border bg-surface p-6 shadow-xs space-y-6">
          {/* Step 1: Patient Context & Organ Function */}
          {currentStep === 1 && (
            <div className="space-y-5 animate-in fade-in duration-150">
              <div className="border-b border-border pb-3">
                <h3 className="text-base font-bold text-ink flex items-center gap-2">
                  <User className="h-5 w-5 text-primary" />
                  Step 1: Patient Demographics &amp; Organ Function
                </h3>
                <p className="text-xs text-slate-clinical mt-0.5">
                  Record age, biological gender, pregnancy status, and renal clearance (eGFR).
                </p>
              </div>

              <div className="space-y-4">
                {/* Age & Age-Band Badge */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-bold text-ink">
                      Patient Age (Years) <span className="text-urgent">*</span>
                    </label>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${ageBand.color}`}>
                      {ageBand.label}
                    </span>
                  </div>
                  <input
                    type="number"
                    min="0"
                    max="120"
                    step="0.1"
                    value={ageYears}
                    onChange={(e) => setAgeYears(e.target.value)}
                    className="w-full rounded-xl border border-border bg-white px-3.5 py-2.5 text-sm font-semibold text-ink focus:border-primary focus:outline-hidden"
                    required
                  />
                  <span className="text-[11px] text-slate-clinical mt-1 block">
                    Pediatric (&lt;18) fluoroquinolone gates and Geriatric (&ge;65) renal holds apply.
                  </span>
                </div>

                {/* Biological Gender Segmented Controls */}
                <div>
                  <label className="block text-xs font-bold text-ink mb-1.5">
                    Biological Gender <span className="text-urgent">*</span>
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { key: "female", label: "Female" },
                      { key: "male", label: "Male" },
                      { key: "other", label: "Other / Not Specified" },
                    ].map((g) => (
                      <button
                        key={g.key}
                        type="button"
                        onClick={() => setGender(g.key as "female" | "male" | "other")}
                        className={`rounded-xl border py-2 text-xs font-bold transition-all ${
                          gender === g.key
                            ? "bg-primary text-white border-primary shadow-xs"
                            : "bg-surface border-border text-slate-clinical hover:bg-canvas"
                        }`}
                      >
                        {g.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Pregnancy Toggle with FDA Alert */}
                {gender === "female" && (
                  <div className="rounded-xl border border-border bg-slate-50/70 p-4 space-y-2">
                    <label className="flex items-start gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isPregnant}
                        onChange={(e) => setIsPregnant(e.target.checked)}
                        className="h-4 w-4 rounded border-border text-primary focus:ring-primary mt-0.5"
                      />
                      <div>
                        <span className="text-xs font-bold text-ink block">
                          Patient is currently pregnant
                        </span>
                        <span className="text-[11px] text-slate-clinical leading-relaxed block mt-0.5">
                          Enforces FDA Category D/X and WHO pregnancy contraindications (Fluoroquinolones, Tetracyclines, Aminoglycosides, Co-trimoxazole in 1st trimester).
                        </span>
                      </div>
                    </label>
                  </div>
                )}

                {/* Renal Function (eGFR) with Live CKD Stage Pill */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-bold text-ink">
                      Renal Function: eGFR (mL/min/1.73m²)
                    </label>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${ckdStage.color}`}>
                      {ckdStage.stage}
                    </span>
                  </div>
                  <input
                    type="number"
                    min="0"
                    max="200"
                    placeholder="e.g. 90 (Leave empty if unrecorded)"
                    value={egfrMlMin}
                    onChange={(e) => setEgfrMlMin(e.target.value)}
                    className="w-full rounded-xl border border-border bg-white px-3.5 py-2.5 text-sm font-semibold text-ink focus:border-primary focus:outline-hidden"
                  />
                  <div className="flex items-center justify-between text-[11px] text-slate-clinical mt-1">
                    <span>{ckdStage.alert || "Leave empty if lab test is pending"}</span>
                    {!egfrMlMin && <span className="text-amber-700 font-semibold">Will trigger Data Gap Hold</span>}
                  </div>
                </div>

                {/* Known Allergies */}
                <div>
                  <label className="block text-xs font-bold text-ink mb-1">
                    Documented Antimicrobial Allergies
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Penicillin, Sulfa (comma-separated)"
                    value={allergies}
                    onChange={(e) => setAllergies(e.target.value)}
                    className="w-full rounded-xl border border-border bg-white px-3.5 py-2.5 text-sm text-ink focus:border-primary focus:outline-hidden"
                  />
                  <span className="text-[11px] text-slate-clinical mt-1 block">
                    Evaluates beta-lactam cross-reactivity and adverse histories.
                  </span>
                </div>
              </div>

              <div className="flex justify-end pt-4 border-t border-border">
                <button
                  type="button"
                  onClick={() => setCurrentStep(2)}
                  className="inline-flex items-center gap-1.5 rounded-xl bg-primary px-5 py-2.5 text-xs font-bold text-white hover:bg-primary-hover shadow-xs transition-colors"
                >
                  Proceed to Indication
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Indication & Care Setting */}
          {currentStep === 2 && (
            <div className="space-y-5 animate-in fade-in duration-150">
              <div className="border-b border-border pb-3">
                <h3 className="text-base font-bold text-ink flex items-center gap-2">
                  <Activity className="h-5 w-5 text-primary" />
                  Step 2: Suspected Clinical Indication &amp; Care Setting
                </h3>
                <p className="text-xs text-slate-clinical mt-0.5">
                  Select the primary diagnosis aligned with ICMR Standard Treatment Guidelines 2022.
                </p>
              </div>

              <div className="space-y-4">
                {/* Indication Selector */}
                <div>
                  <label className="block text-xs font-bold text-ink mb-1">
                    Suspected Clinical Indication <span className="text-urgent">*</span>
                  </label>
                  <select
                    value={indicationCode}
                    onChange={(e) => setIndicationCode(e.target.value)}
                    className="w-full rounded-xl border border-border bg-white px-3.5 py-3 text-sm font-semibold text-ink focus:border-primary focus:outline-hidden"
                  >
                    {CONDITION_CATALOG.map((cond) => (
                      <option key={cond.code} value={cond.code}>
                        [{cond.icmrCategory}] {cond.displayName} {cond.isSelfLimitingOrViral ? " • (Viral / Self-Limiting)" : ""}
                      </option>
                    ))}
                  </select>
                  {activeCondition.isSelfLimitingOrViral && (
                    <div className="mt-2 flex items-start gap-2 rounded-lg bg-amber-50 p-3 text-xs text-amber-900 border border-amber-300">
                      <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold">Self-Limiting / Viral Condition:</span>
                        <p className="mt-0.5 text-[11px] text-amber-800">
                          ICMR &amp; WHO guidelines state antibiotic therapy provides zero clinical efficacy for uncomplicated {activeCondition.displayName}. Supportive care (ORS, hydration, antipyretics) is recommended.
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Care Setting Segmented Buttons */}
                <div>
                  <label className="block text-xs font-bold text-ink mb-1.5">
                    Care Setting <span className="text-urgent">*</span>
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      { key: "outpatient", label: "Outpatient (Ambulatory / Primary Care)", desc: "Oral first-line formulations" },
                      { key: "inpatient", label: "Inpatient (Hospitalized / Ward)", desc: "Parenteral therapy evaluated" },
                    ].map((s) => (
                      <button
                        key={s.key}
                        type="button"
                        onClick={() => setSetting(s.key as "outpatient" | "inpatient")}
                        className={`rounded-xl border p-3 text-left transition-all ${
                          setting === s.key
                            ? "bg-primary-subtle/30 border-primary shadow-xs"
                            : "bg-surface border-border hover:bg-canvas"
                        }`}
                      >
                        <span className={`text-xs font-bold block ${setting === s.key ? "text-primary" : "text-ink"}`}>
                          {s.label}
                        </span>
                        <span className="text-[11px] text-slate-clinical block mt-0.5">
                          {s.desc}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex justify-between pt-4 border-t border-border">
                <button
                  type="button"
                  onClick={() => setCurrentStep(1)}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentStep(3)}
                  className="inline-flex items-center gap-1.5 rounded-xl bg-primary px-5 py-2.5 text-xs font-bold text-white hover:bg-primary-hover shadow-xs"
                >
                  Proceed to Prescription
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Prescribed Antimicrobial Agents */}
          {currentStep === 3 && (
            <div className="space-y-5 animate-in fade-in duration-150">
              <div className="flex items-center justify-between border-b border-border pb-3">
                <div>
                  <h3 className="text-base font-bold text-ink flex items-center gap-2">
                    <Pill className="h-5 w-5 text-primary" />
                    Step 3: Prescribed Antimicrobial Agents
                  </h3>
                  <p className="text-xs text-slate-clinical mt-0.5">
                    Specify generic drugs, dosages, frequencies, and planned durations.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={addPrescriptionLine}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-primary text-primary px-3 py-1.5 text-xs font-bold hover:bg-primary-subtle/30 transition-colors"
                >
                  <Plus className="h-3.5 w-3.5" />
                  Add Medication
                </button>
              </div>

              <div className="space-y-4">
                {prescriptionLines.map((line, index) => {
                  const drugInfo = DRUG_CATALOG.find((d) => d.genericName === line.drugName);
                  const awareClass = drugInfo?.awareClass || "Access";

                  return (
                    <div
                      key={line.id}
                      className="rounded-xl border border-border bg-slate-50/60 p-4 space-y-3 relative group"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-ink">
                            Medication #{index + 1}
                          </span>
                          {/* AWaRe badge */}
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                              awareClass === "Access"
                                ? "bg-emerald-50 text-emerald-700 border-emerald-300"
                                : awareClass === "Watch"
                                ? "bg-amber-50 text-amber-700 border-amber-300"
                                : "bg-purple-50 text-purple-700 border-purple-300"
                            }`}
                          >
                            WHO {awareClass} Class
                          </span>
                        </div>
                        {prescriptionLines.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removePrescriptionLine(line.id)}
                            className="text-slate-400 hover:text-urgent p-1 rounded transition-colors"
                            title="Remove medication"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
                        <div className="sm:col-span-2">
                          <label className="block text-[11px] font-bold text-slate-clinical mb-1">
                            Generic Antimicrobial Agent
                          </label>
                          <select
                            value={line.drugName}
                            onChange={(e) => updatePrescriptionLine(line.id, "drugName", e.target.value)}
                            className="w-full rounded-lg border border-border bg-white px-3 py-2 text-xs font-bold text-ink focus:border-primary focus:outline-hidden"
                          >
                            {DRUG_CATALOG.map((drug) => (
                              <option key={drug.id} value={drug.genericName}>
                                {drug.genericName} ({drug.awareClass})
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-[11px] font-bold text-slate-clinical mb-1">
                            Dosage (e.g. 500 mg)
                          </label>
                          <input
                            type="text"
                            value={line.doseText}
                            onChange={(e) => updatePrescriptionLine(line.id, "doseText", e.target.value)}
                            placeholder="500 mg"
                            className="w-full rounded-lg border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                          />
                        </div>

                        <div>
                          <label className="block text-[11px] font-bold text-slate-clinical mb-1">
                            Frequency
                          </label>
                          <input
                            type="text"
                            value={line.frequencyText}
                            onChange={(e) => updatePrescriptionLine(line.id, "frequencyText", e.target.value)}
                            placeholder="Twice daily (BD)"
                            className="w-full rounded-lg border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                          />
                        </div>

                        <div className="sm:col-span-4">
                          <div className="flex items-center justify-between mb-1">
                            <label className="text-[11px] font-bold text-slate-clinical">
                              Course Duration (Days)
                            </label>
                            {!line.durationDays && (
                              <span className="text-[10px] font-bold text-amber-700">
                                Missing Duration
                              </span>
                            )}
                          </div>
                          <input
                            type="number"
                            min="1"
                            max="60"
                            value={line.durationDays}
                            onChange={(e) => updatePrescriptionLine(line.id, "durationDays", e.target.value)}
                            placeholder="e.g. 5 (Leave empty if unrecorded)"
                            className="w-full rounded-lg border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="flex justify-between pt-4 border-t border-border">
                <button
                  type="button"
                  onClick={() => setCurrentStep(2)}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentStep(4)}
                  className="inline-flex items-center gap-1.5 rounded-xl bg-primary px-5 py-2.5 text-xs font-bold text-white hover:bg-primary-hover shadow-xs"
                >
                  Review &amp; Confirm Facts
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 4: Mandatory Clinician Confirmation */}
          {currentStep === 4 && (
            <div className="space-y-5 animate-in fade-in duration-150">
              <div className="border-b border-border pb-3">
                <h3 className="text-base font-bold text-ink flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-primary" />
                  Step 4: Mandatory Clinician Confirmation &amp; Safety Gate
                </h3>
                <p className="text-xs text-slate-clinical mt-0.5">
                  Review structured clinical facts prior to running deterministic safety evaluation.
                </p>
              </div>

              {/* Facts Summary Table */}
              <div className="rounded-xl border border-border bg-canvas p-4 text-xs space-y-3">
                <h4 className="font-bold text-ink uppercase tracking-wider text-[11px]">
                  Confirmed Input Summary
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="rounded-lg bg-white p-2.5 border border-border">
                    <span className="text-slate-clinical block text-[11px]">Patient Age</span>
                    <span className="font-bold text-ink">{ageYears} years</span>
                  </div>
                  <div className="rounded-lg bg-white p-2.5 border border-border">
                    <span className="text-slate-clinical block text-[11px]">Pregnancy Status</span>
                    <span className="font-bold text-ink">{isPregnant ? "Yes (Pregnant)" : "No"}</span>
                  </div>
                  <div className="rounded-lg bg-white p-2.5 border border-border">
                    <span className="text-slate-clinical block text-[11px]">Renal eGFR</span>
                    <span className="font-bold text-ink">
                      {egfrMlMin ? `${egfrMlMin} mL/min` : "Undocumented"}
                    </span>
                  </div>
                  <div className="rounded-lg bg-white p-2.5 border border-border">
                    <span className="text-slate-clinical block text-[11px]">Known Allergies</span>
                    <span className="font-bold text-ink">{allergies || "None Documented"}</span>
                  </div>
                </div>

                <div className="rounded-lg bg-white p-3 border border-border">
                  <span className="text-slate-clinical block text-[11px] mb-1">
                    Prescribed Regimen ({prescriptionLines.length} Agent{prescriptionLines.length > 1 ? "s" : ""})
                  </span>
                  <ul className="divide-y divide-border">
                    {prescriptionLines.map((line, idx) => (
                      <li key={idx} className="py-2 flex items-center justify-between text-xs">
                        <div>
                          <span className="font-bold text-ink">{line.drugName}</span>
                          <span className="text-slate-clinical ml-2">
                            {line.doseText} • {line.frequencyText}
                          </span>
                        </div>
                        <span className="font-semibold text-slate-clinical">
                          {line.durationDays ? `${line.durationDays} days` : "Missing duration"}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Missing Data Warning if applicable */}
              {(!egfrMlMin || prescriptionLines.some((l) => !l.durationDays)) && (
                <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-xs text-amber-900 flex items-start gap-2.5">
                  <AlertCircle className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold block text-sm">Missing Clinical Parameters Detected:</span>
                    <ul className="list-disc pl-5 mt-1 space-y-0.5 text-xs text-amber-800">
                      {!egfrMlMin && <li>Renal function (eGFR) is unrecorded. Will trigger Data Gap flag.</li>}
                      {prescriptionLines.some((l) => !l.durationDays) && (
                        <li>One or more prescription lines lack a specified course duration.</li>
                      )}
                    </ul>
                    <span className="text-[11px] text-amber-700 block mt-1.5 italic">
                      The pure deterministic rules engine evaluates only confirmed facts and will not assume normal values.
                    </span>
                  </div>
                </div>
              )}

              {/* Mandatory Clinician Checkbox */}
              <div className="rounded-xl border-2 border-primary/30 bg-primary-subtle/20 p-4">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={confirmedByClinician}
                    onChange={(e) => setConfirmedByClinician(e.target.checked)}
                    className="h-5 w-5 rounded border-border text-primary focus:ring-primary mt-0.5"
                  />
                  <div className="space-y-1">
                    <span className="text-xs font-bold text-ink flex items-center gap-1.5">
                      <ShieldCheck className="h-4 w-4 text-primary" />
                      I confirm these structured clinical facts are verified and ready for deterministic audit
                    </span>
                    <p className="text-[11px] text-slate-clinical leading-relaxed">
                      Per the AMR Sentinel Clinical Safety Specification, AI/OCR extraction is untrusted until explicitly confirmed by a qualified human clinician. The deterministic rules engine will evaluate only these confirmed facts.
                    </p>
                  </div>
                </label>
              </div>

              <div className="flex justify-between pt-4 border-t border-border">
                <button
                  type="button"
                  onClick={() => setCurrentStep(3)}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back
                </button>
                <button
                  type="button"
                  onClick={handleAuditSubmit}
                  disabled={!confirmedByClinician || isSubmitting}
                  className={`inline-flex items-center gap-2 rounded-xl px-6 py-2.5 text-xs font-bold shadow-xs transition-all ${
                    confirmedByClinician && !isSubmitting
                      ? "bg-primary text-white hover:bg-primary-hover"
                      : "bg-slate-200 text-slate-400 cursor-not-allowed"
                  }`}
                >
                  {isSubmitting ? "Running Deterministic Audit..." : "Run Deterministic Audit"}
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Right Column (40% ~ 5 cols): Real-Time Clinical Summary & Safety Guardrails Card */}
        <div className="lg:col-span-5 space-y-4 lg:sticky lg:top-24">
          <div className="rounded-2xl border border-border bg-surface p-5 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <HeartPulse className="h-4 w-4 text-primary" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-ink">
                  Live Safety Guardrails Preview
                </h4>
              </div>
              <span className="text-[10px] font-mono text-slate-clinical">11 Rules Active</span>
            </div>

            {/* Live Patient Risk Assessment */}
            <div className="space-y-2 text-xs">
              <span className="font-bold text-slate-clinical block text-[11px] uppercase tracking-wider">
                Patient Risk Profile
              </span>
              <div className="space-y-1.5">
                <div className="flex items-center justify-between p-2 rounded-lg bg-canvas border border-border/70">
                  <span className="text-slate-clinical">Age Band:</span>
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${ageBand.color}`}>
                    {ageBand.label}
                  </span>
                </div>
                <div className="flex items-center justify-between p-2 rounded-lg bg-canvas border border-border/70">
                  <span className="text-slate-clinical">Renal eGFR:</span>
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${ckdStage.color}`}>
                    {ckdStage.stage}
                  </span>
                </div>
                {gender === "female" && (
                  <div className="flex items-center justify-between p-2 rounded-lg bg-canvas border border-border/70">
                    <span className="text-slate-clinical">Pregnancy:</span>
                    <span className="font-bold text-ink">
                      {isPregnant ? "Pregnant (FDA High Risk)" : "Not Pregnant"}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Indication Guidance Preview */}
            <div className="space-y-2 text-xs pt-2 border-t border-border">
              <span className="font-bold text-slate-clinical block text-[11px] uppercase tracking-wider">
                Active Indication Pathway
              </span>
              <div className="rounded-lg bg-canvas p-3 border border-border space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-ink">{activeCondition.displayName}</span>
                  <span className="text-[10px] font-semibold text-slate-clinical">
                    [{activeCondition.icmrCategory}]
                  </span>
                </div>
                <p className="text-[11px] text-slate-clinical leading-relaxed">
                  {activeCondition.isSelfLimitingOrViral
                    ? "ICMR STG classifies this condition as viral / self-limiting. Empiric antibacterial therapy is contraindicated."
                    : "ICMR STG 2022 first-line recommendation: Standard Access group monotherapy."}
                </p>
              </div>
            </div>

            {/* Configured Safety Tiers */}
            <div className="space-y-2 text-xs pt-2 border-t border-border">
              <span className="font-bold text-slate-clinical block text-[11px] uppercase tracking-wider">
                Deterministic Engine Architecture
              </span>
              <div className="space-y-1.5 text-[11px]">
                <div className="flex items-center justify-between text-slate-clinical">
                  <span>Tier 1: Patient Safety Contraindications</span>
                  <span className="font-bold text-urgent">Enforced</span>
                </div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span>Tier 2: Indication Concordance &amp; Viral Check</span>
                  <span className="font-bold text-amber-700">Enforced</span>
                </div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span>Tier 3: WHO AWaRe Escalation Gates</span>
                  <span className="font-bold text-purple-700">Enforced</span>
                </div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span>Tier 4: Missing Clinical Parameter Hold</span>
                  <span className="font-bold text-info">Enforced</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
