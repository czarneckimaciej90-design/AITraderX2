class Brain:

    def __init__(self):
        self.version = "0.5.0"

    def analyze(
        self,
        symbol,
        analysis
    ):

        ema10 = analysis["ema"]["ema10"]
        ema20 = analysis["ema"]["ema20"]

        rsi = analysis["momentum"]["rsi"]
        histogram = analysis["momentum"]["histogram"]

        atr = analysis["volatility"]["atr"]

        volume_ratio = analysis["volume"]["ratio"]
        volume_spike = analysis["volume"]["spike"]

        score = 50
        reasons = []

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

        elif 50 <= rsi < 55:

            score += 10
            reasons.append("RSI Rising")

        elif 65 < rsi <= 70:

            score += 5
            reasons.append("RSI High")

        elif rsi > 75:

            score -= 20
            reasons.append("Overbought")

        elif rsi < 30:

            score += 10
            reasons.append("Oversold")

        # ==========================
        # MACD
        # ==========================

        if histogram > 1:

            score += 20
            reasons.append("Strong MACD")

        elif histogram > 0:

            score += 10
            reasons.append("Positive MACD")

        elif histogram < -1:

            score -= 20
            reasons.append("Strong Negative MACD")

        else:

            score -= 10
            reasons.append("Negative MACD")

        # ==========================
        # ATR
        # ==========================

        if atr > 0:

            score += 5
            reasons.append("ATR Active")

        # ==========================
        # VOLUME
        # ==========================

        if volume_ratio >= 3:

            score += 15
            reasons.append("Huge Volume")

        elif volume_ratio >= 2:

            score += 10
            reasons.append("High Volume")

        elif volume_ratio >= 1.2:

            score += 5
            reasons.append("Good Volume")

        elif volume_ratio < 0.3:

            score -= 20
            reasons.append("Very Low Volume")

        elif volume_ratio < 0.5:

            score -= 10
            reasons.append("Low Volume")

        elif volume_ratio < 0.8:

            score -= 5
            reasons.append("Weak Volume")

        if volume_spike:

            reasons.append("Volume Spike")

        # ==========================
        # LIMIT SCORE
        # ==========================

        score = max(0, min(score, 100))

        # ==========================
        # DECISION
        # ==========================

        if score >= 75:

            decision = "BUY"

        elif score <= 25:

            decision = "SELL"

        else:

            decision = "WAIT"

        confidence = score

        return {

            "decision": decision,

            "score": score,

            "confidence": confidence,

            "reasons": reasons,

            "brain_version": self.version

        }