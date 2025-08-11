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

    """
    Retrieve simulated portfolio performance data for the past 31 days.
    
    Returns:
        List[PerformancePoint]: A list of performance data points, each containing a date (as a string) and a value starting at 10,000 and increasing by 10 for each subsequent day.
    """
    today = date.today()
    data = [
        PerformancePoint(date=str(today - timedelta(days=i)), value=10000 + i * 10)
        for i in range(30, -1, -1)
    ]
    return data
