from brain.learning import LearningMemory
from execution.paper_trading import paper_buy, paper_sell


class TradeManager:

    def __init__(self, portfolio):

        self.portfolio = portfolio
        self.learning = LearningMemory()

    def buy(
        self,
        symbol,
        price,
        size,
        score,
        confidence,
        rsi,
        histogram
    ):

        success = self.portfolio.buy(
            symbol,
            price,
            size
        )

        if not success:
            return False

        paper_buy(
            symbol=symbol,
            price=price,
            size=size
        )

        self.learning.save_trade(
            symbol=symbol,
            decision="BUY",
            entry_price=price,
            size=size,
            score=score,
            confidence=confidence,
            rsi=rsi,
            histogram=histogram
        )

        print(f"[TRADE MANAGER] BUY completed: {symbol}")

        return True

    def sell(
        self,
        symbol,
        price
    ):

        if symbol not in self.portfolio.positions:
            return False

        trade_size = self.portfolio.positions[symbol]["size"]

        profit = self.portfolio.sell(
            symbol,
            price
        )

        paper_sell(
            symbol=symbol,
            price=price,
            size=trade_size
        )

        self.learning.update_trade(
            symbol,
            price
        )

        print(f"[TRADE MANAGER] SELL completed: {symbol}")

        return profit