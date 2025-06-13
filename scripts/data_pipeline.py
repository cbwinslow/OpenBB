"""Data pipeline to fetch prices and load into a database."""
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
    volume REAL
)
"""

INSERT_SQL = """
INSERT INTO prices (symbol, date, open, high, low, close, volume)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""


def fetch_equity(symbol: str, provider: str = "fmp") -> pd.DataFrame:
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    return data.to_dataframe()


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    with conn_manager.context() as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.executemany(
            INSERT_SQL,
            df[["symbol", "date", "open", "high", "low", "close", "volume"]].values.tolist(),
        )
        conn.commit()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"database": "openbb.db"})
    prices = fetch_equity("AAPL")
    print(preview_data(prices))
    load_prices(prices, cm)

