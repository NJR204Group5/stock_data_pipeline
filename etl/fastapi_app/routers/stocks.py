
from fastapi import APIRouter, Query, HTTPException
from services.stock_service import (
    get_all_stocks,
    get_stock_prices,
    get_stock_indicators,
    get_latest_stock_signal,
)
from fastapi.encoders import jsonable_encoder

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