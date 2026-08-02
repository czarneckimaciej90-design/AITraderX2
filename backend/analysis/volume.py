def analyze(market):

    volumes = market["volumes"]

    if len(volumes) < 20:

        return {

            "average": 0,

            "current": 0,

            "ratio": 0,

            "spike": False

        }

    average = sum(volumes[:-1]) / (len(volumes) - 1)

    current = volumes[-1]

    ratio = current / average if average > 0 else 0

    spike = ratio >= 2.0

    return {

        "average": round(average, 2),

        "current": round(current, 2),

        "ratio": round(ratio, 2),

        "spike": spike

    }