class Brain:

    def __init__(self):

        self.version = "0.1"

    def analyze(
        self,
        symbol,
        ema10,
        ema20,
        rsi,
        histogram,
        atr
    ):

        score = 0

        reasons = []

        # EMA
        if ema10 > ema20:
            score += 30
            reasons.append("EMA Bullish")
        else:
            score -= 30
            reasons.append("EMA Bearish")

        # RSI
        if 55 <= rsi <= 70:
            score += 25
            reasons.append("Healthy RSI")

        elif rsi > 70:
            score -= 20
            reasons.append("Overbought")

        elif rsi < 30:
            score += 15
            reasons.append("Oversold")

        # MACD
        if histogram > 0:
            score += 25
            reasons.append("Positive MACD")
        else:
            score -= 25
            reasons.append("Negative MACD")

        # ATR
        if atr > 0:
            score += 10

        score = max(0, min(score, 100))

        if score >= 80:
            decision = "BUY"

        elif score <= 30:
            decision = "SELL"

        else:
            decision = "WAIT"

        confidence = score

        return {
            "decision": decision,
            "score": score,
            "confidence": confidence,
            "reasons": reasons
        }