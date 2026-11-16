# AMR Sentinel — Technology Stack Guide & Educational Manual

> **Clinician-Assistive Antimicrobial Prescription Auditing & Stewardship**  
> *A Senior Software Developer's Comprehensive Guide to the Modern Full-Stack & AI Architecture*

---

## 🧭 Overview & Architecture Blueprint

AMR Sentinel is designed using a **Strict Two-Layer Safety Architecture**:
1. **Assistive Intake & Decision-Support Layer (Stochastic / AI-Powered)**: Ingests prescriptions, runs document OCR, performs fuzzy brand-to-generic resolution, conducts RAG searches across ICMR guidelines, and drafts a suggested clinical profile. **All outputs are labeled as untrusted drafts pending clinician confirmation.**
2. **Deterministic Clinical Audit Core (Pure Python / AST-Isolated)**: Once verified by a clinician, rules are evaluated deterministically with **zero network, zero LLM, and zero database dependencies**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ASSISTIVE INTAKE & RAG LAYER                          │
│                                                                             │
│  [Prescription / Query]                                                     │
│            │                                                                │
│            ▼                                                                │
│  [RapidFuzz Brand Matching]  ──► [Gemini 2.5 Flash / OpenRouter LLM]        │
│            │                                   ▲                            │
│            ▼                                   │ Reranked Context           │
│  [LlamaIndex + pgvector (Dense)] + [Rank_BM25 (Sparse)]                     │
│            │                                   │                            │
│            └──────────────► [BAAI/BGE-Reranker]                             │
│                                                │                            │
│                                                ▼                            │
│                           [LangGraph Clinical Workflow Agent]               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Clinician Confirms Draft
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DETERMINISTIC CLINICAL AUDIT CORE                       │
│                         (Pure Python • AST Isolated)                        │
│                                                                             │
│  • Tier 1: Pediatric, Pregnancy & Renal Contraindications                   │
│  • Tier 2: CDSCO Banned Fixed-Dose Combinations (FDCs)                      │
│  • Tier 3: WHO AWaRe Spectrum De-escalation (Access vs Watch/Reserve)       │
│  • Tier 4: ICMR Short-Course Treatment Duration Limits                      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FRONTEND PRESENTATION & ANALYTICS                       │
│    Next.js 15 • Tailwind CSS • Shadcn UI • Framer Motion • Recharts        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 1: The Technologies Explained Step-by-Step

### 1. Frontend Technologies

#### **Next.js 15 (App Router)**
- **What it is**: The industry-standard React framework providing Server-Side Rendering (SSR), Server Components, and optimized client bundling.
- **Why we use it**: Clinical dashboards require high initial load speeds, strict SEO/security headers, and clean route management (`/`, `/new-audit`, `/insights`, `/knowledge`).

#### **Tailwind CSS 3**
- **What it is**: A utility-first CSS framework that compiles down to minimal, zero-runtime CSS classes.
- **Why we use it**: It guarantees design consistency via theme tokens (`ink`, `slate-clinical`, `primary`, `urgent`, `review`) matching healthcare interfaces.

#### **Shadcn UI & Radix Primitives**
- **What it is**: Unlike traditional component libraries (e.g. MUI) that lock you into rigid npm dependencies, Shadcn UI provides copy-paste, accessible, unstyled primitives (built on Radix UI) that live directly in your repository.
- **Why we use it**: You own 100% of the UI code, can style it with Tailwind, and gain instant WCAG accessibility compliance (keyboard navigation, ARIA live regions, focus trapping).

#### **Framer Motion**
- **What it is**: A production-ready motion library for React that simplifies declarative animations, layout transitions, and micro-interactions.
- **Why we use it**: Smooth transitions between audit steps (Upload → Review → Deterministic Evaluation) reassure clinicians that processing is occurring reliably, reducing perceived latency.

#### **Recharts**
- **What it is**: A composable charting library built on React components and SVG.
- **Why we use it**: Visualizing the WHO AWaRe distribution (Access ≥ 60%, Watch, Reserve) and historical resistance trends in accessible, responsive SVGs with interactive tooltips.

#### **Lucide React**
- **What it is**: A clean, tree-shakeable icon set with over 1,000 icons.
- **Why we use it**: Consistent clinical visual metaphors (`ShieldAlert`, `Pill`, `Activity`, `FileCheck`, `AlertOctagon`).

---

### 2. Backend & Data Layer Technologies

#### **Python 3.10+ / 3.14**
- **What it is**: The premier programming language for data science, bioinformatics, and AI systems.
- **Why we use it**: Pure Python is lightweight, readable, and allows strict Abstract Syntax Tree (AST) inspection to enforce safety constraints.

#### **FastAPI & Pydantic v2**
- **What it is**: A high-performance asynchronous web framework powered by Starlette and Pydantic.
- **Why we use it**: Automatic OpenAPI documentation (`/docs`), millisecond-range latency, and strict schema validation preventing invalid clinical payloads from entering the pipeline.

#### **SQLAlchemy 2.0 (Async) & Psycopg 3**
- **What it is**: Python's most powerful Object Relational Mapper (ORM), coupled with `psycopg3`, the modern async PostgreSQL driver.
- **Why we use it**: Provides safe, type-annotated SQL queries with connection pooling, transaction management, and direct integration with PostgreSQL.

