"""Stub for uploading trades to a broker API."""
import logging
from typing import Iterable

logger = logging.getLogger(__name__)


def upload_trades(trades: Iterable[dict]) -> None:
    """
    Uploads a collection of trades to a broker.
    
    This is a stub function that currently only logs the number of trades to be uploaded. Intended for future integration with a broker SDK or API.
    """
    logger.info("Uploading %d trades", len(list(trades)))
    # TODO: integrate with broker SDK/API

