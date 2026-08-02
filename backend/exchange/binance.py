import requests
import pandas as pd


class BinanceExchange:

    BASE_URL = "https://api.binance.com/api/v3"

    def __init__(self):
        self.name = "BINANCE"

    def connect(self):
        print("[OK] Connected to Binance")

    def get_price(self, symbol="BTCUSDT"):

        url = f"{self.BASE_URL}/ticker/price?symbol={symbol}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return float(data["price"])

    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="1m",
        limit=200
    ):

        url = (
            f"{self.BASE_URL}/klines"
            f"?symbol={symbol}"
            f"&interval={interval}"
            f"&limit={limit}"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        candles = response.json()

        dataframe = pd.DataFrame(
            candles,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore"
            ]
        )

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_asset_volume",
            "taker_buy_base",
            "taker_buy_quote"
        ]

        dataframe[numeric_columns] = (
            dataframe[numeric_columns]
            .astype(float)
        )

        dataframe["number_of_trades"] = (
            dataframe["number_of_trades"]
            .astype(int)
        )

        return dataframe