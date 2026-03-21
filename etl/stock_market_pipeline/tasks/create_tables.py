import os
import psycopg
from pathlib import Path

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

BASE_DIR = Path("/opt/airflow/etl/stock_market_pipeline/db/schema")

SQL_FILES = [
    "schema.sql",
    "stocks.sql",
    "stock_prices.sql"
]

def run():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for sql_file in SQL_FILES:
                path = BASE_DIR / sql_file
                print(f"Executing {path}")
                with open(path, "r") as f:
                    sql = f.read()
                cur.execute(sql)
    print("Database schema initialized")