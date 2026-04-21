from typing import List, Dict, Any
from app.models.opportunity import Opportunity
from app.options.strategy import Strategy


class DashboardViewModel:
    """
    View model for dashboard data.
    """
    def __init__(self, symbol: str, score: float, explanation: str, risk_flags: List[str], summary_stats: Dict[str, Any]):
        self.symbol = symbol
        self.score = score
        self.explanation = explanation
        self.risk_flags = risk_flags
        self.summary_stats = summary_stats


class DashboardService:
    """
    Service for dashboard-related operations.
    """
    
    def __init__(self):
        self.opportunities = []
    
    def get_opportunities_with_regime(self) -> List[Dict[str, Any]]:
        """
        Get opportunities with regime information.
        """
        result = []
        for opp in self.opportunities:
            # Convert opportunity to dict with regime info
            opp_dict = opp.to_dict()
            result.append(opp_dict)
        return result
    
    def filter_by_regime(self, regime: str) -> List[Dict[str, Any]]:
        """
        Filter opportunities by regime.
        """
        return [opp for opp in self.get_opportunities_with_regime() 
                if opp.get('regime') == regime]
    
    def add_opportunity(self, opportunity: Opportunity):
        """
        Add an opportunity to the dashboard.
        """
        self.opportunities.append(opportunity)
    
    def get_opportunities_with_scenarios(self) -> List[Dict[str, Any]]:
        """
        Get opportunities with scenario information.
        """
        result = []
        for opp in self.opportunities:
            opp_dict = opp.to_dict()
            # Include strategy information if available
            if hasattr(opp, 'strategy') and opp.strategy:
                opp_dict['strategy'] = opp.strategy.get_metadata()
            result.append(opp_dict)
        return result
