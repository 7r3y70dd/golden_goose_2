from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class TradeStatus(str, Enum):
    UNRESOLVED = "unresolved"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    EXPIRED = "expired"


class TrackedTrade(BaseModel):
    # Generation-time fields
    candidate_id: str
    symbol: str
    contract_id: str
    strike: float
    expiration: datetime
    option_type: str  # 'call' or 'put'
    strategy_type: str
    generated_at: datetime
    entry_stock_price: float
    entry_option_quote: dict  # snapshot of option quote at entry
    target_definition: dict  # target definition for the trade

    # Outcome-time fields
    status: TradeStatus
    resolved_at: Optional[datetime] = None
    realized_outcome: Optional[dict] = None

    class Config:
        # Allow extra fields for flexibility in outcome metadata
        extra = "allow"
