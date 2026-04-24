from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class EquityBar:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def __post_init__(self):
        if self.open < 0 or self.high < 0 or self.low < 0 or self.close < 0:
            raise ValueError("OHLC values must be non-negative")
        if self.low > self.high:
            raise ValueError("Low price cannot exceed high price")


class OptionsContract:
    symbol: str
    timestamp: datetime
    strike: float
    expiry: datetime
    put_call: str  # 'call' or 'put'
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    volume: int
    open_interest: int
    iv: Optional[float]

    def __post_init__(self):
        if self.strike < 0:
            raise ValueError("Strike price must be non-negative")
        if self.put_call not in ['call', 'put']:
            raise ValueError("put_call must be either 'call' or 'put'")
        if self.bid is not None and self.bid < 0:
            raise ValueError("Bid price must be non-negative")
        if self.ask is not None and self.ask < 0:
            raise ValueError("Ask price must be non-negative")
        if self.volume < 0:
            raise ValueError("Volume must be non-negative")
        if self.open_interest < 0:
            raise ValueError("Open interest must be non-negative")
        if self.iv is not None and self.iv < 0:
            raise ValueError("Implied volatility must be non-negative")