"""Sample script for fetching realtime prices using yfinance."""

from __future__ import annotations

from datetime import datetime

import yfinance as yf


def get_price(symbol: str):
    """Return latest price and timestamp for a symbol."""
    ticker = yf.Ticker(symbol)
    return ticker.fast_info["last_price"], datetime.utcnow()


if __name__ == "__main__":
    price, ts = get_price("AAPL")
    print("AAPL", price, ts.isoformat())  # noqa: T201
