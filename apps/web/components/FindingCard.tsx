import React from "react";
import { AlertOctagon, AlertTriangle, BookOpen, CheckSquare, HelpCircle, Lightbulb } from "lucide-react";
import { EvidenceSource } from "./EvidenceDrawer";

export interface FindingItem {
  id: string;
  ruleId?: string;
  rule_id?: string;
  severity: "URGENT_REVIEW" | "NEEDS_REVIEW" | "DATA_GAP" | "INFO";
  title: string;
  explanation: string;
  inputFactsUsed?: Record<string, string | number | boolean>;
  input_facts_used?: Record<string, string | number | boolean>;
  missingDataStatus?: string[];
  missing_data_status?: string[];
  guidelineDiscussionPrompt?: string;
  guideline_discussion_prompt?: string;
  evidence: EvidenceSource;
  acknowledged?: boolean;
}

interface FindingCardProps {
  finding: FindingItem;
  onOpenEvidence: (evidence: EvidenceSource) => void;
  onAcknowledge?: (findingId: string) => void;
}

export function FindingCard({ finding, onOpenEvidence, onAcknowledge }: FindingCardProps) {
  const isUrgent = finding.severity === "URGENT_REVIEW";
  const isReview = finding.severity === "NEEDS_REVIEW";
  const ruleIdentifier = finding.ruleId || finding.rule_id || "AMR-RULE";
  const inputFacts = finding.inputFactsUsed || finding.input_facts_used || {};
  const prompt = finding.guidelineDiscussionPrompt || finding.guideline_discussion_prompt;
  const missingData = finding.missingDataStatus || finding.missing_data_status || [];

  return (
    <div
      className={`rounded-2xl border p-5 shadow-xs transition-all ${
        isUrgent
          ? "border-urgent-border/80 bg-urgent-subtle/25"
          : isReview
          ? "border-review-border/80 bg-review-subtle/25"
          : "border-border bg-surface"
      }`}
    >
      <div className="flex flex-col gap-3.5">
        {/* Header: Severity Badge & Rule ID */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/70 pb-3">
          <div className="flex items-center gap-2">
            {isUrgent ? (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-urgent-subtle px-3 py-1 text-xs font-bold text-urgent border border-urgent-border">
                <AlertOctagon className="h-3.5 w-3.5" />
                Urgent Clinical Concern
              </span>
            ) : isReview ? (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-review-subtle px-3 py-1 text-xs font-bold text-review border border-review-border">
                <AlertTriangle className="h-3.5 w-3.5" />
                Needs Clinical Review
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-info-subtle px-3 py-1 text-xs font-bold text-info border border-info/30">
                <HelpCircle className="h-3.5 w-3.5" />
                Data Verification
              </span>
            )}
            <span className="font-mono text-[11px] font-bold text-slate-clinical bg-white px-2 py-0.5 rounded border border-border">
              {ruleIdentifier}
            </span>
          </div>

          <button
            type="button"
            onClick={() => onOpenEvidence(finding.evidence)}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-primary hover:text-primary-hover hover:underline transition-colors"
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>View Evidence Citation</span>
          </button>
        </div>

        {/* Title & Explanation */}
        <div>
          <h4 className="text-base font-bold text-ink leading-snug">{finding.title}</h4>
          <p className="mt-1.5 text-xs leading-relaxed text-slate-clinical font-medium">
            {finding.explanation}
          </p>
        </div>

        {/* Guideline Discussion Option (Non-prescriptive prompt) */}
        {prompt && (
          <div className="rounded-xl border border-primary/25 bg-primary-subtle/30 p-3.5 text-xs">
            <div className="flex items-start gap-2.5">
              <Lightbulb className="h-4 w-4 text-primary shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-primary">Guideline Discussion Option: </span>
                <span className="text-ink font-medium">{prompt}</span>
                <p className="mt-1 text-[11px] text-slate-clinical italic">
                  *Discussion prompt only. Consult verified local hospital antibiogram before altering therapy.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Evaluated Input Facts */}
        <div className="rounded-xl bg-canvas p-3 border border-border text-xs">
          <span className="font-bold text-slate-clinical block mb-1.5 text-[10px] uppercase tracking-wider">
            Clinical Input Facts Evaluated:
          </span>
          <div className="flex flex-wrap gap-2">
            {Object.entries(inputFacts).map(([key, value]) => (
              <span
                key={key}
                className="inline-flex items-center gap-1 rounded-md bg-white px-2 py-1 border border-border text-[11px]"
              >
                <span className="text-slate-clinical font-medium">{key}:</span>
                <span className="font-bold text-ink">{String(value)}</span>
              </span>
            ))}
          </div>
        </div>

        {/* Missing Data status */}
        {missingData && missingData.length > 0 && (
          <div className="text-xs text-amber-800 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
            <strong>Data Gaps:</strong> {missingData.join(", ")}
          </div>
        )}

        {/* Clinician Acknowledgement Action */}
        <div className="flex items-center justify-between pt-2 border-t border-border/70">
          <span className="text-[11px] text-slate-clinical">
            {finding.acknowledged ? "✓ Acknowledged by clinician" : "Requires clinical review acknowledgement"}
          </span>
          {onAcknowledge && (
            <button
              type="button"
              onClick={() => onAcknowledge(finding.id)}
              disabled={finding.acknowledged}
              className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors ${
                finding.acknowledged
                  ? "bg-slate-100 text-slate-400 cursor-not-allowed"
                  : "bg-surface border border-border text-ink hover:bg-canvas shadow-xs"
              }`}
            >
              <CheckSquare className="h-3.5 w-3.5 text-primary" />
              {finding.acknowledged ? "Acknowledged" : "Acknowledge Review"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
