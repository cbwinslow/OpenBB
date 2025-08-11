"""Realtime price data router."""

from __future__ import annotations

import os
from datetime import datetime
from typing import List

import yfinance as yf
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Price(Base):
    """Database model for price data."""

    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class PriceResponse(BaseModel):
    """Response model for price data."""

    symbol: str
    price: float
    timestamp: datetime


router = APIRouter(prefix="/realtime", tags=["Realtime Price"])


@router.get("/{symbol}", response_model=PriceResponse)
async def get_price(symbol: str) -> PriceResponse:
    """Fetch realtime price without storing it."""
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info["last_price"]
    timestamp = datetime.utcnow()
    return PriceResponse(symbol=symbol, price=price, timestamp=timestamp)


@router.post("/{symbol}", response_model=PriceResponse)
async def fetch_and_store(symbol: str) -> PriceResponse:
    """Fetch realtime price and store it in the database."""
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info["last_price"]
    timestamp = datetime.utcnow()
    db = SessionLocal()
    db.add(Price(symbol=symbol, price=price, timestamp=timestamp))
    db.commit()
    db.close()
    return PriceResponse(symbol=symbol, price=price, timestamp=timestamp)


@router.get("/stored", response_model=List[PriceResponse])
async def get_stored(limit: int = 100) -> List[PriceResponse]:
    """Retrieve stored prices from the database."""
    db = SessionLocal()
    results = db.query(Price).order_by(Price.timestamp.desc()).limit(limit).all()
    db.close()
    return [
        PriceResponse(symbol=r.symbol, price=r.price, timestamp=r.timestamp)
        for r in results
    ]
