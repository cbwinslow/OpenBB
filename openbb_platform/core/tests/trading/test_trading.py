import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from openbb_core.trading.arbitrage import find_arbitrage
from openbb_core.trading.backtesting import Backtester, BuyAndHoldStrategy


def test_find_arbitrage():
    result = find_arbitrage(100, {"inst_a": 40, "inst_b": 30})
    assert result == {
        "action": "buy_replication_sell_target",
        "profit": 30,
    }


def test_backtester_buy_and_hold():
    prices = [100, 110, 105]
    strategy = BuyAndHoldStrategy()
    backtester = Backtester(prices, strategy)
    perf = backtester.run()
    expected = (110 - 100) / 100 + (105 - 110) / 110
    assert abs(perf - expected) < 1e-9
