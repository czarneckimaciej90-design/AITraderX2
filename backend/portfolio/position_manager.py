class PositionManager:

    def __init__(self):
        pass

    def evaluate(
        self,
        position,
        current_price,
        current_score
    ):

        entry_price = position.get("entry")

        if entry_price is None:
            return "HOLD"

        # ==========================================
        # Learning 2.0
        # ==========================================

        position.setdefault("highest_price", entry_price)
        position.setdefault("lowest_price", entry_price)

        position.setdefault("highest_profit", 0.0)
        position.setdefault("lowest_profit", 0.0)

        position.setdefault("update_count", 0)

        position.setdefault("exit_reason", "")

        # ==========================================
        # Aktualizacja licznika
        # ==========================================

        position["update_count"] += 1

        # ==========================================
        # Highest / Lowest Price
        # ==========================================

        if current_price > position["highest_price"]:
            position["highest_price"] = current_price

        if current_price < position["lowest_price"]:
            position["lowest_price"] = current_price

        # ==========================================
        # Profit %
        # ==========================================

        profit_percent = (
            (current_price - entry_price)
            / entry_price
        ) * 100

        profit_percent = round(
            profit_percent,
            2
        )

        # ==========================================
        # Highest / Lowest Profit
        # ==========================================

        if profit_percent > position["highest_profit"]:

            position["highest_profit"] = profit_percent

        if profit_percent < position["lowest_profit"]:

            position["lowest_profit"] = profit_percent

        # ==========================================
        # Drawdown
        # ==========================================

        highest_price = position["highest_price"]

        if highest_price <= 0:

            drawdown = 0

        else:

            drawdown = (
                (highest_price - current_price)
                / highest_price
            ) * 100

        drawdown = round(
            drawdown,
            2
        )

        # ==========================================
        # EXIT LOGIC
        # ==========================================

        if current_score < 45:

            position["exit_reason"] = "Brain Weak"

            return "SELL"

        if profit_percent <= -2.5:

            position["exit_reason"] = "Stop Loss"

            return "SELL"

        if (
            profit_percent >= 1
            and drawdown >= 0.8
        ):

            position["exit_reason"] = "Trailing Stop"

            return "SELL"

        if (
            profit_percent >= 3
            and drawdown >= 0.5
        ):

            position["exit_reason"] = "Tight Trailing"

            return "SELL"

        return "HOLD"