import pandas as pd
from typing import List, Dict, Any

class RegimeClassifier:
    """
    Classify market regimes based on price and volatility features.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            'trend_threshold': 0.02,
            'volatility_threshold': 0.05,
            'range_threshold': 0.01,
            'trend_window': 20,
            'volatility_window': 20
        }
    
    def classify_regime(self, price_series: pd.Series) -> str:
        """
        Classify the market regime based on price series.
        
        Args:
            price_series: Series of prices
        
        Returns:
            str: Regime label
        """
        if len(price_series) < self.config['trend_window']:
            return 'unknown'
        
        # Calculate trend
        trend = self._calculate_trend(price_series)
        
        # Calculate volatility
        volatility = self._calculate_volatility(price_series)
        
        # Calculate range
        range_val = self._calculate_range(price_series)
        
        # Classify regime
        if abs(trend) > self.config['trend_threshold']:
            if trend > 0:
                return 'trending_up'
            else:
                return 'trending_down'
        elif range_val < self.config['range_threshold']:
            return 'range_bound'
        elif volatility > self.config['volatility_threshold']:
            return 'high_volatility'
        elif volatility < self.config['volatility_threshold']:
            return 'low_volatility'
        else:
            return 'unknown'
    
    def _calculate_trend(self, price_series: pd.Series) -> float:
        """
        Calculate trend using linear regression slope.
        """
        if len(price_series) < self.config['trend_window']:
            return 0.0
        
        window_prices = price_series.tail(self.config['trend_window'])
        x = range(len(window_prices))
        y = window_prices.values
        
        # Simple linear regression
        n = len(x)
        if n < 2:
            return 0.0
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def _calculate_volatility(self, price_series: pd.Series) -> float:
        """
        Calculate volatility using standard deviation.
        """
        if len(price_series) < self.config['volatility_window']:
            return 0.0
        
        window_prices = price_series.tail(self.config['volatility_window'])
        returns = window_prices.pct_change().dropna()
        
        if len(returns) < 2:
            return 0.0
        
        return returns.std()
    
    def _calculate_range(self, price_series: pd.Series) -> float:
        """
        Calculate price range as percentage of average price.
        """
        if len(price_series) < 2:
            return 0.0
        
        max_price = price_series.max()
        min_price = price_series.min()
        avg_price = price_series.mean()
        
        if avg_price == 0:
            return 0.0
        
        return (max_price - min_price) / avg_price