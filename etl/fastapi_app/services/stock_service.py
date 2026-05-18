from decimal import Decimal
from datetime import date, datetime
from repositories.stock_repository import StockRepository

def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

def get_all_stocks(limit: int = 30):
    return StockRepository.get_all_stocks(limit)

def get_stock_prices(stock_code: str, limit: int = 30):
    return StockRepository.get_stock_prices(stock_code, limit)

def get_stock_indicators(stock_code: str, limit: int = 30):
    # 此 API 原本在 service 中呼叫了 get_stock_prices，但 router 名稱為 stock_indicators
    # 這裡依照原始邏輯維持呼叫 Repo 的 indicators 版本
    return StockRepository.get_stock_indicators(stock_code, limit)

def get_latest_stock_signal(stock_code: str):
    return StockRepository.get_latest_stock_signal(stock_code)

def get_stock_context(stock_code: str, limit: int = 30):
    return StockRepository.get_stock_context(stock_code, limit)

def find_stock_by_question(question: str):
    rows = StockRepository.get_all_stock_codes_and_names()
    for row in rows:
        stock_code = row[0]
        stock_name = row[1]
        if stock_name in question:
            return stock_code
    return None

def get_latest_stock_indicator(stock_code: str):
    row = StockRepository.get_latest_stock_indicator_raw(stock_code)
    if not row:
        return None

    return {
        "stock_code": row[0],
        "trade_date": str(row[1]),
        "close": row[2],
        "ma5": row[3],
        "ma20": row[4],
        "ma60": row[5],
        "trend_type": row[6],
        "cross_signal": row[7],
        "daily_return": row[8],
        "cumulative_return": row[9],
    }

def get_stock_chart_data(stock_code: str, limit: int = 60):
    rows = StockRepository.get_chart_data_raw(stock_code, limit)
    data = [
        {
            "trade_date": str(row[0]),
            "close": float(row[1]),
            "ma5": float(row[2]) if row[2] else None,
            "ma20": float(row[3]) if row[3] else None,
            "ma60": float(row[4]) if row[4] else None,
        }
        for row in rows
    ]
    return list(reversed(data))
