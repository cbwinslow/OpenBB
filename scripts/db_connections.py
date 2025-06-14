import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)

def list_config_files() -> list[Path]:
    """
    Lists all JSON configuration files in the configuration directory.
    
    Returns:
        A list of Path objects representing available JSON configuration files.
    """
    return [p for p in CONFIG_DIR.glob("*.json")]


def load_config(name: str) -> dict:
    """
    Loads and returns the contents of a JSON configuration file by name.
    
    Args:
        name: The base name of the configuration file (without the .json extension).
    
    Returns:
        A dictionary containing the configuration data.
    
    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Config {name} not found")
    with path.open() as f:
        return json.load(f)


class ConnectionManager:
    """Manage database connections."""

    def __init__(self, config: Optional[dict] = None):
        """
        Initializes the ConnectionManager with an optional configuration dictionary.
        
        If no configuration is provided, an empty dictionary is used by default.
        """
        self.config = config or {}
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self, config: Optional[dict] = None) -> sqlite3.Connection:
        """
        Establishes and returns a SQLite database connection using the provided or stored configuration.
        
        If no configuration is given, uses the instance's stored configuration or defaults to "openbb.db".
        The connection's row factory is set to return rows as sqlite3.Row objects.
        
        Returns:
            An active SQLite database connection.
        """
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self) -> None:
        """
        Closes the active SQLite database connection and resets the internal reference.
        """
        if self._conn:
            self._conn.close()
            self._conn = None

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        """
        Provides a context manager for a SQLite database connection.
        
        Opens a connection using the provided or stored configuration, yields it for use within a context, and ensures the connection is closed upon exit.
        	
        Yields:
            sqlite3.Connection: An active SQLite database connection.
        """
        conn = self.connect(config)
        try:
            yield conn
        finally:
            self.close()

