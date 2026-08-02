def calculate_score(
    ema10,
    ema20,
    rsi,
    histogram
):

    score = 50

    # ====================================
    # EMA TREND
    # ====================================

    if ema10 > ema20:
        score += 15
    else:
        score -= 15

    # ====================================
    # RSI
    # ====================================

    if 55 <= rsi <= 65:

        score += 15

    elif 50 <= rsi < 55:

        score += 8

    elif 65 < rsi <= 70:

        score += 8

    elif 70 < rsi <= 80:

        score -= 8

    elif rsi > 80:

        score -= 18

    elif 35 <= rsi < 50:

        score -= 5

    else:
        # RSI <35
        score += 5

    # ====================================
    # MACD Histogram
    # ====================================

    if histogram > 0:

        score += 15

    elif histogram < 0:

        score -= 15

    # ====================================
    # BONUS
    # ====================================

    if (
        ema10 > ema20
        and histogram > 0
        and 55 <= rsi <= 68
    ):

        score += 8

    # ====================================
    # KARA
    # ====================================

    if (
        ema10 < ema20
        and histogram < 0
        and rsi > 70
    ):

        score -= 10

    return max(0, min(score, 100))