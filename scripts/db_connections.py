import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)

def list_config_files() -> list[Path]:
    """Return a list of available connection configuration files."""
    return [p for p in CONFIG_DIR.glob("*.json")]


def load_config(name: str) -> dict:
    """Load a configuration file by name (without extension)."""
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Config {name} not found")
    with path.open() as f:
        return json.load(f)


class ConnectionManager:
    """Manage database connections."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self, config: Optional[dict] = None) -> sqlite3.Connection:
        cfg = config or self.config
        db_path = cfg.get("database", "openbb.db")
        self._conn = sqlite3.connect(db_path)
        return self._conn

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    @contextmanager
    def context(self, config: Optional[dict] = None) -> Iterator[sqlite3.Connection]:
        conn = self.connect(config)
        try:
            yield conn
        finally:
            self.close()

