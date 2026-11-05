import React from "react";
import { AlertCircle } from "lucide-react";

interface DataGapCalloutProps {
  missingFields: string[];
  clinicalImpact?: string;
}

export function DataGapCallout({ missingFields, clinicalImpact }: DataGapCalloutProps) {
  if (!missingFields || missingFields.length === 0) return null;

  return (
    <div className="rounded-lg border border-info/30 bg-info-subtle p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="h-5 w-5 text-info shrink-0 mt-0.5" />
        <div className="space-y-1.5 text-xs text-ink">
          <h4 className="font-semibold text-info flex items-center gap-1.5">
            Clinical Data Gaps Identified ({missingFields.length})
          </h4>
          <p className="text-slate-clinical">
            Deterministic safety evaluation requires explicit confirmation. Missing parameters cannot be assumed normal:
          </p>
          <ul className="list-disc pl-5 space-y-0.5 text-slate-clinical">
            {missingFields.map((field, idx) => (
              <li key={idx} className="font-medium text-ink">
                {field}
              </li>
            ))}
          </ul>
          {clinicalImpact && (
            <p className="mt-2 text-[11px] italic text-slate-clinical border-t border-info/20 pt-1.5">
              Impact: {clinicalImpact}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
