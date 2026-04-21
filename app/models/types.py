from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class ScorerInput:
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ScoreBreakdown:
    total_score: float
    components: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ScoringResult:
    score: float
    confidence: float
    explanation: Dict[str, Any]
    breakdown: ScoreBreakdown


# Define Timestamp type alias
Timestamp = Any

# Define missing type aliases
Price = float
Volatility = float
DaysToExpiration = int


@dataclass
class Contract:
    symbol: str
    expiration_date: Any
    strike_price: float
    option_type: str  # 'call' or 'put'
    price: float
    volume: int
    open_interest: int
    spread_width: float
    quote_age_hours: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


# Compatibility exports
Symbol = str
ContractId = str


@dataclass
class Greeks:
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
@dataclass
class Trade:
    entry_date: Any
    exit_date: Any
    entry_price: float
    exit_price: float
    direction: str  # 'long' or 'short'
    pnl: float
    trade_id: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    # Unique identifier for duplicate detection
    unique_hash: Optional[str] = None
