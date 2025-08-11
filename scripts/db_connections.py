import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union

from .postgres_connection import PostgresConnectionManager

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)


def list_config_files() -> list[Path]:

    """
    Return a list of all JSON configuration files in the configs directory.
    
    Returns:
        List of Path objects representing JSON files found in the configuration directory.
    """
    return list(CONFIG_DIR.glob("*.json"))


def load_config(name: str) -> dict:

    """
    Load and return the contents of a JSON configuration file by name.
    
    Parameters:
        name (str): The base name of the configuration file (without the .json extension).
    
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


class ConnectionManager:
    """Manage SQLite connections."""


