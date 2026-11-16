-- AMR Sentinel AI: Vector Knowledge & RAG Schema
-- Enables pgvector for semantic retrieval of ICMR guidelines, CDSCO notices, and WHO AWaRe data.

CREATE EXTENSION IF NOT EXISTS vector;

-- Guideline document chunks with vector embeddings (dimension 768 for text-embedding-004)
CREATE TABLE IF NOT EXISTS public.amr_guideline_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_title TEXT NOT NULL,
    source_category TEXT NOT NULL CHECK (source_category IN ('ICMR_STG_2022', 'WHO_AWARE_2023', 'CDSCO_BANNED_FDC', 'NCDC_SURVEILLANCE', 'RESEARCH_EVIDENCE')),
    file_path TEXT,
    chunk_index INTEGER NOT NULL DEFAULT 0,
    heading TEXT,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(768),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- HNSW index for high-speed approximate nearest neighbor cosine search
CREATE INDEX IF NOT EXISTS amr_guideline_chunks_embedding_hnsw_idx 
ON public.amr_guideline_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Full-text search index for hybrid lexical fallback
CREATE INDEX IF NOT EXISTS amr_guideline_chunks_content_fts_idx 
ON public.amr_guideline_chunks 
USING gin (to_tsvector('english', content));

-- Enable Row Level Security (read-only for all authenticated clinicians, managed by org_admin)
ALTER TABLE public.amr_guideline_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to clinical knowledge chunks"
ON public.amr_guideline_chunks
FOR SELECT
USING (true);

-- Function for similarity match
CREATE OR REPLACE FUNCTION match_amr_guidelines(
    query_embedding vector(768),
    match_threshold float DEFAULT 0.5,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    source_title TEXT,
    source_category TEXT,
    heading TEXT,
    content TEXT,
    similarity float
)
LANGUAGE sql
STABLE
AS $$
    SELECT
        id,
        source_title,
        source_category,
        heading,
        content,
        1 - (amr_guideline_chunks.embedding <=> query_embedding) AS similarity
    FROM public.amr_guideline_chunks
    WHERE 1 - (amr_guideline_chunks.embedding <=> query_embedding) > match_threshold
    ORDER BY amr_guideline_chunks.embedding <=> query_embedding
    LIMIT match_count;
$$;
