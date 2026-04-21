from fastapi import APIRouter, Depends
from typing import Dict
from ..models.portfolio import PortfolioAnalytics
from ..models.opportunity import Opportunity

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def get_portfolio_analytics(opportunities: List[Opportunity]) -> PortfolioAnalytics:
    return PortfolioAnalytics(opportunities)


@router.get("/analytics", response_model=Dict)
def get_portfolio_analytics_endpoint(
    analytics: PortfolioAnalytics = Depends(get_portfolio_analytics)
):
    return {
        "symbol_exposure": analytics.get_symbol_exposure(),
        "sector_exposure": analytics.get_sector_exposure(),
        "expiration_bucket_exposure": analytics.get_expiration_bucket_exposure(),
        "strategy_type_exposure": analytics.get_strategy_type_exposure(),
        "greeks": analytics.get_greeks_summary(),
        "concentration_warnings": analytics.get_concentration_warnings(),
        "net_premium_at_risk": analytics.get_net_premium_at_risk(),
        "stress_test": analytics.stress_test()
    }