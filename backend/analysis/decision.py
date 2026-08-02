def make_decision(
    ema10,
    ema20,
    rsi,
    histogram
):

    score = 0

    # EMA
    if ema10 > ema20:
        score += 40
    else:
        score -= 40

    # RSI
    if 55 <= rsi <= 70:
        score += 20

    elif rsi > 70:
        score -= 20

    elif rsi < 30:
        score += 10

    # MACD
    if histogram > 0:
        score += 20
    else:
        score -= 20

    confidence = max(0, min(score + 50, 100))

    if confidence >= 80:
        decision = "BUY"

    elif confidence <= 20:
        decision = "SELL"

    else:
        decision = "WAIT"

    return decision, confidence