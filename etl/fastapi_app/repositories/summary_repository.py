from database import get_connection

class SummaryRepository:
    @staticmethod
    def get_cached_summary(stock_code: str, trade_date):
        sql = """
            SELECT ai_summary
            FROM stock_ai_summaries
            WHERE stock_code = %s
            AND trade_date = %s
            LIMIT 1
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (stock_code, trade_date))
                row = cur.fetchone()
                return row[0] if row else None

    @staticmethod
    def save_summary_to_db(stock_code: str, trade_date, ai_summary: str):
        sql = """
            INSERT INTO stock_ai_summaries (
                stock_code,
                trade_date,
                ai_summary
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (stock_code, trade_date)
            DO NOTHING
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (stock_code, trade_date, ai_summary))
            conn.commit()
