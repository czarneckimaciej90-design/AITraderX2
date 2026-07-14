def calculate_ema(prices, period):
    if len(prices) < period:
        return None

    multiplier = 2 / (period + 1)

    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return ema


def ema_signal(closes):
    ema10 = calculate_ema(closes, 10)
    ema20 = calculate_ema(closes, 20)

    if ema10 is None or ema20 is None:
        return "HOLD", ema10, ema20

    if ema10 > ema20:
        signal = "BUY"
    elif ema10 < ema20:
        signal = "SELL"
    else:
        signal = "HOLD"

    return signal, ema10, ema20