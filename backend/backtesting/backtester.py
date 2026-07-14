class Backtester:

    def run(self, results):

        total = len(results)

        buys = sum(1 for r in results if r["decision"] == "BUY")
        sells = sum(1 for r in results if r["decision"] == "SELL")
        waits = sum(1 for r in results if r["decision"] == "WAIT")

        print("\n========== BACKTEST REPORT ==========")
        print(f"Markets scanned : {total}")
        print(f"BUY signals     : {buys}")
        print(f"SELL signals    : {sells}")
        print(f"WAIT signals    : {waits}")