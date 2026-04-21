from typing import Dict, Any, List
from .types import ScoringResult
from .explanation import Explanation, generate_bearish_explanation


# Export the Explanation class for use in app.models.__init__
__all__ = ['Explanation', 'generate_bearish_explanation', 'generate_bullish_explanation', 'generate_neutral_explanation', 'generate_explanation']


def generate_bearish_explanation(triggered_rules: List[str], features: Dict[str, Any], score: float) -> Dict[str, Any]:
    explanation = generate_bearish_explanation(triggered_rules, features, score)
    return {
        'type': explanation.type.value,
        'score': score,
        'triggered_rules': triggered_rules,
        'features': features,
        'risk_level': 'high',
        'top_positive_contributors': explanation.top_positive_contributors,
        'top_negative_contributors': explanation.top_negative_contributors,
        'liquidity_notes': explanation.liquidity_notes,
        'event_risk_notes': explanation.event_risk_notes,
        'volatility_notes': explanation.volatility_notes,
        'expiration_selection_rationale': explanation.expiration_selection_rationale
    }


def generate_bullish_explanation(triggered_rules: List[str], features: Dict[str, Any], score: float) -> Dict[str, Any]:
    return {
        'type': 'bullish',
        'score': score,
        'triggered_rules': triggered_rules,
        'features': features,
        'risk_level': 'low'
    }


def generate_neutral_explanation(triggered_rules: List[str], features: Dict[str, Any], score: float) -> Dict[str, Any]:
    return {
        'type': 'neutral',
        'score': score,
        'triggered_rules': triggered_rules,
        'features': features,
        'risk_level': 'medium'
    }


def generate_explanation(triggered_rules: List[str], features: Dict[str, Any], score: float, explanation_type: str = 'bearish') -> Dict[str, Any]:
    if explanation_type == 'bearish':
        return generate_bearish_explanation(triggered_rules, features, score)
    elif explanation_type == 'bullish':
        return generate_bullish_explanation(triggered_rules, features, score)
    else:
        return generate_neutral_explanation(triggered_rules, features, score)


# Re-export the Explanation class for backward compatibility
Explanation = Explanation


from typing import List, Dict, Any
from pydantic import BaseModel


class ExpirationRankingExplanation(BaseModel):
    """
    Explanation for expiration ranking decisions
    """
    expiration_date: str
    days_to_expiration: int
    premium_cost: float
    theta_exposure: float
    liquidity_quality: float
    event_overlap: float
    risk_reward_ratio: float
    recommendation_score: float
    reasoning: str


class ExpirationRankingOutput(BaseModel):
    """
    Output for expiration ranking results
    """
    ranked_expirations: List[ExpirationRankingExplanation]
    preferences: Dict[str, Any]
    strategy_type: str
