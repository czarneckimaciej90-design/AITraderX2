import json
import os


class BrainStatistics:

    FILE = "brain_learning.json"

    def __init__(self):
        pass

    def report(self):

        if not os.path.exists(self.FILE):

            print("[STATISTICS] No learning file found.")
            return

        with open(self.FILE, "r") as file:

            history = json.load(file)

        total = len(history)

        pending = 0
        success = 0
        loss = 0

        buy_total = 0
        buy_success = 0

        sell_total = 0
        sell_success = 0

        for trade in history:

            result = trade["result"]
            decision = trade["decision"]

            if result == "PENDING":
                pending += 1

            elif result == "SUCCESS":
                success += 1

            elif result == "LOSS":
                loss += 1

            if decision == "BUY":
                buy_total += 1

                if result == "SUCCESS":
                    buy_success += 1

            elif decision == "SELL":
                sell_total += 1

                if result == "SUCCESS":
                    sell_success += 1

        if buy_total > 0:
            buy_accuracy = round(
                buy_success / buy_total * 100,
                2
            )
        else:
            buy_accuracy = 0

        if sell_total > 0:
            sell_accuracy = round(
                sell_success / sell_total * 100,
                2
            )
        else:
            sell_accuracy = 0

        completed = success + loss

        if completed > 0:
            overall = round(
                success / completed * 100,
                2
            )
        else:
            overall = 0

        print("\n==============================")
        print(" BRAIN LEARNING REPORT ")
        print("==============================")

        print(f"Total Decisions : {total}")
        print(f"Pending         : {pending}")
        print(f"Success         : {success}")
        print(f"Loss            : {loss}")

        print("------------------------------")

        print(f"BUY Accuracy    : {buy_accuracy}%")
        print(f"SELL Accuracy   : {sell_accuracy}%")

        print("------------------------------")

        print(f"Overall Success : {overall}%")

        print("==============================")