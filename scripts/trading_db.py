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
    """
    Initializes the database by creating tables for trading rules, strategies, and backtests if they do not exist.
    """
    with conn_manager.context() as conn:
        conn.execute(CREATE_RULES_SQL)
        conn.execute(CREATE_STRATEGIES_SQL)
        conn.execute(CREATE_BACKTESTS_SQL)
        conn.commit()


def add_rule(name: str, definition: str, conn_manager: ConnectionManager) -> int:
    """
    Inserts a new trading rule into the database and returns the rule's unique ID.
    
    Args:
        name: The name of the trading rule.
        definition: The definition or logic of the trading rule.
    
    Returns:
        The ID of the newly inserted trading rule.
    """
    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO rules (name, definition) VALUES (?, ?)",
            (name, definition),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_rules(conn_manager: ConnectionManager) -> List[dict]:
    """
    Retrieves all trading rules from the database.
    
    Returns:
        A list of dictionaries, each containing the 'id', 'name', and 'definition' of a rule.
    """
    with conn_manager.context() as conn:
        cur = conn.execute("SELECT id, name, definition FROM rules")
        return [dict(row) for row in cur.fetchall()]


def add_strategy(name: str, rule_ids: Sequence[int], conn_manager: ConnectionManager) -> int:
    """
    Inserts a new strategy with the specified name and associated rule IDs into the database.
    
    Args:
        name: The name of the strategy.
        rule_ids: A sequence of rule IDs that define the strategy.
    
    Returns:
        The ID of the newly created strategy.
    """
    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO strategies (name, rule_ids) VALUES (?, ?)",
            (name, json.dumps(list(rule_ids))),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_strategies(conn_manager: ConnectionManager) -> List[dict]:
    """
    Retrieves all strategies from the database.
    
    Each strategy includes its ID, name, and a list of associated rule IDs.
    Returns:
        A list of dictionaries, each containing 'id', 'name', and 'rule_ids' (as a list of integers).
    """
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
    """
    Inserts a backtest record for a strategy with specified dates and result data.
    
    Args:
        strategy_id: The ID of the strategy associated with the backtest.
        start_date: The start date of the backtest period (ISO format).
        end_date: The end date of the backtest period (ISO format).
        result: The result data of the backtest, which will be JSON-encoded.
    
    Returns:
        The ID of the newly created backtest record.
    """
    with conn_manager.context() as conn:
        cur = conn.execute(
            "INSERT INTO backtests (strategy_id, start_date, end_date, result) VALUES (?, ?, ?, ?)",
            (strategy_id, start_date, end_date, json.dumps(result)),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_backtests(conn_manager: ConnectionManager) -> List[dict]:
    """
    Retrieves all backtest records from the database.
    
    Each record includes the backtest ID, associated strategy ID, start and end dates, and the decoded result data.
    
    Returns:
        A list of dictionaries, each containing 'id', 'strategy_id', 'start_date', 'end_date', and 'result'.
    """
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
