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

def get_stock_context(stock_code: str, limit: int = 30):
    sql = """
        SELECT stock_code, stock_name, trade_date, close, ma5, ma20, ma60, cross_signal, trend_type, daily_return, cumulative_return
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

def find_stock_by_question(question: str):
    sql = """
        SELECT stock_code, stock_name
        FROM stocks
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    for row in rows:
        stock_code = row[0]
        stock_name = row[1]

        if stock_name in question:
            return stock_code

    return None

def get_latest_stock_indicator(stock_code: str):
    sql = """
        SELECT
            stock_code,
            trade_date,
            close,
            ma5,
            ma20,
            ma60,
            trend_type,
            cross_signal,
            daily_return,
            cumulative_return
        FROM stock_indicators
        WHERE stock_code = %s
        ORDER BY trade_date DESC
        LIMIT 1
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (stock_code,))
            row = cur.fetchone()

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