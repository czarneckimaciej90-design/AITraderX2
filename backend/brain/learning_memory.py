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
        histogram,
        atr=0,
        ema10=0,
        ema20=0,
        trend="UNKNOWN",
        volume_ratio=0,
        volume_spike=False,
        brain_version="0.5",
        market_score=0,
        market_validation=None
    ):

        history = self._load()

        for trade in history:

            if (
                trade["symbol"] == symbol
                and trade["status"] == "OPEN"
            ):
                return False

        now = datetime.now()

        trade = {

            # =====================
            # BASIC
            # =====================

            "symbol": symbol,
            "decision": decision,
            "status": "OPEN",
            "result": "PENDING",
            "brain_version": brain_version,
            "market_score": int(market_score),
            "market_validation": market_validation or {},

            # =====================
            # TIME
            # =====================

            "open_time": now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "close_time": None,

            "holding_minutes": 0,

            # =====================
            # PRICE
            # =====================

            "entry_price": float(entry_price),

            "exit_price": None,

            "size": float(size),

            # =====================
            # BRAIN
            # =====================

            "score": int(score),

            "confidence": int(confidence),

            # =====================
            # INDICATORS
            # =====================

            "ema10": round(float(ema10), 8),

            "ema20": round(float(ema20), 8),

            "rsi": round(float(rsi), 2),

            "macd": round(float(histogram), 6),

            "atr": round(float(atr), 8),

            # =====================
            # VOLUME
            # =====================

            "volume_ratio": round(float(volume_ratio), 2),

            "volume_spike": bool(volume_spike),

            # =====================
            # TREND
            # =====================

            "trend": trend,

            # =====================
            # POSITION STATS
            # =====================

            "highest_price": float(entry_price),

            "lowest_price": float(entry_price),

            "highest_profit": 0.0,

            "lowest_profit": 0.0,

            "update_count": 0,

            # =====================
            # EXIT
            # =====================

            "exit_reason": "",

            "profit_percent": 0.0,

            "profit_usdt": 0.0

        }

        history.append(trade)

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

                # =====================
                # PRICE
                # =====================

                trade["highest_price"] = float(
                    position.get(
                        "highest_price",
                        trade["highest_price"]
                    )
                )

                trade["lowest_price"] = float(
                    position.get(
                        "lowest_price",
                        trade["lowest_price"]
                    )
                )

                # =====================
                # PROFIT
                # =====================

                trade["highest_profit"] = round(
                    float(
                        position.get(
                            "highest_profit",
                            trade["highest_profit"]
                        )
                    ),
                    2
                )

                trade["lowest_profit"] = round(
                    float(
                        position.get(
                            "lowest_profit",
                            trade["lowest_profit"]
                        )
                    ),
                    2
                )

                # =====================
                # STATISTICS
                # =====================

                trade["update_count"] = int(
                    position.get(
                        "update_count",
                        trade["update_count"]
                    )
                )

                # =====================
                # SAVE
                # =====================

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

                # ===========================
                # POSITION STATISTICS
                # ===========================

                trade["highest_price"] = float(
                    position.get(
                        "highest_price",
                        trade["highest_price"]
                    )
                )

                trade["lowest_price"] = float(
                    position.get(
                        "lowest_price",
                        trade["lowest_price"]
                    )
                )

                trade["highest_profit"] = round(
                    float(
                        position.get(
                            "highest_profit",
                            trade["highest_profit"]
                        )
                    ),
                    2
                )

                trade["lowest_profit"] = round(
                    float(
                        position.get(
                            "lowest_profit",
                            trade["lowest_profit"]
                        )
                    ),
                    2
                )

                trade["update_count"] = int(
                    position.get(
                        "update_count",
                        trade["update_count"]
                    )
                )

                trade["exit_reason"] = position.get(
                    "exit_reason",
                    ""
                )

                # ===========================
                # PROFIT
                # ===========================

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

                # ===========================
                # RESULT
                # ===========================

                trade["status"] = "CLOSED"

                if percent > 0:

                    trade["result"] = "SUCCESS"

                elif percent < 0:

                    trade["result"] = "LOSS"

                else:

                    trade["result"] = "BREAKEVEN"

                # ===========================
                # AI SUMMARY
                # ===========================

                trade["ai_summary"] = {

                    "decision": trade["decision"],

                    "score": trade["score"],

                    "confidence": trade["confidence"],

                    "trend": trade["trend"],

                    "brain_version": trade["brain_version"],

                    "volume_ratio": trade["volume_ratio"],

                    "volume_spike": trade["volume_spike"],

                    "rsi": trade["rsi"],

                    "macd": trade["macd"],

                    "atr": trade["atr"]

                }

                self._save(history)

                return True

        return False

        # ==========================================
    # AI FUNCTIONS
    # ==========================================

    def get_all_trades(self):

        return self._load()

    def get_open_trades(self):

        history = self._load()

        return [
            trade
            for trade in history
            if trade["status"] == "OPEN"
        ]

    def get_closed_trades(self):

        history = self._load()

        return [
            trade
            for trade in history
            if trade["status"] == "CLOSED"
        ]

    def get_success_trades(self):

        history = self._load()

        return [
            trade
            for trade in history
            if trade["result"] == "SUCCESS"
        ]

    def get_loss_trades(self):

        history = self._load()

        return [
            trade
            for trade in history
            if trade["result"] == "LOSS"
        ]

    def get_statistics(self):

        history = self._load()

        total = len(history)

        closed = len(
            [
                x
                for x in history
                if x["status"] == "CLOSED"
            ]
        )

        success = len(
            [
                x
                for x in history
                if x["result"] == "SUCCESS"
            ]
        )

        loss = len(
            [
                x
                for x in history
                if x["result"] == "LOSS"
            ]
        )

        breakeven = len(
            [
                x
                for x in history
                if x["result"] == "BREAKEVEN"
            ]
        )

        winrate = 0

        if success + loss > 0:

            winrate = round(
                success / (success + loss) * 100,
                2
            )

        return {

            "total": total,

            "closed": closed,

            "success": success,

            "loss": loss,

            "breakeven": breakeven,

            "winrate": winrate

        }

    def export_ai_dataset(self):

        return self._load()