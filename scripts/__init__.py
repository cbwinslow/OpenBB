"""Helper scripts for OpenBB extensions."""

__all__ = [
    "ConnectionManager",
    "fetch_equity",
    "run_backtest",
    "run_strategy_backtest",
    "add_rule",
    "add_strategy",
    "initialize_db",
]

from .backtesting_agent import run_backtest, run_strategy_backtest
from .data_pipeline import fetch_equity
from .db_connections import ConnectionManager
from .trading_db import add_rule, add_strategy, initialize_db
