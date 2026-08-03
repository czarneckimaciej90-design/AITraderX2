"""
====================================================
AI Trader X Platform
Version: 0.3 Stable
====================================================
Main application entry point.
Clean architecture:
Engine -> MarketProcessor -> TradeManager
====================================================
"""

from datetime import datetime

from config.settings import Settings
from logs.logger import log

from exchange.binance import BinanceExchange

from scanner.scanner import MarketScanner

from core.engine import Engine
from core.market_processor import MarketProcessor

from portfolio.portfolio import Portfolio
from portfolio.capital_manager import CapitalManager
from portfolio.position_manager import PositionManager

from brain.brain import Brain
from brain.memory import Memory
from brain.learning_memory import LearningMemory
from brain.statistics import BrainStatistics
from brain.learning_engine import LearningEngine


from backtesting.backtester import Backtester

from execution.trade_manager import TradeManager
from performance.performance import Performance


class ATXCore:

    def __init__(self):

        self.version = "0.3"

        self.started = datetime.now()

    def start(self):

        settings = Settings()

        print("=" * 60)
        print(settings.APP_NAME)
        print(f"Version : {self.version}")
        print(f"Exchange : {settings.EXCHANGE}")
        print(f"Demo Mode : {settings.DEMO_MODE}")
        print("=" * 60)

        print(f"Started : {self.started}")

        print("[OK] Core Engine")
        print("[OK] System Initialised")

        exchange = BinanceExchange()
        exchange.connect()

        scanner = MarketScanner(exchange)

        portfolio = Portfolio(
            balance=1000,
            max_positions=8
        )

        portfolio.load()

        performance = Performance(
            portfolio
        )

        memory = Memory()

        learning_memory = LearningMemory()
        
        backtester = Backtester()

        brain = Brain()

        statistics = BrainStatistics()

        trade_manager = TradeManager(
            portfolio,
            learning_memory
        )

        learning_engine = LearningEngine()

        position_manager = PositionManager()

        capital_manager = CapitalManager(
            portfolio=portfolio,
            reserve_percent=5,
            max_positions=8
        )

        processor = MarketProcessor(
            brain=brain,
            portfolio=portfolio,
            trade_manager=trade_manager,
            capital_manager=capital_manager,
            position_manager=position_manager,
            memory=memory,
            learning_memory=learning_memory
        )

        engine = Engine(
            exchange=exchange,
            scanner=scanner,
            portfolio=portfolio,
            position_manager=position_manager,
            brain=brain,
            trade_manager=trade_manager,
            capital_manager=capital_manager,
            memory=memory,
            backtester=backtester,
            statistics=statistics,
            learning_engine=learning_engine,
            processor=processor,
            performance=performance
        )

        print("[OK] Core Engine Ready")

        print("[OK] Starting Engine...")

        engine.start()

if __name__ == "__main__":

    app = ATXCore()

    app.start()
