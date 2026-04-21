from typing import List, Dict, Any
import pandas as pd


class FeatureExtractor:
    def __init__(self):
        pass

    def extract_features(self, data: pd.DataFrame) -> pd.DataFrame:
        # Example feature extraction logic
        data['price_change'] = data['close'].pct_change()
        data['momentum'] = data['close'].pct_change(periods=5)
        data['volatility'] = data['close'].rolling(window=10).std()
        
        # Add more features as needed
        return data

    def extract_features_from_dict(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Extract features from a dictionary
        return data_dict