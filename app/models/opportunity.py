from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from app.models.types import OptionContract, StrategyMetadata
from app.models.risk_flags import RiskFlag
from app.models.explanation import Explanation


dataclass

class Opportunity:
    """Canonical data model for a generated option trade idea."""

    symbol: str
    company_name: Optional[str] = None
    generated_timestamp: datetime = field(default_factory=datetime.utcnow)
    underlying_price: float = 0.0
    contract: OptionContract
    strategy: StrategyMetadata
    score: float = 0.0
    explanation: Explanation
    risk_flags: List[RiskFlag] = field(default_factory=list)
    status: str = "pending"  # pending, executed, failed, evaluated
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None