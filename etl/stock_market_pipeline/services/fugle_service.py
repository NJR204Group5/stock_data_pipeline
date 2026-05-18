import os

from fugle_marketdata import RestClient

def get_fugle_stock_client():
    api_key = os.getenv("FUGLE_API_KEY")

    if not api_key:
        raise ValueError("FUGLE_API_KEY is not set")

    client = RestClient(api_key=api_key)

    return client.stock