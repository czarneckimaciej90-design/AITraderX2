from datetime import datetime

from portfolio.storage import PortfolioStorage


class Portfolio:

    def __init__(self, balance=1000, max_positions=5):

        self.start_balance = float(balance)
        self.balance = float(balance)
        self.max_positions = max_positions
        self.positions = {}

    def buy(self, symbol, price, size):

        if self.has_position(symbol):
            print(f"[PORTFOLIO] Position already exists: {symbol}")
            return False

        if size <= 0:
            print("[PORTFOLIO] Invalid position size")
            return False

        if len(self.positions) >= self.max_positions:
            print(
                f"[PORTFOLIO] Maximum positions reached ({self.max_positions})"
            )
            return False

        if self.balance < size:
            print("[PORTFOLIO] Not enough balance")
            return False

        self.balance -= size

        self.positions[symbol] = {

            "symbol": symbol,

            "entry": float(price),

            "current_price": float(price),

            "size": float(size),

            "open_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "highest_price": float(price),

            "lowest_price": float(price),

            "highest_profit": 0.0,

            "lowest_profit": 0.0,

            "update_count": 0,

            "exit_reason": ""

        }

        print(f"[PORTFOLIO] BUY {symbol} @ {round(price,8)}")
        print(f"[PORTFOLIO] Remaining Balance: {round(self.balance,2)} USDT")

        PortfolioStorage.save(self)

        return True

    def sell(self, symbol, price):

        if symbol not in self.positions:
            print(f"[PORTFOLIO] Position not found: {symbol}")
            return None

        trade = self.positions.pop(symbol)

        entry = trade["entry"]
        size = trade["size"]

        pnl_percent = (price - entry) / entry

        profit = size * pnl_percent

        self.balance += size + profit

        print(f"[PORTFOLIO] SELL {symbol}")
        print(f"Entry   : {round(entry,8)}")
        print(f"Exit    : {round(price,8)}")
        print(f"Profit  : {round(profit,2)} USDT")
        print(f"Balance : {round(self.balance,2)} USDT")

        PortfolioStorage.save(self)

        return round(profit, 2)

    def has_position(self, symbol):

        return symbol in self.positions

    def get_position(self, symbol):

        return self.positions.get(symbol)

    def invested_balance(self):

        total = 0

        for position in self.positions.values():

            entry = position["entry"]

            current = position["current_price"]

            size = position["size"]

            value = size * (current / entry)

            total += value

        return round(total, 2)

    def total_equity(self):

        return round(
            self.balance + self.invested_balance(),
            2
        )

    def show(self):

        invested = self.invested_balance()

        print("\n========== PORTFOLIO ==========")
        print(f"Start Balance : {round(self.start_balance,2)} USDT")
        print(f"Available     : {round(self.balance,2)} USDT")
        print(f"Invested      : {round(invested,2)} USDT")
        print(f"Total Equity  : {self.total_equity()} USDT")
        print(f"Open Positions: {len(self.positions)}/{self.max_positions}")

        if len(self.positions) == 0:

            print("No open positions.")

        else:

            for symbol, data in self.positions.items():

                print(
                    f"{symbol} | "
                    f"Entry {round(data['entry'],8)} | "
                    f"Size {round(data['size'],2)} USDT | "
                    f"Updates {data['update_count']}"
                )

        print("===============================\n")

    def update_price(self, symbol, price):

        if symbol not in self.positions:
            return

        self.positions[symbol]["current_price"] = float(price)

        self.positions[symbol]["update_count"] += 1

    def load(self):

        if PortfolioStorage.load_into_portfolio(self):

            print("[PORTFOLIO] Portfolio restored.")

        else:

            print("[PORTFOLIO] New portfolio created.")