import os
from pathlib import Path

import psycopg

from pgvector.psycopg import register_vector

from stock_market_pipeline.services.embedding_service import generate_embedding

from stock_market_pipeline.utils.text_chunker import chunk_text

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

RAG_DOCS_DIR = Path(
    "/opt/airflow/etl/stock_market_pipeline/data/rag_docs"
)

def run():
    print(RAG_DOCS_DIR)
    print(list(RAG_DOCS_DIR.glob("*.txt")))

    sql = """
        INSERT INTO rag_documents (
            source_type,
            source_name,
            chunk_text,
            embedding
        )
        VALUES (%s, %s, %s, %s)
    """

    with psycopg.connect(**DB_CONFIG) as conn:

        register_vector(conn)

        with conn.cursor() as cur:
            for file_path in RAG_DOCS_DIR.glob("*.txt"):
                text = file_path.read_text(
                    encoding="utf-8"
                )

                chunks = chunk_text(text)

                for chunk in chunks:
                    embedding = generate_embedding(chunk)
                    cur.execute(
                        sql,
                        (
                            "txt",
                            file_path.name,
                            chunk,
                            embedding
                        )
                    )
        conn.commit()
    print("RAG documents embedded successfully")