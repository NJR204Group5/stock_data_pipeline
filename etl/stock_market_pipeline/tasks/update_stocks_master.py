import os
from datetime import datetime

import psycopg

from stock_market_pipeline.fetch_twse_stocks import fetch_twse_stocks
from stock_market_pipeline.fetch_tpex_stocks import fetch_tpex_stocks
from stock_market_pipeline.services.fugle_service import get_fugle_stock_client

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def parse_date(value):
    if not value:
        return None

    value = str(value).strip()

    # 例如 112/01/01 民國年
    if "/" in value:
        parts = value.split("/")
        if len(parts[0]) == 3:
            year = int(parts[0]) + 1911
            return f"{year}-{parts[1]}-{parts[2]}"

    # 例如 20230101
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:8]}"

    # 例如 2023-01-01
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None

def upsert_stocks(stocks):
    sql = """
        INSERT INTO stocks (
            stock_code,
            stock_name,
            category,
            isin_code,
            listed_date,
            industry,
            delisted_date,
            market,
            is_price_supported
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (stock_code)
        DO UPDATE SET
            stock_name = EXCLUDED.stock_name,
            category = EXCLUDED.category,
            isin_code = EXCLUDED.isin_code,
            listed_date = EXCLUDED.listed_date,
            industry = EXCLUDED.industry,
            delisted_date = EXCLUDED.delisted_date,
            market = EXCLUDED.market,
            is_price_supported = EXCLUDED.is_price_supported,
            updated_at = CURRENT_TIMESTAMP
    """

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for stock in stocks:
                cur.execute(
                    sql,
                    (
                        stock["stock_code"],
                        stock["stock_name"],
                        stock["category"],
                        stock["isin_code"],
                        parse_date(stock["listed_date"]),
                        stock["industry"],
                        stock["delisted_date"],
                        stock["market"],
                        stock["is_price_supported"],
                    ),
                )

        conn.commit()

def validate_stock(stock_client, stock_code: str):
    try:
        stock_client.intraday.quote(
            symbol=stock_code
        )
        return True
    except Exception:
        return False

def run():
    twse_stocks = fetch_twse_stocks()
    tpex_stocks = fetch_tpex_stocks()

    stocks = twse_stocks + tpex_stocks

    print(f"TWSE stocks: {len(twse_stocks)}")
    print(f"TPEx stocks: {len(tpex_stocks)}")
    print(f"Total stocks: {len(stocks)}")

    stock_client = get_fugle_stock_client()

    for stock in stocks:
        stock["is_price_supported"] = validate_stock(stock_client, stock["stock_code"])

    upsert_stocks(stocks)

    print("Stocks master updated successfully.")