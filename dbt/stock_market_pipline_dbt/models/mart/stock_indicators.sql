{{ config(materialized='table') }}

with ma as (
    select *
    from {{ ref('stock_ma') }}
    where ma60 is not null
)

select
    stock_code,
    stock_name,
    trade_date,
    close,
    ma5,
    ma20,
    ma60,
    stock_code || ' - ' || stock_name as stock_display,

    -- 黃金 / 死亡交叉
    case 
        when ma5 > ma20 
         and lag(ma5) over (partition by stock_code order by trade_date)
          <= lag(ma20) over (partition by stock_code order by trade_date)
        then 'golden_cross'

        when ma5 < ma20 
         and lag(ma5) over (partition by stock_code order by trade_date)
          >= lag(ma20) over (partition by stock_code order by trade_date)
        then 'death_cross'

        else 'none'
    end as cross_signal,

    -- 多頭 / 空頭排列
    case 
        when ma5 > ma20 and ma20 > ma60 then 'bullish'
        when ma5 < ma20 and ma20 < ma60 then 'bearish'
        else 'neutral'
    end as trend_type,

    -- 日報酬率 = (今天收盤 - 昨天收盤) / 昨天收盤
    (close - lag(close) over (partition by stock_code order by trade_date)) 
    / NULLIF(lag(close) over (partition by stock_code order by trade_date), 0) as daily_return,
    -- 累積報酬率 = (今天收盤 / 第一日收盤) - 1
    close / NULLIF(first_value(close) over (partition by stock_code order by trade_date), 0) - 1 as cumulative_return

from ma

