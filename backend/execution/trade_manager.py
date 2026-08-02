from brain.learning_memory import LearningMemory
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
        histogram,
        atr,
        ema10,
        ema20,
        trend,
        volume_ratio,
        volume_spike,
        brain_version
    ):

        if self.portfolio.has_position(symbol):
            return False

        if size <= 0:
            print(f"[TRADE MANAGER] Invalid position size ({size})")
            return False

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

        self.learning.create_trade(
            symbol=symbol,
            decision="BUY",
            entry_price=price,
            size=size,
            score=score,
            confidence=confidence,
            rsi=rsi,
            histogram=histogram,
            atr=atr,
            ema10=ema10,
            ema20=ema20,
            trend=trend,
            volume_ratio=volume_ratio,
            volume_spike=volume_spike,
            brain_version=brain_version
        )

        print(f"[TRADE MANAGER] BUY completed -> {symbol}")

        return True

    def sell(
        self,
        symbol,
        price
    ):

        if not self.portfolio.has_position(symbol):
            return False

        position = self.portfolio.positions[symbol].copy()

        trade_size = position["size"]

        profit = self.portfolio.sell(
            symbol,
            price
        )

        if profit is None:
            return False

        paper_sell(
            symbol=symbol,
            price=price,
            size=trade_size
        )

        self.learning.close_trade(
            symbol=symbol,
            exit_price=price,
            position=position
        )

        print(
            f"[TRADE MANAGER] SELL completed -> {symbol} | Profit: {round(profit, 2)} USDT"
        )

        return profit