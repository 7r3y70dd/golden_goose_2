from datetime import datetime
from typing import List, Optional
from app.data.schemas import EquityBar, OptionsContract
from app.data.storage import MarketDataStorage

class MarketDataRepository:
    """
    Repository for accessing market data.
    
    Provides a clean interface for reading and writing equity bars and options
    data using the underlying storage layer.
    """
    
    def __init__(self, storage_path: str = "./data"):
        self.storage = MarketDataStorage(storage_path)
        
    def save_bars(self, symbol: str, bars: List[EquityBar]) -> None:
        """
        Save equity bars for a symbol.
        
        Args:
            symbol: Stock symbol
            bars: List of EquityBar objects to save
        """
        self.storage.save_bars(symbol, bars)
        
    def load_bars(self, symbol: str, start_date: Optional[datetime] = None, 
                  end_date: Optional[datetime] = None) -> List[EquityBar]:
        """
        Load equity bars for a symbol.
        
        Args:
            symbol: Stock symbol
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of EquityBar objects
        """
        return self.storage.load_bars(symbol, start_date, end_date)
        
    def save_options(self, symbol: str, options: List[OptionsContract]) -> None:
        """
        Save options contracts for a symbol.
        
        Args:
            symbol: Stock symbol
            options: List of OptionsContract objects to save
        """
        self.storage.save_options(symbol, options)
        
    def load_options(self, symbol: str, start_date: Optional[datetime] = None, 
                     end_date: Optional[datetime] = None) -> List[OptionsContract]:
        """
        Load options contracts for a symbol.
        
        Args:
            symbol: Stock symbol
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of OptionsContract objects
        """
        return self.storage.load_options(symbol, start_date, end_date)