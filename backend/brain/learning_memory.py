import json
import os
from datetime import datetime


class LearningMemory:

    FILE = "brain_learning.json"

    def __init__(self):

        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as file:
                json.dump([], file, indent=4)

    def _load(self):

        try:

            with open(self.FILE, "r") as file:
                return json.load(file)

        except Exception:

            return []

    def _save(self, history):

        with open(self.FILE, "w") as file:

            json.dump(
                history,
                file,
                indent=4
            )

    def create_trade(
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

        history = self._load()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):
                return False

        now = datetime.now()

        history.append({

            "symbol": symbol,

            "decision": decision,

            "status": "OPEN",

            "result": "PENDING",

            "open_time": now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "close_time": None,

            "holding_minutes": 0,

            "entry_price": float(entry_price),

            "exit_price": None,

            "size": float(size),

            "score": int(score),

            "confidence": int(confidence),

            "rsi": round(float(rsi), 2),

            "macd": round(float(histogram), 6),

            "highest_price": float(entry_price),

            "lowest_price": float(entry_price),

            "highest_profit": 0.0,

            "lowest_profit": 0.0,

            "update_count": 0,

            "exit_reason": "",

            "profit_percent": 0.0,

            "profit_usdt": 0.0

        })

        self._save(history)

        return True

    def update_open_position(
        self,
        symbol,
        position
    ):

        history = self._load()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):

                trade["highest_price"] = position.get(
                    "highest_price",
                    trade["highest_price"]
                )

                trade["lowest_price"] = position.get(
                    "lowest_price",
                    trade["lowest_price"]
                )

                trade["highest_profit"] = position.get(
                    "highest_profit",
                    trade["highest_profit"]
                )

                trade["lowest_profit"] = position.get(
                    "lowest_profit",
                    trade["lowest_profit"]
                )

                trade["update_count"] = position.get(
                    "update_count",
                    trade["update_count"]
                )

                self._save(history)

                return True

        return False

    def close_trade(
        self,
        symbol,
        exit_price,
        position
    ):

        history = self._load()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):

                now = datetime.now()

                trade["close_time"] = now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                open_time = datetime.strptime(
                    trade["open_time"],
                    "%Y-%m-%d %H:%M:%S"
                )

                holding = now - open_time

                trade["holding_minutes"] = round(
                    holding.total_seconds() / 60,
                    2
                )

                trade["exit_price"] = float(exit_price)

                trade["highest_price"] = position.get(
                    "highest_price",
                    trade["highest_price"]
                )

                trade["lowest_price"] = position.get(
                    "lowest_price",
                    trade["lowest_price"]
                )

                trade["highest_profit"] = position.get(
                    "highest_profit",
                    trade["highest_profit"]
                )

                trade["lowest_profit"] = position.get(
                    "lowest_profit",
                    trade["lowest_profit"]
                )

                trade["update_count"] = position.get(
                    "update_count",
                    trade["update_count"]
                )

                trade["exit_reason"] = position.get(
                    "exit_reason",
                    ""
                )

                percent = (
                    (exit_price - trade["entry_price"])
                    / trade["entry_price"]
                ) * 100

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

                elif percent < 0:

                    trade["result"] = "LOSS"

                else:

                    trade["result"] = "BREAKEVEN"

                self._save(history)

                return True

        return False