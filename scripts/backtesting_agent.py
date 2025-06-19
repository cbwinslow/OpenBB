"""Backtesting agent placeholder."""

import pandas as pd

from .db_connections import ConnectionManager
from .trading_db import list_strategies, record_backtest


def run_backtest(prices: pd.DataFrame) -> dict:
    """Simple backtest: buy and hold return."""
    if prices.empty:
        return {"return": 0.0}

    start = prices["close"].iloc[0]

    return {"return": (end - start) / start}


def run_strategy_backtest(
    strategy_id: int,
    prices: pd.DataFrame,
    conn_manager: ConnectionManager,
) -> dict:
    """Backtest a strategy and store the result."""
    strategies = {s["id"]: s for s in list_strategies(conn_manager)}
    strategy = strategies.get(strategy_id)
    if strategy is None:
        raise ValueError(f"Strategy {strategy_id} not found")

    result = run_backtest(prices)

    return result

