import numpy as np
import pandas as pd
from typing import Optional

class OptionsFeatures:
    """
    Class to calculate options activity features.
    """
    
    def __init__(self, window: int = 20):
        self.window = window
    
    def validate_input(self, put_call_ratio: pd.Series, 
                      put_volume: pd.Series, 
                      call_volume: pd.Series,
                      open_interest: pd.Series) -> None:
        """
        Validate input for options features calculation.
        
        Args:
            put_call_ratio: Put/Call ratio time series
            put_volume: Put volume time series
            call_volume: Call volume time series
            open_interest: Open interest time series
        
        Raises:
            ValueError: If inputs are invalid
        """
        series_list = [put_call_ratio, put_volume, call_volume, open_interest]
        series_names = ['put_call_ratio', 'put_volume', 'call_volume', 'open_interest']
        
        for i, series in enumerate(series_list):
            if series is None:
                raise ValueError(f"{series_names[i]} cannot be None")
            
            if not isinstance(series, pd.Series):
                raise ValueError(f"{series_names[i]} must be a pandas Series")
            
            if series.empty:
                raise ValueError(f"{series_names[i]} cannot be empty")
            
            if series.isna().all():
                raise ValueError(f"{series_names[i]} series contains only NaN values")
        
        # Check that all series have the same index
        indices = [s.index for s in series_list if s is not None]
        if len(set(indices)) > 1:
            raise ValueError("All input series must have the same index")
    
    def calculate_features(self, put_call_ratio: pd.Series, 
                          put_volume: pd.Series, 
                          call_volume: pd.Series,
                          open_interest: pd.Series) -> pd.DataFrame:
        """
        Calculate options activity features.
        
        Args:
            put_call_ratio: Put/Call ratio time series
            put_volume: Put volume time series
            call_volume: Call volume time series
            open_interest: Open interest time series
        
        Returns:
            DataFrame with options features
        """
        self.validate_input(put_call_ratio, put_volume, call_volume, open_interest)
        
        # Handle missing values in input series
        put_call_ratio = put_call_ratio.fillna(0)
        put_volume = put_volume.fillna(0)
        call_volume = call_volume.fillna(0)
        open_interest = open_interest.fillna(0)
        
        # Volume skew
        volume_skew = (put_volume - call_volume) / (put_volume + call_volume + 1e-8)  # Avoid division by zero
        
        # Open interest features
        oi_rolling_mean = open_interest.rolling(window=self.window).mean()
        oi_rolling_std = open_interest.rolling(window=self.window).std()
        
        # Volatility features
        put_volume_mean = put_volume.rolling(window=self.window).mean()
        call_volume_mean = call_volume.rolling(window=self.window).mean()
        
        # Put/Call volume ratio
        put_call_volume_ratio = put_volume / (call_volume + 1e-8)  # Avoid division by zero
        
        return pd.DataFrame({
            'put_call_ratio': put_call_ratio,
            'volume_skew': volume_skew,
            'open_interest_mean': oi_rolling_mean,
            'open_interest_std': oi_rolling_std,
            'put_volume_mean': put_volume_mean,
            'call_volume_mean': call_volume_mean,
            'put_call_volume_ratio': put_call_volume_ratio
        })

# For backward compatibility, also export the standalone functions
# (These can be removed if not needed)
validate_options_features_input = OptionsFeatures.validate_input
calculate_options_features = OptionsFeatures.calculate_features
