"""Example script to fetch free news data using the Biztoc API."""

from __future__ import annotations

from openbb_biztoc.models.world_news import BiztocWorldNewsFetcher
from openbb_core.app.service.user_service import UserService


def get_credentials() -> dict:
    """Return stored credentials."""
    return UserService().default_user_settings.credentials.model_dump(mode="json")


def latest_news(limit: int = 10):
    """Fetch latest news articles."""
    params = {"limit": limit}
    data = BiztocWorldNewsFetcher.fetch_data(params=params, credentials=get_credentials())
    return data


if __name__ == "__main__":
    for article in latest_news(5):
        print(article.title, "-", article.source)  # noqa: T201
