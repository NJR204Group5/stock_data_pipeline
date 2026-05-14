from fastapi import APIRouter
from pydantic import BaseModel

from services.rag_service import search_similar_documents, build_hybrid_context
from services.llm_service import answer_with_context

router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)

class RagQuestion(BaseModel):
    question: str

@router.post("/chat")
def rag_chat(request: RagQuestion):
    hybrid_context = build_hybrid_context(request.question)
    stock_data = hybrid_context["stock_data"]
    docs = hybrid_context["retrieved_docs"]
    print(hybrid_context)
    answer = answer_with_context(
        question=request.question,
        stock_data=stock_data,
        context_docs=docs
    )

    return {
        "question": request.question,
        "stock_data": stock_data,
        "retrieved_docs": docs,
        "answer": answer
    }