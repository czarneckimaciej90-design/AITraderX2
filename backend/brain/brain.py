class Brain:

    def __init__(self):

        self.version = "0.6.0"

    def analyze(
        self,
        symbol,
        analysis
    ):

        # ==========================
        # INPUT
        # ==========================

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

        score = 50
        reasons = []

        buy_allowed = True

        # ==========================
        # MARKET QUALITY
        # ==========================

        if market_score >= 90:

            score += 5
            reasons.append("Excellent Market")

        elif market_score >= 80:

            reasons.append("High Market Quality")

        elif market_score >= 70:

            score -= 5
            reasons.append("Average Market")

        else:

            score -= 30
            buy_allowed = False
            reasons.append("Poor Market")

        # ==========================
        # EMA
        # ==========================

        if ema10 > ema20:

            score += 20
            reasons.append("EMA Bullish")

        else:

            score -= 20
            reasons.append("EMA Bearish")

        # ==========================
        # RSI
        # ==========================

        if 55 <= rsi <= 65:

            score += 20
            reasons.append("Strong RSI")

        elif 65 < rsi <= 70:

            score += 10
            reasons.append("RSI High")

        elif 50 <= rsi < 55:

            score += 10
            reasons.append("RSI Rising")

        elif 35 <= rsi < 45:

            score += 5
            reasons.append("Recovering RSI")

        elif 25 <= rsi < 35:

            score += 15
            reasons.append("Oversold Bounce")

        elif rsi > 80:

            score -= 30
            reasons.append("Extremely Overbought")

        elif rsi > 75:

            score -= 20
            reasons.append("Overbought")

        # ==========================
        # MACD
        # ==========================

        if histogram > 2:

            score += 25
            reasons.append("Very Strong MACD")

        elif histogram > 1:

            score += 20
            reasons.append("Strong MACD")

        elif histogram > 0:

            score += 10
            reasons.append("Positive MACD")

        elif histogram < -2:

            score -= 25
            reasons.append("Very Negative MACD")

        elif histogram < -1:

            score -= 20
            reasons.append("Strong Negative MACD")

        else:

            score -= 10
            reasons.append("Negative MACD")

        # ==========================
        # ATR
        # ==========================

        if atr <= 0:

            score -= 20
            buy_allowed = False
            reasons.append("No Volatility")

        elif atr < 0.001:

            score -= 10
            reasons.append("Low ATR")

        else:

            score += 5
            reasons.append("ATR Active")

        # ==========================
        # VOLUME
        # ==========================

        if volume_ratio < 0.15:

            score = min(score, 25)
            buy_allowed = False
            reasons.append("Volume Gate")

        elif volume_ratio < 0.30:

            score -= 30
            reasons.append("Extremely Low Volume")

        elif volume_ratio < 0.50:

            score -= 15
            reasons.append("Low Volume")

        elif volume_ratio < 0.80:

            score -= 5
            reasons.append("Weak Volume")

        elif volume_ratio >= 3:

            score += 15
            reasons.append("Huge Volume")

        elif volume_ratio >= 2:

            score += 10
            reasons.append("High Volume")

        elif volume_ratio >= 1.2:

            score += 5
            reasons.append("Good Volume")

        if volume_spike:

            score += 5
            reasons.append("Volume Spike")

        # ==========================
        # FINAL SCORE
        # ==========================

        score = max(
            0,
            min(score, 100)
        )

        confidence = score

        # ==========================
        # DECISION
        # ==========================

        if buy_allowed and score >= 75:

            decision = "BUY"

        elif score <= 25:

            decision = "SELL"

        else:

            decision = "WAIT"

        # ==========================
        # LEARNING DATA
        # ==========================

        learning_data = {

            "market_score": market_score,

            "ema_bullish": ema10 > ema20,

            "rsi": rsi,

            "histogram": histogram,

            "atr": atr,

            "volume_ratio": volume_ratio,

            "volume_spike": volume_spike

        }

        return {

            "decision": decision,

            "score": score,

            "confidence": confidence,

            "market_score": market_score,

            "reasons": reasons,

            "brain_version": self.version,

            "learning_data": learning_data

        }