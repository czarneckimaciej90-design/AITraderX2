class CapitalManager:

    def __init__(
        self,
        total_balance,
        reserve_percent=20,
        max_positions=8
    ):

        self.total_balance = total_balance
        self.reserve_percent = reserve_percent
        self.max_positions = max_positions


    def available_capital(self):

        reserve = self.total_balance * (
            self.reserve_percent / 100
        )

        return self.total_balance - reserve


    def calculate_position_size(
        self,
        score,
        confidence,
        current_positions
    ):

        if current_positions >= self.max_positions:
            return 0


        capital = self.available_capital()

        base_position = capital / self.max_positions


        strength = (
            score / 100 +
            confidence / 100
        ) / 2


        position = base_position * strength


        return round(position, 2)