def make_decision(ema10, ema20, rsi, histogram):

    if ema10 > ema20 and rsi > 55:
        return "BUY", 75

    if ema10 < ema20 and rsi < 45:
        return "SELL", 75

    return "WAIT", 50
