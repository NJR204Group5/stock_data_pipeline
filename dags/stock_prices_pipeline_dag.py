import sys
from datetime import datetime, timedelta

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging
from airflow.sensors.external_task import ExternalTaskSensor

# 設定台灣時區
TW_TZ = pendulum.timezone("Asia/Taipei")

# 加入 pipeline path
sys.path.append("/opt/airflow/etl")

from stock_market_pipeline.config import HEADERS
from stock_market_pipeline.tasks.save_stocks_prices_to_db import run as run_stock_prices_to_db

# DAG 設定
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def wrapped_run_stock_prices_to_db():
    logging.info("Start updating stock prices...")
    run_stock_prices_to_db()
    logging.info("Stock prices updated successfully.")

with DAG(
    'stock_prices_pipline_dag',
    default_args=default_args,
    description='ETL pipeline for TWSE stock prices data',
    schedule='0 17 * * *',  # 每天 17:00 台灣時間, 分 時 日 月 星期
    start_date=datetime(2026, 3, 12, tzinfo=TW_TZ),
    catchup=False,
    max_active_runs=1,
    tags=['twse', 'stock_prices'],
) as dag:

    update_stock_prices = PythonOperator(
        task_id='update_stock_prices',
        python_callable=wrapped_run_stock_prices_to_db
    )