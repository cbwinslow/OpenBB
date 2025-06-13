"""Backtesting agent placeholder."""

import pandas as pd


def run_backtest(prices: pd.DataFrame) -> dict:
    """Simple backtest: buy and hold return."""
    if prices.empty:
        return {"return": 0.0}

    start = prices["close"].iloc[0]
    end = prices["close"].iloc[-1]
    return {"return": (end - start) / start}

