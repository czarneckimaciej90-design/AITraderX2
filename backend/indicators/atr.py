def calculate_atr(closes, period=14):
    """
    Uproszczona wersja ATR.
    Liczy średnią zmianę pomiędzy kolejnymi cenami zamknięcia.
    """

    if len(closes) < period + 1:
        return 0

    ranges = []

    for i in range(1, len(closes)):
        ranges.append(abs(closes[i] - closes[i - 1]))

    atr = sum(ranges[-period:]) / period

    return round(atr, 4)