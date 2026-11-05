import React from "react";
import { AlertOctagon, AlertTriangle, CheckCircle2, HelpCircle, XCircle } from "lucide-react";

export type AuditStatus =
  | "NEEDS_URGENT_REVIEW"
  | "NEEDS_REVIEW"
  | "NO_RULE_TRIGGERED"
  | "INCOMPLETE_DATA"
  | "UNAVAILABLE";

interface StatusBadgeProps {
  status: AuditStatus;
  size?: "sm" | "md" | "lg";
}

export function StatusBadge({ status, size = "md" }: StatusBadgeProps) {
  const configs: Record<
    AuditStatus,
    { label: string; bg: string; text: string; border: string; icon: React.ReactNode }
  > = {
    NEEDS_URGENT_REVIEW: {
      label: "Needs Urgent Review",
      bg: "bg-urgent-subtle",
      text: "text-urgent",
      border: "border-urgent-border",
      icon: <AlertOctagon className={size === "lg" ? "h-5 w-5" : "h-4 w-4"} />,
    },
    NEEDS_REVIEW: {
      label: "Needs Clinical Review",
      bg: "bg-review-subtle",
      text: "text-review",
      border: "border-review-border",
      icon: <AlertTriangle className={size === "lg" ? "h-5 w-5" : "h-4 w-4"} />,
    },
    NO_RULE_TRIGGERED: {
      label: "No Rule Triggered",
      bg: "bg-success-subtle",
      text: "text-success",
      border: "border-success-border",
      icon: <CheckCircle2 className={size === "lg" ? "h-5 w-5" : "h-4 w-4"} />,
    },
    INCOMPLETE_DATA: {
      label: "Incomplete Clinical Data",
      bg: "bg-info-subtle",
      text: "text-info",
      border: "border-info/30",
      icon: <HelpCircle className={size === "lg" ? "h-5 w-5" : "h-4 w-4"} />,
    },
    UNAVAILABLE: {
      label: "Service Unavailable",
      bg: "bg-slate-100",
      text: "text-slate-clinical",
      border: "border-slate-300",
      icon: <XCircle className={size === "lg" ? "h-5 w-5" : "h-4 w-4"} />,
    },
  };

  const current = configs[status] || configs.UNAVAILABLE;

  const sizeClasses = {
    sm: "px-2.5 py-0.5 text-xs gap-1.5",
    md: "px-3 py-1 text-xs font-semibold gap-2",
    lg: "px-4 py-2 text-sm font-bold gap-2.5",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border ${current.bg} ${current.text} ${current.border} ${sizeClasses[size]}`}
    >
      {current.icon}
      <span>{current.label}</span>
    </span>
  );
}
