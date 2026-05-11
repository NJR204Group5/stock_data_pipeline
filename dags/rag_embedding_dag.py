import sys

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


sys.path.append("/opt/airflow/etl")

from stock_market_pipeline.tasks.embed_rag_documents import (
    run as embed_rag_documents
)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="rag_embedding_dag",

    default_args=default_args,

    start_date=datetime(2026, 3, 12),

    schedule="@once",

    catchup=False,

    tags=["rag", "embedding"],
) as dag:

    embedding_task = PythonOperator(
        task_id="embedding_task",
        python_callable=embed_rag_documents
    )