class PositionManager:

    def __init__(self):
        pass

    def evaluate(
        self,
        position,
        current_price,
        current_score
    ):
        """
        Analizuje otwartą pozycję i zwraca decyzję.
        """

        entry_price = position["entry"]

        profit_percent = (
            (current_price - entry_price)
            / entry_price
        ) * 100

        # Aktualizacja najwyższej ceny
        if current_price > position.get("highest_price", entry_price):
            position["highest_price"] = current_price

        highest_price = position.get(
            "highest_price",
            entry_price
        )

        drawdown = (
            (highest_price - current_price)
            / highest_price
        ) * 100

        # 1. Mocny spadek jakości sygnału
        if current_score < 45:
            return "SELL"

        # 2. Zabezpieczenie zysku
        if profit_percent > 2 and drawdown > 1:
            return "SELL"

        # 3. Duża strata
        if profit_percent < -3:
            return "SELL"

        return "HOLD"