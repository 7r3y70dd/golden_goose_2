from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from app.models.types import ScoreBreakdown
from app.models.explanation import Explanation
from app.models.opportunity import Opportunity


@dataclass
class OpportunityOutput:
    symbol: str
    score: float
    confidence: float
    risk_flags: Optional[Any] = None
    explanation: Optional[Explanation] = None
    metadata: Optional[Dict[str, Any]] = None
    breakdown: Optional[ScoreBreakdown] = None
    # Add persistence metadata
    run_id: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass
class OpportunityList:
    opportunities: List[OpportunityOutput]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class RankedOpportunity:
    symbol: str
    score: float
    confidence: float
    risk_flags: Optional[Any] = None
    explanation: Optional[Explanation] = None
    metadata: Optional[Dict[str, Any]] = None
    breakdown: Optional[ScoreBreakdown] = None
    rank: Optional[int] = None
    # Add persistence metadata
    run_id: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass
class ScoreBucketMetrics:
    count: int
    total_pnl: float
    total_success: int
    success_rate: float
    avg_hours_to_resolution: float


@dataclass
class PerformanceSummary:
    total_trades: int
    resolved_trades: int
    unresolved_trades: int
    success_rate: float
    average_pnl: float
    total_pnl: float
    by_strategy: Dict[str, Dict[str, Any]]
    by_score_bucket: Dict[str, Dict[str, Any]]