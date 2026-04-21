from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from app.models.types import Symbol, ContractId


class UnusualActivitySignal:
    """Represents a signal for unusual activity in options data."""
    symbol: Symbol
    contract_id: Optional[ContractId]
    signal_type: str  # volume_spike, oi_change, call_put_imbalance, iv_spike, premium_spike
    score: float
    value: float
    baseline_value: float
    timestamp: datetime
    
    def __init__(self, symbol: Symbol, contract_id: Optional[ContractId], signal_type: str, score: float, 
                 value: float, baseline_value: float, timestamp: datetime):
        self.symbol = symbol
        self.contract_id = contract_id
        self.signal_type = signal_type
        self.score = score
        self.value = value
        self.baseline_value = baseline_value
        self.timestamp = timestamp


class UnusualActivityResult:
    """Result of unusual activity detection."""
    signals: List[UnusualActivitySignal]
    timestamp: datetime
    
    def __init__(self, signals: List[UnusualActivitySignal], timestamp: datetime):
        self.signals = signals
        self.timestamp = timestamp