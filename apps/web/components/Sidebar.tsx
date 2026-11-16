"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ShieldAlert,
  LayoutDashboard,
  PlusCircle,
  BarChart3,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Activity,
  FileText,
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
      icon: LayoutDashboard,
      badge: "Overview",
    },
    {
      label: "New Audit",
      href: "/new-audit",
      icon: PlusCircle,
      badge: "Intake",
    },
    {
      label: "Stewardship Insights",
      href: "/insights",
      icon: BarChart3,
      badge: "Analytics",
    },
    {
      label: "Knowledge & RAG",
      href: "/knowledge",
      icon: BookOpen,
      badge: "Evidence",
    },
  ];

  return (
    <aside
      className={`relative hidden md:flex flex-col border-r border-border bg-surface transition-all duration-300 z-30 shrink-0 ${
        isCollapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        <Link
          href="/"
          className={`flex items-center gap-3 overflow-hidden ${
            isCollapsed ? "justify-center w-full" : ""
          }`}
          title="AMR Sentinel AI"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-white shadow-xs">
            <ShieldAlert className="h-6 w-6" />
          </div>
          {!isCollapsed && (
            <div className="min-w-0 flex-1">
              <span className="text-base font-bold tracking-tight text-ink flex items-center gap-1.5">
                AMR Sentinel
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-primary-subtle text-primary border border-primary/20">
                  AI
                </span>
              </span>
              <p className="text-[10px] font-semibold text-slate-clinical truncate">
                Clinical Stewardship CDSS
              </p>
            </div>
          )}
        </Link>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 space-y-1.5 p-3 overflow-y-auto">
        {!isCollapsed && (
          <span className="block px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-clinical/80">
            Clinical Modules
          </span>
        )}
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
              title={isCollapsed ? item.label : undefined}
              className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold transition-all ${
                isActive
                  ? "bg-primary text-white shadow-xs"
                  : "text-slate-clinical hover:bg-canvas hover:text-ink"
              } ${isCollapsed ? "justify-center px-2" : ""}`}
            >
              <Icon className={`h-4 w-4 shrink-0 ${isActive ? "text-white" : "text-slate-clinical"}`} />
              {!isCollapsed && (
                <div className="flex flex-1 items-center justify-between min-w-0">
                  <span className="truncate">{item.label}</span>
                  {!isActive && (
                    <span className="text-[10px] font-medium text-slate-400">
                      {item.badge}
                    </span>
                  )}
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      {onToggleCollapse && (
        <div className="p-3 border-t border-border">
          <button
            type="button"
            onClick={onToggleCollapse}
            aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-border bg-canvas/60 p-2 text-xs font-medium text-slate-clinical hover:bg-canvas hover:text-ink transition-colors"
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

      {/* Regulatory & System Status Card */}
      {!isCollapsed && (
        <div className="p-3 border-t border-border bg-slate-50/50">
          <div className="rounded-xl border border-border/80 bg-white p-3 space-y-2 shadow-2xs">
            <div className="flex items-center gap-2">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[11px] font-bold text-ink">Deterministic Core</span>
            </div>
            <p className="text-[10px] text-slate-clinical leading-relaxed">
              Rules v1.0.0-ICMR-STG-2022
              <br />
              WHO AWaRe 2023 Categorized
            </p>
            <div className="pt-1.5 border-t border-border/60 flex items-center justify-between text-[10px] text-slate-clinical">
              <span className="font-semibold text-primary flex items-center gap-1">
                <ShieldCheck className="h-3 w-3" /> Zero PHI
              </span>
              <span className="font-mono">AST-Isolated</span>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
