"""Utilities for ingesting historical prices into a SQLite database."""

from __future__ import annotations

import pandas as pd
from openbb import obb

from .db_connections import ConnectionManager

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    UNIQUE(symbol, date)
)
"""

INSERT_SQL = (
    "INSERT OR REPLACE INTO prices (symbol, date, open, high, low, close, volume)"
    " VALUES (?, ?, ?, ?, ?, ?, ?)"
)


def fetch_equity(symbol: str, provider: str = "fmp") -> pd.DataFrame:
    """
    Fetches historical price data for a given equity symbol using the OpenBB SDK.
    
    Parameters:
        symbol (str): The ticker symbol of the equity to fetch.
        provider (str): The data provider to use (default is "fmp").
    
    Returns:
        pd.DataFrame: DataFrame containing the historical price data for the specified symbol.
    """
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    return data.to_dataframe()


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    """
    Insert historical price data from a DataFrame into the SQLite database.
    
    Creates the `prices` table if it does not exist and inserts or replaces rows for each record in the DataFrame.
    """
    with conn_manager.context() as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.executemany(
            INSERT_SQL,
            df[["symbol", "date", "open", "high", "low", "close", "volume"]].values.tolist(),
        )
        conn.commit()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Return the first `n` rows of the DataFrame for preview.
    
    Parameters:
        n (int): Number of rows to return from the top of the DataFrame.
    
    Returns:
        pd.DataFrame: A DataFrame containing the first `n` rows.
    """
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"database": "openbb.db"})
    prices = fetch_equity("AAPL")
    print(preview_data(prices))
    load_prices(prices, cm)
