from concurrent.futures import ThreadPoolExecutor

from analysis.market_validator import MarketValidator


class MarketScanner:

    def __init__(self, exchange):

        self.exchange = exchange
        self.validator = MarketValidator()

    def scan_market(self, symbol):

        candles = self.exchange.get_candles(symbol=symbol)

        if candles is None or len(candles) == 0:
            return symbol, None

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

        # ZAWSZE zapisujemy wynik walidacji
        market["market_score"] = validation["market_score"]
        market["validation"] = validation

        # UWAGA:
        # Nie odrzucamy rynku tutaj.
        # Validator blokuje tylko nowe zakupy.
        # Otwarte pozycje nadal muszą być aktualizowane.
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
                    continue

                if market["validation"]["valid"]:
                    accepted += 1
                else:
                    rejected += 1

                results[symbol] = market

        print("\n===== MARKET VALIDATOR =====")
        print(f"Accepted : {accepted}")
        print(f"Rejected : {rejected}")
        print(f"Total    : {accepted + rejected}")

        return results