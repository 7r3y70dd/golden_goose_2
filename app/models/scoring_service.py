import logging
import time
from app.logging import setup_logging
from app.models.baseline_scorer import BaselineScorer
from app.models.output import OpportunityOutput
from app.data.repository import DataRepository

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)
from .opportunity import Opportunity
from .risk_flags import generate_risk_flags


class ScoringService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.baseline_scorer = BaselineScorer()
        self.repository = DataRepository()
        pass

    def calculate_opportunity_score(self, 
                                   volume: float,
                                   open_interest: float,
                                   spread_ratio: float,
                                   confidence: float,
                                   data_age_hours: float,
                                   volatility: float,
                                   base_score: float) -> Opportunity:
        """Calculate opportunity score with risk adjustments."""
        risk_flags = generate_risk_flags(
            volume, open_interest, spread_ratio, confidence, data_age_hours, volatility
        )
        
        # Apply soft penalties to base score
        adjusted_score = base_score
        if risk_flags.soft_penalties:
            adjusted_score = max(0.0, base_score - risk_flags.soft_penalty_score_reduction)
        
        return Opportunity(
            id=str(hash(f"{volume}_{open_interest}_{spread_ratio}_{confidence}_{data_age_hours}_{volatility}")),
            score=adjusted_score,
            risk_flags=risk_flags
        )
        # Proceed with scoring logic
        # ... scoring implementation ...
        score = {'score': 0.5}
        
        # Record scoring duration
        duration = time.time() - start_time
        n_metrics.record_timer('scoring_latency', duration)
        
        return score

    def rank_opportunities(self, opportunities: list) -> list:
        """
        Rank opportunities by score (descending), with tie-breaking by symbol.
        
        Args:
            opportunities: List of opportunity dictionaries with 'score' and 'symbol' keys
        
        Returns:
            List of opportunities sorted by score (descending), then by symbol (ascending)
        """
        return sorted(opportunities, key=lambda x: (-x['score'], x['symbol']))

    def score(self, data, run_id):
        logger.info("Scoring data", extra={'run_id': run_id})
        start_time = time.time()
        
        # Use baseline scorer for now
        score_value = self.baseline_scorer.score(data)
        confidence_value = self.baseline_scorer.confidence(data)
        breakdown = self.baseline_scorer.score_breakdown(data)
        
        # Record scoring duration
        duration = time.time() - start_time
        
        # Return structured score with breakdown
        return {
            'score': score_value,
            'confidence': confidence_value,
            'breakdown': breakdown
        }

    def score_and_persist(self, data, run_id, threshold=0.5):
        """Score opportunities and persist those that meet the threshold."""
        # Score the data
        score_result = self.score(data, run_id)
        
        # Create opportunity output
        opportunity_output = OpportunityOutput(
            symbol=data.get('symbol', ''),
            score=score_result['score'],
            confidence=score_result['confidence'],
            breakdown=score_result['breakdown']
        )
        
        # Persist if score meets threshold
        if score_result['score'] >= threshold:
            self.repository.save_opportunity(opportunity_output)
            
        return opportunity_output