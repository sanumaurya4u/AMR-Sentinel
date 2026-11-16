"use client";

import React from "react";
import Link from "next/link";
import { ShieldAlert, PlusCircle, LayoutDashboard, BarChart3, Stethoscope, Sparkles, BookOpen } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-surface shadow-xs">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-white shadow-xs group-hover:bg-primary-hover transition-colors">
              <ShieldAlert className="h-6 w-6" />
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-ink flex items-center gap-1.5">
                AMR Sentinel <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-primary-subtle text-primary border border-primary/20">AI</span>
              </span>
              <p className="text-[11px] font-medium text-slate-clinical">Prescription Stewardship Audit</p>
            </div>
          </Link>
        </div>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 text-sm font-medium text-slate-clinical">
          <Link
            href="/"
            className="flex items-center gap-1.5 px-3 py-2 rounded-md hover:text-ink hover:bg-canvas transition-colors"
          >
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </Link>
          <Link
            href="/new-audit"
            className="flex items-center gap-1.5 px-3 py-2 rounded-md hover:text-ink hover:bg-canvas transition-colors"
          >
            <PlusCircle className="h-4 w-4" />
            New Audit
          </Link>
          <Link
            href="/insights"
            className="flex items-center gap-1.5 px-3 py-2 rounded-md hover:text-ink hover:bg-canvas transition-colors"
          >
            <BarChart3 className="h-4 w-4" />
            Stewardship Insights
          </Link>
          <Link
            href="/knowledge"
            className="flex items-center gap-1.5 px-3 py-2 rounded-md hover:text-ink hover:bg-canvas transition-colors"
          >
            <BookOpen className="h-4 w-4" />
            Knowledge &amp; RAG
          </Link>
        </nav>

        {/* Demo Mode Persona & Quick Action */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border bg-canvas text-xs">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <Stethoscope className="h-3.5 w-3.5 text-primary" />
            <span className="font-medium text-ink">Demo: Dr. Ayesha</span>
            <span className="text-slate-clinical">(General Physician)</span>
          </div>

          <Link
            href="/new-audit"
            className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-3.5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-primary-hover transition-colors"
          >
            <Sparkles className="h-3.5 w-3.5" />
            Start Audit
          </Link>
        </div>
      </div>
    </header>
  );
}
