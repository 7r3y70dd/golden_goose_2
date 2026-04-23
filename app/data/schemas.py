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


class OptionsChain:
    symbol: str
    timestamp: datetime
    contracts: list[OptionsContract]
