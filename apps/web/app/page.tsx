"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Activity,
  Plus,
  History,
  RotateCw,
  Info,
  FileCheck,
  ShieldCheck,
  AlertCircle,
  ShieldAlert,
  PieChart as PieChartIcon,
  BarChart2,
  FileText,
  ArrowRight,
  ExternalLink,
  ChevronRight,
  CheckCircle2,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { AppLayout } from "@/components/AppLayout";
import { DisclaimerBanner, SyntheticDataNotice } from "@/components/DisclaimerBanner";
import { SYNTHETIC_SAMPLE_CASES, SyntheticCase } from "@/lib/sample-cases";

// WHO AWaRe Donut Data matching Screenshot 1 & 2
const awareDonutData = [
  { name: "Access (First-Line)", value: 64.2, color: "#0F766E" },
  { name: "Watch (Caution)", value: 31.8, color: "#F59E0B" },
  { name: "Reserve (Last Resort)", value: 4.0, color: "#E11D48" },
];

// Weekly Prescription Safety Outcomes Data matching Screenshot 1 & 2
const weeklyOutcomesData = [
  { day: "Mon", approved: 24, needsReview: 5, blocked: 2 },
  { day: "Tue", approved: 28, needsReview: 7, blocked: 3 },
  { day: "Wed", approved: 32, needsReview: 4, blocked: 1 },
  { day: "Thu", approved: 27, needsReview: 6, blocked: 2 },
  { day: "Fri", approved: 35, needsReview: 8, blocked: 3 },
  { day: "Sat", approved: 18, needsReview: 3, blocked: 1 },
];

