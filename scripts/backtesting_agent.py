"""Backtesting agent placeholder."""

import pandas as pd

from .db_connections import ConnectionManager
from .trading_db import list_strategies, record_backtest


def run_backtest(prices: pd.DataFrame) -> dict:
    """
    Performs a simple buy-and-hold backtest on price data.
    
    Calculates the total return as the percentage change between the first and last closing prices in the DataFrame. Returns 0.0 if the DataFrame is empty. If the starting price is zero, returns infinity if the ending price is positive, otherwise zero.
    
    Args:
        prices: DataFrame containing a 'close' column with price data.
    
    Returns:
        A dictionary with the key "return" representing the total return.
    """
    if prices.empty:
        return {"return": 0.0}

    start = prices["close"].iloc[0]
    if start == 0:
        return {"return": float('inf') if end > 0 else 0.0}
    return {"return": (end - start) / start}


def run_strategy_backtest(
    strategy_id: int,
    prices: pd.DataFrame,
    conn_manager: ConnectionManager,
) -> dict:
    """
    Backtests a specific trading strategy using provided price data and records the result.
    
    Args:
        strategy_id: The unique identifier of the strategy to backtest.
        prices: A pandas DataFrame containing price data, expected to include a 'date' column.
        
    Returns:
        A dictionary containing the backtest result, typically with a 'return' key.
    
    Raises:
        ValueError: If the specified strategy is not found in the database.
    """
    strategies = {s["id"]: s for s in list_strategies(conn_manager)}
    strategy = strategies.get(strategy_id)
    if strategy is None:
        raise ValueError(f"Strategy {strategy_id} not found")

    result = run_backtest(prices)
    start_date = str(prices["date"].iloc[0]) if "date" in prices.columns else ""
    end_date   = str(prices["date"].iloc[-1]) if "date" in prices.columns else ""
    record_backtest(strategy_id, start_date, end_date, result, conn_manager)
    return result

