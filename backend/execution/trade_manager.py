from datetime import datetime


class TradeManager:

    def __init__(self, portfolio):

        self.portfolio = portfolio
        self.portfolio = portfolio


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

            "time":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "symbol": symbol,

            "decision": "BUY",

            "entry_price": price,

            "size": size,

            "score": score,

            "confidence": confidence,

            "market_score": market_score,

            "market_validation":
                market_validation or {},


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


        self.portfolio.open_position(
            symbol=symbol,
            price=price,
            size=size,
            metadata=trade
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

        return True

