import csv
import os

from datetime import datetime


def paper_buy(symbol, price, size):

    print(">>> PAPER BUY CALLED <<<")

    trade = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "side": "BUY",
        "price": price,
        "size": size,
    }

    print("\n========== PAPER TRADE ==========")
    print(f"Time   : {trade['time']}")
    print(f"Symbol : {trade['symbol']}")
    print(f"Side   : {trade['side']}")
    print(f"Price  : {trade['price']}")
    print(f"Size   : {trade['size']} USDT")
    print("=================================\n")

    file_name = "paper_trades.csv"

    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "Symbol",
                "Side",
                "Price",
                "Size"
            ])

        writer.writerow([
            trade["time"],
            trade["symbol"],
            trade["side"],
            trade["price"],
            trade["size"]
        ])

    return trade

def paper_sell(symbol, price, size):

    trade = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "side": "SELL",
        "price": price,
        "size": size,
    }

    print("\n========== PAPER SELL ==========")
    print(f"Time   : {trade['time']}")
    print(f"Symbol : {trade['symbol']}")
    print(f"Side   : {trade['side']}")
    print(f"Price  : {trade['price']}")
    print(f"Size   : {trade['size']} USDT")
    print("=================================\n")

    file_name = "paper_trades.csv"

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            trade["time"],
            trade["symbol"],
            trade["side"],
            trade["price"],
            trade["size"]
        ])

    return trade