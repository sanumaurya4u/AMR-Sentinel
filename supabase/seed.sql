-- AMR Sentinel AI: Synthetic Seed Data
-- Demo Organization, Rules Version, Evidence Sources and Snapshots

-- Demo Organization
INSERT INTO public.organizations (id, name, is_demo)
VALUES ('00000000-0000-0000-0000-000000000001', 'National Antimicrobial Stewardship Initiative', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Evidence Sources
INSERT INTO public.evidence_sources (id, title, publisher, url, jurisdiction, published_on, reviewed_on, content_hash)
VALUES
('EVID_ICMR_PED_FQ', 'ICMR Standard Treatment Guidelines: Pediatric Antimicrobial Stewardship', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_ped_fq_2022'),
('EVID_ICMR_PED_TETRA', 'ICMR Guidelines: Pediatric Contraindications for Tetracyclines', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_ped_tetra_2022'),
('EVID_WHO_PREG_ANTIBIOTICS', 'WHO Clinical Guidelines on Antibiotic Safety in Pregnancy and Lactation', 'World Health Organization (WHO)', 'https://www.who.int', 'Global', '2023-05-10', '2026-11-01', 'hash_who_preg_2023'),
('EVID_BEERS_ICMR_NITROFURANTOIN', 'AGS Beers Criteria & ICMR Guidelines: Nitrofurantoin in Renal Impairment', 'American Geriatrics Society & ICMR', 'https://main.icmr.nic.in', 'Global / India', '2023-05-04', '2026-11-01', 'hash_nitro_renal_2023'),
('EVID_KDIGO_RENAL_HOLD', 'KDIGO Clinical Practice Guideline for Acute Kidney Injury & Drug Dosing', 'Kidney Disease: Improving Global Outcomes (KDIGO)', 'https://kdigo.org', 'International', '2022-11-20', '2026-11-01', 'hash_kdigo_hold_2022'),
('EVID_ICMR_ALLERGY_ANAPHYLAXIS', 'ICMR Guidelines: Antimicrobial Hypersensitivity and Cross-Reactivity', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_allergy_2022'),
('EVID_CDSCO_BANNED_FDC', 'CDSCO Gazette Notification: Banned Irrational Fixed-Dose Combinations', 'Central Drugs Standard Control Organisation (CDSCO)', 'https://cdsco.gov.in', 'India (National Regulatory)', '2023-06-02', '2026-11-01', 'hash_cdsco_fdc_2023'),
('EVID_ICMR_RESP_BRONCHITIS', 'ICMR STG 2022: Respiratory Infections — Acute Bronchitis', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_resp_bronch_2022'),
('EVID_ICMR_URTI_COLD', 'ICMR STG 2022: Upper Respiratory Infections & Common Cold', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_urti_cold_2022'),
('EVID_WHO_AWARE_2023', 'WHO AWaRe Antibiotic Classification & Stewardship Book 2023', 'World Health Organization (WHO)', 'https://www.who.int', 'Global', '2023-07-15', '2026-11-01', 'hash_aware_book_2023'),
('EVID_ICMR_SHORT_COURSE', 'ICMR Standard Treatment Guidelines: Optimal Antimicrobial Duration', 'Indian Council of Medical Research (ICMR)', 'https://main.icmr.nic.in', 'India (National)', '2022-09-15', '2026-11-01', 'hash_duration_2022')
ON CONFLICT (id) DO NOTHING;

-- Active Rule Set Version
INSERT INTO public.rule_set_versions (id, version, status, manifest, approved_by, approved_at, checksum)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    '1.0.0-ICMR-STG-2022',
    'published',
    '{"name": "ICMR Standard Treatment Guidelines & WHO AWaRe", "version": "1.0.0"}'::jsonb,
    'National Clinical Stewardship Committee',
    '2026-11-01T00:00:00Z',
    'sha256_icmr_stg_2022_v1_immutable'
)
ON CONFLICT (version) DO NOTHING;
