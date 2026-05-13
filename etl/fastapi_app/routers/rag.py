from fastapi import APIRouter
from pydantic import BaseModel

from services.rag_service import search_similar_documents
from services.llm_service import answer_with_context

router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)

class RagQuestion(BaseModel):
    question: str

@router.post("/chat")
def rag_chat(request: RagQuestion):
    docs = search_similar_documents(request.question)
    print(docs)
    answer = answer_with_context(
        question=request.question,
        context_docs=docs
    )

    return {
        "question": request.question,
        "retrieved_docs": docs,
        "answer": answer
    }