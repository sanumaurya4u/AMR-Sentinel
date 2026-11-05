-- AMR Sentinel AI: Initial PostgreSQL Schema & Row Level Security (RLS)
-- Grounded in specs/AMR-Sentinel/Database.md

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- 1. Profiles & Tenancy
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name TEXT NOT NULL,
    role_title TEXT DEFAULT 'Clinician',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    is_demo BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.organization_memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'clinician' CHECK (role IN ('org_admin', 'clinician', 'clinical_reviewer', 'viewer')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    CONSTRAINT uq_org_membership UNIQUE (org_id, user_id)
);

-- Helper security definer functions for RLS
CREATE OR REPLACE FUNCTION public.is_org_member(check_org_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1 FROM public.organization_memberships
        WHERE org_id = check_org_id AND user_id = auth.uid()
    );
$$;

CREATE OR REPLACE FUNCTION public.has_org_role(check_org_id UUID, required_role TEXT)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1 FROM public.organization_memberships
        WHERE org_id = check_org_id
          AND user_id = auth.uid()
          AND role = required_role
    );
$$;

-- ==============================================================================
-- 2. Rules & Evidence Versioning (Immutable Catalogs)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.rule_set_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'published' CHECK (status IN ('draft', 'published', 'superseded', 'archived')),
    manifest JSONB NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    checksum TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.evidence_sources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    url TEXT,
    jurisdiction TEXT NOT NULL,
    published_on DATE NOT NULL,
    reviewed_on DATE NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.evidence_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_set_version_id UUID REFERENCES public.rule_set_versions(id) ON DELETE CASCADE,
    source_manifest JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- ==============================================================================
-- 3. Cases & Prescriptions
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'confirmed' CHECK (status IN ('draft', 'confirmed', 'audited', 'archived')),
    patient_context JSONB NOT NULL,
    indication_code TEXT NOT NULL,
    setting TEXT NOT NULL DEFAULT 'outpatient' CHECK (setting IN ('outpatient', 'inpatient')),
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.prescription_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID NOT NULL REFERENCES public.cases(id) ON DELETE CASCADE,
    drug_name TEXT NOT NULL,
    dose_text TEXT NOT NULL,
    frequency_text TEXT NOT NULL,
    duration_days INT,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- ==============================================================================
