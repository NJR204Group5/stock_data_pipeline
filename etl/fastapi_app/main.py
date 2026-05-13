
from fastapi import FastAPI
from routers import stocks, rag

app = FastAPI(
    title="Stock Market API",
    description="API for stock market data",
    version="1.0.0"
)

app.include_router(stocks.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "Stock Market API is running"}