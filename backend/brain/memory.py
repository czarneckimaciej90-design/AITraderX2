import csv
import os
from datetime import datetime


class Memory:

    def save(self, result):

        file_name = "analysis_history.csv"

        file_exists = os.path.isfile(file_name)

        with open(file_name, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "Date",
                    "Symbol",
                    "Trend",
                    "Decision",
                    "Score",
                    "Confidence",
                    "RSI",
                    "ATR",
                    "Histogram",
                    "EMA10",
                    "EMA20",
                    "MarketScore",
                    "VolumeRatio",
                    "VolumeSpike"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                result.get("symbol"),
                result.get("trend"),
                result.get("decision"),
                result.get("score", 0),
                result.get("confidence", 0),
                round(result.get("rsi", 0), 2),
                result.get("atr", 0),
                result.get("histogram", 0),
                result.get("ema10", 0),
                result.get("ema20", 0),
                result.get("market_score", 0),
                result.get("volume_ratio", 0),
                result.get("volume_spike", False)
            ])

