from fastapi import APIRouter, HTTPException
from typing import List
from app.watchlist import get_watchlist_symbols

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

class WatchlistResponse(BaseModel):
    """Response schema for watchlist endpoint"""
    symbols: List[str]


@router.get("", response_model=WatchlistResponse, summary="Get watchlist", description="Returns the list of symbols in the watchlist")
async def get_watchlist():
    try:
        symbols = get_watchlist_symbols()
        return {"symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
