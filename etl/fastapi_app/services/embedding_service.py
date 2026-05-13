import os

import google.generativeai as genai

def generate_embedding(text: str) -> list[float]:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")

    genai.configure(api_key=api_key)

    response = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        task_type="retrieval_document"
    )

    return response["embedding"]