class RiskManager:

    def __init__(self, balance):
        self.balance = balance

    def calculate_position_size(self, confidence):

        if confidence < 60:
            return 0

        if confidence >= 90:
            risk = 0.10

        elif confidence >= 75:
            risk = 0.05

        else:
            risk = 0.02

        position = self.balance * risk

        return round(position, 2)