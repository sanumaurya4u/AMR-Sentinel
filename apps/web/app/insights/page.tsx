import React from "react";
import { Navbar } from "@/components/Navbar";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { BarChart3, PieChart, TrendingUp, AlertTriangle, ShieldCheck } from "lucide-react";

export default function InsightsPage() {
  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col">
      <Navbar />

      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-primary" />
            Institutional Antimicrobial Stewardship Analytics
          </h1>
          <p className="text-xs text-slate-clinical mt-1">
            De-identified aggregate metrics benchmarking institutional prescribing against WHO AWaRe 2023 targets and ICMR Standard Treatment Guidelines. Zero PHI.
          </p>
        </div>

        <SyntheticDataNotice />

        {/* AWaRe Spectrum Distribution Chart (Pure Accessible CSS / SVG) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 rounded-xl border border-border bg-surface p-6 shadow-xs space-y-5">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-ink flex items-center gap-2">
                  <PieChart className="h-4 w-4 text-primary" />
                  WHO AWaRe Classification Portfolio Distribution
                </h3>
                <p className="text-xs text-slate-clinical">
                  WHO recommends &gt;60% of total antibiotic consumption be from the Access group.
                </p>
              </div>
              <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                Target Met (64.2%)
              </span>
            </div>

            {/* Horizontal Stacked Bar */}
            <div className="space-y-2">
              <div className="h-8 w-full rounded-lg overflow-hidden flex shadow-inner border border-border">
                <div
                  style={{ width: "64.2%" }}
                  className="bg-emerald-600 flex items-center justify-center text-white text-xs font-bold"
                  title="Access Class: 64.2%"
                >
                  Access 64.2%
                </div>
                <div
                  style={{ width: "31.8%" }}
                  className="bg-amber-500 flex items-center justify-center text-white text-xs font-bold"
                  title="Watch Class: 31.8%"
                >
                  Watch 31.8%
                </div>
                <div
                  style={{ width: "4.0%" }}
                  className="bg-purple-600 flex items-center justify-center text-white text-xs font-bold"
                  title="Reserve Class: 4.0%"
                >
                  Res. 4%
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs pt-2">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-emerald-600 shrink-0"></span>
                  <div>
                    <span className="font-bold text-ink">Access (First-line)</span>
                    <p className="text-[11px] text-slate-clinical">Amoxicillin, Nitrofurantoin</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-amber-500 shrink-0"></span>
                  <div>
                    <span className="font-bold text-ink">Watch (High Resistance)</span>
                    <p className="text-[11px] text-slate-clinical">Cefixime, Azithromycin, FQs</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-purple-600 shrink-0"></span>
                  <div>
                    <span className="font-bold text-ink">Reserve (Last-resort)</span>
                    <p className="text-[11px] text-slate-clinical">Meropenem, Colistin, Linezolid</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Top Triggered Safety Gates */}
          <div className="rounded-xl border border-border bg-surface p-6 shadow-xs space-y-4">
            <h3 className="text-sm font-bold text-ink flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-urgent" />
              Top Triggered Safety Rules
            </h3>
            <div className="space-y-3 text-xs">
              <div className="rounded-lg bg-canvas p-3 border border-border">
                <div className="flex items-center justify-between font-semibold text-ink">
                  <span>Viral Bronchitis Prescription</span>
                  <span className="text-urgent font-bold">34% of alerts</span>
                </div>
                <p className="text-[11px] text-slate-clinical mt-0.5">
                  Azithromycin / Cefixime prescribed for self-limiting cough
                </p>
              </div>

              <div className="rounded-lg bg-canvas p-3 border border-border">
                <div className="flex items-center justify-between font-semibold text-ink">
                  <span>Pediatric Fluoroquinolones</span>
                  <span className="text-urgent font-bold">28% of alerts</span>
                </div>
                <p className="text-[11px] text-slate-clinical mt-0.5">
                  Ciprofloxacin/Ofloxacin in patients under 18 years
                </p>
              </div>

              <div className="rounded-lg bg-canvas p-3 border border-border">
                <div className="flex items-center justify-between font-semibold text-ink">
                  <span>Geriatric Renal Nitrofurantoin</span>
                  <span className="text-urgent font-bold">19% of alerts</span>
                </div>
                <p className="text-[11px] text-slate-clinical mt-0.5">
                  eGFR &lt; 30 mL/min or age &ge; 65 years
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Regulatory Conformance Matrix */}
        <div className="rounded-xl border border-border bg-surface p-6 shadow-xs space-y-4">
          <h3 className="text-sm font-bold text-ink flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-primary" />
            Standard Treatment Guideline &amp; Regulatory Alignment
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="rounded-lg border border-border bg-slate-50/50 p-4 space-y-1.5">
              <span className="font-semibold text-primary block">ICMR STG 2022</span>
              <p className="text-slate-clinical leading-relaxed">
                Rules codified against the 2022 Indian Council of Medical Research Treatment Guidelines for common outpatient respiratory, urinary, and gastrointestinal infections.
              </p>
            </div>
            <div className="rounded-lg border border-border bg-slate-50/50 p-4 space-y-1.5">
              <span className="font-semibold text-primary block">WHO AWaRe 2023</span>
              <p className="text-slate-clinical leading-relaxed">
                Integrated AWaRe classification tracking for 81 generic antimicrobials. Empowers health systems to target and achieve the 60% Access threshold.
              </p>
            </div>
            <div className="rounded-lg border border-border bg-slate-50/50 p-4 space-y-1.5">
              <span className="font-semibold text-primary block">CDSCO Banned FDC Directives</span>
              <p className="text-slate-clinical leading-relaxed">
                Zero-tolerance detection for irrational fixed-dose combinations (such as Cefixime + Azithromycin, Ofloxacin + Ornidazole) prohibited under Indian Gazette notifications.
              </p>
            </div>
          </div>
        </div>

        <DisclaimerBanner />
      </main>
    </div>
  );
}
