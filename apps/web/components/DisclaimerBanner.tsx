import React from "react";
import { Info, ShieldAlert } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <div className="rounded-lg border border-border bg-slate-50/80 p-3.5 text-xs text-slate-clinical">
      <div className="flex items-start gap-2.5">
        <ShieldAlert className="h-4 w-4 text-primary shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-ink">
            Clinical Decision Support Prototype — Not Autonomous Prescription or Diagnosis
          </p>
          <p className="leading-relaxed">
            AMR Sentinel AI audits antibiotic prescriptions against ICMR Standard Treatment Guidelines 2022 and WHO AWaRe 2023. A status of &quot;No Rule Triggered&quot; indicates that configured safety and stewardship rules were not breached; it does not constitute clinical validation, medical clearance, or dosage approval. Prescribers retain sole clinical responsibility.
          </p>
        </div>
      </div>
    </div>
  );
}

export function SyntheticDataNotice() {
  return (
    <div className="flex items-center gap-2 rounded-md bg-amber-50 px-3 py-1.5 text-xs text-amber-800 border border-amber-200">
      <Info className="h-3.5 w-3.5 shrink-0 text-amber-600" />
      <span>
        <strong>Synthetic Demonstration Mode:</strong> All patient demographics, prescription orders, and scenarios are 100% synthetic for evaluation. Zero real PHI is stored or processed.
      </span>
    </div>
  );
}
