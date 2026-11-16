"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  FileText,
  Clock,
  ArrowLeft,
  CheckCircle,
  AlertOctagon,
  Printer,
  Share2,
  ShieldCheck,
  Building2,
  ExternalLink,
  BookOpen,
} from "lucide-react";
import { AppLayout } from "@/components/AppLayout";
import { StatusBadge, AuditStatus } from "@/components/StatusBadge";
import { FindingCard, FindingItem } from "@/components/FindingCard";
import { DataGapCallout } from "@/components/DataGapCallout";
import { EvidenceDrawer, EvidenceSource } from "@/components/EvidenceDrawer";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { CONDITION_CATALOG } from "@/lib/clinical-data";

export default function ResultsPage() {
  const [status, setStatus] = useState<AuditStatus>("NEEDS_URGENT_REVIEW");
  const [auditId, setAuditId] = useState<string>("AUD-2026-SYN-001");
  const [ruleSetVersion, setRuleSetVersion] = useState<string>("1.0.0-ICMR-STG-2022");
  const [findings, setFindings] = useState<FindingItem[]>([]);
  const [dataGaps, setDataGaps] = useState<string[]>([]);
  const [confirmedInput, setConfirmedInput] = useState<Record<string, unknown> | null>(null);

  // Evidence Drawer state
  const [activeEvidence, setActiveEvidence] = useState<EvidenceSource | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState<boolean>(false);

  // Acknowledgement State
  const [isAcknowledged, setIsAcknowledged] = useState<boolean>(false);
  const [overrideReason, setOverrideReason] = useState<string>("");
  const [showAckModal, setShowAckModal] = useState<boolean>(false);

  useEffect(() => {
    // 1. Try to load from API result in sessionStorage
    const storedResult = sessionStorage.getItem("amr_active_audit_result");
    const storedPayload = sessionStorage.getItem("amr_active_audit_payload");

    if (storedPayload) {
      try {
        setConfirmedInput(JSON.parse(storedPayload));
      } catch (e) {
        console.error("Failed to parse stored payload", e);
      }
    }

    if (storedResult) {
      try {
        const parsed = JSON.parse(storedResult);
        const resolvedAuditId = parsed.audit_id || parsed.auditId || `AUD-${Date.now()}`;
        setStatus(parsed.status || "NEEDS_REVIEW");
        setAuditId(resolvedAuditId);
        setRuleSetVersion(parsed.rule_set_version || parsed.ruleSetVersion || "1.0.0-ICMR-STG-2022");

        const rawFindings = Array.isArray(parsed.findings) ? parsed.findings : [];
        const normalizedFindings: FindingItem[] = rawFindings.map((f: any, idx: number) => ({
          id: f.id || `FND-${idx + 1}`,
          ruleId: f.ruleId || f.rule_id || "AMR-RULE",
          severity: f.severity || "NEEDS_REVIEW",
          title: f.title || "Clinical Stewardship Advisory",
          explanation: f.explanation || "",
          inputFactsUsed: f.inputFactsUsed || f.input_facts_used || {},
          missingDataStatus: f.missingDataStatus || f.missing_data_status || [],
          guidelineDiscussionPrompt: f.guidelineDiscussionPrompt || f.guideline_discussion_prompt || undefined,
          evidence: f.evidence
            ? {
                ...f.evidence,
                publishedOn: f.evidence.publishedOn || f.evidence.published_on || "N/A",
                sectionRef: f.evidence.sectionRef || f.evidence.section_ref || "Standard Section",
              }
            : {
                id: "EVID_STANDARD",
                title: "ICMR Standard Treatment Guidelines 2022",
                publisher: "Indian Council of Medical Research",
                jurisdiction: "India (National)",
                publishedOn: "2022",
                sectionRef: "General Guidelines",
                excerpt: "Prescribe antimicrobials strictly according to verified indications and local antibiograms.",
              },
          acknowledged: Boolean(f.acknowledged),
        }));

        setFindings(normalizedFindings);
        setDataGaps(parsed.input_gaps || parsed.inputGaps || []);

        const storedAck = sessionStorage.getItem(`amr_ack_${resolvedAuditId}`);
        if (storedAck) {
          try {
            const parsedAck = JSON.parse(storedAck);
            setIsAcknowledged(true);
            setOverrideReason(parsedAck.reason || "");
          } catch {
            // ignore
          }
        }
        return;
      } catch (e) {
        console.error("Failed to parse stored result", e);
      }
    }

    // Default demonstration case if no sessionStorage
    const defaultEvidence: EvidenceSource = {
      id: "EVID_ICMR_PED_FQ_2022",
      title: "ICMR Standard Treatment Guidelines: Pediatric Antimicrobial Use & Safety",
      publisher: "Indian Council of Medical Research (ICMR)",
      jurisdiction: "India (National)",
      publishedOn: "2022-09-15",
      sectionRef: "Pediatric Guidelines • Section 4.2 • Page 38",
      excerpt: "Fluoroquinolones (Ciprofloxacin, Ofloxacin, Levofloxacin) are strictly contraindicated in pediatric patients (<18 years) due to documented animal and clinical evidence of cartilage erosion, arthropathy, and tendon rupture, except in specific life-threatening multidrug-resistant cystic fibrosis or anthrax.",
      url: "https://main.icmr.nic.in",
    };

    setStatus("NEEDS_URGENT_REVIEW");
    setFindings([
      {
        id: "FND-001",
        ruleId: "SAFETY.PED.FQ_UNDER_18",
        severity: "URGENT_REVIEW",
        title: "Contraindicated Fluoroquinolone Prescribed in Pediatric Patient (<18 Years)",
        explanation: "Ciprofloxacin was prescribed for an 8-year-old child. ICMR Pediatric Guidelines and FDA Black Box warnings state fluoroquinolones are contraindicated in patients under 18 due to risk of cartilage erosion, irreversible arthropathy, and weight-bearing joint lesions.",
        inputFactsUsed: {
          "Patient Age": "8 years",
          "Prescribed Drug": "Ciprofloxacin 250mg BD",
          "Minimum Age Threshold": "18.0 years",
        },
        guidelineDiscussionPrompt: "Consider discussing supportive rehydration (ORS + Zinc for 14 days) or guideline-concordant first-line pediatric agents (e.g. Azithromycin 10mg/kg/day only if invasive dysentery is confirmed). Verify current local guidelines.",
        evidence: defaultEvidence,
      },
    ]);
  }, []);

  const handleOpenEvidence = (ev: EvidenceSource) => {
    setActiveEvidence(ev);
    setIsEvidenceOpen(true);
  };

  const handleAcknowledgeFinding = (findingId: string) => {
    setFindings((prev) =>
      prev.map((f) => (f.id === findingId ? { ...f, acknowledged: true } : f))
    );
  };

  const handleConfirmReview = () => {
    setIsAcknowledged(true);
    setShowAckModal(false);
    try {
      sessionStorage.setItem(
        `amr_ack_${auditId}`,
        JSON.stringify({
          acknowledged: true,
          reason: overrideReason,
          timestamp: new Date().toISOString(),
          clinician: "Dr. Ayesha (General Physician)",
        })
      );
    } catch {
      // ignore
    }
  };

  // Resolve human-readable condition name
  const indicationCode = String(confirmedInput?.indicationCode || "SYN_WATERY_DIARRHEA");
  const humanIndicationName =
    CONDITION_CATALOG.find((c) => c.code === indicationCode)?.displayName ||
    (indicationCode.startsWith("SYN_")
      ? indicationCode.replace("SYN_", "").replace(/_/g, " ")
      : indicationCode);

  return (
    <AppLayout>
      <main className="py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-6">
        {/* Navigation & Header Actions */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <Link
            href="/new-audit"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-clinical hover:text-primary transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Case Intake
          </Link>

          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-3.5 py-2 text-xs font-bold text-ink hover:bg-canvas shadow-xs transition-colors"
            >
              <Printer className="h-3.5 w-3.5 text-slate-clinical" />
              Print Report
            </button>
            <button
              onClick={() => alert("De-identified audit summary copied to clipboard.")}
              className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-3.5 py-2 text-xs font-bold text-ink hover:bg-canvas shadow-xs transition-colors"
            >
              <Share2 className="h-3.5 w-3.5 text-slate-clinical" />
              Share Summary
            </button>
          </div>
        </div>

        <SyntheticDataNotice />

        {/* 2-Column Clinical Decision Support Report */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column (65% ~ 8 cols): Audit Findings & Grounded Evidence */}
          <div className="lg:col-span-8 space-y-6">
            {/* Header Card */}
            <div className="rounded-2xl border border-border bg-surface p-6 sm:p-8 shadow-xs space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
                <div className="space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <FileText className="h-5 w-5 text-primary" />
                    <span className="font-mono text-xs font-bold text-slate-clinical">
                      Audit ID: {auditId}
                    </span>
                    <span className="rounded-full bg-slate-100 px-2.5 py-0.5 font-mono text-[11px] text-slate-clinical border border-slate-200">
                      Engine: Pure Deterministic
                    </span>
                  </div>
                  <h1 className="text-2xl font-extrabold tracking-tight text-ink">
                    Prescription Stewardship Audit Report
                  </h1>
                  <p className="text-xs text-slate-clinical flex items-center gap-2">
                    <Clock className="h-3.5 w-3.5" />
                    Evaluated: {new Date().toLocaleDateString()} • Rule Set: {ruleSetVersion}
                  </p>
                </div>

                {/* Status Badge */}
                <div className="shrink-0 flex flex-col items-start md:items-end gap-1.5">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-clinical">
                    Deterministic Status
                  </span>
                  <StatusBadge status={status} size="lg" />
                </div>
              </div>

              {/* Confirmed Input Parameters (Human readable labels, no raw SYN_ tokens!) */}
              {confirmedInput && (
                <div className="rounded-xl bg-canvas p-4 border border-border text-xs space-y-2">
                  <span className="font-bold text-ink uppercase tracking-wider text-[11px]">
                    Confirmed Clinical Inputs Evaluated
                  </span>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
                    <div className="bg-white p-2.5 rounded-lg border border-border">
                      <span className="text-slate-clinical block text-[10px] font-semibold">Patient Demographics</span>
                      <span className="font-bold text-ink">
                        {(confirmedInput.patientContext as { ageYears?: number })?.ageYears ?? "N/A"} yrs •{" "}
                        {(confirmedInput.patientContext as { gender?: string })?.gender ?? "N/A"}
                      </span>
                    </div>
                    <div className="bg-white p-2.5 rounded-lg border border-border">
                      <span className="text-slate-clinical block text-[10px] font-semibold">Suspected Indication</span>
                      <span className="font-bold text-ink truncate block" title={humanIndicationName}>
                        {humanIndicationName}
                      </span>
                    </div>
                    <div className="bg-white p-2.5 rounded-lg border border-border">
                      <span className="text-slate-clinical block text-[10px] font-semibold">Care Setting</span>
                      <span className="font-bold text-ink uppercase">
                        {String(confirmedInput.setting || "outpatient")}
                      </span>
                    </div>
                    <div className="bg-white p-2.5 rounded-lg border border-border">
                      <span className="text-slate-clinical block text-[10px] font-semibold">Renal Function</span>
                      <span className="font-bold text-ink">
                        {(confirmedInput.patientContext as { egfrMlMin?: number })?.egfrMlMin
                          ? `${(confirmedInput.patientContext as { egfrMlMin?: number }).egfrMlMin} mL/min`
                          : "eGFR Unrecorded"}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Data Gaps Callout */}
              <DataGapCallout
                missingFields={dataGaps}
                clinicalImpact="Deterministic rules for nephrotoxicity and duration limits cannot execute completely when required parameters are absent."
              />

              {/* Findings Section */}
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-border pb-2">
                  <h2 className="text-base font-bold text-ink">
                    Clinical Audit Findings ({findings.length})
                  </h2>
                  <span className="text-xs font-semibold text-slate-clinical">
                    ICMR STG 2022 &amp; WHO AWaRe 2023
                  </span>
                </div>

                {findings.length === 0 ? (
                  <div className="rounded-2xl border border-success-border bg-success-subtle/30 p-8 text-center space-y-3">
                    <CheckCircle className="h-10 w-10 text-success mx-auto" />
                    <h3 className="text-base font-bold text-ink">No Prescribing Rule Triggered</h3>
                    <p className="text-xs text-slate-clinical max-w-md mx-auto leading-relaxed">
                      The evaluated prescription lines match ICMR standard first-line recommendations for the declared indication, and no absolute safety contraindications were triggered.
                    </p>
                    <p className="text-[11px] text-slate-clinical italic pt-2">
                      *Reminder: Does not constitute clinical validation or autonomous medical approval.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {findings.map((finding) => (
                      <FindingCard
                        key={finding.id}
                        finding={finding}
                        onOpenEvidence={handleOpenEvidence}
                        onAcknowledge={handleAcknowledgeFinding}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column (35% ~ 4 cols): Clinician Audit Trail & Provenance Registry */}
          <div className="lg:col-span-4 space-y-4 lg:sticky lg:top-24">
            {/* Clinician Review Documentation Card */}
            <div className="rounded-2xl border border-border bg-surface p-5 shadow-xs space-y-4">
              <div className="flex items-center justify-between border-b border-border pb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <h3 className="text-xs font-bold uppercase tracking-wider text-ink">
                    Clinician Review Documentation
                  </h3>
                </div>
                {isAcknowledged && (
                  <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 border border-emerald-300">
                    Logged
                  </span>
                )}
              </div>

              <p className="text-xs text-slate-clinical leading-relaxed">
                Document that clinical alerts were evaluated or record clinical rationale for guideline divergence before proceeding with the prescription.
              </p>

              {isAcknowledged ? (
                <div className="rounded-xl bg-slate-50 p-3.5 border border-border text-xs space-y-2">
                  <span className="font-bold text-ink block text-[11px] uppercase tracking-wider">
                    Audit Trail Documented:
                  </span>
                  <div className="space-y-1 text-slate-clinical text-[11px]">
                    <p>
                      <strong>Clinician:</strong> Dr. Ayesha (General Physician)
                    </p>
                    <p>
                      <strong>Action:</strong> Evaluated &amp; Actioned
                    </p>
                    <p>
                      <strong>Timestamp:</strong> {new Date().toLocaleTimeString()}
                    </p>
                    {overrideReason && (
                      <p className="mt-2 bg-white p-2 rounded border border-border/80 text-ink">
                        <strong>Clinical Justification:</strong> {overrideReason}
                      </p>
                    )}
                  </div>
                </div>
              ) : (
                <button
                  onClick={() => setShowAckModal(true)}
                  className="w-full rounded-xl bg-primary px-4 py-2.5 text-xs font-bold text-white hover:bg-primary-hover shadow-xs transition-colors"
                >
                  Document Clinician Review
                </button>
              )}
            </div>

            {/* Standard Reference Card */}
            <div className="rounded-2xl border border-border bg-surface p-5 shadow-xs space-y-3">
              <div className="flex items-center gap-2 text-ink border-b border-border pb-2.5">
                <BookOpen className="h-4 w-4 text-primary" />
                <h4 className="text-xs font-bold uppercase tracking-wider">Authoritative References</h4>
              </div>
              <div className="space-y-2 text-xs">
                <a
                  href="https://main.icmr.nic.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-2.5 rounded-lg border border-border bg-canvas hover:border-primary/50 transition-colors"
                >
                  <span className="font-semibold text-ink">ICMR STG 2022</span>
                  <ExternalLink className="h-3.5 w-3.5 text-primary" />
                </a>
                <a
                  href="https://www.who.int/publications/i/item/2023-aware-classification"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-2.5 rounded-lg border border-border bg-canvas hover:border-primary/50 transition-colors"
                >
                  <span className="font-semibold text-ink">WHO AWaRe 2023</span>
                  <ExternalLink className="h-3.5 w-3.5 text-primary" />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Modal for Documenting Review */}
        {showAckModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
            <div className="w-full max-w-md rounded-2xl bg-surface p-6 shadow-xl border border-border space-y-4 animate-in fade-in zoom-in-95 duration-150">
              <div className="flex items-center gap-2 text-ink">
                <AlertOctagon className="h-5 w-5 text-primary" />
                <h3 className="text-base font-bold">Document Clinician Review</h3>
              </div>
              <p className="text-xs text-slate-clinical leading-relaxed">
                Confirm you have reviewed all flagged clinical findings. If you intend to proceed with the prescription despite an alert, provide your documented clinical justification (e.g. culture-proven resistance, specialist recommendation).
              </p>

              <div>
                <label className="block text-xs font-bold text-ink mb-1">
                  Clinical Notes / Justification (Optional)
                </label>
                <textarea
                  rows={3}
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  placeholder="e.g. Patient has documented beta-lactam anaphylaxis; alternative approved by ID team..."
                  className="w-full rounded-xl border border-border bg-white p-3 text-xs text-ink focus:border-primary focus:outline-hidden"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-border">
                <button
                  onClick={() => setShowAckModal(false)}
                  className="rounded-xl border border-border px-4 py-2 text-xs font-semibold text-slate-clinical hover:bg-canvas"
                >
                  Cancel
                </button>
                <button
                  onClick={handleConfirmReview}
                  className="rounded-xl bg-primary px-4 py-2 text-xs font-bold text-white hover:bg-primary-hover shadow-xs"
                >
                  Submit Acknowledgement
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Slide-over Evidence Drawer */}
        <EvidenceDrawer
          isOpen={isEvidenceOpen}
          onClose={() => setIsEvidenceOpen(false)}
          evidence={activeEvidence}
          ruleSetVersion={ruleSetVersion}
        />

        <DisclaimerBanner />
      </main>
    </AppLayout>
  );
}
