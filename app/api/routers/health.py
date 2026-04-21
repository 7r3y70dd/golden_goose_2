from fastapi import APIRouter
from typing import Dict
from app.health import HealthChecker
from app.data.storage import HistoricalDataStorage
from app.models.scoring_service import ScoringService

router = APIRouter(prefix="/health", tags=["Health"])

# Initialize health checker
storage = HistoricalDataStorage()
scoring_service = ScoringService()
health_checker = HealthChecker(storage, scoring_service)


class HealthResponse(BaseModel):
    """Response schema for health endpoint"""
    status: str
    services: Dict[str, str]
    timestamp: str


@router.get("", response_model=HealthResponse, summary="Health check endpoint", description="Returns the health status of the service and its dependencies")
async def health_check():
    status = health_checker.get_health_status()
    return status