from database import get_connection
from psycopg.rows import dict_row

class RagRepository:
    @staticmethod
    def search_similar_documents(vector_text: str, limit: int = 5):
        sql = """
            SELECT
                source_name,
                chunk_text,
                embedding <-> %s::vector AS distance
            FROM rag_documents
            ORDER BY embedding <-> %s::vector
            LIMIT %s
        """
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, (vector_text, vector_text, limit))
                return [dict(row) for row in cur.fetchall()]
