from typing import List, Dict, Any
from app.ui.dashboard_service import DashboardService
from app.models.output import Opportunity


class DashboardUI:
    """
    UI component for displaying dashboard data.
    """
    
    def __init__(self, dashboard_service: DashboardService):
        self.dashboard_service = dashboard_service
        self.opportunities = []
    
    def render_opportunities(self, opportunities: List[Opportunity]) -> List[Dict[str, Any]]:
        """
        Render opportunities for display in the dashboard.
        """
        formatted_opportunities = self.dashboard_service.format_opportunities(opportunities)
        return formatted_opportunities
    
    def update_opportunities(self, opportunities: List[Opportunity]):
        """
        Update the dashboard with new opportunities.
        """
        self.opportunities = opportunities
        return self.render_opportunities(opportunities)
    
    def get_opportunity_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the opportunities.
        """
        if not self.opportunities:
            return {}
        
        scores = [opp.score for opp in self.opportunities]
        return {
            'total_opportunities': len(self.opportunities),
            'avg_score': sum(scores) / len(scores),
            'max_score': max(scores),
            'min_score': min(scores)
        }