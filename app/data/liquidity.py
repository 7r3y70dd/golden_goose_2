from typing import List, Tuple, Dict, Optional
from app.models.types import Contract


class LiquidityScore:
    """Represents a liquidity score for a contract."""
    def __init__(self, score: float, components: Dict[str, float], label: str):
        self.score = score
        self.components = components
        self.label = label


def calculate_liquidity_score(contract: Contract, weights: Optional[Dict[str, float]] = None) -> LiquidityScore:
    """
    Calculate a composite liquidity score for a contract.

    Args:
        contract: The contract to score
        weights: Optional dictionary of component weights (default: equal weights)

    Returns:
        LiquidityScore object with overall score, component scores, and label
    """
    if weights is None:
        weights = {
            'spread': 0.25,
            'open_interest': 0.25,
            'volume': 0.25,
            'quote_freshness': 0.25
        }

    # Normalize components (0-1 scale)
    components = {}
    
    # Spread component (inverse - lower spread is better)
    if contract.price > 0:
        spread_ratio = contract.spread_width / contract.price
        components['spread'] = max(0, 1 - spread_ratio * 20)  # Scale to 0-1
    else:
        components['spread'] = 0
    
    # Open interest component
    components['open_interest'] = min(1.0, contract.open_interest / 10000)  # Scale to 0-1
    
    # Volume component
    components['volume'] = min(1.0, contract.volume / 10000)  # Scale to 0-1
    
    # Quote freshness component (inverse - more recent is better)
    if hasattr(contract, 'quote_age_hours') and contract.quote_age_hours is not None:
        components['quote_freshness'] = max(0, 1 - contract.quote_age_hours / 24)  # Scale to 0-1
    else:
        components['quote_freshness'] = 0
    
    # Calculate weighted score
    score = sum(components[key] * weights[key] for key in weights)
    
    # Determine label
    if score >= 0.8:
        label = 'high'
    elif score >= 0.5:
        label = 'acceptable'
    else:
        label = 'poor'
    
    return LiquidityScore(score, components, label)


def filter_liquid_contracts(contracts: List[Contract], min_volume: int = 1000, min_open_interest: int = 100, max_spread_width: float = 0.05) -> List[Contract]:
    """
    Filter contracts based on minimum liquidity thresholds.

    Args:
        contracts: List of contracts to filter
        min_volume: Minimum trading volume threshold
        min_open_interest: Minimum open interest threshold
        max_spread_width: Maximum spread width as a fraction of the contract price

    Returns:
        List of liquid contracts
    """
    liquid_contracts = []
    for contract in contracts:
        if (contract.volume >= min_volume and
            contract.open_interest >= min_open_interest and
            contract.spread_width <= max_spread_width):
            liquid_contracts.append(contract)
    return liquid_contracts


def filter_liquid_symbols(symbols: List[str], min_volume: int = 1000, min_open_interest: int = 100, max_spread_width: float = 0.05) -> List[str]:
    """
    Filter symbols based on minimum liquidity thresholds.

    Args:
        symbols: List of symbol names to filter
        min_volume: Minimum trading volume threshold
        min_open_interest: Minimum open interest threshold
        max_spread_width: Maximum spread width as a fraction of the contract price

    Returns:
        List of liquid symbol names
    """
    # This is a placeholder implementation
    # In a real implementation, this would query data for each symbol
    # and apply the same filtering logic as filter_liquid_contracts
    return symbols
