import re
from services.embedding_service import generate_embedding
from services.stock_service import get_latest_stock_signal, find_stock_by_question
from repositories.rag_repository import RagRepository

def to_vector_string(embedding: list[float]) -> str:
    return "[" + ",".join(str(x) for x in embedding) + "]"

def extract_stock_code(question: str):
    match = re.search(r"\b\d{4}\b", question)
    if match:
        return match.group()
    
    stock_code = find_stock_by_question(question)
    if stock_code:
        return stock_code
    return None

def search_similar_documents(question: str, limit: int = 5):
    question_embedding = generate_embedding(question)
    vector_text = to_vector_string(question_embedding)
    
    # 呼叫 Repository 取得資料
    rows = RagRepository.search_similar_documents(vector_text, limit)
    
    # 維持原本的回傳格式與型別轉換
    return [
        {
            "source_name": row["source_name"],
            "chunk_text": row["chunk_text"],
            "distance": float(row["distance"])
        }
        for row in rows
    ]

def get_structured_stock_context(question: str):
    stock_code = extract_stock_code(question)
    if not stock_code:
        return None
    return get_latest_stock_signal(stock_code)

def build_hybrid_context(question: str):
    stock_data = get_structured_stock_context(question)
    docs = search_similar_documents(question)

    return {
        "stock_data": stock_data,
        "retrieved_docs": docs
    }
