# Dispatch: Forensic Auditor — Milestone 5 Integrity Forensic Audit

## Task Objective
Perform an exhaustive, independent forensic integrity audit of the AMR Sentinel AI codebase:
1. **AST Import Isolation**:
   - Inspect all AST import nodes in `services/api/app/engine/`.
   - Ensure strictly ZERO prohibited imports (`requests`, `httpx`, `aiohttp`, `urllib`, `google`, `google.genai`, `openai`, `anthropic`, `langchain`, `llama_index`, `sqlalchemy`, `asyncpg`, `psycopg2`, `supabase`, `sqlite3`, `subprocess`, `os.system`).
2. **Anti-Cheating & Anti-Hardcoding Forensics**:
   - Grep/scan `services/api/app/` for any benchmark case IDs (`BENCH_01`, `BENCH_30`, `SYN_CASE_*`), hardcoded expected answers, or hardcoded inputs-to-outputs mapping tables.
   - Verify that `ExtractionAdapter` uses genuine clinical regex, tokenizer, posology converter, and brand dictionaries.
   - Verify that `AMRKnowledgeService` dynamically parses and indexes authentic clinical reference CSVs (`guidelines.csv`, `who_aware_antibiotics.csv`, `icmr_surveillance_pages.csv`).
3. **Clinical Safety & Separation of Concerns**:
   - Verify that assistive extraction outputs are ALWAYS untrusted drafts (`clinical_status == "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`).
   - Verify that the deterministic clinical audit core in `app/engine/` remains completely unaltered, authoritative, and non-bypassed.
   - Verify that local offline fallback operates without external network or LLM dependencies.
4. **Execution Tracing & Quality Gate Verification**:
   - Execute and verify `scripts/evaluate_agent.py --compare-baseline`.
   - Execute and verify `ruff check services/api`.
   - Execute and verify `pytest services/api/tests -v`.
   - Execute and verify `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`.
5. **Verdict**:
   - State explicit binary verdict in `handoff.md`: `CLEAN` or `INTEGRITY VIOLATION`.

## Working Directory
`c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\auditor_m5_1\`

## Input Artifacts
- `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md` (MANDATORY)
- `c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md`
- `services/api/app/engine/`
- `services/api/app/extraction/`
- `services/api/app/services/`
- `services/api/tests/`
- `scripts/evaluate_agent.py`

## 2026-11-11T17:12:18Z
You are auditor_m5_1, a teamwork_auditor conducting the Milestone 5 Forensic Integrity Audit for AMR Sentinel AI.

Working directory: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\auditor_m5_1\
Parent orchestrator conversation ID: 993a1695-e727-4162-821a-1cc5b88a100b

MANDATORY FIRST STEP:
Read c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md before starting work.
Also read:
- c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md
- c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\auditor_m5_1\DISPATCH.md
- services/api/app/engine/
- services/api/app/extraction/adapter.py
- services/api/app/services/amr_knowledge.py
- scripts/evaluate_agent.py

TASKS:
1. AST Import Isolation Audit:
   - Walk the AST of every `.py` file in `services/api/app/engine/`.
   - Assert ZERO prohibited imports: no requests, httpx, aiohttp, urllib, socket, google, google.genai, openai, anthropic, langchain, llama_index, sqlalchemy, psycopg2, asyncpg, supabase, sqlite3, subprocess, os.system.
2. Anti-Cheating & Integrity Audit:
   - Grep all `.py` files in `services/api/app/` for hardcoded benchmark IDs (`BENCH_01`, `SYN_CASE_*`) or input-to-output test maps.
   - Verify that `ExtractionAdapter` uses authentic clinical regex, posology logic, and brand lookup tables.
   - Verify that `AMRKnowledgeService` dynamically parses and indexes authentic reference data (`who_aware_antibiotics.csv`, `guidelines.csv`, `icmr_surveillance_pages.csv`).
3. Safety Architecture & Clinical Status Audit:
   - Verify that all draft outputs enforce `clinical_status: "UNTRUSTED_DRAFT_PENDING_CONFIRMATION"`.
   - Verify that the deterministic engine is authoritative, unaltered, and non-bypassed.
4. Independent Execution & Gate Verification:
   - Run `.venv\Scripts\python.exe scripts/evaluate_agent.py --cases services/api/tests/data/benchmark_cases.json --compare-baseline`
   - Run `powershell -ExecutionPolicy Bypass -File scripts/test.ps1`
5. State your explicit binary verdict (`CLEAN` or `INTEGRITY VIOLATION`) in `c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\auditor_m5_1\handoff.md`.
6. Send completion message via send_message to recipient 993a1695-e727-4162-821a-1cc5b88a100b.
