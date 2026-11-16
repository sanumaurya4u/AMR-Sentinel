import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "urgent" | "review" | "success" | "access" | "watch" | "reserve";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants: Record<string, string> = {
    default: "border-transparent bg-primary text-white shadow-xs hover:bg-primary/80",
    secondary: "border-transparent bg-primary-subtle text-primary hover:bg-primary-subtle/80",
    destructive: "border-transparent bg-urgent text-white shadow-xs hover:bg-urgent/80",
    outline: "text-ink border-border",
    urgent: "bg-urgent-subtle text-urgent border border-urgent-border font-bold",
    review: "bg-review-subtle text-review border border-review-border font-bold",
    success: "bg-success-subtle text-success border border-success-border font-bold",
    access: "bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold",
    watch: "bg-amber-50 text-amber-700 border border-amber-300 font-bold",
    reserve: "bg-purple-50 text-purple-700 border border-purple-300 font-bold",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}

export { Badge };
