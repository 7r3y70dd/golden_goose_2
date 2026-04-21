from typing import List, Dict, Any
from .strategy import StrategyLeg, StrategyType


def calculate_payoff(strategy: Strategy, underlying_price: float) -> float:
    """
    Calculate payoff for a given strategy at expiration.
    """
    payoff = 0.0
    
    for leg in strategy.legs:
        if leg.option_type == 'call':
            payoff += leg.quantity * max(0, underlying_price - leg.strike) - leg.premium
        elif leg.option_type == 'put':
            payoff += leg.quantity * max(0, leg.strike - underlying_price) - leg.premium
    
    return payoff


def calculate_break_even(strategy: Strategy) -> List[float]:
    """
    Calculate break-even points for a strategy.
    """
    # Simplified implementation - in practice this would be more complex
    break_even_points = []
    
    # For now, return empty list as detailed implementation would be complex
    return break_even_points


def calculate_max_profit_loss(strategy: Strategy) -> Dict[str, float]:
    """
    Calculate max profit and max loss for a strategy.
    """
    # Simplified implementation
    return {
        'max_profit': float('inf'),
        'max_loss': float('inf')
    }