
from fastapi import FastAPI
from routers import stocks, rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Stock Market API",
    description="API for stock market data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "Stock Market API is running"}