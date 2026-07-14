def detect_trend(ema10, ema20, rsi):
    if ema10 > ema20 and rsi > 55:
        return "UPTREND"

    elif ema10 < ema20 and rsi < 45:
        return "DOWNTREND"

    return "SIDEWAYS"