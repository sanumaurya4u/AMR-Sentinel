"use client";

import React from "react";
import { Navbar } from "@/components/Navbar";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { BarChart3, PieChart, TrendingUp, AlertTriangle, ShieldCheck } from "lucide-react";
import { AwarePieChart } from "@/components/charts/AwarePieChart";
import { SafetyRuleBarChart } from "@/components/charts/SafetyRuleBarChart";
import { ResistanceTrendChart } from "@/components/charts/ResistanceTrendChart";
import { AnimatedCard } from "@/components/AnimatedCard";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function InsightsPage() {
  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col">
      <Navbar />

      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-8">
        <AnimatedCard delay={0.05}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight flex items-center gap-2">
                <BarChart3 className="h-6 w-6 text-primary" />
                Institutional Antimicrobial Stewardship Analytics
              </h1>
              <p className="text-xs text-slate-clinical mt-1">
                De-identified aggregate metrics benchmarking institutional prescribing against WHO AWaRe 2023 targets and ICMR Standard Treatment Guidelines. Zero PHI.
              </p>
            </div>
            <Badge variant="access" className="self-start sm:self-auto py-1 px-3">
              ICMR STG 2022 &amp; WHO AWaRe 2023
            </Badge>
          </div>
        </AnimatedCard>

        <SyntheticDataNotice />

        {/* Top Analytics Row: Pie Chart & Safety Rules */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <AnimatedCard delay={0.1} className="lg:col-span-2">
            <Card className="h-full">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <div>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <PieChart className="h-4 w-4 text-primary" />
                    WHO AWaRe Classification Portfolio Distribution
                  </CardTitle>
                  <CardDescription>
                    WHO recommends &gt;60% of total antibiotic consumption be from the Access group.
                  </CardDescription>
                </div>
                <Badge variant="access">Target Met (64.2%)</Badge>
              </CardHeader>
              <CardContent className="pt-2">
                <AwarePieChart />
              </CardContent>
            </Card>
          </AnimatedCard>

          <AnimatedCard delay={0.15}>
            <Card className="h-full">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-base">
                  <AlertTriangle className="h-4 w-4 text-urgent" />
                  Top Triggered Safety Rules
                </CardTitle>
                <CardDescription>
                  Distribution of intercepted clinical alerts by category.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-2">
                <SafetyRuleBarChart />
              </CardContent>
            </Card>
          </AnimatedCard>
        </div>

        {/* Second Row: Historical Trend Area Chart */}
        <AnimatedCard delay={0.2}>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div>
                <CardTitle className="flex items-center gap-2 text-base">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  6-Month AWaRe De-escalation &amp; Optimization Trend
                </CardTitle>
                <CardDescription>
                  Institutional shift towards Access group antimicrobials and reduction in empirical Watch class exposure.
                </CardDescription>
              </div>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                +12.1% Access Growth
              </span>
            </CardHeader>
            <CardContent className="pt-2">
              <ResistanceTrendChart />
            </CardContent>
          </Card>
        </AnimatedCard>

        {/* Regulatory Conformance Matrix */}
        <AnimatedCard delay={0.25}>
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
        </AnimatedCard>

        <DisclaimerBanner />
      </main>
    </div>
  );
}
