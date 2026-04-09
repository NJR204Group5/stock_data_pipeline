-- 將 raw stock_prices 清理成 統一格式
-- trade_date 轉成 date，價格轉成 numeric，volume 轉成 bigint
-- materialized = view
{{ config(materialized='view') }}

with raw as (
    select
        stock_code,
        stock_name,
        trade_date::date as trade_date,
        open::numeric as open,
        high::numeric as high,
        low::numeric as low,
        close::numeric as close,
        volume::bigint as volume
    from {{ source('raw', 'stock_prices') }}
)

select *
from raw