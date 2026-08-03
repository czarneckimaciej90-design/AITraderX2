from indicators.ema import ema_signal
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.atr import calculate_atr

from analysis.trend import detect_trend
from analysis.volume import analyze as analyze_volume


class AnalysisEngine:

    def __init__(self):

        self.version = "0.5.0"

    def analyze(self, market):

        closes = market["closes"]

        signal, ema10, ema20 = ema_signal(closes)

        rsi = calculate_rsi(closes)

        macd, signal_macd, histogram = calculate_macd(closes)

        atr = calculate_atr(closes)

        volume = analyze_volume(market)

        trend = detect_trend(
            ema10,
            ema20,
            rsi
        )

        analysis = {

            "engine_version": self.version,

            "trend": trend,

            "ema": {

                "signal": signal,

                "ema10": ema10,

                "ema20": ema20

            },

            "momentum": {

                "rsi": rsi,

                "macd": macd,

                "signal": signal_macd,

                "histogram": histogram

            },

            "volatility": {

                "atr": atr

            },

            "volume": volume,

            "market": {

                "score": market.get("market_score", 100),

                "validation": market.get("validation", {})

            }

        }

        return analysis
