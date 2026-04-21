from enum import Enum
from typing import List, Dict, Any
from dataclasses import dataclass


class StrategyType(str, Enum):
    LONG_PUT = "long_put"
    LONG_CALL = "long_call"
    BEAR_PUT_SPREAD = "bear_put_spread"
    BULL_CALL_SPREAD = "bull_call_spread"
    COVERED_CALL = "covered_call"
    CASH_SECURED_PUT = "cash_secured_put"
    STRADDLE = "straddle"
    STRANGLE = "strangle"
    IRON_CONDOR = "iron_condor"


@dataclass
class StrategyLeg:
    symbol: str
    strike: float
    expiration: str
    option_type: str  # 'call' or 'put'
    quantity: int
    premium: float


@dataclass
class Strategy:
    strategy_type: StrategyType
    legs: List[StrategyLeg]
    underlying_symbol: str
    expiration_date: str
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            'strategy_type': self.strategy_type.value,
            'underlying_symbol': self.underlying_symbol,
            'expiration_date': self.expiration_date,
            'leg_count': len(self.legs)
        }
    
    def get_risk_reward(self) -> Dict[str, float]:
        # Placeholder for risk/reward calculations
        return {
            'max_profit': float('inf'),
            'max_loss': float('inf'),
            'break_even': None
        }