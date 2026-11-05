import React from "react";
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
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { StatusBadge } from "@/components/StatusBadge";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { SYNTHETIC_SAMPLE_CASES } from "@/lib/sample-cases";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col">
      <Navbar />

      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Welcome & Organization Banner */}
        <div className="rounded-2xl border border-border bg-surface p-6 sm:p-8 shadow-xs">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full bg-primary-subtle px-3 py-1 text-xs font-semibold text-primary">
                <Building2 className="h-3.5 w-3.5" />
                Demo Org: National Antimicrobial Stewardship Initiative
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-ink">
                Prescription Auditing &amp; Stewardship Dashboard
              </h1>
              <p className="text-sm text-slate-clinical leading-relaxed">
                Empowering prescribers with pure deterministic second-checks against ICMR Standard Treatment Guidelines 2022 and WHO AWaRe 2023. Preventing empiric over-escalation, contraindicated regimens, and irrational combinations in outpatient care.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
              <Link
                href="/new-audit"
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-bold text-white shadow-xs hover:bg-primary-hover transition-colors"
              >
                <Sparkles className="h-4 w-4" />
                Start New Audit
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>

        <SyntheticDataNotice />

        {/* Stewardship Key Metrics (De-identified Institutional Trends) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-clinical">
              <span className="text-xs font-semibold uppercase tracking-wider">Access Class Share</span>
              <Activity className="h-4 w-4 text-emerald-600" />
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-ink">64.2%</span>
              <span className="text-xs font-semibold text-emerald-700 flex items-center">
                ↑ WHO Target &ge;60%
              </span>
            </div>
            <p className="mt-1 text-[11px] text-slate-clinical">WHO AWaRe Benchmark Target</p>
          </div>

          <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-clinical">
              <span className="text-xs font-semibold uppercase tracking-wider">Watch Class Share</span>
              <Activity className="h-4 w-4 text-amber-600" />
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-ink">31.8%</span>
              <span className="text-xs font-semibold text-amber-700 flex items-center">
                <TrendingDown className="h-3 w-3 mr-0.5" /> -4.1% MoM
              </span>
            </div>
            <p className="mt-1 text-[11px] text-slate-clinical">Active De-escalation Rate</p>
          </div>

          <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-clinical">
              <span className="text-xs font-semibold uppercase tracking-wider">Reserve Escapes Intercepted</span>
              <ShieldAlert className="h-4 w-4 text-purple-600" />
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-ink">18</span>
              <span className="text-xs font-semibold text-purple-700">Protected Reserve</span>
            </div>
            <p className="mt-1 text-[11px] text-slate-clinical">Carbapenems &amp; Polymyxins saved</p>
          </div>

          <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-clinical">
              <span className="text-xs font-semibold uppercase tracking-wider">Contraindications Blocked</span>
              <AlertOctagon className="h-4 w-4 text-urgent" />
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-urgent">42</span>
              <span className="text-xs font-semibold text-urgent">Zero-Tolerance</span>
            </div>
            <p className="mt-1 text-[11px] text-slate-clinical">Pediatric, pregnancy &amp; renal safety</p>
          </div>
        </div>

        {/* Guided Synthetic Demo Scenarios */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-ink flex items-center gap-2">
                <FileCheck className="h-5 w-5 text-primary" />
                Featured Synthetic Demonstration Scenarios
              </h2>
              <p className="text-xs text-slate-clinical">
                Explore the 6 core clinical evaluation cases configured for hackathon review.
              </p>
            </div>
            <span className="text-xs font-medium text-slate-clinical">
              6 Verified Golden Cases
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {SYNTHETIC_SAMPLE_CASES.map((sc) => (
              <div
                key={sc.id}
                className="flex flex-col justify-between rounded-xl border border-border bg-surface p-5 shadow-xs hover:border-primary/50 transition-all group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] font-semibold text-slate-clinical">
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

                  <div className="rounded-md bg-canvas p-2.5 text-[11px] text-slate-clinical border border-border/80">
                    <span className="font-semibold text-ink block mb-0.5">Clinical Evaluation:</span>
                    {sc.clinicalObjective}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-border flex items-center justify-between">
                  <span className="text-[11px] font-medium text-slate-clinical">
                    {sc.prescriptionLines.map((l) => l.drugName).join(", ")}
                  </span>
                  <Link
                    href="/new-audit"
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

        {/* Recent Synthetic Audit Activity Log (No PHI) */}
        <div className="rounded-xl border border-border bg-surface p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-ink flex items-center gap-2">
                <Clock className="h-4 w-4 text-primary" />
                Recent Demonstration Audits
              </h2>
              <p className="text-xs text-slate-clinical">
                De-identified record of recent deterministic evaluations for the active demo session.
              </p>
            </div>
            <span className="text-xs text-slate-clinical">Immutable audit logs</span>
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
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                <tr className="hover:bg-canvas/50">
                  <td className="py-3 px-3 font-mono font-medium text-ink">AUD-8921-SYN</td>
                  <td className="py-3 px-3">Acute Bronchitis</td>
                  <td className="py-3 px-3 font-medium">Azithromycin 500mg</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NEEDS_REVIEW" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px]">v1.0.0-ICMR</td>
                  <td className="py-3 px-3">
                    <span className="inline-flex items-center gap-1 text-emerald-700 font-medium">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Acknowledged
                    </span>
                  </td>
                </tr>
                <tr className="hover:bg-canvas/50">
                  <td className="py-3 px-3 font-mono font-medium text-ink">AUD-7412-SYN</td>
                  <td className="py-3 px-3">Uncomplicated UTI</td>
                  <td className="py-3 px-3 font-medium">Nitrofurantoin 100mg BD</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NEEDS_URGENT_REVIEW" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px]">v1.0.0-ICMR</td>
                  <td className="py-3 px-3">
                    <span className="inline-flex items-center gap-1 text-amber-700 font-medium">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Overridden: Culture Proven
                    </span>
                  </td>
                </tr>
                <tr className="hover:bg-canvas/50">
                  <td className="py-3 px-3 font-mono font-medium text-ink">AUD-5530-SYN</td>
                  <td className="py-3 px-3">Community-Acquired Pneumonia</td>
                  <td className="py-3 px-3 font-medium">Amoxicillin 500mg TID</td>
                  <td className="py-3 px-3">
                    <StatusBadge status="NO_RULE_TRIGGERED" size="sm" />
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px]">v1.0.0-ICMR</td>
                  <td className="py-3 px-3 text-slate-clinical">Standard Verification</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <DisclaimerBanner />
      </main>
    </div>
  );
}
