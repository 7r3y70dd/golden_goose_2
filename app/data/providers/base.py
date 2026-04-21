from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class Provider(ABC):
    """
    Abstract base class for market data providers.

    This interface defines the contract that all market data providers must implement.
    Providers must return data in specific formats to ensure compatibility with the rest of the system.

    Expected input/output shapes:
    - get_latest_quote(symbol: str) -> Dict[str, Any]
      Returns a dictionary with keys: symbol, price, change, change_percent, volume, timestamp
    - get_historical_bars(symbol: str, start_date: str, end_date: str, interval: str = '1d') -> List[Dict[str, Any]]
      Returns a list of bar dictionaries with keys: date, open, high, low, close, volume
    - get_options_chain(symbol: str) -> Dict[str, Any]
      Returns a dictionary with keys: symbol, expiration_dates, calls, puts

    Error handling expectations:
    - All methods should raise appropriate exceptions for invalid inputs or data retrieval failures
    - Methods should handle edge cases gracefully

    Optional capability notes:
    - Providers may support different data kinds (e.g., options, futures, forex)
    - Providers may have different performance characteristics
    """

    @abstractmethod
    def get_latest_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch the latest quote for a given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :return: Dictionary containing quote data with keys: symbol, price, change, change_percent, volume, timestamp
        :raises ValueError: If symbol is invalid or empty
        :raises Exception: If data retrieval fails
        """
        pass

    @abstractmethod
    def get_historical_bars(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> List[Dict[str, Any]]:
        """
        Fetch historical price bars for a given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :param start_date: Start date in YYYY-MM-DD format
        :param end_date: End date in YYYY-MM-DD format
        :param interval: Time interval (e.g., '1d', '1h', '5m')
        :return: List of bar dictionaries with keys: date, open, high, low, close, volume
        :raises ValueError: If dates are invalid or interval is unsupported
        :raises Exception: If data retrieval fails
        """
        pass

    @abstractmethod
    def get_options_chain(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch the options chain for a given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :return: Dictionary containing options chain data with keys: symbol, expiration_dates, calls, puts
        :raises ValueError: If symbol is invalid or empty
        :raises Exception: If data retrieval fails
        """
        pass
