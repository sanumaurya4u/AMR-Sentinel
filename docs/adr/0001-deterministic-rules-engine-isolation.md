# ADR 0001: Deterministic Clinical Rules Engine Isolation

## Status
Accepted

## Context
AMR Sentinel AI audits clinical antibiotic prescriptions for life-threatening contraindications, irrational fixed-dose combinations, viral self-limiting indications, and WHO AWaRe spectrum de-escalation opportunities. In clinical decision-support systems, stochastic generation (LLMs), runtime network dependencies, hidden state, or database query variations introduce non-determinism, hallucinations, and reproducibility failures.

A primary requirement of the product specification is that the clinical audit core must be 100% deterministic, side-effect-free, and verifiable. The same confirmed structured input and evidence snapshot must always yield identical findings.

## Decision
1. **Physical & Logical Boundary**: The rules engine lives strictly inside `services/api/app/engine/`.
2. **Prohibited Dependencies**: The engine module must never import:
   - External network clients (`requests`, `httpx`, `urllib`, `aiohttp`).
   - LLM / AI SDKs (`google.genai`, `openai`, `langchain`, `llama_index`).
   - Database / ORM clients (`sqlalchemy`, `asyncpg`, `psycopg2`, `supabase`).
   - Operating system / environment state (`os.environ`, `sys`, subprocesses, file writes).
   - Time-dependent dynamic lookups (e.g. `datetime.now()` for date math without an injected audit timestamp).
3. **Automated Enforcement**: An AST (Abstract Syntax Tree) test (`test_architecture_isolation.py`) runs on every test suite execution, scanning all files inside `app/engine/` and immediately failing CI/CD if any prohibited import or function call is detected.
4. **Data Input via Snapshots**: Clinical guidelines (ICMR STG 2022, WHO AWaRe 2023, CDSCO banned lists) are passed into the engine as versioned, immutable Pydantic models.

## Consequences
- **Positive**: Absolute audit reproducibility, zero hallucination risk in clinical gates, sub-millisecond execution times, independent offline testability.
- **Negative / Trade-off**: The ingestion layer (OCR, brand normalization, LLM extraction) must be strictly decoupled from the engine. Ingestion only produces an editable draft that requires clinician confirmation before the engine evaluates it.
