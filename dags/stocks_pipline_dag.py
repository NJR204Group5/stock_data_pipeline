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
from stock_market_pipeline.tasks.update_stocks_master import run as update_stocks_master

# DAG 設定
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def wrapped_run_stocks_to_db():
    logging.info("Start updating TWSE / TPEX listed stocks...")
    update_stocks_master()
    logging.info("Stocks updated successfully.")

with DAG(
    'stocks_pipline_dag',
    default_args=default_args,
    description='ETL pipeline for TWSE / TPEX stocks data',
    schedule='0 10 * * *',  # 每天 10:00 台灣時間, 分 時 日 月 星期
    start_date=datetime(2026, 3, 12, tzinfo=TW_TZ),
    catchup=False,
    tags=['twse', 'stocks'],
) as dag:

    update_stocks_db = PythonOperator(
        task_id='update_stocks_db',
        python_callable=wrapped_run_stocks_to_db
    )