"""
ATX Platform
Configuration
"""

from dataclasses import dataclass


@dataclass
class Settings:
    APP_NAME: str = "ATX Platform"
    VERSION: str = "0.0.1"

    DEMO_MODE: bool = True
    LOG_LEVEL: str = "INFO"

    EXCHANGE: str = "BINANCE"

    START_BALANCE: float = 10.00

    DAILY_TARGET: float = 0.01