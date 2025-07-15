"""Create tables in the PostgreSQL database."""

from .db_connections import ConnectionManager

# Tables from trading_db.py
CREATE_RULES_SQL = """
CREATE TABLE IF NOT EXISTS rules (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    definition TEXT NOT NULL
)
"""

CREATE_STRATEGIES_SQL = """
CREATE TABLE IF NOT EXISTS strategies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    rule_ids JSONB NOT NULL
)
"""

CREATE_BACKTESTS_SQL = """
CREATE TABLE IF NOT EXISTS backtests (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    result JSONB NOT NULL,
    FOREIGN KEY(strategy_id) REFERENCES strategies(id)
)
"""

# New tables
CREATE_NEWS_SQL = """
CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    symbol TEXT,
    published_at TIMESTAMPTZ NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT,
    summary TEXT
)
"""

CREATE_COMPANY_FUNDAMENTALS_SQL = """
CREATE TABLE IF NOT EXISTS company_fundamentals (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    CIK TEXT,
    name TEXT,
    sector TEXT,
    industry TEXT,
    market_cap BIGINT,
    shares_outstanding BIGINT,
    UNIQUE(symbol)
)
"""

CREATE_ECONOMIC_DATA_SQL = """
CREATE TABLE IF NOT EXISTS economic_data (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    value REAL,
    date TIMESTAMPTZ,
    source TEXT,
    UNIQUE(name, date)
)
"""

CREATE_PRICES_SQL = """
CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume BIGINT,
    UNIQUE(symbol, date)
)
"""


def create_tables(conn_manager: ConnectionManager) -> None:
    """
    Create all required tables in the PostgreSQL database using the provided connection manager.
    
    This function executes SQL statements to create the `rules`, `strategies`, `backtests`, `news`, `company_fundamentals`, `economic_data`, and `prices` tables if they do not already exist.
    """
    with conn_manager.context() as conn:
        cur = conn.cursor()
        cur.execute(CREATE_RULES_SQL)
        cur.execute(CREATE_STRATEGIES_SQL)
        cur.execute(CREATE_BACKTESTS_SQL)
        cur.execute(CREATE_NEWS_SQL)
        cur.execute(CREATE_COMPANY_FUNDAMENTALS_SQL)
        cur.execute(CREATE_ECONOMIC_DATA_SQL)
        cur.execute(CREATE_PRICES_SQL)
        conn.commit()
        cur.close()


if __name__ == "__main__":
    # Example usage with a PostgreSQL database
    cm = ConnectionManager({"type": "postgres"})
    create_tables(cm)
    print("Tables created successfully.")
