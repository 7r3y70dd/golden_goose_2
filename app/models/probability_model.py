from typing import Dict, List, Optional, Tuple
import math

class ProbabilityModel:
    """
    Basic probability model for option opportunities.
    
    Provides estimates for:
    - Probability of expiring ITM
    - Probability of reaching target profit
    - Probability of max loss
    - Expected value
    
    Assumptions:
    - Log-normal distribution of underlying price
    - Constant volatility (implied or historical)
    - No dividends during option life
    - European-style options
    """
    
    def __init__(self, volatility: float, time_to_expiry: float, strike: float, underlying_price: float):
        self.volatility = volatility
        self.time_to_expiry = time_to_expiry
        self.strike = strike
        self.underlying_price = underlying_price
        
    def probability_expiring_itm(self) -> float:
        """
        Calculate probability of expiring ITM using Black-Scholes model.
        
        Returns:
            Probability of expiring ITM (0.0 to 1.0)
        """
        if self.volatility == 0:
            return 1.0 if self.underlying_price > self.strike else 0.0
        
        d1 = (math.log(self.underlying_price / self.strike) + 0.5 * self.volatility ** 2 * self.time_to_expiry) / \
             (self.volatility * math.sqrt(self.time_to_expiry))
        
        return self._norm_cdf(d1)
    
    def probability_reaching_target(self, target_price: float) -> float:
        """
        Calculate probability of reaching target price before expiration.
        
        Args:
            target_price: Target price to reach
            
        Returns:
            Probability of reaching target (0.0 to 1.0)
        """
        if self.volatility == 0:
            return 1.0 if self.underlying_price >= target_price else 0.0
        
        d1 = (math.log(self.underlying_price / target_price) + 0.5 * self.volatility ** 2 * self.time_to_expiry) / \
             (self.volatility * math.sqrt(self.time_to_expiry))
        
        return self._norm_cdf(d1)
    
    def probability_max_loss(self, max_loss: float) -> float:
        """
        Calculate probability of maximum loss being exceeded.
        
        Args:
            max_loss: Maximum loss threshold
            
        Returns:
            Probability of exceeding max loss (0.0 to 1.0)
        """
        # Simplified: assume loss is based on strike price
        # In reality, this would depend on the specific strategy
        if self.volatility == 0:
            return 1.0 if self.underlying_price <= self.strike - max_loss else 0.0
        
        # This is a simplified model - in practice, would need to consider
        # the specific option strategy and position
        return 1.0 - self.probability_expiring_itm()
    
    def expected_value(self, option_price: float, target_profit: Optional[float] = None) -> float:
        """
        Calculate expected value under current assumptions.
        
        Args:
            option_price: Current price of the option
            target_profit: Target profit to consider
            
        Returns:
            Expected value estimate
        """
        # Simplified expected value calculation
        # In practice, this would be more complex and strategy-dependent
        prob_itm = self.probability_expiring_itm()
        
        if target_profit is not None:
            # If we have a target profit, we can estimate the expected value
            # This is a simplified version
            return prob_itm * target_profit - option_price
        
        # Basic expected value based on probability of ITM
        return prob_itm * (self.underlying_price - self.strike) - option_price
    
    def _norm_cdf(self, x: float) -> float:
        """
        Standard normal cumulative distribution function.
        
        Args:
            x: Standard normal variable
            
        Returns:
            CDF value
        """
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    
    def get_assumptions(self) -> Dict[str, str]:
        """
        Get model assumptions for documentation.
        
        Returns:
            Dictionary of assumptions
        """
        return {
            "volatility_assumption": "Constant volatility (implied or historical)",
            "distribution_assumption": "Log-normal distribution of underlying price",
            "dividend_assumption": "No dividends during option life",
            "option_type_assumption": "European-style options",
            "time_assumption": "Time to expiry in years"
        }