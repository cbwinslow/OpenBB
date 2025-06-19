"""Stub for uploading trades to a broker API."""
import logging
from typing import Iterable

logger = logging.getLogger(__name__)


def upload_trades(trades: Iterable[dict]) -> None:
    """
    Prepares to upload a collection of trade records to a broker.
    
    This stub function logs the number of trades intended for upload. Actual integration
    with a broker API or SDK is not yet implemented.
    
    Args:
        trades: An iterable of dictionaries, each representing a trade.
    """
    logger.info("Uploading %d trades", sum(1 for _ in trades))
    # TODO: integrate with broker SDK/API

