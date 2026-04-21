from typing import List, Dict, Any
from app.models.types import ScoringResult, ScorerInput, ScoreBreakdown
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .types import ScorerInput, ScoringResult

logger = logging.getLogger(__name__)

class BaselineScorer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            'price_change_threshold': -0.05,
            'momentum_threshold': -0.1,
            'volatility_threshold': 0.2,
            'put_call_ratio_threshold': 1.5,
            'volume_skew_threshold': 0.5,
            'pcr_mean_threshold': 1.0,
            'put_call_volume_ratio_threshold': 1.2
        }

    def score(self, input_data: ScorerInput) -> ScoringResult:
        rules_fired = self._evaluate_rules(input_data.data)
        score = self._calculate_score(rules_fired)
        
        explanation = {
            'rules_fired': rules_fired,
            'score': score
        }
        
        breakdown = ScoreBreakdown(
            total_score=score,
            components={'rules_fired_count': len(rules_fired)},
            metadata={'rules': rules_fired}
        )
        
        return ScoringResult(
            score=score,
            confidence=0.8,
            explanation=explanation,
            breakdown=breakdown
        )

    def _evaluate_rules(self, data: Any) -> List[str]:
        rules_fired = []
        
        if not isinstance(data, dict):
            return rules_fired
        
        # Price change rule
        if 'price_change' in data and data['price_change'] < self.config['price_change_threshold']:
            rules_fired.append('price_change_bearish')
        
        # Momentum rule
        if 'momentum' in data and data['momentum'] < self.config['momentum_threshold']:
            rules_fired.append('momentum_bearish')
        
        # Volatility rule
        if 'volatility' in data and data['volatility'] > self.config['volatility_threshold']:
            rules_fired.append('high_volatility')
        
        # Put-call ratio rule
        if 'put_call_ratio' in data and data['put_call_ratio'] > self.config['put_call_ratio_threshold']:
            rules_fired.append('high_put_call_ratio')
        
        # Volume skew rule
        if 'volume_skew' in data and data['volume_skew'] > self.config['volume_skew_threshold']:
            rules_fired.append('volume_skew_bearish')
        
        # PCR mean rule
        if 'pcr_mean' in data and data['pcr_mean'] > self.config['pcr_mean_threshold']:
            rules_fired.append('pcr_mean_bearish')
        
        # Put-call volume ratio rule
        if 'put_call_volume_ratio' in data and data['put_call_volume_ratio'] > self.config['put_call_volume_ratio_threshold']:
            rules_fired.append('high_put_call_volume_ratio')
        
        return rules_fired

    def _calculate_score(self, rules_fired: List[str]) -> float:
        return len(rules_fired) * 0.1  # Simple scoring logic

    def score_batch(self, inputs: List[ScorerInput]) -> List[ScoringResult]:
        return [self.score(input_data) for input_data in inputs]

class BaselineScorer:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def score(self, data: ScorerInput) -> float:
        """
        Score input data using baseline logic.
        """
        if not data.data:
            return 0.0

        score = 0.0
        for key, value in data.data.items():
            if key in self.config:
                score += value * self.config[key]
            else:
                score += value * 0.1  # default weight

        return min(1.0, max(0.0, score))

    def confidence(self, data: ScorerInput) -> float:
        """
        Return confidence score based on data quality.
        """
        if not data.data:
            return 0.0

        # Simple confidence based on number of features
        return min(1.0, len(data.data) / 10.0)

    def score_breakdown(self, data: ScorerInput) -> Dict[str, Any]:
        """
        Return detailed breakdown of scoring.
        """
        if not data.data:
            return {
                'total_score': 0.0,
                'components': {},
                'metadata': {}
            }

        components = {}
        total_score = 0.0
        for key, value in data.data.items():
            if key in self.config:
                weight = self.config[key]
            else:
                weight = 0.1
            score = value * weight
            components[key] = score
            total_score += score

        return {
            'total_score': min(1.0, max(0.0, total_score)),
            'components': components,
            'metadata': {}
        }

    def explain(self, data: ScorerInput) -> Dict[str, Any]:
        """
        Return explanation of scoring.
        """
        breakdown = self.score_breakdown(data)
        return {
            'score': breakdown['total_score'],
            'explanation': breakdown['components'],
            'confidence': self.confidence(data)
        }
