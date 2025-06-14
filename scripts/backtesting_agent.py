"""Backtesting agent placeholder."""

import pandas as pd

from .db_connections import ConnectionManager
from .trading_db import list_strategies, record_backtest


def run_backtest(prices: pd.DataFrame) -> dict:
    """
    Performs a simple buy-and-hold backtest on price data.
    
    Calculates the total return as the percentage change from the first to the last closing price in the provided DataFrame. Returns 0.0 if the DataFrame is empty.
    
    Args:
        prices: DataFrame containing at least a 'close' column with price data.
    
    Returns:
        A dictionary with the key 'return' representing the total return as a float.
    """
    if prices.empty:
        return {"return": 0.0}

    start = prices["close"].iloc[0]
    end = prices["close"].iloc[-1]
    return {"return": (end - start) / start}


def run_strategy_backtest(
    strategy_id: int,
    prices: pd.DataFrame,
    conn_manager: ConnectionManager,
) -> dict:
    """
    Executes a backtest for the specified strategy and records the result in the database.
    
    Raises:
        ValueError: If the strategy with the given ID does not exist.
    
    Returns:
        A dictionary containing the backtest result, including the total return.
    """
    strategies = {s["id"]: s for s in list_strategies(conn_manager)}
    strategy = strategies.get(strategy_id)
    if strategy is None:
        raise ValueError(f"Strategy {strategy_id} not found")

    result = run_backtest(prices)
    record_backtest(strategy_id, "", "", result, conn_manager)
    return result

