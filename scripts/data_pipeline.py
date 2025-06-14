"""Data pipeline to fetch prices and load into a database."""
import pandas as pd
from openbb import obb

# scripts/data_pipeline.py

-from .db_connections import ConnectionManager
+from scripts.db_connections import ConnectionManager  # absolute import

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

INSERT_SQL = """
INSERT INTO prices (symbol, date, open, high, low, close, volume)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""


def fetch_equity(symbol: str, provider: str = "fmp") -> pd.DataFrame:
    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    return data.to_dataframe()


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:
    """Load price data into the database with input validation."""
    required_columns = ["symbol", "date", "open", "high", "low", "close", "volume"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame missing required columns: {missing_columns}")
    
    with conn_manager.context() as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.executemany(
            INSERT_SQL,
            df[required_columns].values.tolist(),
        )
        conn.commit()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"database": "openbb.db"})
    prices = fetch_equity("AAPL")
    preview = preview_data(prices)
    for _, row in preview.iterrows():
        pass  # placeholder for display
    load_prices(prices, cm)

