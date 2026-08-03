from concurrent.futures import ThreadPoolExecutor

from analysis.market_validator import MarketValidator


class MarketScanner:

    def __init__(self, exchange):

        self.exchange = exchange
        self.validator = MarketValidator()

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

        validation = self.validator.validate(market)

        # Odrzuć słabe rynki
        if not validation["valid"]:
            return symbol, None

        market["market_score"] = validation["market_score"]
        market["validation"] = validation

        return symbol, market

    def scan_all(self, symbols):

        results = {}

        accepted = 0
        rejected = 0

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

                if market is None:

                    rejected += 1
                    continue

                accepted += 1

                results[symbol] = market

        print("\n===== MARKET VALIDATOR =====")
        print(f"Accepted : {accepted}")
        print(f"Rejected : {rejected}")
        print(f"Total    : {accepted + rejected}")

        return results