# AMR Sentinel AI — Supabase Database and RLS Specification

## 1. Data posture

The hackathon system uses synthetic data by default. Treat all case/audit data as sensitive health-adjacent data: store the minimum necessary, keep documents private, prohibit PHI in logs/analytics, and define deletion/retention before accepting real data. This is not a production compliance certification.

## 2. Roles and tenancy

| Role | Purpose | Data access |
|---|---|---|
| `authenticated` | signed-in clinician/demo user | own organization and authorized cases only via RLS |
| `org_admin` | organization membership/admin | organization membership, approved metrics and evidence workflow |
| `clinical_reviewer` | evidence/rule review | proposal/review workflow; no broad case access by default |
| `service_role` | FastAPI server only | narrowly scoped server tasks; never browser/client |

Use `auth.users` as identity. Map authorization in `profiles` and `organization_memberships`; never trust a client-provided organization ID without RLS membership verification.

## 3. Schema

| Table | Key columns | Purpose |
|---|---|---|
| `profiles` | `id PK → auth.users`, `display_name`, `created_at` | minimal user profile |
| `organizations` | `id`, `name`, `is_demo`, `created_at` | tenancy boundary |
| `organization_memberships` | `org_id`, `user_id`, `role`, `unique(org_id,user_id)` | organization authorization |
| `cases` | `id`, `org_id`, `created_by`, `status`, `patient_context jsonb`, `indication_code`, `is_synthetic`, timestamps | minimum necessary confirmed case input |
| `prescription_lines` | `id`, `case_id`, `drug_code`, `display_name`, `dose_text`, `frequency_text`, `duration_days`, `sort_order` | canonicalized entered prescription lines |
| `audit_runs` | `id`, `case_id`, `org_id`, `requested_by`, `rule_set_version_id`, `evidence_snapshot_id`, `status`, `report jsonb`, `created_at` | immutable audit result |
| `audit_findings` | `id`, `audit_run_id`, `rule_id`, `severity`, `summary`, `input_gaps jsonb`, `evidence_reference_ids jsonb` | queryable report findings |
| `acknowledgements` | `id`, `audit_run_id`, `user_id`, `action`, `reason`, `created_at` | review/override trail; append-only |
| `rule_set_versions` | `id`, `version`, `status`, `manifest jsonb`, `approved_by`, `approved_at`, `checksum` | immutable active/past rule set |
| `evidence_sources` | `id`, `title`, `publisher`, `url`, `jurisdiction`, `published_on`, `reviewed_on`, `content_hash` | source catalogue |
| `evidence_snapshots` | `id`, `rule_set_version_id`, `source_manifest jsonb`, `created_at` | audit reproducibility |
| `document_assets` | `id`, `case_id`, `org_id`, `bucket_path`, `mime_type`, `byte_size`, `scan_status`, `deleted_at` | metadata only; file is private Storage object |
| `security_audit_log` | `id`, `org_id`, `actor_id`, `event_type`, `target_type`, `target_id`, `metadata_redacted`, `created_at` | security-relevant, redacted trail |

Do not store raw OCR text after extraction unless expressly needed and governed. If retained, use a separate short-retention table/storage object with strict RLS and deletion.

## 4. Relationships and indexes

`organizations 1—N memberships/cases/audit_runs`; `cases 1—N prescription_lines/audit_runs/document_assets`; `audit_runs 1—N audit_findings/acknowledgements`; `rule_set_versions 1—N evidence_snapshots`.

Create indexes: `cases(org_id, created_at DESC)`, `cases(created_by, created_at DESC)`, `prescription_lines(case_id, sort_order)`, `audit_runs(case_id, created_at DESC)`, `audit_runs(org_id, created_at DESC)`, `audit_findings(audit_run_id, severity)`, `organization_memberships(user_id, org_id)`, `document_assets(org_id, case_id)`, and partial `document_assets(bucket_path) WHERE deleted_at IS NULL`. Use GIN indexes only on JSONB fields with demonstrated query needs.

## 5. RLS policy blueprint

Enable RLS on every application table. Define security-definer membership helpers carefully with a fixed `search_path`, e.g. `is_org_member(org_id)` and `has_org_role(org_id, role)`.

| Resource | Select | Insert | Update/Delete |
|---|---|---|---|
| `profiles` | own row | trigger/onboarding only | own non-sensitive display fields |
| `organizations` | member | server/admin bootstrap | org admin only |
| memberships | member can view own org roster subject to product need | org admin/server | org admin/server |
| cases/lines/assets | org member; restrict by creator if required | member with `created_by=auth.uid()` and member org | creator or authorized reviewer; no cross-org access |
| audit runs/findings | member of owning org | API/server after validating case access | immutable: no updates/deletes by client |
| acknowledgements | org member for associated audit | `user_id=auth.uid()` | immutable (correction = new acknowledgement) |
| rule/evidence versions | authenticated read of published versions | reviewer/admin workflow only | never edit published record; supersede version |
| security log | server/security admin only | server trigger/API only | append-only |

RLS must validate both `org_id` and relationship ownership. Write tests for unauthenticated, same-user, same-org, different-org, admin, and service scenarios.

## 6. Storage

Create private bucket `prescription-documents`; no public bucket or public URL. Object paths use `org/{org_id}/case/{case_id}/{uuid}`. Storage policies require authenticated membership in the path organization and verified case access. Generate short-lived signed URLs only after authorization. Enforce MIME allowlist (PDF/JPEG/PNG/WebP), size cap, and scan state before processing. A separate private `evidence-assets` bucket may hold public-source copies/metadata; do not mix it with case files.

## 7. Data lifecycle and operations

- `audit_runs`, findings, evidence snapshots, and acknowledgements are append-only for reproducibility.
- Delete a demo case by deleting its assets then redacting/minimizing linked case data according to an explicit retention job; preserve only non-identifying operational audit metadata where justified.
- Use migrations and seeded synthetic fixtures in source control; never use dashboard-only schema edits without exporting a migration.
- The FastAPI server verifies JWTs and applies server authorization even when using service credentials; service role bypasses RLS and must be treated as highly privileged.
- Backups, export, telemetry, and error reporting must exclude documents and raw case payloads by default.
