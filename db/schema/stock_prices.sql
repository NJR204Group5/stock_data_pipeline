CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY, -- 自增主鍵
    stock_code VARCHAR(10) NOT NULL, -- 證券代碼
    stock_name VARCHAR(100) NOT NULL, -- 證券名稱
    trade_date DATE NOT NULL, -- 日期
    volume BIGINT, -- 成交股數
    turnover NUMERIC(20, 2), -- 成交金額
    open NUMERIC(10, 2), -- 開盤價
    high NUMERIC(10, 2), -- 最高價
    low NUMERIC(10, 2), -- 最低價
    close NUMERIC(10, 2), -- 收盤價
    change NUMERIC(10, 2), -- 漲跌價差
    transactions BIGINT, -- 成交筆數
    note TEXT, -- 註記

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新時間
);
-- 建立 唯一索引，確保資料表裡 同一支股票在同一天只能有一筆資料
CREATE UNIQUE INDEX IF NOT EXISTS uq_stock_date
ON stock_prices(stock_code, trade_date);

-- 常用索引
CREATE INDEX IF NOT EXISTS idx_stock_code ON stock_prices(stock_code);
CREATE INDEX IF NOT EXISTS idx_trade_date ON stock_prices(trade_date);
CREATE INDEX IF NOT EXISTS idx_stock_date_desc ON stock_prices(stock_code, trade_date DESC);

DROP TRIGGER IF EXISTS update_stock_prices_updated_at ON stock_prices;
-- 建立 trigger 更新 updated_at
CREATE TRIGGER update_stock_prices_updated_at
BEFORE UPDATE ON stock_prices
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();