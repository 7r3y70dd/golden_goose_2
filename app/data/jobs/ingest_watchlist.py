import logging
from typing import List
from app.data.schemas import EquityBar, OptionsChain
from app.data.repository import save_equity_data, save_options_data
from app.watchlist import get_watchlist_symbols
from app.data.providers import get_provider

logger = logging.getLogger(__name__)


def ingest_watchlist_data():
    """
    Fetch and store data for all symbols in the watchlist.
    """
    symbols = get_watchlist_symbols()
    provider = get_provider()

    for symbol in symbols:
        try:
            logger.info(f"Fetching equity data for {symbol}")
            equity_data = provider.get_equity_data(symbol)
            save_equity_data(equity_data)

            logger.info(f"Fetching options data for {symbol}")
            options_data = provider.get_options_data(symbol)
            save_options_data(options_data)

            logger.info(f"Successfully ingested data for {symbol}")
        except Exception as e:
            logger.error(f"Failed to ingest data for {symbol}: {e}")
            continue
