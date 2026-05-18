import os
import random
import psycopg
import pandas as pd
import time

from datetime import datetime, timedelta
from stock_market_pipeline.services.fugle_service import get_fugle_stock_client

# PostgreSQL 連線設定
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def fetch_month_data(stock, stock_code, year, month, debug=False):
    month_start = datetime(year, month, 1)
    month_end = month_start + pd.offsets.MonthEnd(0)

    from_date = month_start.strftime("%Y-%m-%d")
    to_date = month_end.strftime("%Y-%m-%d")

    for attempt in range(5):
        try:
            result = stock.historical.candles(
                **{
                    "symbol": stock_code,
                    "from": from_date,
                    "to": to_date,
                    "fields": "open,high,low,close,volume,turnover,change",
                    "timeframe": "D",
                    "sort": "asc",
                }
            )
            break
        except Exception as e:
            error_text = str(e)

            if "Rate limit exceeded" in error_text:
                wait_seconds = 2 ** attempt
                print(
                    f"{stock_code} {year}/{month:02d} rate limited, "
                    f"retry in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                continue

            print(f"{stock_code} {year}/{month:02d} Fugle failed: {e}")
            return None
    else:
        print(f"{stock_code} {year}/{month:02d} failed after retries")
        return None

    data = result.get("data", [])

    if not data:
        print(f"{stock_code} {year}/{month:02d} Fugle no data")
        return None

    df = pd.DataFrame(data)

    df = df.rename(
        columns={
            "date": "日期",
            "open": "開盤價",
            "high": "最高價",
            "low": "最低價",
            "close": "收盤價",
            "volume": "成交股數",
            "turnover": "成交金額",
            "change": "漲跌價差",
        }
    )

    df["成交筆數"] = None
    df["註記"] = None

    if debug:
        print(df[["日期", "收盤價"]].tail())

    return df

def fetch_full_history(stock, stock_code, stock_name, start_year, start_month, debug=False):
    if start_year is None or start_month is None:
        print(f"找不到 {stock_code}{stock_name} 的上市年月")
        return None

    start_date = datetime(
        int(start_year),
        int(start_month),
        1
    )

    min_fugle_start = datetime(2010, 1, 1)

    if start_date < min_fugle_start:
        start_date = min_fugle_start

    print(f"API 要求改查 {start_date}")

    current = datetime.now()

    print(f"開始抓取 股票代碼: {stock_code}{stock_name} 全部歷史股價...")
    year, month = start_date.year, start_date.month

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            while (year < current.year) or (year == current.year and month <= current.month):
                month_start = datetime(year, month, 1)
                month_end = month_start + pd.offsets.MonthEnd(0)

                cur.execute("""
                    SELECT MAX(trade_date)
                    FROM stock_prices
                    WHERE stock_code = %s
                    AND trade_date BETWEEN %s AND %s
                """, (stock_code, month_start, month_end))

                max_trade_date = cur.fetchone()[0]

                is_current_month = (
                    year == current.year
                    and month == current.month
                )
                if (
                    max_trade_date is not None
                    and max_trade_date >= (month_end - timedelta(days=3)).date()
                    and not is_current_month
                ):
                    print(
                        f"{stock_code} {year}/{month:02d} "
                        f"最新資料已到 {max_trade_date}，跳過"
                    )
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                    continue

                result = fetch_month_data(stock, stock_code, year, month, debug=debug)

                if isinstance(result, pd.DataFrame):
                    if debug:
                        print(result[["日期", "收盤價"]].tail())

                    # 加上股票代碼與名稱欄位
                    result.insert(0, "股票代碼", stock_code)
                    result.insert(1, "股票名稱", stock_name)
                    result["日期"] = pd.to_datetime(result["日期"])
                    sql = """
                        INSERT INTO stock_prices
                        (
                            stock_code,
                            stock_name,
                            trade_date,
                            volume,
                            turnover,
                            open,
                            high,
                            low,
                            close,
                            change,
                            transactions,
                            note
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (stock_code, trade_date)
                        DO UPDATE SET
                            stock_name = excluded.stock_name,
                            volume = excluded.volume,
                            turnover = excluded.turnover,
                            open = excluded.open,
                            high = excluded.high,
                            low = excluded.low,
                            close = excluded.close,
                            change = excluded.change,
                            transactions = excluded.transactions,
                            note = excluded.note
                        """
                    data = [
                        (
                            row["股票代碼"],
                            row["股票名稱"],
                            row["日期"],
                            row["成交股數"],
                            row["成交金額"],
                            row["開盤價"],
                            row["最高價"],
                            row["最低價"],
                            row["收盤價"],
                            row["漲跌價差"],
                            row["成交筆數"],
                            row["註記"]
                        )
                        for _, row in result.iterrows()
                    ]

                    cur.executemany(sql, data)
                    conn.commit()
                    print(f"Current Time: {datetime.now()}, Stock: {stock_code}{stock_name}, year/month: {year}/{month:02d} Done!")
                else:
                    print(f"{stock_code} {year}/{month:02d} result type: {type(result)}, value: {result}")
                    print(f"Current Time: {datetime.now()}, Stock: {stock_code}{stock_name}, year/month: {year}/{month:02d} Failed!")

                    # 下一個月
                month += 1
                if month > 12:
                    month = 1
                    year += 1

                time.sleep(1.0 + random.uniform(0.5, 1.0))
    print(f"{stock_code}{stock_name} 全部歷史資料寫入完成")

def fetch_all_stocks_history(debug=False):
    # 從 DB 讀取上市股票清單
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("""
                SELECT stock_code, stock_name, listed_date
                FROM stocks
                WHERE is_price_supported = TRUE
                AND delisted_date IS NULL
                AND listed_date IS NOT NULL
            """)
            rows = cur.fetchall()

    df = pd.DataFrame(rows)
    if df.empty:
        print("stocks table 沒有資料")
        return

    # 確保 listed_date 是 datetime
    df["listed_date"] = pd.to_datetime(df["listed_date"], errors="coerce")

    # 取年份與月份
    df["上市年"] = df["listed_date"].dt.year
    df["上市月"] = df["listed_date"].dt.month

    stock_list = list(df[["stock_code", "stock_name", "上市年", "上市月"]].itertuples(index=False, name=None))
    print(f"證券代號, 證券名稱和上市年月轉換完成! 共 {len(stock_list)} 檔股票")

    stock = get_fugle_stock_client()
    for stock_code, stock_name, year, month in stock_list:
        try:
            fetch_full_history(stock, stock_code, stock_name, year, month, debug)
        except Exception as e:
            print(f"{stock_code} 整體失敗: {e}")

def run():
    fetch_all_stocks_history(debug=False)