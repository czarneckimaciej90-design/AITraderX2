def ema(values, period):
    alpha = 2 / (period + 1)
    ema_values = [values[0]]

    for price in values[1:]:
        ema_values.append(
            alpha * price + (1 - alpha) * ema_values[-1]
        )

    return ema_values


def calculate_macd(closes):
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)

    macd = []

    for a, b in zip(ema12, ema26):
        macd.append(a - b)

    signal = ema(macd, 9)

    histogram = []

    for m, s in zip(macd, signal):
        histogram.append(m - s)

    return (
        macd[-1],
        signal[-1],
        histogram[-1]
    )