export default function DashboardPage() {
  const [isMounted, setIsMounted] = useState<boolean>(false);
  const [isBackendOnline, setIsBackendOnline] = useState<boolean>(true);
  const [isCheckingBackend, setIsCheckingBackend] = useState<boolean>(false);
  const [showSimulatedOffline, setShowSimulatedOffline] = useState<boolean>(false);
  const [showDemonstrationLedger, setShowDemonstrationLedger] = useState<boolean>(false);
  const [refreshKey, setRefreshKey] = useState<number>(0);

  // Check live backend connection status
  const checkBackendHealth = async () => {
    setIsCheckingBackend(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/health`, {
        method: "GET",
        headers: { Accept: "application/json" },
        cache: "no-store",
      });
      setIsBackendOnline(res.ok);
    } catch {
      setIsBackendOnline(false);
    } finally {
      setIsCheckingBackend(false);
    }
  };

  useEffect(() => {
    setIsMounted(true);
    checkBackendHealth();
  }, []);

  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1);
    checkBackendHealth();
  };

  const isServerOffline = !isBackendOnline || showSimulatedOffline;

  return (
    <AppLayout>
      <div className="min-h-screen bg-[#F0F4F8] py-6 px-4 sm:px-6 lg:px-8">
        <main className="max-w-7xl mx-auto w-full space-y-6">
          {/* 1. DASHBOARD HEADER CARD */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-xs transition-all">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
              {/* Left: Icon, Title & Subtitle */}
              <div className="flex items-start sm:items-center gap-3.5 sm:gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-teal-50 border border-teal-100/80 text-[#0F766E] shadow-2xs">
                  <Activity className="h-6 w-6 text-[#0F766E]" />
                </div>
                <div>
                  <div className="flex flex-wrap items-center gap-2.5">
                    <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                      Clinical Antimicrobial Dashboard
                    </h1>
                    <span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 border border-emerald-200 shadow-2xs">
                      Active Monitoring
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-500 mt-1 leading-relaxed">
                    Overview of outpatient antibiotic prescriptions, guideline safety checks, and stewardship adherence.
                  </p>
                </div>
              </div>

              {/* Right: Actions */}
              <div className="flex flex-wrap items-center gap-2.5 shrink-0">
                <Link
                  href="/new-audit"
                  className="inline-flex items-center justify-center gap-1.5 rounded-xl bg-[#0F766E] px-4 py-2.5 text-xs sm:text-sm font-bold text-white shadow-xs hover:bg-[#0D655E] transition-all"
                >
                  <Plus className="h-4 w-4" />
                  <span>New Prescription</span>
                </Link>
                <Link
                  href="/#history"
                  onClick={() => setShowDemonstrationLedger(true)}
                  className="inline-flex items-center justify-center gap-1.5 rounded-xl border border-slate-200/90 bg-white px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-2xs"
                >
                  <History className="h-4 w-4 text-slate-500" />
                  <span>Audit History</span>
                </Link>
                <button
                  type="button"
                  onClick={handleRefresh}
                  disabled={isCheckingBackend}
                  className="inline-flex items-center justify-center p-2.5 rounded-xl border border-slate-200/90 bg-white text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors shadow-2xs focus:outline-hidden"
                  title="Refresh clinical metrics & connection"
                >
                  <RotateCw className={`h-4 w-4 ${isCheckingBackend ? "animate-spin text-[#0F766E]" : ""}`} />
                </button>
              </div>
            </div>
          </div>

          {/* 2. SERVER CONNECTION NOTICE (matching Screenshot 1) */}
          {isServerOffline && (
            <div className="rounded-2xl border border-amber-200/90 bg-[#FEFCE8] p-4 shadow-2xs animate-in fade-in duration-200">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start sm:items-center gap-3">
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-amber-100 text-amber-700 mt-0.5 sm:mt-0">
                    <Info className="h-4 w-4" />
                  </div>
                  <div>
                    <span className="text-xs sm:text-sm font-bold text-amber-950 block">
                      Clinical Server Connection Notice
                    </span>
                    <span className="text-xs text-amber-800/90 block mt-0.5 leading-relaxed">
                      Could not reach the AMR Sentinel decision support server. The system is operating in resilient offline mode.
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2 self-start sm:self-center shrink-0">
                  <button
                    type="button"
                    onClick={checkBackendHealth}
                    disabled={isCheckingBackend}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-amber-300 bg-white px-3 py-1.5 text-xs font-semibold text-amber-950 hover:bg-amber-50 transition-colors shadow-2xs"
                  >
                    <RotateCw className={`h-3.5 w-3.5 ${isCheckingBackend ? "animate-spin" : ""}`} />
                    <span>Retry</span>
                  </button>
                  {showSimulatedOffline && (
                    <button
                      type="button"
                      onClick={() => setShowSimulatedOffline(false)}
                      className="text-[11px] text-amber-700 hover:underline px-1"
                    >
                      Dismiss Preview
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Optional Developer / Auditor Banner Simulator Toggle */}
          {!isServerOffline && (
            <div className="flex justify-end">
              <button
                type="button"
                onClick={() => setShowSimulatedOffline(true)}
                className="text-[11px] font-medium text-slate-400 hover:text-slate-600 transition-colors"
                title="Preview the offline server connection notice banner"
              >
                Simulate Offline Banner Notice
              </button>
            </div>
          )}

          {/* 3. KPI SUMMARY CARDS (matching Screenshot 1) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Card 1: TOTAL PRESCRIPTIONS */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                  Total Prescriptions
                </span>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-teal-50 border border-teal-100 text-[#0F766E]">
                  <FileCheck className="h-5 w-5 text-[#0F766E]" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-extrabold text-slate-900 tabular-nums">
                  42
                </span>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  All cases checked
                </p>
              </div>
            </div>

            {/* Card 2: APPROVED & SAFE */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                  Approved &amp; Safe
                </span>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-sky-50 border border-sky-100 text-sky-600">
                  <ShieldCheck className="h-5 w-5 text-sky-600" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-extrabold text-slate-900 tabular-nums">
                  6
                </span>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  Guideline compliant
                </p>
              </div>
            </div>

            {/* Card 3: NEEDS DOCTOR REVIEW */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                  Needs Doctor Review
                </span>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-amber-50 border border-amber-100 text-amber-600">
                  <AlertCircle className="h-5 w-5 text-amber-600" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-extrabold text-slate-900 tabular-nums">
                  18
                </span>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  Dosage or duration flagged
                </p>
              </div>
            </div>

            {/* Card 4: HIGH RISK (BLOCKED) */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                  High Risk (Blocked)
                </span>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-rose-50 border border-rose-100 text-rose-600">
                  <ShieldAlert className="h-5 w-5 text-rose-600" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-extrabold text-slate-900 tabular-nums">
                  18
                </span>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  Unsafe antibiotics intercepted
                </p>
              </div>
            </div>
          </div>

          {/* 4. ANTIBIOTIC SAFETY & USAGE TRENDS */}
          <section className="space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-800">
                  Antibiotic Safety &amp; Usage Trends
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  WHO AWaRe group distribution and weekly safety outcomes
                </p>
              </div>
              <span className="self-start sm:self-center inline-flex items-center rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800 border border-emerald-200 shadow-2xs">
                ICMR &amp; WHO Guidelines
              </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Card A: Antibiotic Group Breakdown (WHO AWaRe) */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-xs flex flex-col justify-between">
                <div className="flex items-start justify-between gap-3 border-b border-slate-100 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-teal-50 border border-teal-100 text-[#0F766E]">
                      <PieChartIcon className="h-4 w-4 text-[#0F766E]" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">
                        Antibiotic Group Breakdown (WHO AWaRe)
                      </h3>
                      <p className="text-[11px] text-slate-500 mt-0.5">
                        Global guideline target: At least 60% should be safe first-line (Access) antibiotics
                      </p>
                    </div>
                  </div>
                  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-bold text-emerald-700 border border-emerald-200 shrink-0">
                    <CheckCircle2 className="h-3 w-3 text-emerald-600" />
                    100% Target Met
                  </span>
                </div>

                {/* Donut Chart */}
                <div className="py-6 flex items-center justify-center">
                  {isMounted ? (
                    <div className="h-48 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={awareDonutData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={88}
                            paddingAngle={2}
                            dataKey="value"
                            stroke="#FFFFFF"
                            strokeWidth={3}
                          >
                            {awareDonutData.map((entry) => (
                              <Cell key={entry.name} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip
                            formatter={(value: any) => [`${value}%`, "Share"]}
                            contentStyle={{
                              backgroundColor: "#FFFFFF",
                              border: "1px solid #E2E8F0",
                              borderRadius: "12px",
                              fontSize: "12px",
                              fontWeight: "600",
                              color: "#0F172A",
                              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
                            }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="h-48 w-48 rounded-full border-8 border-teal-600 border-t-amber-500 border-r-rose-600 animate-pulse" />
                  )}
                </div>

                {/* Legends */}
                <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 pt-3 border-t border-slate-100 text-xs font-medium text-slate-700">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#0F766E]" />
                    <span>Access (First-Line)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#E11D48]" />
                    <span>Reserve (Last Resort)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#F59E0B]" />
                    <span>Watch (Caution)</span>
                  </div>
                </div>
              </div>

              {/* Card B: Weekly Prescription Safety Outcomes */}
              <div className="rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-xs flex flex-col justify-between">
                <div className="flex items-start justify-between gap-3 border-b border-slate-100 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-sky-50 border border-sky-100 text-sky-600">
                      <BarChart2 className="h-4 w-4 text-sky-600" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">
                        Weekly Prescription Safety Outcomes
                      </h3>
                      <p className="text-[11px] text-slate-500 mt-0.5">
                        Number of prescriptions approved, flagged for review, or blocked this week
                      </p>
                    </div>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600 shrink-0">
                    Past 6 Days
                  </span>
                </div>

                {/* Grouped Bar Chart */}
                <div className="py-4">
                  {isMounted ? (
                    <div className="h-52 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={weeklyOutcomesData}
                          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                        >
                          <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                            stroke="#E2E8F0"
                          />
                          <XAxis
                            dataKey="day"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#64748B", fontSize: 11, fontWeight: 500 }}
                          />
                          <YAxis
                            ticks={[0, 9, 18, 27, 36]}
                            domain={[0, 36]}
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#64748B", fontSize: 11 }}
                          />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "#FFFFFF",
                              border: "1px solid #E2E8F0",
                              borderRadius: "12px",
                              fontSize: "12px",
                              fontWeight: "600",
                              color: "#0F172A",
                              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
                            }}
                          />
                          <Bar
                            dataKey="approved"
                            name="Approved & Safe"
                            fill="#0F766E"
                            radius={[4, 4, 0, 0]}
                            maxBarSize={16}
                          />
                          <Bar
                            dataKey="needsReview"
                            name="Needs Review"
                            fill="#F59E0B"
                            radius={[4, 4, 0, 0]}
                            maxBarSize={16}
                          />
                          <Bar
                            dataKey="blocked"
                            name="High Risk (Blocked)"
                            fill="#E11D48"
                            radius={[4, 4, 0, 0]}
                            maxBarSize={16}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="h-52 w-full bg-slate-50 animate-pulse rounded-xl" />
                  )}
                </div>

                {/* Legends */}
                <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 pt-3 border-t border-slate-100 text-xs font-medium text-slate-700">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#0F766E]" />
                    <span>Approved &amp; Safe</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#E11D48]" />
                    <span>High Risk (Blocked)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#F59E0B]" />
                    <span>Needs Review</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 5. RECENT PRESCRIPTIONS (matching Screenshot 2 & Dynamic Toggle) */}
          <section id="history" className="space-y-3 pt-2">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-800">
                  Recent Prescriptions
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Click &ldquo;View Details&rdquo; on any prescription to see its full safety audit and recommendations
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowDemonstrationLedger((prev) => !prev)}
                className="text-xs font-bold text-[#0F766E] hover:text-[#0D655E] inline-flex items-center gap-1 transition-colors"
              >
                <span>{showDemonstrationLedger ? "Hide Ledger" : "View Full History"}</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            </div>

            {/* View State: Empty State vs. Historical/Demonstration Case Ledger */}
            {!showDemonstrationLedger ? (
              /* CLEAN EMPTY STATE (exact replica of Screenshot 2) */
              <div className="rounded-2xl border border-slate-200/80 bg-white p-10 sm:p-14 text-center shadow-xs transition-all">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-50 border border-teal-100/80 text-[#0F766E] mx-auto shadow-2xs">
                  <FileText className="h-7 w-7 text-[#0F766E]" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-4 tracking-tight">
                  No Prescriptions Checked Yet Today
                </h3>
                <p className="text-xs text-slate-500 max-w-md mx-auto mt-1 leading-relaxed">
                  Prescriptions you create and evaluate with the clinical safety engine will appear here in real-time.
                </p>
                <div className="mt-5 flex flex-col sm:flex-row items-center justify-center gap-3">
                  <Link
                    href="/new-audit"
                    className="inline-flex items-center gap-1.5 rounded-xl bg-[#0F766E] px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-[#0D655E] transition-all"
                  >
                    <Plus className="h-4 w-4" />
                    <span>New Prescription Intake</span>
                  </Link>
                  <button
                    type="button"
                    onClick={() => setShowDemonstrationLedger(true)}
                    className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors shadow-2xs"
                  >
                    <History className="h-3.5 w-3.5 text-slate-500" />
                    <span>Inspect Golden Demonstration Cases (6)</span>
                  </button>
                </div>
              </div>
            ) : (
              /* POPULATED AUDIT TABLE (Interactive Verification Ledger) */
              <div className="rounded-2xl border border-slate-200/80 bg-white shadow-xs overflow-hidden transition-all animate-in fade-in duration-150">
                <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                  <span className="text-xs font-bold text-slate-700">
                    Synthetic Demonstration Ledger (6 Verified ICMR Cases)
                  </span>
                  <button
                    type="button"
                    onClick={() => setShowDemonstrationLedger(false)}
                    className="text-xs text-slate-500 hover:text-slate-800 font-medium"
                  >
                    Show Empty State
                  </button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-50/80 text-[11px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200/70">
                      <tr>
                        <th className="px-5 py-3">Case ID</th>
                        <th className="px-5 py-3">Patient Context</th>
                        <th className="px-5 py-3">Suspected Indication</th>
                        <th className="px-5 py-3">Prescribed Regimen</th>
                        <th className="px-5 py-3">Audit Outcome</th>
                        <th className="px-5 py-3 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {SYNTHETIC_SAMPLE_CASES.map((c) => {
                        const isUrgent = c.expectedStatus === "NEEDS_URGENT_REVIEW";
                        const isReview = c.expectedStatus === "NEEDS_REVIEW";
                        const isGaps = c.expectedStatus === "INCOMPLETE_DATA";
                        const isSafe = c.expectedStatus === "NO_RULE_TRIGGERED";

                        return (
                          <tr key={c.id} className="hover:bg-slate-50/60 transition-colors">
                            <td className="px-5 py-3.5 font-mono text-[11px] font-bold text-slate-900">
                              {c.id}
                            </td>
                            <td className="px-5 py-3.5 text-slate-600 font-medium">
                              {c.patientContext.ageYears}y
                              {c.patientContext.weightKg ? ` • ${c.patientContext.weightKg}kg` : ""} •{" "}
                              {c.patientContext.gender}
                            </td>
                            <td className="px-5 py-3.5 font-semibold text-slate-800">
                              {c.indicationName}
                            </td>
                            <td className="px-5 py-3.5 text-slate-700 font-medium">
                              {c.prescriptionLines.map((l) => `${l.drugName} ${l.doseText}`).join(", ")}
                            </td>
                            <td className="px-5 py-3.5">
                              {isUrgent && (
                                <span className="inline-flex items-center gap-1 rounded-full bg-rose-50 px-2.5 py-0.5 text-[11px] font-bold text-rose-700 border border-rose-200">
                                  <ShieldAlert className="h-3 w-3 text-rose-600" />
                                  High Risk (Blocked)
                                </span>
                              )}
                              {isReview && (
                                <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-0.5 text-[11px] font-bold text-amber-800 border border-amber-200">
                                  <AlertCircle className="h-3 w-3 text-amber-600" />
                                  Needs Review
                                </span>
                              )}
                              {isGaps && (
                                <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2.5 py-0.5 text-[11px] font-bold text-blue-800 border border-blue-200">
                                  <Info className="h-3 w-3 text-blue-600" />
                                  Data Gap Hold
                                </span>
                              )}
                              {isSafe && (
                                <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800 border border-emerald-200">
                                  <ShieldCheck className="h-3 w-3 text-emerald-600" />
                                  Approved &amp; Safe
                                </span>
                              )}
                            </td>
                            <td className="px-5 py-3.5 text-right">
                              <Link
                                href={`/new-audit?case=${c.id}`}
                                className="inline-flex items-center gap-1 text-xs font-bold text-[#0F766E] hover:text-[#0D655E] transition-colors"
                              >
                                <span>View Details</span>
                                <ChevronRight className="h-3.5 w-3.5" />
                              </Link>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>

          {/* Persistent Disclaimers & Synthetic Data Notice */}
          <div className="pt-4 space-y-4">
            <SyntheticDataNotice />
            <DisclaimerBanner />
          </div>
        </main>
      </div>
    </AppLayout>
  );
}
