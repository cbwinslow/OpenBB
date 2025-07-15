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
    Load and return the contents of a JSON configuration file by name.
    
    Parameters:
        name (str): The base name of the configuration file (without the `.json` extension).
    
    Returns:
        dict: The parsed JSON content of the configuration file.
    
    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Config {name} not found")
    with path.open() as f:
        return json.load(f)



    """Manage SQLite connections."""

    def __init__(self, config: Optional[dict] = None) -> None:
        """
        Initialize the instance with an optional configuration dictionary.
        
        Parameters:
            config (dict, optional): Configuration settings to use. Defaults to an empty dictionary if not provided.
        """
        self.config = config or {}

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        """
        Context manager that yields a SQLite connection with row access by column name.
        
        Parameters:
        	config (dict, optional): Configuration dictionary specifying the database path under the "database" key. If not provided, uses the instance's configuration. Defaults to "openbb.db" if unspecified.
        
        Yields:
        	sqlite3.Connection: An open SQLite connection with row factory set to return rows as dictionaries.
        """
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            yield conn

