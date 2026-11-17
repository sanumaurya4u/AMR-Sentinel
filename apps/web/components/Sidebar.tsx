"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutGrid,
  FilePlus,
  ShieldCheck,
  History,
  BookOpen,
  ChevronRight,
  ChevronLeft,
  Stethoscope,
} from "lucide-react";

interface SidebarProps {
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

export function Sidebar({ isCollapsed = false, onToggleCollapse }: SidebarProps) {
  const pathname = usePathname();

  const navItems = [
    {
      label: "Dashboard",
      href: "/",
      icon: LayoutGrid,
    },
    {
      label: "New Prescription",
      href: "/new-audit",
      icon: FilePlus,
    },
    {
      label: "Clinical Remediation",
      href: "/results",
      icon: ShieldCheck,
    },
    {
      label: "Prescription History",
      href: "/#history",
      icon: History,
    },
    {
      label: "Guideline Library",
      href: "/knowledge",
      icon: BookOpen,
    },
  ];

  return (
    <aside
      className={`relative hidden md:flex flex-col border-r border-slate-200/80 bg-white transition-all duration-300 z-30 shrink-0 ${
        isCollapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div className="flex h-20 items-center px-5 border-b border-slate-100">
        <Link
          href="/"
          className={`flex items-center gap-3 overflow-hidden ${
            isCollapsed ? "justify-center w-full" : ""
          }`}
          title="AMR Sentinel — Antibiotic Safety Support"
        >
          {/* Medical DNA / Leaf Emblem */}
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-50 border border-teal-100 text-primary shadow-2xs">
            <svg
              className="h-6 w-6 text-teal-700"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M2 15c6.667-6 13.333 0 20-6" />
              <path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993" />
              <path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993" />
              <path d="M17 6l3-3" />
              <path d="M14 9l5-5" />
              <path d="M7 18l-3 3" />
              <path d="M10 15l-5 5" />
            </svg>
          </div>
          {!isCollapsed && (
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-1.5">
                <span className="text-base font-bold tracking-tight text-slate-900">
                  AMR Sentinel
                </span>
                <span className="inline-block h-2 w-2 rounded-full bg-emerald-500" />
              </div>
              <p className="text-[11px] font-medium text-slate-400 truncate mt-0.5">
                Antibiotic Safety Support
              </p>
            </div>
          )}
        </Link>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 space-y-1 px-3 py-4 overflow-y-auto">
        {!isCollapsed && (
          <span className="block px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Navigation
          </span>
        )}
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            pathname === item.href ||
            (item.href !== "/" && item.href !== "/#history" && pathname.startsWith(item.href));

          return (
            <Link
              key={item.label}
              href={item.href}
              title={isCollapsed ? item.label : undefined}
              className={`flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-xs font-semibold transition-all ${
                isActive
                  ? "bg-teal-50/80 text-teal-900 font-bold border border-teal-100 shadow-2xs"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              } ${isCollapsed ? "justify-center px-2" : ""}`}
            >
              <Icon
                className={`h-4 w-4 shrink-0 ${
                  isActive ? "text-teal-700" : "text-slate-400"
                }`}
              />
              {!isCollapsed && <span className="truncate">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      {onToggleCollapse && (
        <div className="px-3 py-2 border-t border-slate-100">
          <button
            type="button"
            onClick={onToggleCollapse}
            aria-label={isCollapsed ? "Expand View" : "Collapse View"}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-slate-200/80 bg-slate-50/80 p-2 text-xs font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
          >
            {isCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <>
                <ChevronLeft className="h-4 w-4" />
                <span className="text-[11px]">Collapse View</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Doctor Profile Section at the Bottom */}
      <div className="p-3 border-t border-slate-100 bg-white">
        {!isCollapsed ? (
          <div className="flex items-center justify-between gap-2.5 rounded-xl border border-slate-200/80 bg-white p-2.5 shadow-2xs hover:border-slate-300 transition-colors">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#0F766E] text-white font-bold text-xs shadow-2xs">
                AS
              </div>
              <div className="min-w-0 flex-1">
                <span className="block text-xs font-bold text-slate-900 truncate">
                  Dr. Ananya Sharma, MD
                </span>
                <span className="flex items-center gap-1 text-[10px] text-slate-400 truncate mt-0.5">
                  <Stethoscope className="h-2.5 w-2.5 text-teal-600 shrink-0" />
                  Lead Antimicrobial Ste...
                </span>
              </div>
            </div>
            <ChevronRight className="h-4 w-4 text-slate-400 shrink-0" />
          </div>
        ) : (
          <div className="flex justify-center">
            <div
              className="flex h-9 w-9 items-center justify-center rounded-full bg-[#0F766E] text-white font-bold text-xs shadow-2xs"
              title="Dr. Ananya Sharma, MD"
            >
              AS
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
