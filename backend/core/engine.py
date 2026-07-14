from exchange.markets import get_markets
import time


class Engine:

    def __init__(
        self,
        exchange=None,
        scanner=None,
        portfolio=None,
        position_manager=None
    ):

        self.exchange = exchange
        self.scanner = scanner
        self.portfolio = portfolio
        self.position_manager = position_manager

        self.running = False
        self.market_data = {}
        self.cycle = 0

    def start(self):

        print("==============================")
        print(" AI TRADER X ENGINE STARTED ")
        print("==============================")

        self.running = True

        while self.running:

            try:
                self.run_cycle()

            except Exception as e:
                print(f"[ENGINE ERROR] {e}")

            print("\nWaiting 60 seconds...\n")

            time.sleep(60)

    def stop(self):

        self.running = False

        print("==============================")
        print(" ENGINE STOPPED ")
        print("==============================")

    def run_cycle(self):

        self.cycle += 1

        print("\n==============================")
        print(f" NEW MARKET CYCLE #{self.cycle}")
        print("==============================")

        # BTC Price
        if self.exchange:

            btc_price = self.exchange.get_price()

            print(f"BTC Price : {btc_price}")

        # Scanner
        print("\n===== MARKET SCANNER =====")

        symbols = get_markets()

        self.market_data = self.scanner.scan_all(symbols)

        print(f"Markets scanned : {len(self.market_data)}")

        if len(self.market_data) == 0:
            print("[WARNING] Scanner returned 0 markets.")
        else:
            print("[OK] Scanning finished.")

        # Portfolio
        self.check_positions()

        return self.market_data

    def get_market_data(self):

        return self.market_data

    def check_positions(self):

        if self.portfolio is None:
            return

        print("\n===== POSITION CHECK =====")

        if len(self.portfolio.positions) == 0:
            print("No open positions.")
            return

        for symbol in self.portfolio.positions:

            print(f"Checking {symbol}...")

            if self.position_manager:

                print("Position Manager : ACTIVE")