class CapitalManager:

    def __init__(
        self,
        portfolio,
        reserve_percent=5,
        max_positions=8
    ):

        self.portfolio = portfolio
        self.reserve_percent = reserve_percent
        self.max_positions = max_positions

    def available_capital(self):

        reserve = (
            self.portfolio.balance
            * self.reserve_percent
            / 100
        )

        return max(
            0,
            self.portfolio.balance - reserve
        )

    def calculate_position_size(
        self,
        score,
        confidence,
        current_positions
    ):

        if current_positions >= self.max_positions:
            return 0

        available = self.available_capital()

        remaining_slots = (
            self.max_positions - current_positions
        )

        if remaining_slots <= 0:
            return 0

        base_position = (
            available / remaining_slots
        )

        strength = (
            score + confidence
        ) / 200

        multiplier = 0.8 + (strength * 0.4)

        position = base_position * multiplier

        if position > available:
            position = available

        return round(position, 2)