"use client";

import React, { useState, useEffect } from "react";
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
} from "lucide-react";
import { DRUG_CATALOG, CONDITION_CATALOG } from "@/lib/clinical-data";
import { SYNTHETIC_SAMPLE_CASES, SyntheticCase } from "@/lib/sample-cases";
import { DisclaimerBanner, SyntheticDataNotice } from "./DisclaimerBanner";

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
      // Offline fallback handling
      console.warn("Backend unavailable, client will evaluate deterministic offline fallback");
    } finally {
      setIsSubmitting(false);
      router.push("/results");
    }
  };

  const steps = [
    { num: 1, title: "Patient Context", icon: User },
    { num: 2, title: "Indication & Setting", icon: Activity },
    { num: 3, title: "Prescription Lines", icon: Pill },
    { num: 4, title: "Confirm Facts", icon: CheckCircle },
  ];

  return (
    <div className="space-y-6">
      {/* Sample Cases Quick Loader Banner */}
      <div className="rounded-xl border border-primary/20 bg-primary-subtle/20 p-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-primary">
                Quick-Load Synthetic Golden Test Case
              </h3>
              <p className="text-xs text-slate-clinical">
                Select an ICMR/WHO scenario to instantly populate clinical facts
              </p>
            </div>
          </div>
          <select
            value={selectedCaseId}
            onChange={(e) => {
              const selected = SYNTHETIC_SAMPLE_CASES.find((c) => c.id === e.target.value);
              if (selected) loadSyntheticCase(selected);
            }}
            className="w-full sm:w-auto rounded-lg border border-border bg-white px-3 py-2 text-xs font-medium text-ink shadow-xs focus:border-primary focus:outline-hidden"
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

      {/* Upload Prescription Card */}
      <div className="rounded-xl border border-border bg-surface p-4 shadow-xs">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <UploadCloud className="h-5 w-5 text-primary" />
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

      {/* Stepper Navigation */}
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
                  className={`flex w-full items-center gap-2.5 rounded-lg border p-3 text-left transition-all ${
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
                    <p className="text-xs font-medium truncate">{s.title}</p>
                  </div>
                </button>
              </li>
            );
          })}
        </ol>
      </nav>

      {/* Step Panels */}
      <div className="rounded-xl border border-border bg-surface p-6 shadow-xs">
        {/* Step 1: Patient Context */}
        {currentStep === 1 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-ink flex items-center gap-2">
                <User className="h-5 w-5 text-primary" />
                Step 1: Patient Context & Organ Function
              </h3>
              <p className="text-xs text-slate-clinical">
                Enter age, pregnancy status, renal function, and documented allergies.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-xs font-semibold text-ink mb-1">
                  Patient Age (Years) <span className="text-urgent">*</span>
                </label>
                <input
                  type="number"
                  min="0"
                  max="120"
                  step="0.1"
                  value={ageYears}
                  onChange={(e) => setAgeYears(e.target.value)}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2 text-sm text-ink focus:border-primary focus:outline-hidden"
                  required
                />
                <span className="text-[11px] text-slate-clinical">Pediatric (&lt;18) and Geriatric (&ge;65) safety gates apply.</span>
              </div>

              <div>
                <label className="block text-xs font-semibold text-ink mb-1">
                  Biological Gender <span className="text-urgent">*</span>
                </label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value as "female" | "male" | "other")}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2 text-sm text-ink focus:border-primary focus:outline-hidden"
                >
                  <option value="female">Female</option>
                  <option value="male">Male</option>
                  <option value="other">Other / Not Specified</option>
                </select>
              </div>

              {gender === "female" && (
                <div className="sm:col-span-2 rounded-lg border border-border bg-slate-50/60 p-3.5">
                  <label className="flex items-center gap-2.5 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={isPregnant}
                      onChange={(e) => setIsPregnant(e.target.checked)}
                      className="h-4 w-4 rounded border-border text-primary focus:ring-primary"
                    />
                    <div>
                      <span className="text-xs font-semibold text-ink block">
                        Patient is currently pregnant
                      </span>
                      <span className="text-[11px] text-slate-clinical">
                        Enforces FDA Category D/X and WHO contraindications (Fluoroquinolones, Tetracyclines, Aminoglycosides).
                      </span>
                    </div>
                  </label>
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-ink mb-1">
                  eGFR (mL/min/1.73m²)
                </label>
                <input
                  type="number"
                  min="0"
                  max="200"
                  placeholder="e.g. 90 (Leave empty if unrecorded)"
                  value={egfrMlMin}
                  onChange={(e) => setEgfrMlMin(e.target.value)}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2 text-sm text-ink focus:border-primary focus:outline-hidden"
                />
                <span className="text-[11px] text-slate-clinical">
                  Unrecorded eGFR will trigger mandatory safety holds on nephrotoxic agents.
                </span>
              </div>

              <div>
                <label className="block text-xs font-semibold text-ink mb-1">
                  Known Drug Allergies (comma-separated)
                </label>
                <input
                  type="text"
                  placeholder="e.g. Penicillin, Sulfa"
                  value={allergies}
                  onChange={(e) => setAllergies(e.target.value)}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2 text-sm text-ink focus:border-primary focus:outline-hidden"
                />
                <span className="text-[11px] text-slate-clinical">Evaluates beta-lactam cross-reactivity and adverse histories.</span>
              </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-border">
              <button
                type="button"
                onClick={() => setCurrentStep(2)}
                className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-white hover:bg-primary-hover shadow-xs"
              >
                Proceed to Indication
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Indication & Setting */}
        {currentStep === 2 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-ink flex items-center gap-2">
                <Activity className="h-5 w-5 text-primary" />
                Step 2: Suspected Clinical Indication & Care Setting
              </h3>
              <p className="text-xs text-slate-clinical">
                Select the diagnosis aligned with ICMR Standard Treatment Guidelines 2022.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-ink mb-1">
                  Clinical Indication <span className="text-urgent">*</span>
                </label>
                <select
                  value={indicationCode}
                  onChange={(e) => setIndicationCode(e.target.value)}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2.5 text-sm text-ink focus:border-primary focus:outline-hidden"
                >
                  {CONDITION_CATALOG.map((cond) => (
                    <option key={cond.code} value={cond.code}>
                      [{cond.icmrCategory}] {cond.displayName} {cond.isSelfLimitingOrViral ? " (Viral / Self-Limiting)" : ""}
                    </option>
                  ))}
                </select>
                <span className="text-[11px] text-slate-clinical">
                  Conditions flagged as viral/self-limiting will trigger Tier 2 indication appropriateness reviews.
                </span>
              </div>

              <div>
                <label className="block text-xs font-semibold text-ink mb-1">
                  Care Setting <span className="text-urgent">*</span>
                </label>
                <select
                  value={setting}
                  onChange={(e) => setSetting(e.target.value as "outpatient" | "inpatient")}
                  className="w-full rounded-lg border border-border bg-white px-3.5 py-2 text-sm text-ink focus:border-primary focus:outline-hidden"
                >
                  <option value="outpatient">Outpatient (Ambulatory / Primary Care)</option>
                  <option value="inpatient">Inpatient (Hospitalized / Ward)</option>
                </select>
              </div>
            </div>

            <div className="flex justify-between pt-4 border-t border-border">
              <button
                type="button"
                onClick={() => setCurrentStep(1)}
                className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </button>
              <button
                type="button"
                onClick={() => setCurrentStep(3)}
                className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-white hover:bg-primary-hover shadow-xs"
              >
                Proceed to Prescription
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Prescription Lines */}
        {currentStep === 3 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-ink flex items-center gap-2">
                  <Pill className="h-5 w-5 text-primary" />
                  Step 3: Prescribed Antimicrobial Agents
                </h3>
                <p className="text-xs text-slate-clinical">
                  Enter drugs, dosages, frequencies, and durations.
                </p>
              </div>
              <button
                type="button"
                onClick={addPrescriptionLine}
                className="inline-flex items-center gap-1.5 rounded-lg border border-primary text-primary px-3 py-1.5 text-xs font-semibold hover:bg-primary-subtle/30"
              >
                <Plus className="h-3.5 w-3.5" />
                Add Medication
              </button>
            </div>

            <div className="space-y-4">
              {prescriptionLines.map((line, index) => (
                <div
                  key={line.id}
                  className="rounded-lg border border-border bg-slate-50/50 p-4 space-y-3 relative"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-ink">
                      Medication #{index + 1}
                    </span>
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
                      <label className="block text-[11px] font-semibold text-slate-clinical mb-1">
                        Antimicrobial / Agent Name
                      </label>
                      <select
                        value={line.drugName}
                        onChange={(e) => updatePrescriptionLine(line.id, "drugName", e.target.value)}
                        className="w-full rounded-md border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                      >
                        {DRUG_CATALOG.map((drug) => (
                          <option key={drug.id} value={drug.genericName}>
                            {drug.genericName} ({drug.awareClass})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-[11px] font-semibold text-slate-clinical mb-1">
                        Dose (e.g. 500 mg)
                      </label>
                      <input
                        type="text"
                        value={line.doseText}
                        onChange={(e) => updatePrescriptionLine(line.id, "doseText", e.target.value)}
                        placeholder="500 mg"
                        className="w-full rounded-md border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                      />
                    </div>

                    <div>
                      <label className="block text-[11px] font-semibold text-slate-clinical mb-1">
                        Frequency
                      </label>
                      <input
                        type="text"
                        value={line.frequencyText}
                        onChange={(e) => updatePrescriptionLine(line.id, "frequencyText", e.target.value)}
                        placeholder="Twice daily (BD)"
                        className="w-full rounded-md border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                      />
                    </div>

                    <div>
                      <label className="block text-[11px] font-semibold text-slate-clinical mb-1">
                        Duration (Days)
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="60"
                        value={line.durationDays}
                        onChange={(e) => updatePrescriptionLine(line.id, "durationDays", e.target.value)}
                        placeholder="5 (Leave empty if unrecorded)"
                        className="w-full rounded-md border border-border bg-white px-3 py-2 text-xs text-ink focus:border-primary focus:outline-hidden"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-between pt-4 border-t border-border">
              <button
                type="button"
                onClick={() => setCurrentStep(2)}
                className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </button>
              <button
                type="button"
                onClick={() => setCurrentStep(4)}
                className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-white hover:bg-primary-hover shadow-xs"
              >
                Review & Confirm Facts
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 4: Confirm Facts (Safety Gate) */}
        {currentStep === 4 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-ink flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-primary" />
                Step 4: Mandatory Clinician Confirmation
              </h3>
              <p className="text-xs text-slate-clinical">
                Review structured clinical facts prior to running deterministic safety evaluation.
              </p>
            </div>

            {/* Facts Summary Table */}
            <div className="rounded-xl border border-border bg-canvas p-4 text-xs space-y-3">
              <h4 className="font-bold text-ink uppercase tracking-wider text-[11px]">
                Confirmed Input Summary
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="rounded-md bg-white p-2.5 border border-border">
                  <span className="text-slate-clinical block text-[11px]">Patient Age</span>
                  <span className="font-bold text-ink">{ageYears} years</span>
                </div>
                <div className="rounded-md bg-white p-2.5 border border-border">
                  <span className="text-slate-clinical block text-[11px]">Pregnancy Status</span>
                  <span className="font-bold text-ink">{isPregnant ? "Yes (Pregnant)" : "No"}</span>
                </div>
                <div className="rounded-md bg-white p-2.5 border border-border">
                  <span className="text-slate-clinical block text-[11px]">Renal eGFR</span>
                  <span className="font-bold text-ink">
                    {egfrMlMin ? `${egfrMlMin} mL/min` : "Undocumented / Missing"}
                  </span>
                </div>
                <div className="rounded-md bg-white p-2.5 border border-border">
                  <span className="text-slate-clinical block text-[11px]">Known Allergies</span>
                  <span className="font-bold text-ink">{allergies || "None Documented"}</span>
                </div>
              </div>

              <div className="rounded-md bg-white p-3 border border-border">
                <span className="text-slate-clinical block text-[11px] mb-1">Prescription Lines ({prescriptionLines.length})</span>
                <ul className="divide-y divide-border">
                  {prescriptionLines.map((line, idx) => (
                    <li key={idx} className="py-1.5 flex items-center justify-between text-xs">
                      <span className="font-bold text-ink">{line.drugName}</span>
                      <span className="text-slate-clinical">
                        {line.doseText} • {line.frequencyText} • {line.durationDays ? `${line.durationDays} days` : "Missing duration"}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Missing Data Warning if applicable */}
            {(!egfrMlMin || prescriptionLines.some((l) => !l.durationDays)) && (
              <div className="rounded-lg border border-amber-300 bg-amber-50 p-3.5 text-xs text-amber-900 flex items-start gap-2.5">
                <AlertCircle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold block">Missing Clinical Parameters Detected:</span>
                  <ul className="list-disc pl-5 mt-1 space-y-0.5">
                    {!egfrMlMin && <li>Renal function (eGFR) is unrecorded.</li>}
                    {prescriptionLines.some((l) => !l.durationDays) && <li>One or more lines lack specified duration in days.</li>}
                  </ul>
                  <span className="text-[11px] text-amber-700 block mt-1">
                    The audit engine will evaluate available facts and flag explicit data gaps.
                  </span>
                </div>
              </div>
            )}

            {/* Mandatory Checkbox */}
            <div className="rounded-lg border-2 border-primary/30 bg-primary-subtle/20 p-4">
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
                className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-white px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </button>
              <button
                type="button"
                onClick={handleAuditSubmit}
                disabled={!confirmedByClinician || isSubmitting}
                className={`inline-flex items-center gap-2 rounded-lg px-6 py-2.5 text-xs font-bold shadow-xs transition-all ${
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

      <DisclaimerBanner />
    </div>
  );
}
