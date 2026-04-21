import datetime
from typing import List, Optional


class ContractSelector:
    """
    Selects suitable options contracts based on scoring and risk flags.

    The selection process filters contracts based on:
    1. Expiry date matching the target date
    2. Strike price within reasonable bounds
    3. Minimum open interest threshold
    4. Sorting by open interest (descending)

    Edge cases handled:
    - Empty contract list returns empty candidate list
    - No valid contracts meet criteria returns empty candidate list
    - Contracts with zero or negative open interest are excluded
    - Contracts with invalid expiry dates are excluded
    """

    def __init__(self, min_open_interest: int = 100):
        self.min_open_interest = min_open_interest

    def select_bearish_candidates(
        self,
        contracts: List[dict],
        target_date: datetime.date,
        current_price: float
    ) -> List[dict]:
        """
        Select bearish candidates from a list of contracts.

        Args:
            contracts: List of contract dictionaries with keys 'strike', 'expiry', 'open_interest'
            target_date: The target date for contract expiry
            current_price: Current price of the underlying asset

        Returns:
            List of valid contracts sorted by open interest (descending)
        """
        if not contracts:
            return []

        valid_contracts = []
        for contract in contracts:
            # Skip contracts with invalid expiry dates
            if not contract.get('expiry') or not isinstance(contract['expiry'], datetime.date):
                continue
            
            # Skip contracts with insufficient open interest
            if contract.get('open_interest', 0) < self.min_open_interest:
                continue
            
            # Skip contracts with invalid strike prices
            if contract.get('strike', 0) <= 0:
                continue
            
            # Only consider contracts that expire on target date
            if contract['expiry'] != target_date:
                continue
            
            valid_contracts.append(contract)

        # Sort by open interest descending
        valid_contracts.sort(key=lambda x: x.get('open_interest', 0), reverse=True)
        return valid_contracts

    def select_bullish_candidates(
        self,
        contracts: List[dict],
        target_date: datetime.date,
        current_price: float
    ) -> List[dict]:
        """
        Select bullish candidates from a list of contracts.

        Args:
            contracts: List of contract dictionaries with keys 'strike', 'expiry', 'open_interest'
            target_date: The target date for contract expiry
            current_price: Current price of the underlying asset

        Returns:
            List of valid contracts sorted by open interest (descending)
        """
        if not contracts:
            return []

        valid_contracts = []
        for contract in contracts:
            # Skip contracts with invalid expiry dates
            if not contract.get('expiry') or not isinstance(contract['expiry'], datetime.date):
                continue
            
            # Skip contracts with insufficient open interest
            if contract.get('open_interest', 0) < self.min_open_interest:
                continue
            
            # Skip contracts with invalid strike prices
            if contract.get('strike', 0) <= 0:
                continue
            
            # Only consider contracts that expire on target date
            if contract['expiry'] != target_date:
                continue
            
            valid_contracts.append(contract)

        # Sort by open interest descending
        valid_contracts.sort(key=lambda x: x.get('open_interest', 0), reverse=True)
        return valid_contracts

    def rank_expirations(
        self,
        contracts: List[dict],
        strategy_type: str,
        preferences: dict = None
    ) -> List[dict]:
        """
        Rank expirations based on various metrics and preferences.

        Args:
            contracts: List of contract dictionaries with expiration metrics
            strategy_type: Type of strategy ('bullish', 'bearish')
            preferences: User preferences for ranking criteria

        Returns:
            List of expirations ranked by recommendation score
        """
        if not contracts:
            return []

        # Default preferences if none provided
        if preferences is None:
            preferences = {
                'theta_decay': 0.3,
                'premium_cost': 0.2,
                'liquidity_quality': 0.2,
                'convexity': 0.15,
                'event_overlap': 0.15
            }

        # Calculate metrics for each contract
        ranked_contracts = []
        for contract in contracts:
            # Calculate days to expiration
            days_to_expiration = (contract['expiry'] - datetime.date.today()).days
            
            # Calculate recommendation score based on preferences
            score = 0
            
            # Lower theta decay (better for longer term)
            if 'theta' in contract:
                score += (1 / (1 + contract['theta'])) * preferences['theta_decay']
            
            # Cheaper premium (better for cost-conscious strategies)
            if 'premium' in contract:
                score += (1 / (1 + contract['premium'])) * preferences['premium_cost']
            
            # Tighter spreads (better for liquidity)
            if 'spread' in contract:
                score += (1 / (1 + contract['spread'])) * preferences['liquidity_quality']
            
            # Convexity (better for volatility strategies)
            if 'convexity' in contract:
                score += contract['convexity'] * preferences['convexity']
            
            # Event overlap penalty (lower is better)
            if 'event_overlap' in contract:
                score -= contract['event_overlap'] * preferences['event_overlap']
            
            contract['recommendation_score'] = score
            contract['days_to_expiration'] = days_to_expiration
            ranked_contracts.append(contract)

        # Sort by recommendation score (descending)
        ranked_contracts.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return ranked_contracts
