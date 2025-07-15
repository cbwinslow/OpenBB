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
    """
    Load and return the configuration dictionary from a JSON file with the given name.
    
    Parameters:
        name (str): The base name of the configuration file (without extension).
    
    Returns:
        dict: The configuration data loaded from the JSON file.
    
    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Config {name} not found")
    with path.open() as f:
        return json.load(f)


class SQLiteConnectionManager:
    """Manage SQLite connections."""

    def __init__(self, config: Optional[dict] = None) -> None:
        """
        Initialize the SQLiteConnectionManager with an optional configuration dictionary.
        
        Parameters:
            config (dict, optional): Configuration settings for the SQLite connection. If not provided, defaults to an empty dictionary.
        """
        self.config = config or {}

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        """
        Context manager that yields a SQLite database connection using the specified configuration.
        
        Parameters:
        	config (dict, optional): Configuration dictionary specifying the database file path under the "database" key. If not provided, the instance's configuration is used.
        
        Yields:
        	sqlite3.Connection: An open SQLite connection with row factory set to return rows as dictionaries.
        """
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            yield conn


def ConnectionManager(
    config: Optional[dict] = None,
) -> Union[SQLiteConnectionManager, PostgresConnectionManager]:
    """
    Return a connection manager instance for SQLite or PostgreSQL based on the provided configuration.
    
    If the configuration specifies a `"type"` of `"sqlite"`, returns a `SQLiteConnectionManager`. If `"type"` is `"postgres"`, returns a `PostgresConnectionManager`. Raises a `ValueError` for unsupported database types.
    
    Parameters:
        config (dict, optional): Configuration dictionary with a `"type"` key indicating the database type.
    
    Returns:
        SQLiteConnectionManager or PostgresConnectionManager: An instance appropriate for the specified database type.
    
    Raises:
        ValueError: If the database type specified in the config is not supported.
    """
    config = config or {}
    db_type = config.get("type", "sqlite")
    if db_type == "sqlite":
        return SQLiteConnectionManager(config)
    if db_type == "postgres":
        return PostgresConnectionManager(config)
    raise ValueError(f"Unsupported database type: {db_type}")
