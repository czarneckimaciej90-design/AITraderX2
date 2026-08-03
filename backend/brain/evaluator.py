import json
import os
from datetime import datetime


class LearningEvaluator:

    FILE = "brain_learning.json"

    def __init__(self):

        if not os.path.exists(self.FILE):

            print("[LEARNING] No memory file found")

    def evaluate_trade(
        self,
        symbol,
        current_price
    ):

        if not os.path.exists(self.FILE):
            return

        with open(self.FILE, "r") as file:

            history = json.load(file)

        updated = False

        for trade in history:

            if trade.get("symbol") != symbol:
                continue

            if trade.get("result") != "PENDING":
                continue

            entry_price = trade.get("entry_price")

            if entry_price is None:
                entry_price = trade.get("price")

            if entry_price is None:
                continue

            decision = trade.get("decision", "BUY")

            if decision == "BUY":

                success = current_price > entry_price
                profit_percent = (
                    (current_price - entry_price)
                    / entry_price
                ) * 100

            else:

                success = current_price < entry_price
                profit_percent = (
                    (entry_price - current_price)
                    / entry_price
                ) * 100

            trade["exit_price"] = round(current_price, 8)

            trade["profit_percent"] = round(
                profit_percent,
                2
            )

            trade["closed"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            trade["result"] = (
                "SUCCESS"
                if success
                else "LOSS"
            )

            updated = True

        if updated:

            with open(self.FILE, "w") as file:

                json.dump(
                    history,
                    file,
                    indent=4
                )

            print(
                f"[LEARNING] {symbol} evaluated"
            )