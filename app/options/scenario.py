from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pydantic import BaseModel
from app.models.types import Price, Volatility, DaysToExpiration


class Scenario(BaseModel):
    """
    Represents a single scenario with specific parameter values.
    """
    underlying_price: Price
    volatility: Volatility
    days_to_expiration: DaysToExpiration
    
    def __init__(self, underlying_price: Price, volatility: Volatility, days_to_expiration: DaysToExpiration):
        super().__init__(underlying_price=underlying_price, volatility=volatility, days_to_expiration=days_to_expiration)


class ScenarioGrid(BaseModel):
    """
    Represents a grid of scenarios for analysis.
    """
    scenarios: List[Scenario]
    
    def __init__(self, scenarios: List[Scenario]):
        super().__init__(scenarios=scenarios)


def generate_scenario_grid(underlying_range: Tuple[Price, Price], 
                          volatility_range: Tuple[Volatility, Volatility], 
                          expiration_range: Tuple[DaysToExpiration, DaysToExpiration], 
                          steps: int = 3) -> ScenarioGrid:
    """
    Generate a grid of scenarios based on ranges and steps.
    """
    # Simple grid generation - in future could be more sophisticated
    scenarios = []
    
    underlying_step = (underlying_range[1] - underlying_range[0]) / (steps - 1)
    volatility_step = (volatility_range[1] - volatility_range[0]) / (steps - 1)
    expiration_step = (expiration_range[1] - expiration_range[0]) / (steps - 1)
    
    for i in range(steps):
        underlying = underlying_range[0] + i * underlying_step
        volatility = volatility_range[0] + i * volatility_step
        expiration = expiration_range[0] + i * expiration_step
        
        scenarios.append(Scenario(underlying, volatility, expiration))
    
    return ScenarioGrid(scenarios)


def generate_presets() -> Dict[str, ScenarioGrid]:
    """
    Generate preset scenario grids (best-case, base-case, worst-case).
    """
    # These are example presets - actual values would depend on business logic
    presets = {
        'best_case': ScenarioGrid([Scenario(120.0, 0.2, 30)]),
        'base_case': ScenarioGrid([Scenario(100.0, 0.3, 60)]),
        'worst_case': ScenarioGrid([Scenario(80.0, 0.4, 90)])
    }
    
    return presets
