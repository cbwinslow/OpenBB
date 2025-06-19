"""Stub for uploading trades to a broker API."""
import logging
from typing import Iterable

logger = logging.getLogger(__name__)


def upload_trades(trades: Iterable[dict]) -> None:
    """Upload trades to a broker. This is a stub implementation."""

    # TODO: integrate with broker SDK/API

