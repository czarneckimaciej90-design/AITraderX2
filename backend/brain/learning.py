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

                return False

        now = datetime.now()

        history.append({

            "open_time": now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "close_time": None,

            "holding_minutes": 0,

            "symbol": symbol,

            "decision": decision,

            "entry_price": float(entry_price),

            "exit_price": None,

            "size": float(size),

            "score": int(score),

            "confidence": int(confidence),

            "rsi": round(float(rsi), 2),

            "macd": round(float(histogram), 6),

            "profit_percent": 0.0,

            "profit_usdt": 0.0,

            "highest_profit": 0.0,

            "lowest_profit": 0.0,

            "highest_price": float(entry_price),

            "lowest_price": float(entry_price),

            "update_count": 0,

            "exit_reason": "",

            "status": "OPEN",

            "result": "PENDING"

        })

        self.save_history(history)

        print(f"[LEARNING] Trade saved -> {symbol}")

        return True

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

                entry = trade["entry_price"]

                if entry <= 0:
                    return False

                trade["exit_price"] = float(exit_price)

                close_time = datetime.now()

                trade["close_time"] = close_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                open_time = datetime.strptime(
                    trade["open_time"],
                    "%Y-%m-%d %H:%M:%S"
                )

                holding = close_time - open_time

                trade["holding_minutes"] = round(
                    holding.total_seconds() / 60,
                    2
                )

                percent = (
                    (exit_price - entry)
                    / entry
                ) * 100

                if trade["decision"] == "SELL":

                    percent *= -1

                profit = (
                    trade["size"]
                    * percent
                    / 100
                )

                trade["profit_percent"] = round(
                    percent,
                    2
                )

                trade["profit_usdt"] = round(
                    profit,
                    2
                )

                trade["status"] = "CLOSED"

                if percent > 0:

                    trade["result"] = "SUCCESS"

                elif percent < 0:

                    trade["result"] = "LOSS"

                else:

                    trade["result"] = "BREAKEVEN"

                self.save_history(history)

                print(f"[LEARNING] Trade closed -> {symbol}")

                return True

        return False

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

            symbol=symbol,

            decision=decision,

            entry_price=price,

            size=0,

            score=score,

            confidence=confidence,

            rsi=rsi,

            histogram=histogram

        )

    def get_history(self):

        return self.load_history()

    def clear(self):

        self.save_history([])

        print("[LEARNING] History cleared.")