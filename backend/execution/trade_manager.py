from datetime import datetime


class TradeManager:

    def __init__(
        self,
        portfolio,
        learning_memory=None
    ):

        self.portfolio = portfolio
        self.learning_memory = learning_memory

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
        brain_version,
        market_score=0,
        market_validation=None
    ):

        print("\n========== BUY ==========")
        print(f"Symbol : {symbol}")
        print(f"Price  : {price}")
        print(f"Size   : {size}")
        print("=========================")

        trade = {

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "symbol": symbol,

            "decision": "BUY",

            "entry_price": price,

            "size": size,

            "score": score,

            "confidence": confidence,

            "market_score": market_score,

            "market_validation": market_validation or {},

            "rsi": rsi,

            "histogram": histogram,

            "atr": atr,

            "ema10": ema10,

            "ema20": ema20,

            "trend": trend,

            "volume_ratio": volume_ratio,

            "volume_spike": volume_spike,

            "brain_version": brain_version,

            "result": "PENDING"

        }

        print("[LEARNING] TradeManager.buy() called")

        opened = self.portfolio.open_position(
            symbol=symbol,
            price=price,
            size=size,
            metadata=trade
        )

        print(f"[LEARNING] Portfolio opened = {opened}")

        if not opened:
            return None

        if self.learning_memory:

            print("[LEARNING] Saving trade")

            self.learning_memory.create_trade(
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
                brain_version=brain_version,
                market_score=market_score,
                market_validation=market_validation or {}
            )

        return trade

    def sell(
        self,
        symbol,
        price
    ):

        print("\n========== SELL ==========")
        print(f"Symbol : {symbol}")
        print(f"Price  : {price}")
        print("==========================")

        position = self.portfolio.get_position(symbol)

        if position is None:
            return False

        entry_price = position["entry"]

        profit_percent = (
            (price - entry_price)
            / entry_price
        ) * 100

        result = "SUCCESS"

        if profit_percent < 0:
            result = "LOSS"

        profit = self.portfolio.sell(
            symbol,
            price
        )

        if self.learning_memory:

            print(
                f"[LEARNING] Closing trade ({result})"
            )

            self.learning_memory.close_trade(
                symbol=symbol,
                exit_price=price,
                position=position
            )

        return profit