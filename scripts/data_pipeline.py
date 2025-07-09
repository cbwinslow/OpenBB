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
    """Fetch historical prices using the OpenBB SDK."""
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    return data.to_dataframe()


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    """Load price data into the database."""
    with conn_manager.context() as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.executemany(
            INSERT_SQL,
            df[["symbol", "date", "open", "high", "low", "close", "volume"]].values.tolist(),
        )
        conn.commit()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return a sample of the data for quick inspection."""
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"database": "openbb.db"})
    prices = fetch_equity("AAPL")
    print(preview_data(prices))
    load_prices(prices, cm)
