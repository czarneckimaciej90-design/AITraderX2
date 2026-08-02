def analyze_candlestick(closes):

    if len(closes) < 5:

        return "UNKNOWN"

    o = closes[-2]
    c = closes[-1]

    previous = closes[-2]

    body = abs(c - o)

    # Doji
    if body < previous * 0.001:

        return "DOJI"

    # Bullish
    if c > o:

        if body > previous * 0.01:

            return "BULLISH"

    # Bearish
    if c < o:

        if body > previous * 0.01:

            return "BEARISH"

    return "NEUTRAL"