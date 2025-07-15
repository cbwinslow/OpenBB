"""Simplistic backtesting utilities."""

import pandas as pd

from .db_connections import ConnectionManager
from .trading_db import list_strategies, record_backtest


def run_backtest(prices: pd.DataFrame) -> dict:
    """
    Performs a simple buy-and-hold backtest on price data.
    
    Calculates the total return as the percentage change from the first to the last closing price. Returns 0.0 if the input data is empty or the initial closing price is zero.
    
    Returns:
        dict: A dictionary with the key "return" containing the calculated return as a float.
    """
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
    """
    Executes a backtest for the specified strategy using provided price data and records the result in the database.
    
    Raises:
        ValueError: If the strategy with the given ID does not exist.
    
    Returns:
        dict: The backtest result, typically containing the total return.
    """
    strategies = {s["id"]: s for s in list_strategies(conn_manager)}
    strategy = strategies.get(strategy_id)
    if strategy is None:
        raise ValueError(f"Strategy {strategy_id} not found")

    result = run_backtest(prices)
    start_date = str(prices["date"].iloc[0]) if "date" in prices.columns else ""
    end_date = str(prices["date"].iloc[-1]) if "date" in prices.columns else ""
    record_backtest(strategy_id, start_date, end_date, result, conn_manager)
    return result


