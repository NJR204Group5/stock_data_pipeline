
from fastapi import APIRouter, Query, HTTPException
from services.stock_service import (
    get_all_stocks,
    get_stock_prices,
    get_stock_indicators,
    get_latest_stock_signal,
)
from fastapi.encoders import jsonable_encoder
from services.llm_service import generate_stock_summary

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)

@router.get("")
def list_stocks():
    return jsonable_encoder(get_all_stocks())

@router.get("/{stock_code}/prices")
def stock_prices(
    stock_code: str,
    limit: int = Query(default=30, ge=1, le=365)
):
    return jsonable_encoder(get_stock_prices(stock_code, limit))

@router.get("/{stock_code}/indicators")
def stock_indicators(
    stock_code: str,
    limit: int = Query(default=30, ge=1, le=365)
):
    return jsonable_encoder(get_stock_prices(stock_code, limit))

@router.get("/{stock_code}/signal")
def stock_signal(stock_code: str):
    result = get_latest_stock_signal(stock_code)
    if result is None:
        raise HTTPException(status_code=404, detail="Stock signal not found")
    return jsonable_encoder(result)

@router.get("/{stock_code}/ai-summary")
def stock_summary(stock_code: str):
    stock_data = get_latest_stock_signal(stock_code)

    if stock_data is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    summary = generate_stock_summary(stock_data)

    return {
        "stock_code": stock_code,
        "ai_summary": summary,
    }