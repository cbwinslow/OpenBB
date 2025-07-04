"""News router for fetching latest articles."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException
from openbb_biztoc.models.world_news import BiztocWorldNewsFetcher
from openbb_core.app.service.user_service import UserService

router = APIRouter(prefix="/news", tags=["News"])


def _credentials() -> dict:
    """Return user credentials from settings."""
    return UserService().default_user_settings.credentials.model_dump(mode="json")


@router.get("/latest", response_model=List[dict])
async def get_latest_news(
    term: str | None = None,
    source: str | None = None,
    limit: int = 10,
) -> List[dict]:
    """Fetch latest news articles."""
    params = {"term": term, "source": source, "limit": limit}
    try:
        data = await BiztocWorldNewsFetcher.fetch_data(params=params, credentials=_credentials())
        return [item.model_dump() for item in data]
    except Exception as err:  # pragma: no cover - simple handler
        raise HTTPException(status_code=500, detail=str(err)) from err
