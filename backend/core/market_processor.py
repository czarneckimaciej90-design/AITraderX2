from analysis.analysis_engine import AnalysisEngine


class MarketProcessor:

    def __init__(
        self,
        brain,
        portfolio,
        trade_manager,
        capital_manager,
        position_manager,
        memory,
        learning_memory
    ):

        self.brain = brain
        self.portfolio = portfolio
        self.trade_manager = trade_manager
        self.capital_manager = capital_manager
        self.position_manager = position_manager
        self.memory = memory
        self.learning_memory = learning_memory
        self.analysis = AnalysisEngine()

    def process(self, symbol, market):

        closes = market["closes"]

        if len(closes) < 20:
            return None

        analysis = self.analysis.analyze(market)

        trend = analysis["trend"]

        ema10 = analysis["ema"]["ema10"]
        ema20 = analysis["ema"]["ema20"]

        rsi = analysis["momentum"]["rsi"]
        histogram = analysis["momentum"]["histogram"]

        atr = analysis["volatility"]["atr"]

        volume_ratio = analysis["volume"]["ratio"]
        volume_spike = analysis["volume"]["spike"]

        market_score = analysis.get(
            "market",
            {}
        ).get(
            "score",
            100
        )

        market_validation = analysis.get(
            "market",
            {}
        ).get(
            "validation",
            {}
        )

        brain_result = self.brain.analyze(
            symbol,
            analysis
        )
        if self.portfolio.has_position(symbol):

            self.portfolio.update_price(
                symbol,
                closes[-1]
            )

            self.learning_memory.update_open_position(
                symbol,
                self.portfolio.positions[symbol]
            )

        return {

            "symbol": symbol,

            "price": closes[-1],

            "trend": trend,

            "decision": brain_result["decision"],

            "score": brain_result["score"],

            "confidence": brain_result["confidence"],

            "reasons": brain_result["reasons"],

            "brain_version": brain_result["brain_version"],

            "learning_data": brain_result.get(
                "learning_data",
                {}
            ),

            "ema10": ema10,
            "ema20": ema20,

            "rsi": rsi,
            "histogram": histogram,

            "atr": atr,

            "volume_ratio": volume_ratio,
            "volume_spike": volume_spike,

            "market_score": market_score,
            "market_validation": market_validation

        }

    def execute_buy(self, processed):

        symbol = processed["symbol"]

        # ===========================
        # MARKET VALIDATOR
        # ===========================

        if not processed["market_validation"].get("valid", False):
            return

        # ===========================
        # BRAIN DECISION
        # ===========================

        if processed["decision"] != "BUY":
            return

        # ===========================
        # POSITION EXISTS
        # ===========================

        if self.portfolio.has_position(symbol):
            return

        # ===========================
        # CAPITAL MANAGER
        # ===========================

        position_size = self.capital_manager.calculate_position_size(
            processed["score"],
            processed["confidence"],
            len(self.portfolio.positions)
        )

        if position_size <= 0:
            return

        # ===========================
        # EXECUTE BUY
        # ===========================

        self.trade_manager.buy(
            symbol=symbol,
            price=processed["price"],
            size=position_size,
            score=processed["score"],
            confidence=processed["confidence"],
            rsi=processed["rsi"],
            histogram=processed["histogram"],
            atr=processed["atr"],
            ema10=processed["ema10"],
            ema20=processed["ema20"],
            trend=processed["trend"],
            volume_ratio=processed["volume_ratio"],
            volume_spike=processed["volume_spike"],
            brain_version=processed["brain_version"],
            market_score=processed["market_score"],
            market_validation=processed["market_validation"]
        )

    def execute_sell(self, processed):

        symbol = processed["symbol"]

        if not self.portfolio.has_position(symbol):
            return

        exit_decision = self.position_manager.evaluate(
            self.portfolio.positions[symbol],
            processed["price"],
            processed["score"]
        )

        if exit_decision == "SELL":

            self.trade_manager.sell(
                symbol,
                processed["price"]
            )

    def save_result(self, processed, results):

        result = {

            "symbol": processed["symbol"],

            "trend": processed["trend"],

            "decision": processed["decision"],

            "confidence": processed["confidence"],

            "score": processed["score"],

            "rsi": processed["rsi"],

            "market_score": processed["market_score"],

            "volume_ratio": processed["volume_ratio"]

        }

        results.append(result)

        self.memory.save(result)

    def print_analysis(self, processed):

        print("--------------------------------")
        print(f"Symbol      : {processed['symbol']}")
        print(f"Price       : {processed['price']}")
        print(f"Trend       : {processed['trend']}")
        print(f"Decision    : {processed['decision']}")
        print(f"Score       : {processed['score']}")
        print(f"Confidence  : {processed['confidence']}%")
        print(f"RSI         : {round(processed['rsi'], 2)}")
        print(f"ATR         : {processed['atr']}")
        print(f"Volume x    : {processed['volume_ratio']}")
        print(f"VolumeSpike : {processed['volume_spike']}")
        print(f"MarketScore : {processed['market_score']}")
        print(f"Brain       : {processed['brain_version']}")
        print(
            f"Reasons     : {', '.join(processed['reasons'])}"
        )
