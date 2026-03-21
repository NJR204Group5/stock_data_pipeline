import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

# 加入 pipeline path
sys.path.append("/opt/airflow/etl")

from stock_market_pipeline.tasks.create_tables import run as create_tables

# DAG 設定
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def wrapped_create_tables():
    logging.info("Start creating tables...")
    create_tables()
    logging.info("Tables created successfully.")

with DAG(
    'create_tables_dag',
    default_args=default_args,
    description='DAG to create database tables once',
    schedule='@once',
    start_date=datetime(2026, 3, 12),
    catchup=False,
    tags=['twse', 'db'],
) as dag:

    create_tables_task = PythonOperator(
        task_id='create_tables_task',
        python_callable=wrapped_create_tables
    )

    # create_tables_task