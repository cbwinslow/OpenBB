"""Streamlit GUI for strategy management and backtesting."""
from __future__ import annotations

import streamlit as st

from .backtesting_agent import run_strategy_backtest
from .data_pipeline import fetch_equity
from .db_connections import ConnectionManager
from .trading_db import (
    add_rule,
    add_strategy,
    initialize_db,
    list_backtests,
    list_rules,
    list_strategies,
)

st.set_page_config(page_title="OpenBB Strategy Lab", layout="wide")

cm = ConnectionManager({"database": "openbb.db"})
initialize_db(cm)


def tab_data():
    st.header("Price Data & Backtesting")
    symbol = st.text_input("Symbol", "AAPL")
    provider = st.text_input("Provider", "fmp")
    if st.button("Fetch Data"):
        data = fetch_equity(symbol, provider)
        st.line_chart(data.set_index("date")["close"])
        strategies = list_strategies(cm)
        if strategies:
            strategy_names = {s["name"]: s["id"] for s in strategies}
            selected_name = st.selectbox("Strategy", list(strategy_names))
            if st.button("Run Backtest"):
                result = run_strategy_backtest(strategy_names[selected_name], data, cm)
                st.write("Result", result)


def tab_rules():
    st.header("Manage Trading Rules")
    name = st.text_input("Rule Name")
    definition = st.text_area("Definition")
    if st.button("Add Rule") and name and definition:
        add_rule(name, definition, cm)
    st.subheader("Existing Rules")
    for rule in list_rules(cm):
        st.write(rule)


def tab_strategies():
    st.header("Strategies")
    strategies = list_strategies(cm)
    rules = list_rules(cm)
    rule_map = {r["name"]: r["id"] for r in rules}
    name = st.text_input("Strategy Name")
    selected = st.multiselect("Rules", list(rule_map))
    if st.button("Add Strategy") and name and selected:
        add_strategy(name, [rule_map[r] for r in selected], cm)
    st.subheader("Existing Strategies")
    for strat in strategies:
        rule_names = [r for r, _id in rule_map.items() if _id in strat["rule_ids"]]
        st.write(strat["name"], rule_names)


def tab_results():
    st.header("Backtest Results")
    for record in list_backtests(cm):
        st.write(record)


tabs = {
    "Data": tab_data,
    "Rules": tab_rules,
    "Strategies": tab_strategies,
    "Results": tab_results,
}

selected = st.sidebar.selectbox("View", list(tabs))

with st.container():
    tabs[selected]()
