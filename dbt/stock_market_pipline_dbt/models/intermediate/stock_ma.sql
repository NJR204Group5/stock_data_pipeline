select
    stock_code,
    trade_date,
    close,

    avg(close) over (
        partition by stock_code 
        order by trade_date 
        rows between 4 preceding and current row -- 今天 + 前4天 = 5天平均(MA5)
    ) as ma5,

    avg(close) over (
        partition by stock_code 
        order by trade_date 
        rows between 19 preceding and current row -- 今天 + 前19天 = 20天平均(MA20)
    ) as ma20,

    avg(close) over (
        partition by stock_code 
        order by trade_date 
        rows between 59 preceding and current row -- 今天 + 前59天 = 60天平均(MA60)
    ) as ma60

from {{ ref('stg_stock_prices') }}