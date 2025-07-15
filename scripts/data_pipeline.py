def fetch_equity(symbol: str, provider: str = "fmp") -> pd.DataFrame:
    """
    Fetches historical equity price data for a given stock symbol using the specified data provider.
    
    Parameters:
        symbol (str): The stock symbol to retrieve historical price data for.
        provider (str, optional): The data provider to use. Defaults to "fmp".
    
    Returns:
        pd.DataFrame: DataFrame containing historical price data with an added "symbol" column.
    """
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
