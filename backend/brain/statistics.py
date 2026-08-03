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

        try:

            with open(self.FILE, "r") as file:
                history = json.load(file)

        except Exception as e:

            print(f"[STATISTICS] Cannot read learning file: {e}")
            return

        total = len(history)

        pending = 0
        success = 0
        loss = 0

        buy_total = 0
        buy_success = 0

        sell_total = 0
        sell_success = 0

        unknown = 0

        profits = []

        market_scores = []

        rsi_values = []

        volume_ratios = []

        gross_profit = 0
        gross_loss = 0

        for trade in history:

            result = trade.get("result", "PENDING")
            decision = trade.get("decision", "UNKNOWN")

            profit = trade.get("profit_percent", 0)

            if isinstance(profit, (int, float)):
                profits.append(profit)

                if profit > 0:
                    gross_profit += profit

                elif profit < 0:
                    gross_loss += abs(profit)

            market_score = trade.get("market_score")

            if isinstance(market_score, (int, float)):
                market_scores.append(market_score)

            rsi = trade.get("rsi")

            if isinstance(rsi, (int, float)):
                rsi_values.append(rsi)

            volume = trade.get("volume_ratio")

            if isinstance(volume, (int, float)):
                volume_ratios.append(volume)

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

            else:

                unknown += 1

        buy_accuracy = (
            round(buy_success / buy_total * 100, 2)
            if buy_total else 0
        )

        sell_accuracy = (
            round(sell_success / sell_total * 100, 2)
            if sell_total else 0
        )

        completed = success + loss

        overall = (
            round(success / completed * 100, 2)
            if completed else 0
        )

        average_profit = (
            round(sum(profits) / len(profits), 2)
            if profits else 0
        )

        best_trade = (
            round(max(profits), 2)
            if profits else 0
        )

        worst_trade = (
            round(min(profits), 2)
            if profits else 0
        )

        avg_market_score = (
            round(sum(market_scores) / len(market_scores), 2)
            if market_scores else 0
        )

        avg_rsi = (
            round(sum(rsi_values) / len(rsi_values), 2)
            if rsi_values else 0
        )

        avg_volume = (
            round(sum(volume_ratios) / len(volume_ratios), 2)
            if volume_ratios else 0
        )

        profit_factor = (
            round(gross_profit / gross_loss, 2)
            if gross_loss > 0
            else 0
        )

        print("\n==============================")
        print(" BRAIN LEARNING REPORT ")
        print("==============================")

        print(f"Total Trades       : {total}")
        print(f"Pending            : {pending}")
        print(f"Success            : {success}")
        print(f"Loss               : {loss}")
        print(f"Unknown            : {unknown}")

        print("------------------------------")

        print(f"BUY Accuracy       : {buy_accuracy}%")
        print(f"SELL Accuracy      : {sell_accuracy}%")
        print(f"Overall Success    : {overall}%")

        print("------------------------------")

        print(f"Average Profit %   : {average_profit}")
        print(f"Best Trade %       : {best_trade}")
        print(f"Worst Trade %      : {worst_trade}")

        print("------------------------------")

        print(f"Profit Factor      : {profit_factor}")

        print("------------------------------")

        print(f"Average RSI        : {avg_rsi}")
        print(f"Average Volume     : {avg_volume}")
        print(f"Average MarketScore: {avg_market_score}")

        print("==============================")
