from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional



class EquityBar:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class OptionsChain:
    symbol: str
    timestamp: datetime
    contracts: List[dict]


class OpportunitySchema:
    symbol: str
    company_name: Optional[str]
    generated_timestamp: datetime
    underlying_price: float
    contract: dict
    strategy: dict
    score: float
    explanation: dict
    risk_flags: List[dict]
    status: str
    created_at: datetime
    updated_at: datetime


class MarketDataSnapshot:
    symbol: str
    timestamp: datetime
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    volume: Optional[int]
    open_interest: Optional[int]
    iv: Optional[float]
    strike: Optional[float]
    expiry: Optional[datetime]
    put_call: Optional[str]

    @validator('expiry', 'timestamp', pre=True)
    def parse_dates(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v

    @validator('symbol', 'put_call')
    def non_empty_strings(cls, v):
        if v is None:
            return ''
        return v

    class Config:
        orm_mode = True