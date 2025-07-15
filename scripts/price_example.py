"""Sample script for fetching realtime prices using yfinance."""

from __future__ import annotations

from datetime import datetime

import yfinance as yf


def get_price(symbol: str) -> tuple[float, datetime]:
    """Return latest price and timestamp for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info["last_price"]
        if price is None:
            raise ValueError(f"No price data available for symbol: {symbol}")
        return price, datetime.now(timezone.utc)
    except Exception as e:
        raise ValueError(f"Failed to fetch price for {symbol}: {e}") from e


if __name__ == "__main__":
    price, ts = get_price("AAPL")
    print("AAPL", price, ts.isoformat())  # noqa: T201
