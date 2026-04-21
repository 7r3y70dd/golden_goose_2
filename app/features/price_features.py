from dataclasses import dataclass
from typing import List, Optional


class PriceFeatures:
    """Container for price-related features."""
    
    # Example attributes - adjust based on actual usage
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None
    
    def __init__(self, open_price: Optional[float] = None, high_price: Optional[float] = None,
                 low_price: Optional[float] = None, close_price: Optional[float] = None,
                 volume: Optional[float] = None):
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume

    def to_dict(self) -> dict:
        return {
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'close_price': self.close_price,
            'volume': self.volume
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
