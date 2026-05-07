import os

from pathlib import Path
from dotenv import load_dotenv

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