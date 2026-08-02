def calculate_confidence(score):
    """
    Zamienia AI Score na poziom pewności (%)
    """

    confidence = max(0, min(100, score))

    return confidence