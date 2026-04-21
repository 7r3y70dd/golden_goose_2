import pandas as pd
from typing import Optional, Tuple
from app.data.repository import DataRepository
from app.models.types import Timestamp


def generate_bearish_label(
    repo: DataRepository,
    symbol: str,
    start_time: Timestamp,
    end_time: Timestamp,
    label_window: int,
    threshold: float = 0.1
) -> Optional[pd.DataFrame]:
    """
    Generate bearish option outcome labels for a given symbol.
    
    Labels are 1 if the underlying asset price drops by at least `threshold` 
    within `label_window` days after the start_time, else 0.
    
    Parameters:
        repo: DataRepository instance
        symbol: ticker symbol
        start_time: start timestamp for label computation
        end_time: end timestamp for label computation
        label_window: number of days to look ahead for label
        threshold: percentage drop threshold to consider a "hit"
    
    Returns:
        DataFrame with timestamps and labels (1 or 0)
    """
    # Fetch price data for the symbol
    price_data = repo.get_price_data(symbol, start_time, end_time)
    
    if price_data is None or price_data.empty:
        return None
    
    # Ensure data is sorted by timestamp
    price_data = price_data.sort_values('timestamp')
    
    # Compute price drops over the label window
    labels = []
    for idx, row in price_data.iterrows():
        current_time = row['timestamp']
        future_time = current_time + pd.Timedelta(days=label_window)
        
        # Get price at future_time
        future_price = repo.get_price_at_time(symbol, future_time)
        
        if future_price is None:
            labels.append(0)
            continue
        
        # Compute percentage drop
        current_price = row['close']
        drop_pct = (current_price - future_price) / current_price
        
        # Label as 1 if drop exceeds threshold
        labels.append(1 if drop_pct >= threshold else 0)
    
    # Create DataFrame with labels
    result = price_data.copy()
    result['label'] = labels
    
    return result[['timestamp', 'label']]


class Labels:
    """
    A class to handle label generation for options strategies.
    """
    
    @staticmethod
    def generate_bearish_label(
        repo: DataRepository,
        symbol: str,
        start_time: Timestamp,
        end_time: Timestamp,
        label_window: int,
        threshold: float = 0.1
    ) -> Optional[pd.DataFrame]:
        """
        Generate bearish option outcome labels for a given symbol.
        
        Labels are 1 if the underlying asset price drops by at least `threshold` 
        within `label_window` days after the start_time, else 0.
        
        Parameters:
            repo: DataRepository instance
            symbol: ticker symbol
            start_time: start timestamp for label computation
            end_time: end timestamp for label computation
            label_window: number of days to look ahead for label
            threshold: percentage drop threshold to consider a "hit"
        
        Returns:
            DataFrame with timestamps and labels (1 or 0)
        """
        # Fetch price data for the symbol
        price_data = repo.get_price_data(symbol, start_time, end_time)
        
        if price_data is None or price_data.empty:
            return None
        
        # Ensure data is sorted by timestamp
        price_data = price_data.sort_values('timestamp')
        
        # Compute price drops over the label window
        labels = []
        for idx, row in price_data.iterrows():
            current_time = row['timestamp']
            future_time = current_time + pd.Timedelta(days=label_window)
            
            # Get price at future_time
            future_price = repo.get_price_at_time(symbol, future_time)
            
            if future_price is None:
                labels.append(0)
                continue
            
            # Compute percentage drop
            current_price = row['close']
            drop_pct = (current_price - future_price) / current_price
            
            # Label as 1 if drop exceeds threshold
            labels.append(1 if drop_pct >= threshold else 0)
        
        # Create DataFrame with labels
        result = price_data.copy()
        result['label'] = labels
        
        return result[['timestamp', 'label']]
