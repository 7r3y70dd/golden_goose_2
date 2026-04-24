from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from app.data.schemas import EquityBar, OptionsContract


class MarketDataProvider(ABC):
    """
    Abstract base class for market data providers.
    
    This interface defines the contract for fetching market data from various sources.
    """

    @abstractmethod
    def get_latest_quote(self, symbol: str) -> Optional[EquityBar]:
        """
        Fetch the latest equity bar for a given symbol.
        
        Args:
            symbol: The stock symbol to fetch data for
        
        Returns:
            EquityBar object with latest data, or None if not found
        """
        pass

    @abstractmethod
    def get_historical_bars(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d"
    ) -> List[EquityBar]:
        """
        Fetch historical OHLCV bars for a given symbol.
        
        Args:
            symbol: The stock symbol to fetch data for
            start_date: Start date for historical data
            end_date: End date for historical data
            interval: Time interval for bars (e.g., '1d', '1h', '5m')
        
        Returns:
            List of EquityBar objects
        """
        pass

    @abstractmethod
    def get_options_chain(
        self,
        symbol: str,
        expiration_date: Optional[datetime] = None
    ) -> List[OptionsContract]:
        """
        Fetch options chain for a given symbol.
        
        Args:
            symbol: The stock symbol to fetch options for
            expiration_date: Specific expiration date to filter by (optional)
        
        Returns:
            List of OptionsContract objects
        """
        pass