-- 啟用 pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id SERIAL PRIMARY KEY,
    source_type VARCHAR(50),
    source_name TEXT,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(768),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- vector similarity index
CREATE INDEX IF NOT EXISTS idx_rag_embedding
ON rag_documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);