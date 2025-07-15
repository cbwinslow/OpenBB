"""PostgreSQL connection manager."""

import psycopg2
from contextlib import contextmanager
from typing import Iterator, Optional

class PostgresConnectionManager:
    """Manage PostgreSQL connections."""

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[psycopg2.extensions.connection]:
        cfg = config or self.config
        conn = psycopg2.connect(
            host=cfg.get("host", "localhost"),
            port=cfg.get("port", 5432),
            user=cfg.get("user", "postgres"),
            password=cfg.get("password", "postgres"),
            dbname=cfg.get("database", "openbb"),
        )
        try:
            yield conn
        finally:
            conn.close()
