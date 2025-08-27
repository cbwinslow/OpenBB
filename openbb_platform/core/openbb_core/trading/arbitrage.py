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
    """
    Identify a simple arbitrage opportunity by comparing the target market price to the cost of a synthetic replication.
    
    Compute the replication cost via recreate_position(instruments) and:
    - return None when replication cost equals target price (no arbitrage),
    - return {"action": "buy_replication_sell_target", "profit": target_price - replication_cost}
      when the replication is cheaper than the target (sell target, buy replication),
    - return {"action": "buy_target_sell_replication", "profit": replication_cost - target_price}
      when the replication is more expensive than the target (buy target, sell replication).
    
    Parameters
    ----------
    target_price : float
        Market price of the target instrument.
    instruments : Dict[str, float]
        Mapping of instrument names to their prices used to recreate the target.
        Negative values may represent short positions and are included in the replication cost.
    
    Returns
    -------
    Dict[str, float] | None
        A dictionary with keys:
          - "action": a string describing the trade to capture the arbitrage,
          - "profit": the positive monetary profit per unit from executing the trade;
        or None if no arbitrage exists (replication cost equals target price).
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
