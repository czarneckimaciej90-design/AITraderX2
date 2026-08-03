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
                    "Confidence",
                    "RSI"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                result["symbol"],
                result["trend"],
                result["decision"],
                result["confidence"],
                round(result["rsi"], 2)
            ])
