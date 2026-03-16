import psycopg
from pathlib import Path

DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "stockdb",
    "user": "stockuser",
    "password": "stockpass"
}

BASE_DIR = Path("/opt/airflow/pipeline/db/schema")

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