def calculate_position_size(balance, score, confidence):
    """
    Inteligentny Money Manager AI Trader X
    """

    if score < 60 or confidence < 60:
        return 0

    if score >= 90 and confidence >= 90:
        risk = 0.06

    elif score >= 80 and confidence >= 80:
        risk = 0.04

    elif score >= 70 and confidence >= 70:
        risk = 0.02

    else:
        risk = 0.01

    position_size = balance * risk

    return round(position_size, 2)