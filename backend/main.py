"""
====================================================
AI Trader X Platform
Version: 0.0.1
====================================================
Main application entry point.
"""

from datetime import datetime
from config.settings import Settings
from logs.logger import log
from exchange.binance import BinanceExchange
from indicators.ema import calculate_ema, ema_signal


class ATXCore:
    def __init__(self):
        self.version = "0.0.1"
        self.started = datetime.now()

    def start(self):
        settings = Settings()

        print("=" * 60)
        print(settings.APP_NAME)
        print(f"Version : {settings.VERSION}")
        print(f"Exchange : {settings.EXCHANGE}")
        print(f"Demo Mode : {settings.DEMO_MODE}")
        print(f"Start Balance : £{settings.START_BALANCE}")
        print("=" * 60)

        print("AI Trader X Platform")
        print(f"Version : {self.version}")
        print(f"Started : {self.started}")
        print("=" * 60)
        print("[OK] Core Engine")
        print("[OK] System Initialised")
        print("[WAIT] Loading modules...")
        exchange = BinanceExchange()
        exchange.connect()

        price = exchange.get_price()
        print(f"BTC Price : ${price}") 

        closes = exchange.get_candles()

        print("Last 100 candles")

        for close in closes:
            print(f"Close: {close}")

        ema10 = calculate_ema(closes, 10)
        print(f"EMA 10: {ema10}")

        signal, ema10, ema20 = ema_signal(closes)
        print(f"EMA10: {ema10}")
        print(f"EMA20: {ema20}")
        print(f"Signal: {signal}")

        log("ATX Platform uruchomiona poprawnie.")


if __name__ == "__main__":
    app = ATXCore()
    app.start()