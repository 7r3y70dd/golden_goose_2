from fastapi import APIRouter, Depends
from typing import List
from app.features.unusual_activity import UnusualActivityDetector
from app.models.unusual_activity import UnusualActivitySignal, UnusualActivityResult

router = APIRouter(prefix="/unusual_activity", tags=["unusual_activity"])

detector = UnusualActivityDetector()


@router.get("/recent", response_model=List[UnusualActivitySignal])
async def get_recent_unusual_activity():
    """Get recent unusual activity signals."""
    # This would typically fetch data from storage
    # For now, we'll return an empty list
    return []


@router.get("/ranked", response_model=List[UnusualActivitySignal])
async def get_ranked_unusual_activity(top_n: int = 10):
    """Get ranked unusual activity signals."""
    # This would typically fetch data from storage
    # For now, we'll return an empty list
    return []