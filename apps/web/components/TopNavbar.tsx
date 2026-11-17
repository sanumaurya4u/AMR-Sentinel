"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Menu,
  X,
  HelpCircle,
  LayoutGrid,
  FilePlus,
  ShieldCheck,
  History,
  BookOpen,
  Wifi,
  WifiOff,
} from "lucide-react";

export function TopNavbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isBackendOnline, setIsBackendOnline] = useState<boolean>(true);

  // Real-time backend connection status check
  useEffect(() => {
    let isMounted = true;
    const checkHealth = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/health`, {
          method: "GET",
          headers: { Accept: "application/json" },
          cache: "no-store",
        });
        if (isMounted) {
          setIsBackendOnline(res.ok);
        }
      } catch {
        if (isMounted) {
          setIsBackendOnline(false);
        }
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30s polling
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const getPageTitle = () => {
    if (pathname === "/") return "Dashboard";
    if (pathname === "/new-audit") return "New Prescription Audit";
    if (pathname === "/results") return "Clinical Remediation";
    if (pathname === "/insights") return "Stewardship Insights";
    if (pathname === "/knowledge") return "Guideline Library";
    return "Clinical Decision Support";
  };

  const navItems = [
    { label: "Dashboard", href: "/", icon: LayoutGrid },
    { label: "New Prescription", href: "/new-audit", icon: FilePlus },
    { label: "Clinical Remediation", href: "/results", icon: ShieldCheck },
    { label: "Prescription History", href: "/#history", icon: History },
    { label: "Guideline Library", href: "/knowledge", icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/95 backdrop-blur-xs">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left: Mobile Toggle & Page Title */}
        <div className="flex items-center gap-3">
          {/* Mobile hamburger menu button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900 focus:outline-hidden"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>

          {/* Current Page Title matching Reference Screenshot */}
          <h1 className="text-sm sm:text-base font-bold text-slate-800 tracking-tight">
            {getPageTitle()}
          </h1>
        </div>

        {/* Right: Live Clinical API, Help Icon & Doctor Profile */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* Live Clinical API Status Indicator */}
          {isBackendOnline ? (
            <div
              className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 border border-emerald-200 shadow-2xs"
              title="Clinical CDS Rules Engine online & verified"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span>Live Clinical API</span>
            </div>
          ) : (
            <div
              className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700 border border-amber-200 shadow-2xs"
              title="Clinical Server connection pending. Operating in resilient offline mode."
            >
              <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
              <span>Offline Mode</span>
            </div>
          )}

          {/* Help Icon */}
          <button
            type="button"
            className="text-slate-400 hover:text-slate-600 p-1 rounded-full transition-colors focus:outline-hidden"
            title="Guideline Documentation & Help"
            onClick={() => window.open("https://main.icmr.nic.in/", "_blank")}
          >
            <HelpCircle className="h-4 w-4" />
          </button>

          {/* Doctor Profile & Name */}
          <div className="flex items-center gap-2 pl-1 border-l border-slate-200">
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#0F766E] text-white font-bold text-xs shadow-2xs">
              AS
            </div>
            <span className="text-xs font-semibold text-slate-800 hidden sm:inline">
              Dr. Ananya Sharma
            </span>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white p-4 shadow-lg animate-in slide-in-from-top-2 duration-150">
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive =
                pathname === item.href ||
                (item.href !== "/" && item.href !== "/#history" && pathname.startsWith(item.href));

              return (
                <Link
                  key={item.label}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-xs font-semibold transition-all ${
                    isActive
                      ? "bg-teal-50 text-teal-800 font-bold border border-teal-100"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </header>
  );
}
