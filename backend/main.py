"""
====================================================
AI Trader X Platform
Version: 0.0.1
====================================================
Main application entry point.
"""

from datetime import datetime
from config.settings import Settings


class ATXCore:
    def __init__(self):
        self.version = "0.0.1"
        self.started = datetime.now()

    def start(self):
        settings = Settings()

        print("=" * 60)
        print(settings.APP_NAME)
        print(f"Version : {settings.VERSION}")
        print(f"Exchange : {settings.EXCHANGE}")
        print(f"Demo Mode : {settings.DEMO_MODE}")
        print(f"Start Balance : £{settings.START_BALANCE}")
        print("=" * 60)

        print("AI Trader X Platform")
        print(f"Version : {self.version}")
        print(f"Started : {self.started}")
        print("=" * 60)
        print("[OK] Core Engine")
        print("[OK] System Initialised")
        print("[WAIT] Loading modules...")


if __name__ == "__main__":
    app = ATXCore()
    app.start()