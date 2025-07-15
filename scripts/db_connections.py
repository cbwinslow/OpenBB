"""Connection manager for SQLite and PostgreSQL."""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union

from .postgres_connection import PostgresConnectionManager

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)


def list_config_files() -> list[Path]:
    """Return available connection configuration files."""
    return list(CONFIG_DIR.glob("*.json"))


def load_config(name: str) -> dict:
    """Load a configuration file by name."""
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Config {name} not found")
    with path.open() as f:
        return json.load(f)


class SQLiteConnectionManager:
    """Manage SQLite connections."""

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            yield conn


def ConnectionManager(
    config: Optional[dict] = None,
) -> Union[SQLiteConnectionManager, PostgresConnectionManager]:
    """Return a connection manager based on the config."""
    config = config or {}
    db_type = config.get("type", "sqlite")
    if db_type == "sqlite":
        return SQLiteConnectionManager(config)
    if db_type == "postgres":
        return PostgresConnectionManager(config)
    raise ValueError(f"Unsupported database type: {db_type}")
