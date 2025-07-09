"""Portfolio performance router."""

from __future__ import annotations

from datetime import date, timedelta
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


class PerformancePoint(BaseModel):
    date: str
    value: float


@router.get("/performance", response_model=List[PerformancePoint])
async def get_performance() -> List[PerformancePoint]:
    """Return sample portfolio performance data."""
    today = date.today()
    data = [
        PerformancePoint(date=str(today - timedelta(days=i)), value=10000 + i * 10)
        for i in range(30, -1, -1)
    ]
    return data
