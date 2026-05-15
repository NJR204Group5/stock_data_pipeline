import requests


TPEX_STOCKS_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"

def fetch_tpex_stocks():
    response = requests.get(TPEX_STOCKS_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    stocks = []

    for item in data:
        stock_code = item.get("公司代號")
        stock_name = item.get("公司簡稱")
        industry = item.get("產業別")
        listed_date = item.get("上櫃日期") or item.get("掛牌日期")

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
            "market": "TPEX",
            "is_price_supported": True,
        })

    return stocks