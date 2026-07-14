def calculate_score(ema10, ema20, rsi, histogram):

    score = 50    # start od neutralnego wyniku

    # EMA
    if ema10 > ema20:
        score += 15
    else:
        score -= 15

    # RSI
    if 55 <= rsi <= 60:
        score += 8
    elif 60 < rsi <= 65:
        score += 12
    elif 65 < rsi <= 70:
        score += 16
    elif rsi > 70:
        score -= 15
    elif rsi < 35:
        score -= 15

    # MACD
    if histogram > 1:
        score += 15
    elif histogram > 0.5:
        score += 10
    elif histogram > 0:
        score += 5
    elif histogram < -1:
        score -= 15
    else:
        score -= 5

    return max(0, min(score, 100))