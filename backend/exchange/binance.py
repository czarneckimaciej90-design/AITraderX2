import requests

class BinanceExchange:

    def __init__(self):
        self.name = "BINANCE"

    def connect(self):
        print("[OK] Connected to Binance")

    def get_price(self):
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    
    def get_candles(self, symbol="BTCUSDT", interval="1m", limit=10):
         url = (
             f"https://api.binance.com/api/v3/klines"
             f"?symbol={symbol}&interval={interval}&limit={limit}"
         )

         response = requests.get(url)
         candles = response.json()
         closes = []
         for candle in candles:
             closes.append(float(candle[4]))
         return closes