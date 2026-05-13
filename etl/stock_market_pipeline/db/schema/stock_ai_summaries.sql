CREATE TABLE IF NOT EXISTS stock_ai_summaries (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    ai_summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_code, trade_date)
);
CREATE INDEX IF NOT EXISTS idx_stock_ai_summaries_code
ON stock_ai_summaries(stock_code);

CREATE INDEX IF NOT EXISTS idx_stock_ai_summaries_trade_date
ON stock_ai_summaries(trade_date);