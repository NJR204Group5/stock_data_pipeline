from contextlib import contextmanager

import psycopg
from psycopg import OperationalError

# PostgreSQL 連線設定，依 Docker 設定修改
DB_CONFIG = {
    "host": "localhost",        # 本機執行
    # "host": "postgres",        # Docker 對外的 port 對應的 host
    "port": 5432,               # Docker PostgreSQL port
    "dbname": "stockdb",        # 資料庫名稱
    "user": "stockuser",         # Docker 建立時的帳號
    "password": "stockpass"      # Docker 建立時設定的密碼
}

@contextmanager
def get_connection():
    conn = psycopg.connect(**DB_CONFIG)
    try:
        yield conn
    except OperationalError as e:
        print(f"PostgreSQL error: {e}")
        raise
    finally:
        if conn:
            conn.close()