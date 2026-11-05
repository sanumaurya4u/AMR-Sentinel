import React from "react";
import { X, BookOpen, ExternalLink, Calendar, MapPin, Building2, CheckCircle2 } from "lucide-react";

export interface EvidenceSource {
  id: string;
  title: string;
  publisher: string;
  jurisdiction: string;
  publishedOn: string;
  sectionRef: string;
  excerpt: string;
  url?: string;
}

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  evidence: EvidenceSource | null;
  ruleSetVersion: string;
}

export function EvidenceDrawer({ isOpen, onClose, evidence, ruleSetVersion }: EvidenceDrawerProps) {
  if (!isOpen || !evidence) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-xs transition-opacity">
      <div className="relative flex h-full w-full max-w-lg flex-col bg-surface shadow-2xl border-l border-border animate-in slide-in-from-right duration-200">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border px-6 py-4">
          <div className="flex items-center gap-2 text-ink">
            <BookOpen className="h-5 w-5 text-primary" />
            <h3 className="text-base font-bold">Evidence Provenance</h3>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-clinical hover:bg-canvas hover:text-ink transition-colors"
            aria-label="Close evidence drawer"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 text-sm">
          {/* Rule Set Version Pinned */}
          <div className="rounded-lg bg-canvas p-3 border border-border flex items-center justify-between text-xs">
            <span className="text-slate-clinical">Active Rule Set Version:</span>
            <span className="font-mono font-semibold text-primary">{ruleSetVersion}</span>
          </div>

          {/* Guideline Title & Publisher */}
          <div className="space-y-2">
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-primary">
              <Building2 className="h-3.5 w-3.5" />
              {evidence.publisher}
            </span>
            <h4 className="text-lg font-bold text-ink leading-snug">{evidence.title}</h4>
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="rounded-lg border border-border bg-slate-50/50 p-2.5">
              <div className="flex items-center gap-1.5 text-slate-clinical mb-1">
                <MapPin className="h-3.5 w-3.5" />
                <span>Jurisdiction</span>
              </div>
              <span className="font-semibold text-ink">{evidence.jurisdiction}</span>
            </div>
            <div className="rounded-lg border border-border bg-slate-50/50 p-2.5">
              <div className="flex items-center gap-1.5 text-slate-clinical mb-1">
                <Calendar className="h-3.5 w-3.5" />
                <span>Published Date</span>
              </div>
              <span className="font-semibold text-ink">{evidence.publishedOn}</span>
            </div>
          </div>

          {/* Section Reference & Excerpt */}
          <div className="space-y-2">
            <h5 className="text-xs font-semibold text-slate-clinical uppercase tracking-wider">
              Section Reference
            </h5>
            <div className="rounded-md bg-canvas px-3 py-2 text-xs font-mono font-medium text-ink border border-border">
              {evidence.sectionRef}
            </div>
          </div>

          <div className="space-y-2">
            <h5 className="text-xs font-semibold text-slate-clinical uppercase tracking-wider">
              Cited Guideline Excerpt
            </h5>
            <blockquote className="rounded-lg border-l-4 border-primary bg-primary-subtle/30 p-4 text-xs italic text-ink leading-relaxed">
              &ldquo;{evidence.excerpt}&rdquo;
            </blockquote>
          </div>

          {evidence.url && (
            <a
              href={evidence.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary hover:underline"
            >
              View Official Reference Portal
              <ExternalLink className="h-3.5 w-3.5" />
            </a>
          )}

          {/* Clinician Advisory Notice */}
          <div className="rounded-lg border border-border bg-canvas p-4 text-xs space-y-1 text-slate-clinical">
            <div className="flex items-center gap-1.5 font-semibold text-ink">
              <CheckCircle2 className="h-4 w-4 text-primary" />
              <span>Institutional Policy Notice</span>
            </div>
            <p>
              Guidelines reflect national and global standards (ICMR / WHO). Always verify with your facility&apos;s current local hospital antibiogram and formulary guidance.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="rounded-lg bg-white border border-border px-4 py-2 text-xs font-semibold text-ink hover:bg-canvas transition-colors"
          >
            Close Provenance
          </button>
        </div>
      </div>
    </div>
  );
}
