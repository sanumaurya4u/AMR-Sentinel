"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Menu,
  X,
  ShieldAlert,
  Sparkles,
  Stethoscope,
  ChevronRight,
  LayoutDashboard,
  PlusCircle,
  BarChart3,
  BookOpen,
  Building2,
  CheckCircle2,
} from "lucide-react";

export function TopNavbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Dynamic breadcrumb mapping
  const getBreadcrumbs = () => {
    if (pathname === "/") {
      return [{ label: "Clinical Dashboard", href: "/" }];
    }
    if (pathname === "/new-audit") {
      return [
        { label: "Dashboard", href: "/" },
        { label: "New Prescription Audit", href: "/new-audit" },
      ];
    }
    if (pathname === "/results") {
      return [
        { label: "Dashboard", href: "/" },
        { label: "Audit Intake", href: "/new-audit" },
        { label: "Audit Findings & Report", href: "/results" },
      ];
    }
    if (pathname === "/insights") {
      return [
        { label: "Dashboard", href: "/" },
        { label: "Stewardship Insights & Analytics", href: "/insights" },
      ];
    }
    if (pathname === "/knowledge") {
      return [
        { label: "Dashboard", href: "/" },
        { label: "Clinical Knowledge & Evidence RAG", href: "/knowledge" },
      ];
    }
    return [{ label: "Clinical Workspace", href: "/" }];
  };

  const breadcrumbs = getBreadcrumbs();

  const navItems = [
    { label: "Dashboard", href: "/", icon: LayoutDashboard },
    { label: "New Audit", href: "/new-audit", icon: PlusCircle },
    { label: "Stewardship Insights", href: "/insights", icon: BarChart3 },
    { label: "Knowledge & RAG", href: "/knowledge", icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-surface/95 backdrop-blur-xs shadow-2xs">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left: Mobile Toggle & Breadcrumbs */}
        <div className="flex items-center gap-3">
          {/* Mobile menu button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden rounded-lg p-2 text-slate-clinical hover:bg-canvas hover:text-ink focus:outline-hidden"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>

          {/* Mobile brand fallback */}
          <Link href="/" className="md:hidden flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-white">
              <ShieldAlert className="h-5 w-5" />
            </div>
            <span className="font-bold text-sm text-ink">AMR Sentinel</span>
          </Link>

          {/* Desktop Breadcrumbs */}
          <nav aria-label="Breadcrumb" className="hidden sm:flex items-center gap-1.5 text-xs text-slate-clinical">
            {breadcrumbs.map((crumb, idx) => (
              <React.Fragment key={crumb.href + idx}>
                {idx > 0 && <ChevronRight className="h-3 w-3 text-slate-300" />}
                {idx === breadcrumbs.length - 1 ? (
                  <span className="font-bold text-ink truncate max-w-xs sm:max-w-md">
                    {crumb.label}
                  </span>
                ) : (
                  <Link
                    href={crumb.href}
                    className="hover:text-primary transition-colors truncate max-w-[120px]"
                  >
                    {crumb.label}
                  </Link>
                )}
              </React.Fragment>
            ))}
          </nav>
        </div>

        {/* Right: Demo Persona, Regulatory Badges & Primary CTA */}
        <div className="flex items-center gap-2.5 sm:gap-3">
          {/* Regulatory Guideline Badge */}
          <div className="hidden xl:flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-[11px] font-semibold text-emerald-800 border border-emerald-200">
            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
            <span>ICMR STG 2022 • WHO AWaRe 2023</span>
          </div>

          {/* Clinician Persona Pill */}
          <div className="flex items-center gap-2 rounded-xl border border-border bg-canvas/80 px-2.5 sm:px-3 py-1.5 text-xs">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <Stethoscope className="h-3.5 w-3.5 text-primary shrink-0" />
            <div className="flex flex-col sm:flex-row sm:items-center sm:gap-1.5 text-[11px]">
              <span className="font-bold text-ink">Dr. Ayesha</span>
              <span className="hidden sm:inline text-slate-clinical">(General Physician)</span>
            </div>
          </div>

          {/* Primary Action Button (hidden on new-audit to prevent redundancy) */}
          {pathname !== "/new-audit" && (
            <Link
              href="/new-audit"
              className="inline-flex items-center gap-1.5 rounded-xl bg-primary px-3 sm:px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-primary-hover transition-colors"
            >
              <Sparkles className="h-3.5 w-3.5" />
              <span>New Audit</span>
            </Link>
          )}
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-border bg-surface p-4 shadow-lg animate-in slide-in-from-top-2 duration-150">
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive =
                pathname === item.href ||
                (item.href !== "/" && pathname.startsWith(item.href)) ||
                (item.href === "/new-audit" && pathname === "/results");

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs font-semibold ${
                    isActive
                      ? "bg-primary text-white"
                      : "text-slate-clinical hover:bg-canvas hover:text-ink"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="mt-4 pt-3 border-t border-border flex items-center justify-between text-[11px] text-slate-clinical">
            <span className="flex items-center gap-1 font-semibold text-primary">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
              ICMR STG 2022 Concordant
            </span>
            <span className="rounded bg-slate-100 px-2 py-0.5 font-mono text-[10px]">
              v1.0.0-ICMR
            </span>
          </div>
        </div>
      )}
    </header>
  );
}
