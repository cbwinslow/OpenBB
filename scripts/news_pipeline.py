"""Example script to fetch free news data using the Biztoc API."""

from __future__ import annotations

from openbb_biztoc.models.world_news import BiztocWorldNewsFetcher
from openbb_core.app.service.user_service import UserService

from .db_connections import ConnectionManager

INSERT_SQL = """
    INSERT INTO news (symbol, published_at, title, url, source, summary)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING
"""


def get_credentials() -> dict:
    """
    Retrieve the stored user credentials as a JSON-compatible dictionary.
    
    Returns:
        dict: User credentials in a format suitable for JSON serialization.
    """
    return UserService().default_user_settings.credentials.model_dump(mode="json")


def latest_news(limit: int = 10):
    """
    Fetches the latest news articles from the BiztocWorldNewsFetcher API.
    
    Parameters:
        limit (int): The maximum number of news articles to retrieve. Defaults to 10.
    
    Returns:
        list: A list of news articles retrieved from the API.
    """
    params = {"limit": limit}
    data = BiztocWorldNewsFetcher.fetch_data(params=params, credentials=get_credentials())
    return data


def load_news(articles: list, conn_manager: ConnectionManager) -> None:
    """
    Insert a list of news articles into the database, skipping duplicates based on URL.
    
    Parameters:
        articles (list): List of news article objects to be inserted.
    """
    with conn_manager.context() as conn:
        cur = conn.cursor()
        for article in articles:
            cur.execute(
                INSERT_SQL,
                (
                    article.symbol,
                    article.published_at,
                    article.title,
                    article.url,
                    article.source,
                    article.summary,
                ),
            )
        conn.commit()
        cur.close()


if __name__ == "__main__":
    articles = latest_news(20)
    cm = ConnectionManager({"type": "postgres"})
    load_news(articles, cm)
    print(f"Loaded {len(articles)} articles into the database.")
