class MarketValidator:

    MIN_BARS = 200

    def validate(self, market):

        closes = market["closes"]
        volumes = market["volumes"]
        trades = market["trades"]

        score = 100

        reasons = []

        # ---------- Candles ----------

        if len(closes) < self.MIN_BARS:

            score -= 40

            reasons.append("Not enough candles")

        # ---------- Volume ----------

        total_volume = sum(volumes)

        if total_volume <= 0:

            score -= 40

            reasons.append("Zero volume")

        elif total_volume < 100:

            score -= 20

            reasons.append("Low volume")

        # ---------- Trades ----------

        total_trades = sum(trades)

        if total_trades <= 0:

            score -= 40

            reasons.append("Zero trades")

        elif total_trades < 500:

            score -= 20

            reasons.append("Low trades")

        # ---------- Zero volume candles ----------

        zero_bars = sum(
            1
            for v in volumes
            if v == 0
        )

        if zero_bars > 100:

            score -= 20

            reasons.append(
                "Too many zero-volume candles"
            )

        score = max(score, 0)

        return {

            "valid": score >= 60,

            "market_score": score,

            "zero_volume_bars": zero_bars,

            "total_volume": round(total_volume, 2),

            "total_trades": total_trades,

            "reasons": reasons

        }