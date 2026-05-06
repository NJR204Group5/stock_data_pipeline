from decimal import Decimal
from datetime import date, datetime
from database import get_connection
from psycopg.rows import dict_row

def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

def get_all_stocks(limit: int = 30):
    sql = """
        SELECT stock_code, stock_name, category, industry, market 
        FROM stocks
        ORDER BY stock_code
        LIMIT %s
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, (limit,))
            rows = cur.fetchall()
    return [dict(row) for row in rows]

def get_stock_prices(stock_code: str, limit: int = 30):
    sql = """
        SELECT stock_code, trade_date, open, high, low, close, volume
        FROM stock_prices
        WHERE TRIM(stock_code) = %s
        ORDER BY trade_date DESC
        LIMIT %s 
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, (stock_code, limit))
            rows = cur.fetchall()
    return [dict(row) for row in rows]

def get_stock_indicators(stock_code: str, limit: int = 30):
    sql = """"
        SELECT stock_code, trade_date, close, ma5, ma20, ma60, stock_display, cross_signal, trend_type, daily_return, cumulative_return
        FROM stock_indicators
        WHERE stock_code = %s
        ORDER BY trade_date DESC
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, (stock_code, limit))
            rows = cur.fetchall()
    return [dict(row) for row in rows]

def get_latest_stock_signal(stock_code: str):
    sql = """
        SELECT stock_code, stock_name, trade_date, close, ma5, ma20, ma60, cross_signal, trend_type, daily_return, cumulative_return
        FROM stock_indicators
        WHERE stock_code = %s
        ORDER BY trade_date DESC
        LIMIT 1
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, (stock_code,))
            row = cur.fetchone()

    return dict(row) if row else None