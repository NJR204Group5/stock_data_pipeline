from services.embedding_service import generate_embedding
from database import get_connection

def to_vector_string(embedding: list[float]) -> str:
    return "[" + ",".join(str(x) for x in embedding) + "]"

def search_similar_documents(question: str, limit: int = 5):
    question_embedding = generate_embedding(question)
    vector_text = to_vector_string(question_embedding)

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
        with conn.cursor() as cur:
            cur.execute(sql, (vector_text, vector_text, limit))
            rows = cur.fetchall()

    return [
        {
            "source_name": row[0],
            "chunk_text": row[1],
            "distance": float(row[2])
        }
        for row in rows
    ]