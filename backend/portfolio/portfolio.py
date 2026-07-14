from portfolio.storage import PortfolioStorage


class Portfolio:

    def __init__(self, balance=1000, max_positions=5):

        self.start_balance = balance
        self.balance = balance
        self.max_positions = max_positions
        self.positions = {}

    def buy(self, symbol, price, size):

        if len(self.positions) >= self.max_positions:
            print(f"[PORTFOLIO] Maximum positions reached ({self.max_positions})")
            return False

        if self.balance < size:
            print("[PORTFOLIO] Not enough balance")
            return False

        self.balance -= size

        self.positions[symbol] = {
            "entry": price,
            "size": size
        }

        print(f"[PORTFOLIO] BUY {symbol} @ {price}")
        print(f"[PORTFOLIO] Remaining Balance: {round(self.balance,2)} USDT")

        PortfolioStorage.save(self)

        return True

    def sell(self, symbol, price):

        if symbol not in self.positions:
            return None

        trade = self.positions.pop(symbol)

        pnl_percent = ((price - trade["entry"]) / trade["entry"])
        profit = trade["size"] * pnl_percent

        self.balance += trade["size"] + profit

        print(f"[PORTFOLIO] SELL {symbol}")
        print(f"Entry : {trade['entry']}")
        print(f"Exit  : {price}")
        print(f"Profit : {round(profit,2)} USDT")
        print(f"Balance : {round(self.balance,2)} USDT")

        PortfolioStorage.save(self)

        return profit

    def has_position(self, symbol):
        return symbol in self.positions

    def show(self):

        invested = sum(p["size"] for p in self.positions.values())

        print("\n========== PORTFOLIO ==========")
        print(f"Start Balance : {self.start_balance} USDT")
        print(f"Available     : {round(self.balance,2)} USDT")
        print(f"Invested      : {round(invested,2)} USDT")
        print(f"Open Positions: {len(self.positions)}/{self.max_positions}")

        for symbol, data in self.positions.items():
            print(
                f"{symbol} | Entry {data['entry']} | Size {data['size']} USDT"
            )

        print("===============================\n")
        
    def load(self):

        if PortfolioStorage.load_into_portfolio(self):

            print("[PORTFOLIO] Portfolio restored.")

        else:

            print("[PORTFOLIO] New portfolio created.")