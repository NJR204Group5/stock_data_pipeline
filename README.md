# AI-Powered Stock Data Platform

An end-to-end data engineering project that builds a scalable **AI-Powered Stock Data Platform**, covering data ingestion, transformation, storage, and visualization for financial analysis.

---

## Overview

This project follows a modern data stack architecture, separating data ingestion, storage, transformation, and visualization layers.
It implements a complete end-to-end data pipeline for stock market data, designed to be scalable, maintainable, and analytics-ready.
In addition to traditional data engineering workflows, the platform also integrates LLM-powered analytics and Retrieval-Augmented Generation (RAG) capabilities.

The system supports:
- AI-generated stock analysis summaries
- Semantic document search using pgvector
- Embedding pipelines powered by Gemini
- RAG-based question answering APIs
- AI response caching for performance optimization

### Key Components

- **API Service**
  Provide stock analytics APIs using FastAPI

- **LLM Integration**
  Generate AI-powered stock analysis summaries using Gemini

- **RAG Pipeline**
  Build Retrieval-Augmented Generation workflows with embeddings and pgvector

- **Semantic Search**
  Perform vector similarity search for contextual document retrieval

- **AI Summary Cache**
  Store generated AI summaries in PostgreSQL to reduce LLM API usage

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

To design a scalable AI-powered data platform for stock market analytics, combining modern data engineering workflows with LLM-powered financial analysis and RAG capabilities.

---

## Architecture
```text
          +-----------------------------+
          |        Data Sources         |
          | (TWSE / TPEx / Fugle / TXT) |
          +--------------+--------------+
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
                |  + pgvector      |
                +--------+---------+
                         |
          +--------------+--------------+
          |                             |
          v                             v
+-------------------+        +-------------------+
| dbt Transformation|        | Embedding Pipeline|
+--------+----------+        +--------+----------+
         |                             |
         v                             v
+------------------+         +--------------------+
| Analytics Layer  |         | RAG Knowledge Base |
+------------------+         +--------------------+
         ^                             ^
         |                             |
+------------------+         +---------------------+
| Apache Airflow   |         | Gemini Embedding API|
+------------------+         +---------------------+
                         |
                         v
                +------------------+
                | FastAPI Service  |
                | AI / RAG APIs    |
                +------------------+
```

---

## Tech Stack

- **Language**: Python, SQL
- **Orchestration**: Apache Airflow  
- **Transformation**: dbt  
- **Database**: PostgreSQL
- **Visualization**: Metabase
- **Data Sources**:  
  - TWSE OpenAPI
  - TPEx OpenAPI
  - Fugle Market Data API
- **Backend API**: FastAPI
- **LLM**: Gemini API
- **Vector Database**: pgvector
- **AI / RAG**: Embedding-based Retrieval-Augmented Generation

---

## Data Pipeline

1. Use Airflow DAGs to periodically fetch Taiwan stock market data  
2. Store raw and transformed data in PostgreSQL  
3. Transform and model data using dbt  
4. Generate embeddings using Gemini Embedding API  
5. Store vector embeddings in pgvector  
6. Provide AI-powered APIs using FastAPI  
7. Support RAG-based semantic search and question answering  
8. Serve analytical dashboards through Metabase

### Incremental Refresh Strategy

The historical ingestion pipeline uses an incremental refresh strategy:

- Historical completed months are automatically skipped
- Current month data is automatically refreshed
- Recent market data can be safely re-fetched using PostgreSQL upsert logic
- Exponential backoff is applied for API rate-limit handling

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

## AI & RAG Features

### AI Stock Summary

The platform integrates Gemini LLM to generate AI-powered stock analysis summaries based on technical indicators.

Features:
- Trend analysis
- Risk assessment
- Short-term market observations

### Embedding Pipeline

The system uses Gemini Embedding API to generate vector embeddings for financial documents and stores them in PostgreSQL with pgvector.

Pipeline:
txt documents → chunking → embeddings → pgvector

### Semantic Search

The platform supports vector similarity search using pgvector for semantic retrieval.

### RAG Chat API

FastAPI provides RAG-based APIs that:
1. Convert user questions into embeddings
2. Retrieve similar documents using pgvector
3. Generate contextual answers using Gemini

### AI Summary Cache

Generated AI summaries are cached in PostgreSQL to:
- Reduce API costs
- Improve response latency
- Minimize repeated LLM requests

## ETL Reliability Features

- Incremental monthly refresh strategy
- Exponential backoff retry handling
- API rate limit protection
- Missing market data detection
- Idempotent PostgreSQL upsert ingestion
- Automatic current-month market refresh

## Features

- Automated ETL pipelines with Apache Airflow
- Reproducible data transformations using dbt
- Technical indicator analysis (MA / Golden Cross / Trend)
- AI-powered stock summaries using Gemini
- Embedding pipeline with pgvector
- Hybrid RAG-based stock analysis
- Technical indicator enhanced AI responses
- Incremental financial ETL pipelines
- Fugle-based historical market ingestion
- Semantic vector search
- RAG-based stock Q&A APIs
- AI summary caching with PostgreSQL
- FastAPI-based backend services
- AI-powered frontend built with Next.js
- Real-time analytical dashboards with Metabase

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