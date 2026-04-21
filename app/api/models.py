from typing import Optional, List
from pydantic import BaseModel
from pydantic.config import ConfigDict


class TrackedTradeResponse(BaseModel):
    id: str
    symbol: str
    strategy: str
    start_date: str
    end_date: str
    entry_price: float
    exit_price: Optional[float] = None
    outcome: Optional[str] = None
    resolved: bool
    timestamp: str

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class TrackedTradeListResponse(BaseModel):
    trades: List[TrackedTradeResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class PerformanceSummaryResponse(BaseModel):
    total_trades: int
    resolved_trades: int
    unresolved_trades: int
    win_rate: float
    avg_return: float
    total_return: float

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class OpportunityResponse(BaseModel):
    id: str
    symbol: str
    score: float
    confidence: float
    timestamp: str

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class OpportunityListResponse(BaseModel):
    opportunities: List[OpportunityResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    timestamp: str

    model_config = ConfigDict(
        # Allow extra fields for flexibility
        extra='allow'
    )

class OptulityResponse(BaseModel):
    symbol: str
    price: float
    volatility: float
    region: Optional[str] = None # Add region field
    explanation: Optional[str] = None
    risk_flags: Optional[List[str]] = None
    features: Optional[dict] = None

   # Probability estiates
    probability_expiring_itm: Optional[float] = None
    probability_reaching_target: Optional[float] = None
    probability_max_lost: Optional[float] = None
    expected_value: Optional[float] = None
    acss_assumptions: Optional[dict] = None


    model_config = ConfigDict(
      # Allow extra fields for flexibility
      extra='allow'
    )

class OptulityListResponse(BaseModel):
    optunities: List[OptulityResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(
      # Allow extra fields for flexibility
      extra='allow'
    )

class RegimeFilterRequest(BaseModel):
    region: str

    model_config = ConfigDict(
      # Allow extra fields for flexibility
      extra='allow'
    )