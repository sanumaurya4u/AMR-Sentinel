import React from "react";
import { Navbar } from "@/components/Navbar";
import { PrescriptionStepper } from "@/components/PrescriptionStepper";

export default function NewAuditPage() {
  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col">
      <Navbar />

      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-ink tracking-tight">New Prescription Audit</h1>
          <p className="text-xs text-slate-clinical mt-1">
            Deterministic clinical antimicrobial stewardship second-check grounded in ICMR STG 2022 &amp; WHO AWaRe 2023.
          </p>
        </div>

        <PrescriptionStepper />
      </main>
    </div>
  );
}
