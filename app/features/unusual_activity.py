import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
from app.models.types import Symbol, ContractId


class UnusualActivitySignal:
    """Represents a signal for unusual activity in options data."""
    symbol: Symbol
    contract_id: ContractId
    signal_type: str  # volume_spike, oi_change, call_put_imbalance, iv_spike, premium_spike
    score: float
    value: float
    baseline_value: float
    timestamp: pd.Timestamp


class UnusualActivityDetector:
    """Detects unusual activity in options data."""
    
    def __init__(self):
        self.signals = []
        
    def detect_volume_spike(self, df: pd.DataFrame, threshold: float = 2.0) -> List[UnusualActivitySignal]:
        """Detect volume spikes compared to average."""
        signals = []
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            avg_volume = symbol_data['volume'].mean()
            current_volume = symbol_data['volume'].iloc[-1]
            if current_volume > avg_volume * threshold:
                signals.append(UnusualActivitySignal(
                    symbol=symbol,
                    contract_id=None,
                    signal_type='volume_spike',
                    score=current_volume / avg_volume,
                    value=current_volume,
                    baseline_value=avg_volume,
                    timestamp=pd.Timestamp.now()
                ))
        return signals
    
    def detect_oi_change(self, df: pd.DataFrame, threshold: float = 1.5) -> List[UnusualActivitySignal]:
        """Detect significant open interest changes."""
        signals = []
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            if len(symbol_data) < 2:
                continue
            
            # Use the last two values to calculate change
            prev_oi = symbol_data['open_interest'].iloc[-2]
            current_oi = symbol_data['open_interest'].iloc[-1]
            oi_change = current_oi - prev_oi
            
            # Calculate average absolute change from previous data points
            if len(symbol_data) >= 3:
                changes = symbol_data['open_interest'].diff().dropna()
                avg_change = changes.abs().mean()
            else:
                avg_change = 0.0
            
            if avg_change != 0 and abs(oi_change) > avg_change * threshold:
                signals.append(UnusualActivitySignal(
                    symbol=symbol,
                    contract_id=None,
                    signal_type='oi_change',
                    score=abs(oi_change) / avg_change,
                    value=oi_change,
                    baseline_value=avg_change,
                    timestamp=pd.Timestamp.now()
                ))
        return signals
    
    def detect_call_put_imbalance(self, df: pd.DataFrame, threshold: float = 1.5) -> List[UnusualActivitySignal]:
        """Detect call/put imbalance."""
        signals = []
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            if len(symbol_data) < 1:
                continue
            call_volume = symbol_data['call_volume'].iloc[-1]
            put_volume = symbol_data['put_volume'].iloc[-1]
            total_volume = call_volume + put_volume
            if total_volume > 0:
                imbalance = abs(call_volume - put_volume) / total_volume
                if imbalance > threshold:
                    signals.append(UnusualActivitySignal(
                        symbol=symbol,
                        contract_id=None,
                        signal_type='call_put_imbalance',
                        score=imbalance,
                        value=imbalance,
                        baseline_value=0,
                        timestamp=pd.Timestamp.now()
                    ))
        return signals
    
    def detect_iv_spike(self, df: pd.DataFrame, threshold: float = 2.0) -> List[UnusualActivitySignal]:
        """Detect IV spikes compared to average."""
        signals = []
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            avg_iv = symbol_data['implied_volatility'].mean()
            current_iv = symbol_data['implied_volatility'].iloc[-1]
            if current_iv > avg_iv * threshold:
                signals.append(UnusualActivitySignal(
                    symbol=symbol,
                    contract_id=None,
                    signal_type='iv_spike',
                    score=current_iv / avg_iv,
                    value=current_iv,
                    baseline_value=avg_iv,
                    timestamp=pd.Timestamp.now()
                ))
        return signals
    
    def detect_premium_spike(self, df: pd.DataFrame, threshold: float = 2.0) -> List[UnusualActivitySignal]:
        """Detect premium traded spikes compared to average."""
        signals = []
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            avg_premium = symbol_data['premium_traded'].mean()
            current_premium = symbol_data['premium_traded'].iloc[-1]
            if current_premium > avg_premium * threshold:
                signals.append(UnusualActivitySignal(
                    symbol=symbol,
                    contract_id=None,
                    signal_type='premium_spike',
                    score=current_premium / avg_premium,
                    value=current_premium,
                    baseline_value=avg_premium,
                    timestamp=pd.Timestamp.now()
                ))
        return signals
    
    def detect_all_signals(self, df: pd.DataFrame) -> List[UnusualActivitySignal]:
        """Detect all types of unusual activity signals."""
        all_signals = []
        all_signals.extend(self.detect_volume_spike(df))
        all_signals.extend(self.detect_oi_change(df))
        all_signals.extend(self.detect_call_put_imbalance(df))
        all_signals.extend(self.detect_iv_spike(df))
        all_signals.extend(self.detect_premium_spike(df))
        return all_signals
    
    def rank_signals(self, signals: List[UnusualActivitySignal], top_n: int = 10) -> List[UnusualActivitySignal]:
        """Rank signals by their scores."""
        sorted_signals = sorted(signals, key=lambda x: x.score, reverse=True)
        return sorted_signals[:top_n]
