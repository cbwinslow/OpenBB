"""Minimal framework for strategy backtesting."""
from __future__ import annotations

from typing import List, Protocol, Sequence


class Strategy(Protocol):
    """Protocol for trading strategies used by :class:`Backtester`."""

    def generate_signals(self, prices: Sequence[float]) -> Sequence[int]:
        """Return position signals for each price point."""


class BuyAndHoldStrategy:
    """Simple strategy that stays long for the entire period."""

    def generate_signals(self, prices: Sequence[float]) -> List[int]:
        return [1] * len(prices)


class Backtester:
    """Simulate a strategy on historical price data."""

    def __init__(self, prices: Sequence[float], strategy: Strategy) -> None:
        self.prices = list(prices)
        self.strategy = strategy

    def run(self) -> float:
        """Return cumulative performance of the strategy."""
        if len(self.prices) < 2:
            return 0.0
        signals = list(self.strategy.generate_signals(self.prices))
        if len(signals) != len(self.prices):
            raise ValueError("signals and prices must have same length")
        returns = [
            (self.prices[i] - self.prices[i - 1]) / self.prices[i - 1]
            for i in range(1, len(self.prices))
        ]
        performance = 0.0
        for ret, sig in zip(returns, signals[1:]):
            performance += ret * sig
        return performance
