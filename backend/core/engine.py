from exchange.markets import get_markets
import time

from indicators.ema import ema_signal
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.atr import calculate_atr

from analysis.trend import detect_trend


class Engine:

    def __init__(
        self,
        exchange=None,
        scanner=None,
        portfolio=None,
        position_manager=None,
        brain=None,
        trade_manager=None,
        capital_manager=None,
        memory=None,
        backtester=None,
        statistics=None,
        processor=None,
        performance=None
    ):

        self.exchange = exchange
        self.scanner = scanner
        self.portfolio = portfolio
        self.position_manager = position_manager

        # Kolejne moduły (na razie jeszcze niewykorzystywane)
        self.brain = brain
        self.trade_manager = trade_manager
        self.capital_manager = capital_manager
        self.memory = memory
        self.backtester = backtester
        self.statistics = statistics
        self.processor = processor
        self.performance = performance

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

                results = self.process_market()

                self.show_top_opportunities(
                    results
                )

                self.show_portfolio()

                self.show_performance()

                self.run_backtest(
                    results
                )

                self.show_statistics()

            except Exception as e:

                print(
                    f"[ENGINE ERROR] {e}"
                )

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
        print(f" MARKET CYCLE #{self.cycle}")
        print("==============================")

        # BTC PRICE
        if self.exchange:

            try:

                btc_price = self.exchange.get_price()

                print(f"BTC Price : {btc_price}")

            except Exception as e:

                print(f"[ENGINE] BTC ERROR: {e}")

        # MARKET SCAN
        print("\n===== MARKET SCANNER =====")

        symbols = get_markets()

        if len(symbols) == 0:

            print("[ENGINE] No symbols received.")

            self.market_data = {}

            return self.market_data

        self.market_data = self.scanner.scan_all(symbols)

        print(f"Markets scanned : {len(self.market_data)}")

        if len(self.market_data) == 0:

            print("[WARNING] Scanner returned 0 markets.")

        else:

            print("[OK] Market scan completed.")

        self.check_positions()

        return self.market_data

    def get_market_data(self):

        return self.market_data

    def get_cycle(self):

        return self.cycle

    def check_positions(self):

        if self.portfolio is None:

            return

        print("\n===== POSITION CHECK =====")

        if len(self.portfolio.positions) == 0:

            print("No open positions.")

            return

        for symbol in self.portfolio.positions.keys():

            print(f"Checking {symbol}...")

            if self.position_manager:

                print("Position Manager : ACTIVE")

            else:

                print("Position Manager : DISABLED")

    def process_market(self):

        results = []

        if not self.market_data:
            return results

        print("\n========== MARKET ANALYSIS ==========")

        for symbol, market in self.market_data.items():

            processed = self.processor.process(
                symbol,
                market
            )

            if processed is None:
                continue

            self.processor.print_analysis(
                processed
            )

            self.processor.execute_buy(
                processed
            )

            self.processor.execute_sell(
                processed
            )

            self.processor.save_result(
                processed,
                results
            )

        return results

    def show_top_opportunities(self, results):

        print("\n==============================")
        print(" TOP OPPORTUNITIES ")
        print("==============================")

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        for result in results[:10]:

            print(
                f"{result['symbol']} | "
                f"SCORE {result['score']}/100 | "
                f"{result['decision']} | "
                f"CONF {result['confidence']}% | "
                f"RSI {round(result['rsi'], 2)}"
            )

    def show_portfolio(self):

        print("\n==============================")
        print(" PORTFOLIO STATUS ")
        print("==============================")

        if self.portfolio:

            self.portfolio.show()


    def show_performance(self):

        print("\n==============================")
        print(" PERFORMANCE ")
        print("==============================")

        if self.performance:

            self.performance.report()


    def run_backtest(self, results):

        print("\n==============================")
        print(" BACKTEST REPORT ")
        print("==============================")
        if self.backtester:

            try:

                self.backtester.run(
                    results
                )

            except Exception as e:

                print(
                    f"[BACKTEST ERROR] {e}"
                )

    def show_statistics(self):

        print("\n==============================")
        print(" BRAIN STATISTICS ")
        print("==============================")

        if self.statistics:

            try:

                self.statistics.report()

            except Exception as e:

                print(
                    f"[STATISTICS ERROR] {e}"
                )
