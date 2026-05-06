
from fastapi import FastAPI
from routers import stocks

app = FastAPI(
    title="Stock Market API",
    description="API for stock market data",
    version="1.0.0"
)

app.include_router(stocks.router)

@app.get("/")
def root():
    return {"message": "Stock Market API is running"}