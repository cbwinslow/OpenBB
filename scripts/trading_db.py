"""Utilities for storing trading rules and strategies."""
import json
from typing import Any, List, Sequence

from .db_connections import ConnectionManager

CREATE_RULES_SQL = """
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    definition TEXT NOT NULL
)
"""

CREATE_STRATEGIES_SQL = """
CREATE TABLE IF NOT EXISTS strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rule_ids TEXT NOT NULL
)
"""

CREATE_BACKTESTS_SQL = """
CREATE TABLE IF NOT EXISTS backtests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id INTEGER NOT NULL,
    start_date TEXT,
    end_date TEXT,
    result TEXT NOT NULL,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
)
"""


def initialize_db(conn_manager: ConnectionManager) -> None:
    """Create tables for trading rules and strategies."""
    with conn_manager.context() as conn:
        conn.execute(CREATE_RULES_SQL)
        conn.execute(CREATE_STRATEGIES_SQL)
        conn.execute(CREATE_BACKTESTS_SQL)
        conn.commit()


def add_rule(name: str, definition: str, conn_manager: ConnectionManager) -> int:
    """Insert a trading rule and return its ID."""
    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO rules (name, definition) VALUES (?, ?)",
            (name, definition),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_rules(conn_manager: ConnectionManager) -> List[dict]:
    """Return all rules."""
    with conn_manager.context() as conn:
        cur = conn.execute("SELECT id, name, definition FROM rules")
        return [dict(row) for row in cur.fetchall()]


def add_strategy(name: str, rule_ids: Sequence[int], conn_manager: ConnectionManager) -> int:
    """Insert a strategy composed of rule IDs."""

    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO strategies (name, rule_ids) VALUES (?, ?)",
            (name, json.dumps(list(rule_ids))),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_strategies(conn_manager: ConnectionManager) -> List[dict]:
    """Return all strategies."""
    with conn_manager.context() as conn:
        cur = conn.execute("SELECT id, name, rule_ids FROM strategies")
        rows = cur.fetchall()
        return [dict(id=row[0], name=row[1], rule_ids=json.loads(row[2])) for row in rows]


def record_backtest(
    strategy_id: int,
    start_date: str,
    end_date: str,
    result: Any,
    conn_manager: ConnectionManager,
) -> int:
    """Record backtest results."""
    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO backtests (strategy_id, start_date, end_date, result) VALUES (?, ?, ?, ?)",
            (strategy_id, start_date, end_date, json.dumps(result)),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_backtests(conn_manager: ConnectionManager) -> List[dict]:
    """Return all backtest records."""
    with conn_manager.context() as conn:
        cur = conn.execute(
            "SELECT id, strategy_id, start_date, end_date, result FROM backtests"
        )
        rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "strategy_id": row[1],
                "start_date": row[2],
                "end_date": row[3],
                "result": json.loads(row[4]),
            }
            for row in rows
        ]
