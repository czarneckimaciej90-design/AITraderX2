import requests


def get_markets():

    url = "https://api.binance.com/api/v3/exchangeInfo"

    data = requests.get(url).json()

    markets = []

    for symbol in data["symbols"]:

        if (
            symbol["status"] == "TRADING"
            and symbol["quoteAsset"] == "USDT"
        ):
            markets.append(symbol["symbol"])

    return markets