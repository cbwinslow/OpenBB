"""Utilities for ingesting historical prices into a database."""

from __future__ import annotations

import pandas as pd
from openbb import obb

from .db_connections import ConnectionManager

INSERT_SQL = """
    INSERT INTO prices (symbol, date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (symbol, date) DO UPDATE SET
        open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        volume = EXCLUDED.volume
"""


def fetch_equity(symbol: str, provider: str = "fmp") -> pd.DataFrame:
    """Fetch historical prices using the OpenBB SDK."""
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    df = data.to_dataframe()
    df["symbol"] = symbol
    return df


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    """Load price data into the database."""
    with conn_manager.context() as conn:
        cur = conn.cursor()
        cur.executemany(
            INSERT_SQL,
            df[["symbol", "date", "open", "high", "low", "close", "volume"]].values.tolist(),
        )
        conn.commit()
        cur.close()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return a sample of the data for quick inspection."""
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"type": "postgres"})
    prices = fetch_equity("AAPL")
    print(preview_data(prices))
    load_prices(prices, cm)
