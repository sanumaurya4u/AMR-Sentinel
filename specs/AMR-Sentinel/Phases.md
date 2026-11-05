# AMR Sentinel AI — Incremental Build Plan

Each phase ends with a small, runnable, reviewable increment. Do not move to the next phase with failing safety gates.

## Phase 0 — Foundation and guardrails

Create monorepo, environment templates, CI, formatting, basic health endpoint, synthetic-data policy, and these specs. Establish a local run command and ADR for deterministic engine isolation.

**Exit:** web and API start locally; no secrets committed; CI runs lint and a smoke test.

## Phase 1 — Clinical SaaS shell

Build responsive navigation, dashboard, new-case form, disclaimer, synthetic sample selector, loading/empty/error states, and accessible component primitives. No clinical claims beyond static demo copy.

**Exit:** user can complete a mock case flow in the browser; keyboard navigation and mobile layout are checked.

## Phase 2 — Contracts and deterministic audit core

Define canonical schemas for patient context, medication line, indication, input gap, evidence reference, finding, and report. Implement the pure engine with a very small, reviewed seed ruleset and version metadata.

**Exit:** `POST /v1/audits` produces repeatable reports; rule unit tests plus engine import-isolation test pass.

## Phase 3 — Results experience and evidence provenance

Connect UI to API. Build severity overview, findings cards, input gaps, evidence drawer, clinician acknowledgement, and printable/share-safe report view. Phrase alternatives as review prompts only.

**Exit:** an end-to-end synthetic case has traceable inputs, findings, evidence version, and acknowledgement.

## Phase 4 — Supabase foundation

Provision Supabase through MCP, add migrations/seed data, Auth, private Storage, RLS, and least-privilege API configuration. Add repositories and audit persistence.

**Exit:** signed-in users can access only their organization’s authorized demo cases; RLS denial tests pass.

## Phase 5 — Document intake (optional and bounded)

Add private upload, OCR/extraction adapter, confidence-labelled editable draft, local/manual fallback, and deletion workflow. Keep extraction separate from audit.

**Exit:** synthetic image/PDF can yield a draft; low confidence or outage never triggers an automatic audit.

## Phase 6 — Stewardship insights and admin workflow

Add de-identified aggregates, rule/evidence version administration workflow, case review filters, and audit-log views. Do not expose patient details in aggregate endpoints.

**Exit:** authorized admin sees only aggregated metrics and evidence change history.

## Phase 7 — Hardening and deployment

Run threat/privacy review, rate/upload limits, error redaction, backup/export policy, test suite, deployment previews, and demo script. Deploy Vercel + Railway only if current tier limits support the demo; otherwise use the documented local demo.

**Exit:** reproducible local demo, deployment checklist, known-limitations page, and no claim of production clinical readiness.

## Antigravity working loop

For each phase: open the relevant specification → generate only the scoped files → run checks → inspect output → commit a focused change → record decisions/limitations. Use SDK/tool calls only behind adapters; keep rule evaluation offline and deterministic.
