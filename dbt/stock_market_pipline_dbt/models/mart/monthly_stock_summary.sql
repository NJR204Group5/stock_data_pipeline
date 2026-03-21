-- 聚合成 月 K 線表
{{ config(materialized='table') }}

with daily as (
    select *
    from {{ ref('daily_stock_summary') }}
)

select
    stock_code,
    DATE_TRUNC('month', trade_date) as month,
    min(open) as open,
    max(high) as high,
    min(low) as low,
    max(close) as close,
    sum(volume) as volume,
    avg(close) as avg_price
from daily
group by stock_code, DATE_TRUNC('month', trade_date)
order by stock_code, month