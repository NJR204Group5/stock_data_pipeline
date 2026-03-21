# 台股股票 / ETF 資料自動化搜集與分析系統

## 介紹

建立一套完整的資料工程流程，自動化蒐集台股股票與 ETF 資料，並透過資料建模與視覺化，提供投資分析與決策參考。

系統涵蓋：

* 資料抓取（ETL）
* 資料庫（PostgreSQL）
* 資料建模（dbt）
* 資料視覺化（Metabase）

---

## 系統架構

```
    TWSE API(取資料)
        ↓
    Airflow（排程）
        ↓
    PostgreSQL（資料庫）
        ↓
    dbt（資料轉換、資料分析）
        ↓
    Metabase（Dashboard）
```

---

## 技術

| 類別  | 工具         |
| --- | ---------- |
| 語言  | Python     |
| 排程  | Airflow    |
| 資料庫 | PostgreSQL |
| 建模  | dbt        |
| 視覺化 | Metabase   |
| 容器化 | Docker     |

---

## 資料流程（Data Pipeline）

1. 使用 Airflow DAG 定期抓取台股資料
2. 原始資料寫入 PostgreSQL
3. dbt 進行資料清洗與建模
4. Metabase 建立 Dashboard 提供視覺分析

---

## dbt Models

### 1 資料清洗

* `stg_stock_prices`

  * 資料型別轉換（date / numeric / bigint）

---

### 2 技術指標

* `stock_ma`

  * MA5 / MA20 / MA60（移動平均線）

* `stock_indicators`

  * 黃金交叉（Golden Cross）
  * 死亡交叉（Death Cross）
  * 多頭 / 空頭排列（Trend Type）

---

## Dashboard（Metabase）

### 股價與技術指標

* 收盤價 + MA5 / MA20 / MA60
* 顯示趨勢變化

---

### 買賣訊號分析

* 黃金交叉（買點）
* 死亡交叉（賣點）

---

### 成交量分析

* 成交量變化
* 爆量偵測

---

## 功能特色

* 自動化資料收集（Airflow）
* 可重現的資料轉換（dbt）
* 即時視覺化 Dashboard（Metabase）
* 技術分析指標整合
* 支援多股票查詢與比較

---

## 如何啟動專案

### 1 啟動 Docker

```bash
docker-compose up -d
```

### 2 開啟 Airflow

```text
http://localhost:8080
```

### 3 啟動 dbt

```bash
dbt run
```

### 4 開啟 Metabase

```text
http://localhost:3000
```

---

## 未來優化方向

* 加入更多技術指標
* 加入其他股票市場
* 部署至 GCP / AWS
* 建立 API（FastAPI）