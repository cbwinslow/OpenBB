"""Utilities for detecting arbitrage opportunities.

These functions compare the market price of a target instrument against
its synthetic replication using other instruments.  A difference between
these values implies an arbitrage opportunity.
"""
from __future__ import annotations

from typing import Dict


def recreate_position(instruments: Dict[str, float]) -> float:
    """Return the cost of recreating a position from market instruments.

    Parameters
    ----------
    instruments : Dict[str, float]
        Mapping of instrument names to their prices.  Negative prices may be
        used to represent short positions.

    Returns
    -------
    float
        Total cost of the synthetic position.
    """
    return sum(instruments.values())


def find_arbitrage(target_price: float, instruments: Dict[str, float]) -> Dict[str, float] | None:
    """Identify arbitrage relative to the target price.

    Parameters
    ----------
    target_price : float
        Market price of the target instrument.
    instruments : Dict[str, float]
        Instruments used to recreate the target.

    Returns
    -------
    Dict[str, float] | None
        Information about the arbitrage trade if one exists, otherwise ``None``.
    """
    replication_cost = recreate_position(instruments)
    if replication_cost == target_price:
        return None
    if replication_cost < target_price:
        return {
            "action": "buy_replication_sell_target",
            "profit": target_price - replication_cost,
        }
    return {
        "action": "buy_target_sell_replication",
        "profit": replication_cost - target_price,
    }
