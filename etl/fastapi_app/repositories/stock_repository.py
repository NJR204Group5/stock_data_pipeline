from database import get_connection
from psycopg.rows import dict_row

class StockRepository:
    @staticmethod
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
                return [dict(row) for row in cur.fetchall()]

    @staticmethod
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
                return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_stock_indicators(stock_code: str, limit: int = 30):
        sql = """
            SELECT stock_code, trade_date, close, ma5, ma20, ma60, stock_display, cross_signal, trend_type, daily_return, cumulative_return
            FROM stock_indicators
            WHERE stock_code = %s
            ORDER BY trade_date DESC
            LIMIT %s
        """
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, (stock_code, limit))
                return [dict(row) for row in cur.fetchall()]

    @staticmethod
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

    @staticmethod
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
                return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_all_stock_codes_and_names():
        sql = "SELECT stock_code, stock_name FROM stocks"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    @staticmethod
    def get_latest_stock_indicator_raw(stock_code: str):
        sql = """
            SELECT
                stock_code, trade_date, close, ma5, ma20, ma60,
                trend_type, cross_signal, daily_return, cumulative_return
            FROM stock_indicators
            WHERE stock_code = %s
            ORDER BY trade_date DESC
            LIMIT 1
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (stock_code,))
                return cur.fetchone()

    @staticmethod
    def get_chart_data_raw(stock_code: str, limit: int = 60):
        sql = """
            SELECT trade_date, close, ma5, ma20, ma60
            FROM stock_indicators
            WHERE stock_code = %s
            ORDER BY trade_date DESC
            LIMIT %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (stock_code, limit))
                return cur.fetchall()
