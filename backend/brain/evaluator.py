import json
import os


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

        with open(self.FILE, "r") as file:

            history = json.load(file)


        updated = False


        for trade in history:


            if trade["symbol"] != symbol:
                continue


            if trade["result"] != "PENDING":
                continue


            entry_price = trade["price"]

            decision = trade["decision"]


            if decision == "BUY":

                if current_price > entry_price:
                    trade["result"] = "SUCCESS"
                else:
                    trade["result"] = "LOSS"


            elif decision == "SELL":

                if current_price < entry_price:
                    trade["result"] = "SUCCESS"
                else:
                    trade["result"] = "LOSS"


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