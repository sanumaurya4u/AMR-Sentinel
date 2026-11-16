"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  Sparkles,
  ArrowRight,
  TrendingDown,
  Activity,
  AlertOctagon,
  Clock,
  CheckCircle2,
  Building2,
  FileCheck,
  Filter,
  ShieldCheck,
  Pill,
  Info,
  HelpCircle,
  ExternalLink,
} from "lucide-react";
import { AppLayout } from "@/components/AppLayout";
import { StatusBadge, AuditStatus } from "@/components/StatusBadge";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { SYNTHETIC_SAMPLE_CASES, SyntheticCase } from "@/lib/sample-cases";
import { AnimatedCard } from "@/components/AnimatedCard";

export default function DashboardPage() {
  const [activeFilter, setActiveFilter] = useState<string>("ALL");

  // Filter logic for 6 synthetic cases
  const filteredCases = SYNTHETIC_SAMPLE_CASES.filter((sc) => {
    if (activeFilter === "ALL") return true;
    if (activeFilter === "URGENT") return sc.expectedStatus === "NEEDS_URGENT_REVIEW";
    if (activeFilter === "REVIEW") return sc.expectedStatus === "NEEDS_REVIEW";
    if (activeFilter === "GAPS") return sc.expectedStatus === "INCOMPLETE_DATA";
    if (activeFilter === "CONCORDANT") return sc.expectedStatus === "NO_RULE_TRIGGERED";
    return true;
  });

  return (
    <AppLayout>
      <main className="py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Welcome & Organization Clinical Banner */}
        <AnimatedCard delay={0.05}>
          <div className="rounded-2xl border border-border bg-surface p-6 sm:p-8 shadow-xs relative overflow-hidden">
            <div className="absolute top-0 right-0 h-48 w-48 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
              <div className="space-y-3 max-w-3xl">
                <div className="flex flex-wrap items-center gap-2">
                  <div className="inline-flex items-center gap-1.5 rounded-full bg-primary-subtle px-3 py-1 text-xs font-semibold text-primary border border-primary/20">
                    <Building2 className="h-3.5 w-3.5" />
                    Demo Org: National Antimicrobial Stewardship Initiative
                  </div>
                  <div className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-2.5 py-0.5 text-[11px] font-mono text-slate-clinical border border-slate-200">
                    <ShieldCheck className="h-3 w-3 text-emerald-600" />
                    ICMR STG 2022 • WHO AWaRe 2023
                  </div>
                </div>

                <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-ink">
                  Prescription Auditing &amp; Stewardship Dashboard
                </h1>
                <p className="text-xs sm:text-sm text-slate-clinical leading-relaxed">
                  Clinician-assistive decision support delivering pure deterministic second-checks against codified guidelines. Prevents empiric over-escalation, contraindicated regimens, and irrational combinations before dispensing.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
                <Link
                  href="/new-audit"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-xs sm:text-sm font-bold text-white shadow-xs hover:bg-primary-hover transition-all"
                >
                  <Sparkles className="h-4 w-4" />
                  Start New Audit
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/insights"
                  className="inline-flex items-center justify-center gap-2 rounded-xl border border-border bg-white px-4 py-3 text-xs sm:text-sm font-semibold text-ink hover:bg-canvas transition-colors"
                >
                  <Activity className="h-4 w-4 text-primary" />
                  Stewardship Insights
                </Link>
              </div>
            </div>
          </div>
        </AnimatedCard>

        {/* Persistent Synthetic Demonstration Notice */}
        <SyntheticDataNotice />

        {/* Clinical KPI Cards (Institutional Stewardship Trends) */}
        <AnimatedCard delay={0.1}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* KPI 1: Access Class Share */}
            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs flex flex-col justify-between group hover:border-primary/40 transition-all">
              <div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span className="text-[11px] font-bold uppercase tracking-wider">
                    Access Class Share
                  </span>
                  <Activity className="h-4 w-4 text-emerald-600" />
                </div>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-ink tabular-nums">64.2%</span>
                  <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 flex items-center">
                    ↑ &ge;60% WHO Target
                  </span>
                </div>
                {/* Visual Target Progress Bar */}
                <div className="mt-3 w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-emerald-600 h-1.5 rounded-full"
                    style={{ width: "64.2%" }}
                    title="Current Access rate: 64.2% (Target: >=60%)"
                  />
                </div>
              </div>
              <p className="mt-3 text-[11px] text-slate-clinical pt-2 border-t border-border/60">
                WHO AWaRe Benchmark Target met institutional-wide
              </p>
            </div>

            {/* KPI 2: Watch Class Share */}
            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs flex flex-col justify-between group hover:border-primary/40 transition-all">
              <div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span className="text-[11px] font-bold uppercase tracking-wider">
                    Watch Class Share
                  </span>
                  <Activity className="h-4 w-4 text-amber-600" />
                </div>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-ink tabular-nums">31.8%</span>
                  <span className="text-[11px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200 flex items-center">
                    <TrendingDown className="h-3 w-3 mr-0.5" /> -4.1% MoM
                  </span>
                </div>
                {/* Visual Target Progress Bar */}
                <div className="mt-3 w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-amber-500 h-1.5 rounded-full"
                    style={{ width: "31.8%" }}
                    title="Current Watch rate: 31.8%"
                  />
                </div>
              </div>
              <p className="mt-3 text-[11px] text-slate-clinical pt-2 border-t border-border/60">
                Active de-escalation of empirical fluoroquinolones &amp; 3rd-gen cephalosporins
              </p>
            </div>

            {/* KPI 3: Reserve Escapes Intercepted */}
            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs flex flex-col justify-between group hover:border-primary/40 transition-all">
              <div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span className="text-[11px] font-bold uppercase tracking-wider">
                    Reserve Interceptions
                  </span>
                  <ShieldAlert className="h-4 w-4 text-purple-600" />
                </div>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-ink tabular-nums">18</span>
                  <span className="text-[11px] font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-full border border-purple-200">
                    Protected Reserve
                  </span>
                </div>
                <div className="mt-3 w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-purple-600 h-1.5 rounded-full"
                    style={{ width: "100%" }}
                    title="18 Reserve antibiotic orders intercepted without microbiological culture"
                  />
                </div>
              </div>
              <p className="mt-3 text-[11px] text-slate-clinical pt-2 border-t border-border/60">
                Carbapenems &amp; Polymyxins saved from irrational initiation
              </p>
            </div>

            {/* KPI 4: Contraindications Blocked */}
            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs flex flex-col justify-between group hover:border-primary/40 transition-all">
              <div>
                <div className="flex items-center justify-between text-slate-clinical">
                  <span className="text-[11px] font-bold uppercase tracking-wider">
                    Contraindications Blocked
                  </span>
                  <AlertOctagon className="h-4 w-4 text-urgent" />
                </div>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-urgent tabular-nums">42</span>
                  <span className="text-[11px] font-bold text-urgent bg-urgent-subtle px-2 py-0.5 rounded-full border border-urgent-border">
                    Zero-Tolerance
                  </span>
                </div>
                <div className="mt-3 w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-urgent h-1.5 rounded-full"
                    style={{ width: "100%" }}
                    title="42 patient safety contraindications blocked"
                  />
                </div>
              </div>
              <p className="mt-3 text-[11px] text-slate-clinical pt-2 border-t border-border/60">
                Pediatric, pregnancy &amp; severe renal safety gates enforced
              </p>
            </div>
          </div>
        </AnimatedCard>

        {/* Featured Synthetic Demonstration Scenarios Library */}
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border pb-3">
            <div>
              <h2 className="text-lg font-bold text-ink flex items-center gap-2">
                <FileCheck className="h-5 w-5 text-primary" />
                Featured Synthetic Demonstration Scenarios
              </h2>
              <p className="text-xs text-slate-clinical mt-0.5">
                Explore the 6 verified golden clinical cases configured for hackathon review.
              </p>
            </div>

            {/* Scenario Filter Tabs */}
            <div className="flex flex-wrap items-center gap-1.5">
              {[
                { key: "ALL", label: "All Cases (6)" },
                { key: "URGENT", label: "Urgent Safety (2)" },
                { key: "REVIEW", label: "Stewardship Review (2)" },
                { key: "GAPS", label: "Data Gaps (1)" },
                { key: "CONCORDANT", label: "Concordant (1)" },
              ].map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setActiveFilter(tab.key)}
                  className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-all ${
                    activeFilter === tab.key
                      ? "bg-primary text-white shadow-2xs"
                      : "bg-surface border border-border text-slate-clinical hover:bg-canvas hover:text-ink"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Grid of Cases */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredCases.map((sc) => (
              <div
                key={sc.id}
                className="flex flex-col justify-between rounded-xl border border-border bg-surface p-5 shadow-xs hover:border-primary/50 hover:shadow-sm transition-all group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] font-bold text-slate-clinical bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                      {sc.id}
                    </span>
                    <StatusBadge status={sc.expectedStatus} size="sm" />
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-ink group-hover:text-primary transition-colors">
                      {sc.title}
                    </h3>
                    <p className="mt-1 text-xs text-slate-clinical leading-relaxed">
                      {sc.scenarioSubtitle}
                    </p>
                  </div>

                  {/* Drug Prescribed with Pill Icon */}
                  <div className="rounded-lg bg-canvas p-2.5 border border-border/70 flex items-center gap-2 text-xs">
                    <Pill className="h-4 w-4 text-primary shrink-0" />
                    <div className="min-w-0">
                      <span className="text-[10px] text-slate-clinical uppercase font-semibold block">
                        Prescribed Regimen
                      </span>
                      <span className="font-bold text-ink truncate block">
                        {sc.prescriptionLines.map((l) => `${l.drugName} ${l.doseText}`).join(", ")}
                      </span>
                    </div>
                  </div>

                  {/* Clinical Evaluation Callout */}
                  <div className="rounded-lg bg-slate-50/70 p-2.5 text-[11px] text-slate-clinical border border-border/60">
                    <span className="font-bold text-ink block mb-0.5">Clinical Evaluation:</span>
                    {sc.clinicalObjective}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-border flex items-center justify-between">
                  <span className="text-[11px] font-medium text-slate-clinical">
                    Age: {sc.patientContext.ageYears}y • {sc.patientContext.gender}
                  </span>
                  <Link
                    href={`/new-audit?case=${sc.id}`}
                    className="inline-flex items-center gap-1 text-xs font-bold text-primary group-hover:translate-x-0.5 transition-transform"
                  >
                    Load Case
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Demonstration Audits Table */}
        <div className="rounded-xl border border-border bg-surface p-6 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/80 pb-3">
            <div>
              <h2 className="text-base font-bold text-ink flex items-center gap-2">
                <Clock className="h-4 w-4 text-primary" />
                Recent Demonstration Audits
              </h2>
              <p className="text-xs text-slate-clinical">
                De-identified record of deterministic evaluations conducted in the active demo environment. Zero PHI.
              </p>
            </div>
            <span className="text-xs font-semibold text-slate-clinical bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200">
              Deterministic Audit Ledger
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-border bg-canvas text-slate-clinical font-semibold">
                  <th className="py-2.5 px-3">Audit ID</th>
                  <th className="py-2.5 px-3">Suspected Indication</th>
                  <th className="py-2.5 px-3">Prescribed Agent(s)</th>
                  <th className="py-2.5 px-3">Deterministic Outcome</th>
                  <th className="py-2.5 px-3">Rule Set</th>
                  <th className="py-2.5 px-3">Clinician Review</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                <tr className="hover:bg-canvas/50 transition-colors">
                  <td className="py-3 px-3 font-mono font-bold text-ink">AUD-8921-SYN</td>
                  <td className="py-3 px-3 font-medium">Acute Bronchitis (Self-Limiting)</td>
                  <td className="py-3 px-3 font-semibold text-amber-700">Azithromycin 500mg</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NEEDS_REVIEW" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px] text-slate-clinical">v1.0.0-ICMR</td>
                  <td className="py-3 px-3">
                    <span className="inline-flex items-center gap-1 text-emerald-700 font-semibold text-[11px]">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Acknowledged: Supportive Care
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <Link
                      href="/new-audit?case=SYN_CASE_03_VIRAL_BRONCHITIS"
                      className="font-bold text-primary hover:underline text-[11px]"
                    >
                      Inspect
                    </Link>
                  </td>
                </tr>
                <tr className="hover:bg-canvas/50 transition-colors">
                  <td className="py-3 px-3 font-mono font-bold text-ink">AUD-7412-SYN</td>
                  <td className="py-3 px-3 font-medium">Uncomplicated UTI (eGFR 22)</td>
                  <td className="py-3 px-3 font-semibold text-urgent">Nitrofurantoin 100mg BD</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NEEDS_URGENT_REVIEW" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px] text-slate-clinical">v1.0.0-ICMR</td>
                  <td className="py-3 px-3">
                    <span className="inline-flex items-center gap-1 text-amber-700 font-semibold text-[11px]">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Overridden: Culture Proven
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <Link
                      href="/new-audit?case=SYN_CASE_02_GERIATRIC_RENAL"
                      className="font-bold text-primary hover:underline text-[11px]"
                    >
                      Inspect
                    </Link>
                  </td>
                </tr>
                <tr className="hover:bg-canvas/50 transition-colors">
                  <td className="py-3 px-3 font-mono font-bold text-ink">AUD-5530-SYN</td>
                  <td className="py-3 px-3 font-medium">Community-Acquired Pneumonia</td>
                  <td className="py-3 px-3 font-semibold text-emerald-700">Amoxicillin 500mg TID</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NO_RULE_TRIGGERED" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px] text-slate-clinical">v1.0.0-ICMR</td>
                  <td className="py-3 px-3 text-slate-clinical text-[11px]">
                    Guideline Concordant Verification
                  </td>
                  <td className="py-3 px-3 text-right">
                    <Link
                      href="/new-audit?case=SYN_CASE_06_CLEAN_GUIDELINE"
                      className="font-bold text-primary hover:underline text-[11px]"
                    >
                      Inspect
                    </Link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Clinical Disclaimer Banner */}
        <DisclaimerBanner />
      </main>
    </AppLayout>
  );
}
