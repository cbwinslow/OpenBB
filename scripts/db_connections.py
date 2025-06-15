import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)

def list_config_files() -> list[Path]:
    """
    Lists all available JSON configuration files in the configs directory.
    
    Returns:
        A list of Path objects representing JSON configuration files.
    """
    return list(CONFIG_DIR.glob("*.json"))


def load_config(name: str) -> dict:
    """
    Loads and returns the contents of a JSON configuration file by name.
    
    Args:
        name: The base name of the configuration file (without the ".json" extension).
    
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


Drop the manual `_conn` state and `close()` in favor of sqlite3’s built-in context manager. This halves the code and removes error-prone state. For example:

```python
from contextlib import contextmanager

class ConnectionManager:
    def __init__(self, config: Optional[dict] = None):
        """
        Initializes the ConnectionManager with an optional default configuration dictionary.
        
        Args:
        	config: Optional dictionary specifying default database connection settings.
        """
        self.config = config or {}

    @contextmanager
    def connection(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        """
        Context manager that yields a SQLite database connection using the specified or default configuration.
        
        The connection is automatically closed when exiting the context.
        """
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        # sqlite3.connect already cleans up on exit
        with sqlite3.connect(db_path) as conn:
            yield conn
    """Manage database connections."""

    def __init__(self, config: Optional[dict] = None):
        """
        Initializes the ConnectionManager with an optional default configuration.
        
        Args:
            config: Optional dictionary specifying default database connection settings.
        """
        self.config = config or {}
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self, config: Optional[dict] = None) -> sqlite3.Connection:
        """
        Opens a SQLite database connection using the specified or default configuration.
        
        If a configuration dictionary is provided, its "database" key determines the database file path; otherwise, the instance's default configuration or "openbb.db" is used. The connection's row factory is set to allow named column access.
        
        Returns:
            A SQLite connection object with row access by column name.
        """
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self) -> None:
        """
        Closes the active SQLite database connection managed by this instance.
        
        If no connection is open, this method has no effect.
        """
        if self._conn:
            self._conn.close()
            self._conn = None

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        """
        Context manager that yields a SQLite connection and ensures it is closed after use.
        
        Opens a connection using the provided or default configuration, yields it for use within a context, and guarantees the connection is closed upon exiting the context.
        """
        conn = self.connect(config)
        try:
            yield conn
        finally:
            self.close()

