-- 聚合成 每日統計表
-- 計算開盤/最高/最低/收盤/成交量/平均價
{{ config(materialized='table') }}

with staged as (
    select *
    from {{ ref('stg_stock_prices') }}
)

select
    stock_code,
    trade_date,
    min(open) as open,  -- 當日開盤價，通常是最早的價格
    max(high) as high,
    min(low) as low,
    max(close) as close, -- 當日收盤價，通常是最後的價格
    sum(volume) as volume,
    avg(close) as avg_price
from staged
group by stock_code, trade_date
order by stock_code, trade_date