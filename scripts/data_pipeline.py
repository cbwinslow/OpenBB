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
    """
    Fetches historical price data for a given equity symbol from a specified provider.
    
    Args:
        symbol: The ticker symbol of the equity to fetch.
        provider: The data provider to use (default is "fmp").
    
    Returns:
        A pandas DataFrame containing historical price data for the specified symbol.
    """
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    return data.to_dataframe()


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    """
    Loads historical equity price data from a DataFrame into the database.
    
    Creates the `prices` table if it does not exist and inserts all rows from the DataFrame into the table.
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
    Returns the first n rows of a DataFrame for preview.
    
    Args:
        df: The DataFrame to preview.
        n: Number of rows to return from the top of the DataFrame.
    
    Returns:
        A DataFrame containing the first n rows.
    """
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"database": "openbb.db"})
    prices = fetch_equity("AAPL")
    preview = preview_data(prices)
    for _, row in preview.iterrows():
        pass  # placeholder for display
    load_prices(prices, cm)

