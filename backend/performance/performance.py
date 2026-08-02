class Performance:

    def __init__(self, portfolio):

        self.portfolio = portfolio

        self.start_equity = portfolio.total_equity()

        self.last_equity = portfolio.total_equity()

        self.cycle = 0

    def report(self):

        self.cycle += 1

        equity = self.portfolio.total_equity()

        available = self.portfolio.balance

        invested = self.portfolio.invested_balance()

        cycle_profit = equity - self.last_equity

        total_profit = equity - self.start_equity

        roi = (total_profit / self.start_equity) * 100

        print("\n==============================")
        print(f" CYCLE #{self.cycle}")
        print("==============================")

        print(
            f"Cycle Profit : {cycle_profit:+.2f} USDT"
        )

        print(
            f"Total Profit : {total_profit:+.2f} USDT"
        )

        print(
            f"Equity       : {equity:.2f} USDT"
        )

        print(
            f"Available    : {available:.2f} USDT"
        )

        print(
            f"Invested     : {invested:.2f} USDT"
        )

        print(
            f"ROI          : {roi:+.2f}%"
        )

        self.last_equity = equity