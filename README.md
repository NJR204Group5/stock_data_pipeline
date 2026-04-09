# Stock Data Pipeline

An end-to-end data engineering project that builds a scalable **stock data pipeline**, covering data ingestion, transformation, storage, and visualization for financial analysis.

---

## Overview

This project follows a modern data stack architecture, separating data ingestion, storage, transformation, and visualization layers.
It implements a complete end-to-end data pipeline for stock market data, designed to be scalable, maintainable, and analytics-ready.

### Key Components

- **Data Ingestion**  
  Collect stock market data from external APIs (e.g., TWSE)

- **Data Storage**  
  Store raw data in PostgreSQL as the centralized data warehouse

- **Data Transformation**  
  Use dbt to clean, transform, and model data into analytics-ready datasets

- **Workflow Orchestration**  
  Automate and schedule pipelines using Apache Airflow

- **Data Visualization**  
  Build interactive dashboards in Metabase for data exploration

### Objective

To design a **scalable, maintainable, and analytics-ready data pipeline** for stock market analysis.

---

## Architecture
    +------------------+
    |   Data Sources   |
    | (TWSE API)|
    +--------+---------+
             |
             v
    +------------------+
    | Data Ingestion   |
    | (Python Scripts) |
    +--------+---------+
             |
             v
    +------------------+
    |  PostgreSQL      |
    | (Raw Data Layer) |
    +--------+---------+
             |
             v
    +------------------+
    | dbt Transformation|
    | (Data Modeling)  |
    +--------+---------+
             |
             v
    +------------------+
    | Analytics Layer  |
    +------------------+
             ^
             |
    +------------------+
    |  Apache Airflow  |
    | (Orchestration)  |
    +------------------+

---

## Tech Stack

- **Language**: Python, SQL
- **Orchestration**: Apache Airflow  
- **Transformation**: dbt  
- **Database**: PostgreSQL
- **Visualization**: Metabase
- **Data Sources**:  
  - TWSE (Taiwan Stock Exchange)  

---

## Data Pipeline

1. Use Airflow DAGs to periodically fetch Taiwan stock market data  
2. Store raw data in PostgreSQL  
3. Transform and model data using dbt 
4. Serve analytical data through Metabase dashboards

---

## Database Schema (PostgreSQL)

PostgreSQL is used as the centralized data warehouse, with a schema optimized for performance, data integrity, and analytical workloads.
Raw data is stored in normalized tables, while dbt transforms the data into denormalized star schema models for downstream analytics.

### Core Tables

#### stocks

Stores static information about listed stocks.

- `stock_code` (PK)  
- `stock_name`  
- `industry`  
- `market`  
- `listed_date`  
- `delisted_date`  

**Features:**
- Indexed on `industry` and `listed_date`
- Automatically maintains `updated_at` via trigger

---

#### stock_prices

Stores daily trading data for each stock.

- `stock_code`  
- `trade_date`  
- `open`, `high`, `low`, `close`  
- `volume`, `turnover`  
- `transactions`  

**Features:**
- Unique constraint on (`stock_code`, `trade_date`)
- Indexed for time-series queries
- Supports fast lookup for historical analysis
- Automatic `updated_at` tracking via trigger

---

### Data Integrity & Automation

- **Triggers**
  - Automatically update `updated_at` on row updates

- **Indexes**
  - Optimized for:
    - Time-series queries (`trade_date`)
    - Stock-based queries (`stock_code`)
    - Combined queries (`stock_code`, `trade_date DESC`)

---

### Design Considerations

- Ensures **data consistency** with unique constraints  
- Optimized for **analytical queries and time-series analysis**  
- Supports downstream transformations in dbt  

---

## dbt Models

### 1. Staging Layer

- `stg_stock_prices`
  - Data type normalization (date, numeric, bigint)  
  - Data standardization for downstream processing 

---

### 2. Technical Indicators Layer

- `stock_ma`
  - Moving averages: MA5 / MA20 / MA60

- `stock_indicators`
  - Golden Cross
  - Death Cross
  - Bullish / Bearish trend classification

---

## Data Model (Star Schema)

The analytics layer is generated from dbt models and contains daily stock prices with technical indicators.  
It is optimized for dashboards, reporting, and stock analysis.

### dbt Models

1. **`stg_stock_prices`** – Cleans and normalizes raw stock prices.  
   - Converts `trade_date` to `DATE`, prices to `NUMERIC`, `volume` to `BIGINT`.  
   - Materialized as a **view**.

2. **`stock_ma`** – Calculates moving averages (MA5 / MA20 / MA60).  
   - Uses window functions over `stg_stock_prices`.

3. **`stock_indicators`** – Computes technical indicators and returns.  
   - Cross signals: golden cross / death cross  
   - Trend type: bullish / bearish / neutral  
   - Daily return & cumulative return  
   - Materialized as a **table** for analysis and dashboards

---

### Stock Indicators Table (`stock_indicators`)

| Column                  | Type      | Description |
|-------------------------|----------|------------|
| `stock_code`            | VARCHAR  | Stock code |
| `stock_name`            | VARCHAR  | Stock name |
| `trade_date`            | DATE     | Trading date |
| `close`                 | NUMERIC  | Closing price |
| `ma5`                   | NUMERIC  | 5-day moving average |
| `ma20`                  | NUMERIC  | 20-day moving average |
| `ma60`                  | NUMERIC  | 60-day moving average |
| `cross_signal`          | VARCHAR  | Golden Cross / Death Cross / None |
| `trend_type`            | VARCHAR  | Bullish / Bearish / Neutral trend |
| `daily_return`          | NUMERIC  | Daily return |
| `cumulative_return`     | NUMERIC  | Cumulative return |
| `stock_display`         | VARCHAR  | Stock display name (`stock_code - stock_name`) |

**Notes:**  
- The final analytics table is generated via dbt transformations:  
  `stg_stock_prices` → `stock_ma` → `stock_indicators`  
- Window functions are used to calculate moving averages, cross signals, and returns.  

---

### dbt Pipeline Overview

```text
stg_stock_prices → stock_ma → stock_indicators
```

---

## Dashboard (Metabase)

### Stock Price & Technical Indicators

- Closing price with MA5 / MA20 / MA60
- Trend visualization

---

### Trading Signal Analysis

- Golden Cross (buy signal) 
- Death Cross (sell signal)

---

### Return Analysis

- Cumulative returns 
- Daily return volatility 

---

## Features

- Automated data ingestion (Airflow)
- Reproducible data transformations (dbt)
- Real-time visualization dashboards (Metabase) 
- Integrated technical analysis indicators
- Flexible filtering by stock and date 

---

## Getting Started

### 1 Start Docker

```bash
docker-compose up -d
```

### 2 Access Airflow

```text
http://localhost:8080
```

### 3 Run dbt

```bash
dbt run
```

### 4 Access Metabase

```text
http://localhost:3000
```

---

## Future Improvements

* Add more technical indicators
* Support additional stock markets
* Deploy to cloud platforms (GCP / AWS)
* Build an API service (e.g., FastAPI)