"""News router for fetching latest articles."""

from __future__ import annotations

import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from openbb_biztoc.models.world_news import BiztocWorldNewsFetcher
from openbb_core.app.service.auth_service import AuthService
from openbb_core.app.service.user_service import UserService

router = APIRouter(prefix="/news", tags=["News"])
auth_hook = AuthService().auth_hook

_cache: dict[str, tuple[float, list[dict]]] = {}


def _credentials() -> dict:
    """
    Retrieve the current user's credentials as a JSON-compatible dictionary.
    
    Returns:
        dict: The user's credentials extracted from default user settings.
    """
    return UserService().default_user_settings.credentials.model_dump(mode="json")


@router.get("/latest", response_model=List[dict])
async def get_latest_news(
    term: str | None = None,
    source: str | None = None,
    limit: int = 10,
    _: None = Depends(auth_hook),
) -> List[dict]:
    """
    Retrieve the latest news articles, filtered by optional search term and source, with results cached for five minutes.
    
    Parameters:
        term (str, optional): Search term to filter news articles.
        source (str, optional): Specific news source to filter results.
        limit (int): Maximum number of articles to return.
    
    Returns:
        List[dict]: A list of news article dictionaries matching the specified filters.
    """
    key = f"{term}-{source}-{limit}"
    ts, cached = _cache.get(key, (0.0, []))
    if time.time() - ts < 300 and cached:
        return cached
    params = {"term": term, "source": source, "limit": limit}
    try:
        data = await BiztocWorldNewsFetcher.fetch_data(params=params, credentials=_credentials())
        items = [item.model_dump() for item in data]
        _cache[key] = (time.time(), items)
        return items
    except Exception as err:  # pragma: no cover - simple handler
        raise HTTPException(status_code=500, detail=str(err)) from err
