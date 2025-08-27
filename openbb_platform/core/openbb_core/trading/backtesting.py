"""Minimal framework for strategy backtesting."""
from __future__ import annotations

from typing import List, Protocol, Sequence


class Strategy(Protocol):
    """Protocol for trading strategies used by :class:`Backtester`."""

    def generate_signals(self, prices: Sequence[float]) -> Sequence[int]:
        """
        Return position signals for each price point.
        
        Parameters:
            prices (Sequence[float]): Price series to generate signals for.
        
        Returns:
            Sequence[int]: Sequence of integer position signals with the same length as `prices`, where each element corresponds to the desired position at the same index (commonly -1 for short, 0 for flat, 1 for long).
        """


class BuyAndHoldStrategy:
    """Simple strategy that stays long for the entire period."""

    def generate_signals(self, prices: Sequence[float]) -> List[int]:
        """
        Return a long (1) position for every price point.
        
        Parameters:
            prices (Sequence[float]): Sequence of price observations to generate signals for.
        
        Returns:
            List[int]: A list of 1s with the same length as `prices`, representing a buy-and-hold (always long) signal at each time step.
        """
        return [1] * len(prices)


class Backtester:
    """Simulate a strategy on historical price data."""

    def __init__(self, prices: Sequence[float], strategy: Strategy) -> None:
        """
        Initialize the Backtester.
        
        Parameters:
            prices (Sequence[float]): Historical price series; copied to an internal list.
            strategy (Strategy): Strategy instance that implements `generate_signals(prices)` used during backtesting.
        """
        self.prices = list(prices)
        self.strategy = strategy

    def run(self) -> float:
        """
        Compute and return the strategy's cumulative performance over the stored price series.
        
        If fewer than two prices are available, returns 0.0. The method obtains signals from the strategy (one signal per price), validates that the signals length matches the prices length (raises ValueError otherwise), computes per-period returns as (price[i] - price[i-1]) / price[i-1], and accumulates performance by summing each period return multiplied by the strategy's signal for that period (signals are aligned so the first return is paired with signals[1]).
        
        Returns:
            float: Accumulated performance (sum of period returns weighted by corresponding signals).
        
        Raises:
            ValueError: If the number of signals returned by the strategy does not equal the number of prices.
        """
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
