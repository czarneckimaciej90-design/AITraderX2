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

    print(f"Markets found: {len(markets)}")
    print("AAPLBUSDT:", "AAPLBUSDT" in markets)
    print("AMZNBUSDT:", "AMZNBUSDT" in markets)
    print("TQQQBUSDT:", "TQQQBUSDT" in markets)
    print("SOXSBUSDT:", "SOXSBUSDT" in markets)
    print("Total:", len(markets))

    return markets