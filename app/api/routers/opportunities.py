from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.scoring_service import ScoringService
from app.options.strategy import Strategy
from datetime import datetime

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


class Opportunity(BaseModel):
    symbol: str
    prediction: float
    confidence: float
    risk_level: str
    strategy: Strategy = None
    upcoming_earnings: Optional[str] = None
    upcoming_dividend: Optional[str] = None
    upcoming_economic_event: Optional[str] = None
    upcoming_fomc_event: Optional[str] = None


class OpportunitiesResponse(BaseModel):
    """Response schema for opportunities endpoint"""
    opportunities: List[Opportunity]
    total: int
    page: int
    size: int


@router.get("", response_model=OpportunitiesResponse, summary="Get opportunities", description="Returns a list of opportunities with their risk scores and confidence levels")
async def get_opportunities():
    try:
        # Placeholder data - in real implementation this would come from predictions
        opportunities = [
            Opportunity(
                symbol="AAPL",
                prediction=0.75,
                confidence=0.85,
                risk_level="medium",
                upcoming_earnings="Earnings in 5 days"
            ),
            Opportunity(
                symbol="MSFT",
                prediction=0.60,
                confidence=0.70,
                risk_level="low",
                upcoming_dividend="Dividend in 10 days"
            ),
            Opportunity(
                symbol="GOOGL",
                prediction=0.80,
                confidence=0.90,
                risk_level="high",
                upcoming_economic_event="Economic event in 3 days"
            )
        ]
        
        # Sort opportunities by score (descending) and symbol (ascending) for deterministic output
        scoring_service = ScoringService()
        # Convert to dict format for ranking
        opportunities_dict = [
            {
                'symbol': opp.symbol,
                'score': opp.prediction,
                'confidence': opp.confidence,
                'risk_level': opp.risk_level
            }
            for opp in opportunities
        ]
        
        ranked_opportunities = scoring_service.rank_opportunities(opportunities_dict)
        
        # Convert back to Opportunity objects
        ranked_opportunities_obj = [
            Opportunity(
                symbol=opp['symbol'],
                prediction=opp['score'],
                confidence=opp['confidence'],
                risk_level=opp['risk_level'],
                upcoming_earnings=opp.get('upcoming_earnings'),
                upcoming_dividend=opp.get('upcoming_dividend'),
                upcoming_economic_event=opp.get('upcoming_economic_event'),
                upcoming_fomc_event=opp.get('upcoming_fomc_event')
            )
            for opp in ranked_opportunities
        ]
        
        return {
            "opportunities": ranked_opportunities_obj,
            "total": len(ranked_opportunities_obj),
            "page": 1,
            "size": len(ranked_opportunities_obj)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))