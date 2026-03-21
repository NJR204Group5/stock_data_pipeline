FROM apache/airflow:3.0.3

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# copy pipeline code
# COPY etl/stock_market_pipeline /opt/airflow/pipeline

# airflow user 預設就能使用 /opt/airflow/pipeline

# 複製 requirements.txt 到 container
# COPY requirements.txt /opt/airflow/requirements.txt