import os
from datetime import datetime
from typing import List, Optional
import pandas as pd
from app.data.schemas import EquityBar, OptionsContract


class MarketDataStorage:
    """
    Storage layer for persisted historical market data.
    
    Supports storing and retrieving equity bars and options snapshots
    using parquet format for efficient local storage.
    """
    
    def __init__(self, storage_path: str = "./data"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
    def save_bars(self, symbol: str, bars: List[EquityBar]) -> None:
        """
        Save equity bars to parquet file.
        
        Args:
            symbol: Stock symbol
            bars: List of EquityBar objects to save
        """
        if not bars:
            return
        
        # Convert to DataFrame
        df_data = []
        for bar in bars:
            df_data.append({
                'symbol': bar.symbol,
                'timestamp': bar.timestamp,
                'open': bar.open,
                'high': bar.high,
                'low': bar.low,
                'close': bar.close,
                'volume': bar.volume
            })
        
        df = pd.DataFrame(df_data)
        
        # Save to parquet
        file_path = os.path.join(self.storage_path, f"{symbol}_bars.parquet")
        df.to_parquet(file_path, index=False)
        
    def load_bars(self, symbol: str, start_date: Optional[datetime] = None, 
                  end_date: Optional[datetime] = None) -> List[EquityBar]:
        """
        Load equity bars from parquet file.
        
        Args:
            symbol: Stock symbol
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of EquityBar objects
        """
        file_path = os.path.join(self.storage_path, f"{symbol}_bars.parquet")
        
        if not os.path.exists(file_path):
            return []
        
        # Load from parquet
        df = pd.read_parquet(file_path)
        
        # Apply date filters if provided
        if start_date:
            df = df[df['timestamp'] >= start_date]
        if end_date:
            df = df[df['timestamp'] <= end_date]
        
        # Convert back to EquityBar objects
        bars = []
        for _, row in df.iterrows():
            bars.append(EquityBar(
                symbol=row['symbol'],
                timestamp=row['timestamp'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume']
            ))
        
        return bars
        
    def save_options(self, symbol: str, options: List[OptionsContract]) -> None:
        """
        Save options contracts to parquet file.
        
        Args:
            symbol: Stock symbol
            options: List of OptionsContract objects to save
        """
        if not options:
            return
        
        # Convert to DataFrame
        df_data = []
        for option in options:
            df_data.append({
                'symbol': option.symbol,
                'timestamp': option.timestamp,
                'strike': option.strike,
                'expiry': option.expiry,
                'put_call': option.put_call,
                'bid': option.bid,
                'ask': option.ask,
                'last': option.last,
                'volume': option.volume,
                'open_interest': option.open_interest,
                'iv': option.iv
            })
        
        df = pd.DataFrame(df_data)
        
        # Save to parquet
        file_path = os.path.join(self.storage_path, f"{symbol}_options.parquet")
        df.to_parquet(file_path, index=False)
        
    def load_options(self, symbol: str, start_date: Optional[datetime] = None, 
                     end_date: Optional[datetime] = None) -> List[OptionsContract]:
        """
        Load options contracts from parquet file.
        
        Args:
            symbol: Stock symbol
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of OptionsContract objects
        """
        file_path = os.path.join(self.storage_path, f"{symbol}_options.parquet")
        
        if not os.path.exists(file_path):
            return []
        
        # Load from parquet
        df = pd.read_parquet(file_path)
        
        # Apply date filters if provided
        if start_date:
            df = df[df['timestamp'] >= start_date]
        if end_date:
            df = df[df['timestamp'] <= end_date]
        
        # Convert back to OptionsContract objects
        options = []
        for _, row in df.iterrows():
            options.append(OptionsContract(
                symbol=row['symbol'],
                timestamp=row['timestamp'],
                strike=row['strike'],
                expiry=row['expiry'],
                put_call=row['put_call'],
                bid=row['bid'],
                ask=row['ask'],
                last=row['last'],
                volume=row['volume'],
                open_interest=row['open_interest'],
                iv=row['iv']
            ))
        
        return options