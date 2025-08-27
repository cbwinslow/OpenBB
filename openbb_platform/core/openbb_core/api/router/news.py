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
    Retrieve the latest news articles with optional filtering and caching.
    
    Parameters:
        term (str, optional): Keyword to filter news articles by content.
        source (str, optional): Source to filter news articles.
        limit (int, optional): Maximum number of articles to return. Defaults to 10.
    
    Returns:
        List[dict]: A list of news articles as dictionaries, filtered and limited according to the query parameters.
    
    Raises:
        HTTPException: If an error occurs while fetching news data.
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
