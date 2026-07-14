from concurrent.futures import ThreadPoolExecutor


class MarketScanner:

    def __init__(self, exchange):
        self.exchange = exchange

    def scan_market(self, symbol):
        closes = self.exchange.get_candles(symbol=symbol)
        return symbol, closes

    def scan_all(self, symbols):

        results = {}

        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [
                executor.submit(self.scan_market, symbol)
                for symbol in symbols
            ]

            for future in futures:
                symbol, closes = future.result()
                results[symbol] = closes

        return results