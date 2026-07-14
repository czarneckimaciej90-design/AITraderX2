import json
import os
from datetime import datetime


class LearningMemory:

    FILE = "brain_learning.json"

    def __init__(self):

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w") as file:
                json.dump([], file)

    def load_history(self):

        try:

            with open(self.FILE, "r") as file:

                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            return []

    def save_history(self, history):

        with open(self.FILE, "w") as file:

            json.dump(
                history,
                file,
                indent=4
            )

    def save_trade(
        self,
        symbol,
        decision,
        entry_price,
        size,
        score,
        confidence,
        rsi,
        histogram
    ):

        history = self.load_history()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):

                return

        history.append({

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "symbol": symbol,

            "decision": decision,

            "entry_price": entry_price,

            "exit_price": None,

            "size": size,

            "score": score,

            "confidence": confidence,

            "rsi": round(rsi, 2),

            "macd": round(histogram, 6),

            "profit_percent": 0.0,

            "profit_usdt": 0.0,

            "status": "OPEN",

            "result": "PENDING"

        })

        self.save_history(history)

        print(f"[LEARNING] Trade saved {symbol}")

    def update_trade(
        self,
        symbol,
        exit_price
    ):

        history = self.load_history()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):

                trade["exit_price"] = exit_price

                entry = trade["entry_price"]

                percent = (
                    (exit_price - entry)
                    / entry
                ) * 100

                if trade["decision"] == "SELL":

                    percent *= -1

                trade["profit_percent"] = round(
                    percent,
                    2
                )

                trade["profit_usdt"] = round(
                    trade["size"] * percent / 100,
                    2
                )

                trade["status"] = "CLOSED"

                if percent > 0:

                    trade["result"] = "SUCCESS"

                else:

                    trade["result"] = "LOSS"

        self.save_history(history)

    # Zostawiamy dla zgodności ze starym kodem
    def save_decision(
        self,
        symbol,
        decision,
        score,
        confidence,
        rsi,
        histogram,
        price
    ):

        if decision == "WAIT":
            return

        if confidence < 60:
            return

        self.save_trade(
            symbol,
            decision,
            price,
            0,
            score,
            confidence,
            rsi,
            histogram
        )

    def get_history(self):

        return self.load_history()

    def clear(self):

        self.save_history([])

        print("[LEARNING] History cleared.")