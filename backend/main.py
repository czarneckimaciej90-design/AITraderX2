"""
====================================================
AI Trader X Platform
Version: 0.0.1
====================================================
Main application entry point.
"""

from datetime import datetime

from config.settings import Settings
from logs.logger import log

from exchange.binance import BinanceExchange
from exchange.markets import get_markets

from scanner.scanner import MarketScanner

from indicators.ema import calculate_ema, ema_signal
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd

from analysis.trend import detect_trend
from analysis.decision import make_decision
from analysis.score import calculate_score
from analysis.confidence import calculate_confidence
from analysis.filter import trade_allowed

from execution.paper_trading import paper_buy, paper_sell

from portfolio.portfolio import Portfolio
from brain.memory import Memory
from backtesting.backtester import Backtester

from indicators.atr import calculate_atr
from portfolio.capital_manager import CapitalManager
from portfolio.position_manager import PositionManager

from core.engine import Engine

from brain.brain import Brain
from brain.learning import LearningMemory
from brain.statistics import BrainStatistics
from execution.trade_manager import TradeManager

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
        print(f"Start Balance : {settings.START_BALANCE}")
        print("=" * 60)

        print("AI Trader X Platform")
        print(f"Started : {self.started}")
        print("=" * 60)

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
        trade_manager = TradeManager(portfolio)

        memory = Memory()
        backtester = Backtester()
        brain = Brain()
        learning_memory = LearningMemory()
        brain_statistics = BrainStatistics()

        position_manager = PositionManager()

        capital_manager = CapitalManager(
            portfolio.balance,
            reserve_percent=20,
            max_positions=8
        )

        engine = Engine(
            exchange=exchange,
            scanner=scanner,
            portfolio=portfolio,
            position_manager=position_manager
        )

        engine.run_cycle()

        market_data = engine.get_market_data()

        results = []

        print("\n===== POSITION CHECK =====")

        for symbol in list(portfolio.positions.keys()):

            if symbol not in market_data:
                continue

            closes = market_data[symbol]

            current_price = closes[-1]

            ema10 = calculate_ema(closes, 10)

            signal, ema10, ema20 = ema_signal(closes)

            rsi = calculate_rsi(closes)

            macd, signal_macd, histogram = calculate_macd(closes)

            score = calculate_score(
                ema10,
                ema20,
                rsi,
                histogram
            )

            decision = position_manager.evaluate(
                portfolio.positions[symbol],
                current_price,
                score
            )

            print(
                f"{symbol} -> {decision}"
            )

            if decision == "SELL":
                trade_size = portfolio.positions[symbol]["size"]

                portfolio.sell(
                    symbol,
                    current_price
                )

                paper_sell(
                    symbol=symbol,
                    price=current_price,
                    size=trade_size
                )

        for symbol, closes in market_data.items():

            if len(closes) < 20:
                continue


            ema10 = calculate_ema(closes, 10)

            signal, ema10, ema20 = ema_signal(closes)

            rsi = calculate_rsi(closes)

            macd, signal_macd, histogram = calculate_macd(closes)

            atr = calculate_atr(closes)

            brain_result = brain.analyze(
                symbol,
                ema10,
                ema20,
                rsi,
                histogram,
                atr
            )

            brain_decision = brain_result["decision"]
            brain_score = brain_result["score"]
            brain_confidence = brain_result["confidence"]
            brain_reasons = brain_result["reasons"]

            learning_memory.save_decision(
                symbol,
                brain_decision,
                brain_score,
                brain_confidence,
                rsi,
                histogram,
                closes[-1]
            )


            trend = detect_trend(
                ema10,
                ema20,
                rsi
            )


            decision, confidence = make_decision(
                ema10,
                ema20,
                rsi,
                histogram
            )


            score = calculate_score(
                ema10,
                ema20,
                rsi,
                histogram
            )


            confidence = calculate_confidence(score)

            allowed = trade_allowed(score, confidence)

            if allowed:
                position_size = capital_manager.calculate_position_size(
                    score,
                    confidence,
                    len(portfolio.positions)
                )
            else:
                position_size = 0


            print("--------------------------------")
            print(f"Market : {symbol}")
            print(f"Trend  : {trend}")
            print(f"RSI    : {round(rsi,2)}")
            print(f"Score  : {score}")
            print(f"Decision : {decision}")
            print(f"Confidence : {confidence}%")
            print(f"Allowed : {allowed}")
            print(f"ATR: {atr}")
            print(f"Brain Decision : {brain_decision}")
            print(f"Brain Score    : {brain_score}")
            print(f"Brain Reasons  : {', '.join(brain_reasons)}")


            if decision == "BUY" and allowed:

                if not portfolio.has_position(symbol):
                    print("--------------------------------")
                    print("CAPITAL MANAGER SIZE:", position_size)
                    print("SYMBOL:", symbol)
                    print("SCORE:", score)
                    print("CONFIDENCE:", confidence)
                    print("--------------------------------")

                    trade_manager.buy(
                        symbol=symbol,
                        price=closes[-1],
                        size=position_size,
                        score=score,
                        confidence=confidence,
                        rsi=rsi,
                        histogram=histogram
)

            # if decision == "SELL":
            #     if portfolio.has_position(symbol):
            #         portfolio.sell(
            #             symbol,
            #             closes[-1]
            #         )
            #         paper_sell(
            #             symbol=symbol,
            #             price=closes[-1],
            #             size=position_size
            #         )
            print(f"Position Size : {position_size} USDT")


            result = {
                "symbol": symbol,
                "trend": trend,
                "decision": decision,
                "confidence": confidence,
                "score": score,
                "rsi": rsi
            }


            results.append(result)


            memory.save(result)



        print("\n==============================")
        print(" TOP OPPORTUNITIES ")
        print("==============================")


        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        for result in results[:10]:

            print(
                f"{result['symbol']} | "
                f"SCORE {result['score']}/100 | "
                f"{result['decision']} | "
                f"RSI {round(result['rsi'],2)}"
            )


        print("\n==============================")
        print(" PORTFOLIO STATUS ")
        print("==============================")


        portfolio.show()



        print("\n==============================")
        print(" BACKTEST REPORT ")
        print("==============================")


        backtester.run(results)
        print("\n==============================")
        print(" SYSTEM FINISHED ")
        print("==============================")

        log("ATX Platform uruchomiona poprawnie.")
        
        brain_statistics.report()


if __name__ == "__main__":

    app = ATXCore()

    app.start()