#### **Supabase & PostgreSQL**
- **What it is**: Enterprise-grade PostgreSQL database with built-in Row-Level Security (RLS) and real-time capabilities.
- **Why we use it**: Enforces multi-tenant organizational isolation (`org_admin`, `clinician`, `clinical_reviewer`) directly at the database engine level.

---

### 3. AI, RAG & Search Technologies

#### **pgvector**
- **What it is**: An open-source extension for PostgreSQL that enables storing and indexing vector embeddings alongside traditional relational rows.
- **Why we use it**: Allows similarity search (Cosine distance `<=>` or Inner Product `<#>`) directly inside PostgreSQL without needing a separate vector database like Pinecone.

#### **LlamaIndex**
- **What it is**: A data framework for connecting custom data sources (PDFs, CSVs, clinical guideline manuals) to Large Language Models.
- **Why we use it**: Reads 50+ ICMR STG manuals, NCDC AMR reports, and WHO AWaRe listings, chunks them into semantic fragments, and builds vector indices.

#### **Rank_BM25 (Best Matching 25)**
- **What it is**: A classic probabilistic information retrieval algorithm that scores documents based on exact keyword frequencies, document length, and inverse document frequency.
- **Why we use it**: Vector search often struggles with precise pharmaceutical tokens (e.g. distinguishing `Cefixime` from `Cefuroxime` or spotting exact brand names like `Martifur`). BM25 guarantees that rare clinical terms are retrieved accurately.

#### **Hybrid Search (Dense Vector + Sparse BM25 via Reciprocal Rank Fusion)**
- **What it is**: Combining semantic meaning (Dense embeddings) with exact term matches (Sparse BM25).
- **Why we use it**: Clinicians search both conceptually ("first-line urinary tract infection medication") and specifically ("Augmentin 625mg BD"). Hybrid search delivers the highest retrieval accuracy across both modes.

#### **BAAI/BGE-Reranker**
- **What it is**: A cross-encoder model that scores pairs of `(Query, Candidate Document)` together rather than encoding them independently.
- **Why we use it**: Dense and sparse retrievers return the top 10-20 candidates quickly; the BGE-Reranker re-evaluates them with deep cross-attention to bubble the single most relevant clinical guideline to the top.

#### **RapidFuzz**
- **What it is**: A blazingly fast C++-backed fuzzy string matching library for Python.
- **Why we use it**: Prescriptions often contain handwritten typos or transcription errors (e.g. `Cifran` vs `Cipran`, `Augmentn`, `Azythromycin`). RapidFuzz resolves brand and misspelling variants to canonical generic INN names in sub-millisecond time.

#### **Gemini 2.5 Flash & Google GenAI SDK**
- **What it is**: Google DeepMind's state-of-the-art multimodal model with native JSON schema constraints and fast inference speeds.
- **Why we use it**: Capable of reading handwritten or printed prescription images and PDFs, extracting patient demographics, dosage, and frequency into structured JSON.

#### **OpenRouter API**
- **What it is**: A resilient API gateway supporting hundreds of LLM models with automatic fallbacks and load balancing.
- **Why we use it**: Prevents clinical service degradation if primary API keys exceed rate limits or experience regional downtime during live hospital operation.

#### **LangGraph**
- **What it is**: A framework for building stateful, multi-actor applications with LLMs using graph-based workflows (Nodes = processing steps, Edges = conditional decisions).
- **Why we use it**: Clinical decision-support is not a simple linear prompt; it requires stateful cycles: `Extract → Validate → Retrieve AMR Knowledge → Suggest Draft → Await Clinician Review → Deterministic Audit`.

---

## 🛠️ Step-by-Step Developer Implementation Guide

### Phase 1: Enabling PostgreSQL Vector Store (`pgvector`)
1. In Supabase or PostgreSQL, run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. Create embedding tables:
   ```sql
   CREATE TABLE amr_guideline_chunks (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       source_document TEXT NOT NULL,
       chunk_index INTEGER NOT NULL,
       content TEXT NOT NULL,
       metadata JSONB DEFAULT '{}',
       embedding vector(768) -- Matches text-embedding-004 dimensions
   );
   CREATE INDEX amr_chunks_embedding_idx ON amr_guideline_chunks USING hnsw (embedding vector_cosine_ops);
   ```

### Phase 2: Running Hybrid Retrieval (BM25 + Dense)
1. Ingest clinical guideline documents via LlamaIndex.
2. Index content tokens using `rank_bm25.BM25Okapi`.
3. Compute Reciprocal Rank Fusion (RRF):
   $$\text{RRF Score}(d) = \frac{1}{60 + \text{Rank}_{\text{dense}}(d)} + \frac{1}{60 + \text{Rank}_{\text{sparse}}(d)}$$

### Phase 3: LangGraph Clinical State Machine
Define state containing:
- `raw_input`: bytes or string
- `extracted_draft`: Pydantic draft
- `clinical_evidence`: retrieved citations
- `audit_findings`: deterministic results
- `workflow_status`: current execution step

---

## 🔒 Mandatory Safety Protocols
1. **Never bypass the Deterministic Audit Engine (`app/engine/`)**. It evaluates 100% locally with zero external network access.
2. **Always mark AI extractions as `UNTRUSTED_DRAFT_PENDING_CONFIRMATION`**.
3. **No Autonomous Prescribing**: The system serves as a second-check safety net, never a replacement for registered clinician judgment.
