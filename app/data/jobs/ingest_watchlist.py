import logging
from typing import List
from app.data.repository import save_equity_data, save_options_data
from app.watchlist import get_watchlist_symbols

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_and_save_equity_data(symbol: str):
    """
    Simulate fetching equity data for a symbol and saving it.
    In a real implementation, this would call an API or data source.
    """
    try:
        # Simulate data fetching
        equity_data = {
            "symbol": symbol,
            "price": 150.0,
            "volume": 1000000
        }
        save_equity_data(equity_data)
        logger.info(f"Successfully saved equity data for {symbol}")
        return True
    except Exception as e:
        logger.error(f"Failed to save equity data for {symbol}: {e}")
        return False


def fetch_and_save_options_data(symbol: str):
    """
    Simulate fetching options data for a symbol and saving it.
    In a real implementation, this would call an API or data source.
    """
    try:
        # Simulate data fetching
        options_data = [
            {
                "symbol": symbol,
                "strike": 150.0,
                "expiry": "2023-12-31",
                "put_call": "call",
                "price": 2.5,
                "volume": 5000
            }
        ]
        save_options_data(options_data)
        logger.info(f"Successfully saved options data for {symbol}")
        return True
    except Exception as e:
        logger.error(f"Failed to save options data for {symbol}: {e}")
        return False


def ingest_watchlist_data(retries: int = 3):
    """
    Ingest data for all symbols in the watchlist.
    Handles retries for failed symbol ingestions.
    """
    symbols = get_watchlist_symbols()
    logger.info(f"Starting ingestion for {len(symbols)} symbols")

    for symbol in symbols:
        success = False
        for attempt in range(retries):
            logger.info(f"Attempt {attempt + 1} to ingest data for {symbol}")
            equity_success = fetch_and_save_equity_data(symbol)
            options_success = fetch_and_save_options_data(symbol)
            
            if equity_success and options_success:
                success = True
                break
            else:
                logger.warning(f"Failed to ingest data for {symbol} on attempt {attempt + 1}")
        
        if not success:
            logger.error(f"Failed to ingest data for {symbol} after {retries} attempts")


if __name__ == "__main__":
    ingest_watchlist_data()
