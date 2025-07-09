"""Simplistic backtesting utilities."""

import pandas as pd

from .db_connections import ConnectionManager
from .trading_db import list_strategies, record_backtest


def run_backtest(prices: pd.DataFrame) -> dict:
    """Simple buy-and-hold backtest."""
    if prices.empty:
        return {"return": 0.0}

    start = prices["close"].iloc[0]
    end = prices["close"].iloc[-1]
    if start == 0:
        return {"return": 0.0}

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
    start_date = str(prices["date"].iloc[0]) if "date" in prices.columns else ""
    end_date = str(prices["date"].iloc[-1]) if "date" in prices.columns else ""
    record_backtest(strategy_id, start_date, end_date, result, conn_manager)
    return result


