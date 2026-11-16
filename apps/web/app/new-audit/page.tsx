import React from "react";
import { AppLayout } from "@/components/AppLayout";
import { PrescriptionStepper } from "@/components/PrescriptionStepper";
import { DisclaimerBanner } from "@/components/DisclaimerBanner";
import { Sparkles, ShieldCheck } from "lucide-react";

export default function NewAuditPage() {
  return (
    <AppLayout>
      <main className="py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border pb-4">
          <div>
            <h1 className="text-2xl font-bold text-ink tracking-tight flex items-center gap-2">
              <Sparkles className="h-6 w-6 text-primary" />
              New Prescription Audit
            </h1>
            <p className="text-xs text-slate-clinical mt-1">
              Review antibiotic prescriptions against configured patient-safety and antimicrobial stewardship rules. Grounded in ICMR STG 2022 &amp; WHO AWaRe 2023.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-primary-subtle px-3 py-1 font-mono text-[11px] font-semibold text-primary border border-primary/20 flex items-center gap-1.5">
              <ShieldCheck className="h-3.5 w-3.5" />
              Pure Deterministic Engine
            </span>
          </div>
        </div>

        <PrescriptionStepper />

        <DisclaimerBanner />
      </main>
    </AppLayout>
  );
}
