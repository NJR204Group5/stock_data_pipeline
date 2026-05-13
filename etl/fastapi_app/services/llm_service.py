import os

from pathlib import Path
from dotenv import load_dotenv
from database import get_connection

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

env_path = Path(__file__).resolve().parents[3] / ".env"

load_dotenv(dotenv_path=env_path)

print("ENV PATH:", env_path)
print("GEMINI API KEY:", os.getenv("GEMINI_API_KEY"))

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
)

# 可使用的 model
for m in genai.list_models():
    print(m.name)

model = genai.GenerativeModel("models/gemini-flash-lite-latest")

def get_cached_summary(stock_code: str, trade_date):
    sql = """
        SELECT ai_summary
        FROM stock_ai_summaries
        WHERE stock_code = %s
        AND trade_date = %s
        LIMIT 1
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    stock_code,
                    trade_date
                )
            )
            row = cur.fetchone()

    if row:
        return row[0]

    return None

def save_summary_to_db(stock_code: str, trade_date, ai_summary: str):
    sql = """
        INSERT INTO stock_ai_summaries (
            stock_code,
            trade_date,
            ai_summary
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (stock_code, trade_date)
        DO NOTHING
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    stock_code,
                    trade_date,
                    ai_summary
                )
            )
        conn.commit()

def get_or_create_stock_summary(stock_data: dict):
    stock_code = stock_data["stock_code"]
    trade_date = stock_data["trade_date"]

    cached_summary = get_cached_summary(
        stock_code=stock_code,
        trade_date=trade_date
    )

    if cached_summary:
        print("Using cached AI summary")
        return cached_summary

    print("Generating new AI summary")
    summary = generate_stock_summary(stock_data)
    save_summary_to_db(
        stock_code=stock_code,
        trade_date=trade_date,
        ai_summary=summary
    )

    return summary

def generate_stock_summary(stock_data: dict):
    prompt = f"""
        Analyze the following stock indicators.
        
        Stock: {stock_data['stock_code']}
        Close Price: {stock_data['close']}
        
        MA5: {stock_data['ma5']}
        MA20: {stock_data['ma20']}
        MA60: {stock_data['ma60']}
        
        Trend: {stock_data['trend_type']}
        Cross Signal: {stock_data['cross_signal']}
        
        Daily Return: {stock_data['daily_return']}
        Cumulative Return: {stock_data['cumulative_return']}
        
        Please provide:
        1. Trend summary
        2. Risk level
        3. Short-term observation
        
        Keep the response concise.
    """

    try:
        print("Calling Gemini API...")
        response = model.generate_content(prompt)
        print("Gemini response received")
        return response.text
    except ResourceExhausted:
        return "Gemini quota exceeded, please try again later."
    except Exception as e:
        return f"LLM error: {str(e)}"

def answer_stock_question(question: str, stock_context: list[dict]):
    prompt = f"""
        You are a stock data assistant.
        Answer the user's question based only on the following stock data:
        Do not make up information.
        If the data is not enough, say the data is not enough.
        
        User question: {question}
        
        Stock data: {stock_context}
        
        Please answer in Traditional Chinese.
        Keep the answer clear and concise.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted:
        return "Gemini quota exceeded, please try again later."
    except Exception as e:
        return f"LLM error: {str(e)}"

def answer_with_context(question: str, context_docs: list[dict]):
    context_text = "\n\n".join(
        doc["chunk_text"] for doc in context_docs
    )

    prompt = f"""
    You are a stock analysis assistant.

    Answer the user's question based only on the context below.
    If the context is not enough, say the data is not enough.

    Context:
    {context_text}

    Question:
    {question}

    Please answer in Traditional Chinese.
    """

    response = model.generate_content(prompt)

    return response.text