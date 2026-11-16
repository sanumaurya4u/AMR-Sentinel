"use client";

import React, { useState } from "react";
import { AppLayout } from "@/components/AppLayout";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import {
  BarChart3,
  PieChart,
  TrendingUp,
  AlertTriangle,
  ShieldCheck,
  Activity,
  FileCheck,
  CheckCircle2,
  Calendar,
  Filter,
} from "lucide-react";
import { AwarePieChart } from "@/components/charts/AwarePieChart";
import { SafetyRuleBarChart } from "@/components/charts/SafetyRuleBarChart";
import { ResistanceTrendChart } from "@/components/charts/ResistanceTrendChart";
import { AnimatedCard } from "@/components/AnimatedCard";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function InsightsPage() {
  const [selectedTimeframe, setSelectedTimeframe] = useState("6M");

  return (
    <AppLayout>
      <main className="py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Header with Regulatory Badge & Period Filter */}
        <AnimatedCard delay={0.05}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight flex items-center gap-2">
                <BarChart3 className="h-6 w-6 text-primary" />
                Institutional Antimicrobial Stewardship Analytics
              </h1>
              <p className="text-xs text-slate-clinical mt-1">
                De-identified aggregate metrics benchmarking institutional prescribing against WHO AWaRe 2023 targets and ICMR Standard Treatment Guidelines. Zero PHI.
              </p>
            </div>
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-800 border border-emerald-300 flex items-center gap-1.5">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                ICMR STG 2022 &amp; WHO AWaRe 2023
              </span>
            </div>
          </div>
        </AnimatedCard>

        <SyntheticDataNotice />

        {/* 4-Card Institutional Stewardship KPI Ribbon */}
        <AnimatedCard delay={0.08}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-clinical">
                <span className="text-[11px] font-bold uppercase tracking-wider">
                  Total Prescriptions Audited
                </span>
                <FileCheck className="h-4 w-4 text-primary" />
              </div>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-ink tabular-nums">1,420</span>
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                  +18.4% MoM
                </span>
              </div>
              <p className="mt-2 text-[11px] text-slate-clinical">
                Synthetic institutional outpatient cohort
              </p>
            </div>

            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-clinical">
                <span className="text-[11px] font-bold uppercase tracking-wider">
                  Access Class Share
                </span>
                <Activity className="h-4 w-4 text-emerald-600" />
              </div>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-ink tabular-nums">64.2%</span>
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                  Target Met (&ge;60%)
                </span>
              </div>
              <p className="mt-2 text-[11px] text-slate-clinical">
                WHO AWaRe Benchmark Target
              </p>
            </div>

            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-clinical">
                <span className="text-[11px] font-bold uppercase tracking-wider">
                  Watch Class Share
                </span>
                <Activity className="h-4 w-4 text-amber-600" />
              </div>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-ink tabular-nums">31.8%</span>
                <span className="text-[11px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                  -4.1% De-escalation
                </span>
              </div>
              <p className="mt-2 text-[11px] text-slate-clinical">
                Reduced broad-spectrum empirical exposure
              </p>
            </div>

            <div className="rounded-xl border border-border bg-surface p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-clinical">
                <span className="text-[11px] font-bold uppercase tracking-wider">
                  Safety Violations Blocked
                </span>
                <AlertTriangle className="h-4 w-4 text-urgent" />
              </div>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-urgent tabular-nums">60</span>
                <span className="text-[11px] font-bold text-urgent bg-urgent-subtle px-2 py-0.5 rounded-full border border-urgent-border">
                  100% Intercepted
                </span>
              </div>
              <p className="mt-2 text-[11px] text-slate-clinical">
                Pediatric FQs, severe renal holds &amp; banned FDCs
              </p>
            </div>
          </div>
        </AnimatedCard>

        {/* 2x2 Responsive Analytics Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top Left: AWaRe Donut Chart */}
          <AnimatedCard delay={0.1}>
            <Card className="h-full">
              <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-border/70">
                <div>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <PieChart className="h-4 w-4 text-primary" />
                    WHO AWaRe Classification Portfolio Distribution
                  </CardTitle>
                  <CardDescription className="mt-1">
                    WHO recommends &gt;60% of total antibiotic consumption be from the Access group.
                  </CardDescription>
                </div>
                <Badge variant="access">Target Met (64.2%)</Badge>
              </CardHeader>
              <CardContent className="pt-4">
                <AwarePieChart />
              </CardContent>
            </Card>
          </AnimatedCard>

          {/* Top Right: Safety Rules Horizontal Bar Chart */}
          <AnimatedCard delay={0.15}>
            <Card className="h-full">
              <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-border/70">
                <div>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <AlertTriangle className="h-4 w-4 text-urgent" />
                    Top Triggered Safety Rules
                  </CardTitle>
                  <CardDescription className="mt-1">
                    Distribution of intercepted clinical alerts by category.
                  </CardDescription>
                </div>
                <Badge variant="urgent">Safety Interceptions</Badge>
              </CardHeader>
              <CardContent className="pt-4">
                <SafetyRuleBarChart />
              </CardContent>
            </Card>
          </AnimatedCard>
        </div>

        {/* Bottom Full-Width: 6-Month AWaRe De-escalation & Optimization Trend */}
        <AnimatedCard delay={0.2}>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-border/70">
              <div>
                <CardTitle className="flex items-center gap-2 text-base">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  6-Month AWaRe De-escalation &amp; Optimization Trend
                </CardTitle>
                <CardDescription className="mt-1">
                  Institutional shift towards Access group antimicrobials and reduction in empirical Watch class exposure.
                </CardDescription>
              </div>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                +12.1% Access Growth
              </span>
            </CardHeader>
            <CardContent className="pt-4">
              <ResistanceTrendChart />
            </CardContent>
          </Card>
        </AnimatedCard>

        {/* Regulatory Conformance Matrix */}
        <AnimatedCard delay={0.25}>
          <div className="rounded-2xl border border-border bg-surface p-6 shadow-xs space-y-4">
            <h3 className="text-sm font-bold text-ink flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-primary" />
              Standard Treatment Guideline &amp; Regulatory Alignment Matrix
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="rounded-xl border border-border bg-slate-50/60 p-4 space-y-2">
                <span className="font-bold text-primary block text-sm">ICMR STG 2022</span>
                <p className="text-slate-clinical leading-relaxed">
                  Rules codified against the 2022 Indian Council of Medical Research Treatment Guidelines for common outpatient respiratory, urinary, and gastrointestinal infections.
                </p>
              </div>
              <div className="rounded-xl border border-border bg-slate-50/60 p-4 space-y-2">
                <span className="font-bold text-primary block text-sm">WHO AWaRe 2023</span>
                <p className="text-slate-clinical leading-relaxed">
                  Integrated AWaRe classification tracking for 81 generic antimicrobials. Empowers health systems to target and achieve the 60% Access threshold.
                </p>
              </div>
              <div className="rounded-xl border border-border bg-slate-50/60 p-4 space-y-2">
                <span className="font-bold text-primary block text-sm">CDSCO Banned FDC Directives</span>
                <p className="text-slate-clinical leading-relaxed">
                  Zero-tolerance detection for irrational fixed-dose combinations (such as Cefixime + Azithromycin, Ofloxacin + Ornidazole) prohibited under Indian Gazette notifications.
                </p>
              </div>
            </div>
          </div>
        </AnimatedCard>

        <DisclaimerBanner />
      </main>
    </AppLayout>
  );
}
