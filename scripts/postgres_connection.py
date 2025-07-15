"""PostgreSQL connection manager."""

import psycopg2
from contextlib import contextmanager
from typing import Iterator, Optional

class PostgresConnectionManager:
    """Manage PostgreSQL connections."""

    def __init__(self, config: Optional[dict] = None) -> None:
        """
        Initialize the PostgresConnectionManager with an optional configuration dictionary.
        
        If no configuration is provided, defaults to an empty dictionary.
        """
        self.config = config or {}

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[psycopg2.extensions.connection]:
        """
        Context manager that yields a PostgreSQL database connection using the provided or default configuration.
        
        Parameters:
            config (Optional[dict]): Optional dictionary specifying connection parameters. If not provided, the instance's configuration is used.
        
        Yields:
            psycopg2.extensions.connection: An active PostgreSQL connection, which is automatically closed upon exiting the context.
        """
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
