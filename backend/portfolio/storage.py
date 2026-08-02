import json
import os


class PortfolioStorage:

    FILE_NAME = "portfolio.json"

    @classmethod
    def save(cls, portfolio):

        data = {
            "balance": portfolio.balance,
            "start_balance": portfolio.start_balance,
            "positions": portfolio.positions
        }

        with open(cls.FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load(cls):

        if not os.path.exists(cls.FILE_NAME):
            return None

        try:

            with open(cls.FILE_NAME, "r") as file:

                content = file.read().strip()

                if not content:

                    print("[PORTFOLIO] Empty portfolio file.")

                    return None

                return json.loads(content)

        except Exception as e:

            print(f"[PORTFOLIO] Cannot load portfolio: {e}")

            return None

    @classmethod
    def load_into_portfolio(cls, portfolio):

        data = cls.load()

        if data is None:
            return False

        portfolio.balance = data.get(
            "balance",
            portfolio.balance
        )

        portfolio.start_balance = data.get(
            "start_balance",
            portfolio.start_balance
        )

        portfolio.positions = data.get(
            "positions",
            {}
        )

        return True