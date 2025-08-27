

    data = obb.equity.price.historical(symbol=symbol, provider=provider)
    df = data.to_dataframe()
    df["symbol"] = symbol
    return df


def load_prices(df: pd.DataFrame, conn_manager: ConnectionManager) -> None:

    """
    Insert multiple rows of equity price data from a DataFrame into the database.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing columns 'symbol', 'date', 'open', 'high', 'low', 'close', and 'volume' to be inserted.
    """
    with conn_manager.context() as conn:
        cur = conn.cursor()
        cur.executemany(
            INSERT_SQL,
            df[["symbol", "date", "open", "high", "low", "close", "volume"]].values.tolist(),
        )
        conn.commit()
        cur.close()


def preview_data(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:

    """
    Return the first `n` rows of the provided DataFrame.
    
    Parameters:
        n (int): Number of rows to return from the top of the DataFrame. Defaults to 5.
    
    Returns:
        pd.DataFrame: A DataFrame containing the first `n` rows.
    """
    return df.head(n)


if __name__ == "__main__":  # pragma: no cover - manual execution
    cm = ConnectionManager({"type": "postgres"})
    prices = fetch_equity("AAPL")
    print(preview_data(prices))
    load_prices(prices, cm)
