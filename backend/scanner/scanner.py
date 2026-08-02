from concurrent.futures import ThreadPoolExecutor


class MarketScanner:

    def __init__(self, exchange):

        self.exchange = exchange

    def scan_market(self, symbol):

        candles = self.exchange.get_candles(symbol=symbol)

        market = {

            "candles": candles,

            "opens": candles["open"].tolist(),

            "highs": candles["high"].tolist(),

            "lows": candles["low"].tolist(),

            "closes": candles["close"].tolist(),

            "volumes": candles["volume"].tolist(),

            "trades": candles["number_of_trades"].tolist()

        }

        return symbol, market

    def scan_all(self, symbols):

        results = {}

        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [
                executor.submit(
                    self.scan_market,
                    symbol
                )
                for symbol in symbols
            ]

            for future in futures:

                symbol, market = future.result()

                results[symbol] = market

        return results