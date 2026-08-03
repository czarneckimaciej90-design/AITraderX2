class MarketValidator:

    MIN_BARS = 200

    def validate(self, market):

        closes = market["closes"]
        volumes = market["volumes"]
        trades = market["trades"]

        score = 100
        reasons = []

        # ==========================
        # Enough candles
        # ==========================

        if len(closes) < self.MIN_BARS:

            return {

                "valid": False,

                "market_score": 0,

                "reasons": [
                    "Not enough candles"
                ]

            }

        # ==========================
        # Volume statistics
        # ==========================

        total_volume = sum(volumes)
        average_volume = total_volume / len(volumes)
        last_volume = volumes[-1]

        # ==========================
        # Trades statistics
        # ==========================

        total_trades = sum(trades)
        average_trades = total_trades / len(trades)

        # ==========================
        # Zero volume candles
        # ==========================

        zero_volume = sum(

            1

            for v in volumes

            if v <= 0

        )

        zero_ratio = zero_volume / len(volumes)

        # ==========================
        # TOTAL VOLUME
        # ==========================

        if total_volume < 100:

            score -= 40
            reasons.append("Very Low Total Volume")

        elif total_volume < 500:

            score -= 20
            reasons.append("Low Total Volume")

        # ==========================
        # AVERAGE VOLUME
        # ==========================

        if average_volume < 0.5:

            score -= 30
            reasons.append("Very Low Average Volume")

        elif average_volume < 2:

            score -= 15
            reasons.append("Low Average Volume")

        # ==========================
        # LAST CANDLE
        # ==========================

        if last_volume <= 0:

            score -= 50
            reasons.append("Zero Last Volume")

        elif last_volume < average_volume * 0.10:

            score -= 25
            reasons.append("Weak Last Volume")

        elif last_volume < average_volume * 0.25:

            score -= 10
            reasons.append("Low Last Volume")

        # ==========================
        # TRADES
        # ==========================

        if total_trades < 500:

            score -= 30
            reasons.append("Low Trades")

        if average_trades < 5:

            score -= 20
            reasons.append("Low Average Trades")

        # ==========================
        # ZERO VOLUME BARS
        # ==========================

        if zero_ratio > 0.50:

            score -= 50
            reasons.append("Too Many Zero Volume Bars")

        elif zero_ratio > 0.30:

            score -= 30
            reasons.append("Many Zero Volume Bars")

        elif zero_ratio > 0.10:

            score -= 10
            reasons.append("Some Zero Volume Bars")

        # ==========================
        # FINAL SCORE
        # ==========================

        score = max(0, min(score, 100))

        valid = score >= 70

        return {

            "valid": valid,

            "market_score": score,

            "total_volume": round(total_volume, 2),

            "average_volume": round(average_volume, 2),

            "last_volume": round(last_volume, 2),

            "total_trades": total_trades,

            "average_trades": round(average_trades, 2),

            "zero_volume_bars": zero_volume,

            "zero_volume_ratio": round(zero_ratio * 100, 2),

            "reasons": reasons

        }