-- 4. Audit Runs, Findings & Acknowledgements (Immutable / Append-only)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.audit_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID NOT NULL REFERENCES public.cases(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    requested_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    rule_set_version_id UUID REFERENCES public.rule_set_versions(id),
    evidence_snapshot_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('NEEDS_URGENT_REVIEW', 'NEEDS_REVIEW', 'NO_RULE_TRIGGERED', 'INCOMPLETE_DATA', 'UNAVAILABLE')),
    report JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.audit_findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_run_id UUID NOT NULL REFERENCES public.audit_runs(id) ON DELETE CASCADE,
    rule_id TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('URGENT_REVIEW', 'NEEDS_REVIEW', 'DATA_GAP', 'INFO')),
    title TEXT NOT NULL,
    explanation TEXT NOT NULL,
    input_facts_used JSONB NOT NULL,
    missing_data_status JSONB DEFAULT '[]'::jsonb,
    guideline_discussion_prompt TEXT,
    evidence_reference_id TEXT REFERENCES public.evidence_sources(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.acknowledgements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_run_id UUID NOT NULL REFERENCES public.audit_runs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    action TEXT NOT NULL DEFAULT 'acknowledged' CHECK (action IN ('acknowledged', 'overridden', 'escalated')),
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- ==============================================================================
-- 5. Private Document Assets & Redacted Security Audit Log
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.document_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID NOT NULL REFERENCES public.cases(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    bucket_path TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    byte_size BIGINT NOT NULL,
    scan_status TEXT NOT NULL DEFAULT 'clean' CHECK (scan_status IN ('pending', 'clean', 'quarantined', 'failed')),
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS public.security_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES public.organizations(id) ON DELETE SET NULL,
    actor_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    metadata_redacted JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- ==============================================================================
-- 6. Indexes
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_cases_org_created ON public.cases(org_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_cases_creator_created ON public.cases(created_by, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_prescription_lines_case ON public.prescription_lines(case_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_audit_runs_case ON public.audit_runs(case_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_runs_org ON public.audit_runs(org_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_findings_run_sev ON public.audit_findings(audit_run_id, severity);
CREATE INDEX IF NOT EXISTS idx_org_memberships_user ON public.organization_memberships(user_id, org_id);
CREATE INDEX IF NOT EXISTS idx_document_assets_case ON public.document_assets(org_id, case_id);

-- ==============================================================================
-- 7. Row Level Security (RLS) Enablement & Policies
-- ==============================================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organization_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prescription_lines ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.acknowledgements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rule_set_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evidence_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evidence_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.document_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.security_audit_log ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can view and edit only their own profile
CREATE POLICY "profiles_select_own" ON public.profiles FOR SELECT USING (id = auth.uid());
CREATE POLICY "profiles_update_own" ON public.profiles FOR UPDATE USING (id = auth.uid());

-- Organizations: Visible only to members of that organization
CREATE POLICY "org_select_members" ON public.organizations FOR SELECT USING (public.is_org_member(id));

-- Memberships: Members can see rosters in their org
CREATE POLICY "org_members_select" ON public.organization_memberships FOR SELECT USING (public.is_org_member(org_id));

-- Cases: Members can access and insert cases in their org
CREATE POLICY "cases_select_org" ON public.cases FOR SELECT USING (public.is_org_member(org_id));
CREATE POLICY "cases_insert_org" ON public.cases FOR INSERT WITH CHECK (public.is_org_member(org_id));
CREATE POLICY "cases_update_org" ON public.cases FOR UPDATE USING (public.is_org_member(org_id));

-- Prescription Lines: Accessible if parent case is accessible
CREATE POLICY "lines_select_case" ON public.prescription_lines FOR SELECT
USING (EXISTS (SELECT 1 FROM public.cases c WHERE c.id = case_id AND public.is_org_member(c.org_id)));
CREATE POLICY "lines_insert_case" ON public.prescription_lines FOR INSERT
WITH CHECK (EXISTS (SELECT 1 FROM public.cases c WHERE c.id = case_id AND public.is_org_member(c.org_id)));

-- Audit Runs: Read-only for org members (immutable)
CREATE POLICY "audits_select_org" ON public.audit_runs FOR SELECT USING (public.is_org_member(org_id));

-- Audit Findings: Read-only for org members
CREATE POLICY "findings_select_org" ON public.audit_findings FOR SELECT
USING (EXISTS (SELECT 1 FROM public.audit_runs a WHERE a.id = audit_run_id AND public.is_org_member(a.org_id)));

-- Acknowledgements: Org members can view, authenticated users can sign
CREATE POLICY "acks_select_org" ON public.acknowledgements FOR SELECT
USING (EXISTS (SELECT 1 FROM public.audit_runs a WHERE a.id = audit_run_id AND public.is_org_member(a.org_id)));
CREATE POLICY "acks_insert_own" ON public.acknowledgements FOR INSERT
WITH CHECK (user_id = auth.uid() AND EXISTS (SELECT 1 FROM public.audit_runs a WHERE a.id = audit_run_id AND public.is_org_member(a.org_id)));

-- Rules & Evidence: Globally readable for authenticated/anon users
CREATE POLICY "rules_select_all" ON public.rule_set_versions FOR SELECT USING (true);
CREATE POLICY "evidence_select_all" ON public.evidence_sources FOR SELECT USING (true);
CREATE POLICY "snapshots_select_all" ON public.evidence_snapshots FOR SELECT USING (true);

-- Document Assets: Private to org
CREATE POLICY "assets_select_org" ON public.document_assets FOR SELECT USING (public.is_org_member(org_id));
CREATE POLICY "assets_insert_org" ON public.document_assets FOR INSERT WITH CHECK (public.is_org_member(org_id));
