"""Historical price data router."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import yfinance as yf
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import Column, Date, Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "sqlite:///historical.db"
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class HistoricalPrice(Base):
    __tablename__ = "historical_prices"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


Base.metadata.create_all(bind=engine)


class PriceBar(BaseModel):
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


router = APIRouter(prefix="/history", tags=["Historical Price"])


@router.get("/{symbol}", response_model=List[PriceBar])
async def get_history(
    symbol: str,
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
) -> List[PriceBar]:
    """
    Retrieve historical price data for a financial symbol, store it in the database, and return the stored records.
    
    Downloads historical price data for the specified symbol and optional date range from Yahoo Finance, updates the local database with the retrieved data, and returns all stored historical price records for the symbol in descending date order.
    
    Parameters:
        symbol (str): The financial symbol to fetch historical prices for.
        start (Optional[str]): The start date for the historical data range (YYYY-MM-DD). If not provided, retrieves all available data.
        end (Optional[str]): The end date for the historical data range (YYYY-MM-DD). If not provided, retrieves data up to the most recent available.
    
    Returns:
        List[PriceBar]: A list of historical price records for the symbol, ordered by date descending.
    """
    df = yf.download(symbol, start=start, end=end, progress=False)
    df.reset_index(inplace=True)
    with Session(engine) as session:
        for _, row in df.iterrows():
            session.merge(
                HistoricalPrice(
                    symbol=symbol,
                    date=row["Date"].date(),
                    open=row["Open"],
                    high=row["High"],
                    low=row["Low"],
                    close=row["Close"],
                    volume=row["Volume"],
                )
            )
        session.commit()
        stmt = select(HistoricalPrice).where(HistoricalPrice.symbol == symbol).order_by(HistoricalPrice.date.desc())
        rows = session.execute(stmt).scalars().all()
    return [
        PriceBar(
            symbol=r.symbol,
            date=datetime.combine(r.date, datetime.min.time()),
            open=r.open,
            high=r.high,
            low=r.low,
            close=r.close,
            volume=r.volume,
        )
        for r in rows
    ]
