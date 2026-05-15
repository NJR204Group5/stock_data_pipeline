import requests


TWSE_STOCKS_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"

def fetch_twse_stocks():
    response = requests.get(TWSE_STOCKS_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    stocks = []

    for item in data:
        stock_code = item.get("公司代號")
        stock_name = item.get("公司簡稱")
        industry = item.get("產業別")
        listed_date = item.get("上市日期")

        if not stock_code or not stock_name:
            continue

        stocks.append({
            "stock_code": stock_code,
            "stock_name": stock_name,
            "category": "股票",
            "isin_code": None,
            "listed_date": listed_date,
            "industry": industry,
            "delisted_date": None,
            "market": "TWSE",
            "is_price_supported": True,
        })

    return stocks