from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.explanations import ExpirationRankingOutput
from ..options.contract_selector import ContractSelector

router = APIRouter()


@router.post("/rank_expirations", response_model=ExpirationRankingOutput)
async def rank_expirations(
    contracts: List[Dict[str, Any]],
    strategy_type: str,
    preferences: Dict[str, Any] = None
):
    """
    Rank expirations based on various metrics and preferences
    """
    try:
        selector = ContractSelector()
        ranked_contracts = selector.rank_expirations(contracts, strategy_type, preferences)
        
        # Format output for API response
        output = ExpirationRankingOutput(
            ranked_expirations=[],  # Will be populated in the future
            preferences=preferences or {},
            strategy_type=strategy_type
        )
        
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
