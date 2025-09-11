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



    replication_cost = recreate_position(instruments)
    if math.isclose(replication_cost, target_price, rel_tol=tol, abs_tol=tol):
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
