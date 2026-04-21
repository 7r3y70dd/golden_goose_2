from typing import List, Dict, Tuple
from dataclasses import dataclass
from .opportunity import Opportunity
from .types import Greeks


class PortfolioAnalytics:
    def __init__(self, opportunities: List[Opportunity]):
        self.opportunities = opportunities

    def get_symbol_exposure(self) -> Dict[str, float]:
        """Aggregate exposure by symbol"""
        exposure = {}
        for opp in self.opportunities:
            symbol = opp.symbol
            exposure[symbol] = exposure.get(symbol, 0) + opp.position_size
        return exposure

    def get_sector_exposure(self) -> Dict[str, float]:
        """Aggregate exposure by sector"""
        exposure = {}
        for opp in self.opportunities:
            sector = opp.sector
            exposure[sector] = exposure.get(sector, 0) + opp.position_size
        return exposure

    def get_expiration_bucket_exposure(self) -> Dict[str, float]:
        """Aggregate exposure by expiration bucket"""
        exposure = {}
        for opp in self.opportunities:
            bucket = opp.expiration_bucket
            exposure[bucket] = exposure.get(bucket, 0) + opp.position_size
        return exposure

    def get_strategy_type_exposure(self) -> Dict[str, float]:
        """Aggregate exposure by strategy type"""
        exposure = {}
        for opp in self.opportunities:
            strategy = opp.strategy_type
            exposure[strategy] = exposure.get(strategy, 0) + opp.position_size
        return exposure

    def get_greeks_summary(self) -> Greeks:
        """Calculate portfolio-level Greeks summary"""
        total_delta = 0.0
        total_gamma = 0.0
        total_theta = 0.0
        total_vega = 0.0

        for opp in self.opportunities:
            total_delta += opp.greeks.delta * opp.position_size
            total_gamma += opp.greeks.gamma * opp.position_size
            total_theta += opp.greeks.theta * opp.position_size
            total_vega += opp.greeks.vega * opp.position_size

        return Greeks(
            delta=total_delta,
            gamma=total_gamma,
            theta=total_theta,
            vega=total_vega
        )

    def get_concentration_warnings(self) -> List[str]:
        """Generate concentration warnings"""
        warnings = []
        symbol_exposure = self.get_symbol_exposure()
        total_exposure = sum(symbol_exposure.values())

        if total_exposure > 0:
            for symbol, exposure in symbol_exposure.items():
                ratio = exposure / total_exposure
                if ratio > 0.5:
                    warnings.append(f"High concentration in {symbol}: {ratio:.2%}")

        return warnings

    def get_net_premium_at_risk(self) -> float:
        """Calculate net premium at risk"""
        return sum(opp.net_premium for opp in self.opportunities)

    def stress_test(self, stress_factor: float = 0.1) -> Dict[str, float]:
        """Simple stress test at portfolio level"""
        greeks = self.get_greeks_summary()
        return {
            'delta': greeks.delta * stress_factor,
            'gamma': greeks.gamma * stress_factor,
            'theta': greeks.theta * stress_factor,
            'vega': greeks.vega * stress_factor
        }