import logging
from typing import List

from app.data.providers.base import MarketDataProvider
from app.data.repository import DataRepository
from app.watchlist import load_watchlist

logger = logging.getLogger(__name__)


def ingest_watchlist(provider: MarketDataProvider, repository: DataRepository) -> None:
    """Ingest historical data for all symbols in the watchlist."""
    symbols = load_watchlist()
    logger.info(f"Starting ingestion for {len(symbols)} symbols")

    for symbol in symbols:
        try:
            logger.info(f"Fetching data for symbol: {symbol}")
            # Fetch historical bars
            bars = provider.get_historical_bars(symbol, days=30)
            # Fetch options chain
            options_chain = provider.get_options_chain(symbol)

            # Persist data
            repository.save_historical_bars(symbol, bars)
            repository.save_options_chain(symbol, options_chain)

            logger.info(f"Successfully ingested data for {symbol}")
        except Exception as e:
            logger.error(f"Failed to ingest data for {symbol}: {e}")
            continue

    logger.info("Ingestion job completed")