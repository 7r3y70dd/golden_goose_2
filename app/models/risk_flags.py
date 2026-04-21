from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta


class RiskFlag:
    """Represents a risk flag that can be attached to an opportunity."""
    name: str
    description: str
    severity: str  # 'low', 'medium', 'high'
    is_hard_exclusion: bool = False  # Indicates if this flag blocks the opportunity entirely


@dataclass
class RiskFlags:
    """Container for all risk flags associated with an opportunity."""
    illiquid_contract: Optional[RiskFlag] = None
    wide_spread: Optional[RiskFlag] = None
    low_confidence: Optional[RiskFlag] = None
    stale_data: Optional[RiskFlag] = None
    high_volatility: Optional[RiskFlag] = None
    poor_liquidity: Optional[RiskFlag] = None
    upcoming_earnings: Optional[RiskFlag] = None
    upcoming_dividend: Optional[RiskFlag] = None
    upcoming_economic_event: Optional[RiskFlag] = None
    upcoming_fomc_event: Optional[RiskFlag] = None

    def has_hard_exclusions(self) -> bool:
        """Check if any hard exclusions are present."""
        return any(flag is not None and flag.is_hard_exclusion for flag in self.__dict__.values())

    def get_all_flags(self) -> List[RiskFlag]:
        """Get all non-None flags."""
        return [flag for flag in self.__dict__.values() if flag is not None]


def check_illiquid_contract(volume: float, open_interest: float) -> Optional[RiskFlag]:
    """Check if contract has insufficient volume or open interest."""
    # Simple check - if both are very low, flag as illiquid
    if volume < 100 and open_interest < 100:
        return RiskFlag(
            name='illiquid_contract',
            description='Insufficient volume and open interest',
            severity='high',
            is_hard_exclusion=True
        )
    return None


def check_wide_spread(spread_ratio: float) -> Optional[RiskFlag]:
    """Check if spread is too wide."""
    if spread_ratio > 0.05:  # 5% threshold
        return RiskFlag(
            name='wide_spread',
            description='Wide bid-ask spread indicates poor liquidity',
            severity='medium',
            is_hard_exclusion=False
        )
    return None


def check_low_confidence(confidence: float) -> Optional[RiskFlag]:
    """Check if prediction confidence is too low."""
    if confidence < 0.5:  # 50% threshold
        return RiskFlag(
            name='low_confidence',
            description='Prediction confidence is below threshold',
            severity='medium',
            is_hard_exclusion=False
        )
    return None


def check_stale_data(data_age_hours: float) -> Optional[RiskFlag]:
    """Check if data is stale."""
    if data_age_hours > 24:  # 24 hour threshold
        return RiskFlag(
            name='stale_data',
            description='Data is older than maximum allowed age',
            severity='high',
            is_hard_exclusion=True
        )
    return None


def check_high_volatility(volatility: float) -> Optional[RiskFlag]:
    """Check if volatility is too high."""
    if volatility > 0.5:  # 50% threshold
        return RiskFlag(
            name='high_volatility',
            description='High volatility indicates instability',
            severity='high',
            is_hard_exclusion=True
        )
    return None


def check_poor_liquidity(liquidity_score: float) -> Optional[RiskFlag]:
    """Check if liquidity score is poor."""
    if liquidity_score < 0.5:  # Poor liquidity threshold
        return RiskFlag(
            name='poor_liquidity',
            description='Poor liquidity score',
            severity='medium',
            is_hard_exclusion=False
        )
    return None


def check_upcoming_earnings(earnings_date: Optional[datetime], window_days: int = 30) -> Optional[RiskFlag]:
    """Check if earnings are upcoming within the specified window."""
    if earnings_date is None:
        return None
    
    days_until_earnings = (earnings_date - datetime.now()).days
    if 0 <= days_until_earnings <= window_days:
        return RiskFlag(
            name='upcoming_earnings',
            description=f'Upcoming earnings in {days_until_earnings} days',
            severity='medium',
            is_hard_exclusion=False
        )
    return None


def check_upcoming_dividend(dividend_date: Optional[datetime], window_days: int = 30) -> Optional[RiskFlag]:
    """Check if dividend is upcoming within the specified window."""
    if dividend_date is None:
        return None
    
    days_until_dividend = (dividend_date - datetime.now()).days
    if 0 <= days_until_dividend <= window_days:
        return RiskFlag(
            name='upcoming_dividend',
            description=f'Upcoming dividend in {days_until_dividend} days',
            severity='low',
            is_hard_exclusion=False
        )
    return None


def check_upcoming_economic_event(event_date: Optional[datetime], window_days: int = 7) -> Optional[RiskFlag]:
    """Check if economic event is upcoming within the specified window."""
    if event_date is None:
        return None
    
    days_until_event = (event_date - datetime.now()).days
    if 0 <= days_until_event <= window_days:
        return RiskFlag(
            name='upcoming_economic_event',
            description=f'Upcoming economic event in {days_until_event} days',
            severity='medium',
            is_hard_exclusion=False
        )
    return None


def check_upcoming_fomc_event(event_date: Optional[datetime], window_days: int = 30) -> Optional[RiskFlag]:
    """Check if FOMC event is upcoming within the specified window."""
    if event_date is None:
        return None
    
    days_until_event = (event_date - datetime.now()).days
    if 0 <= days_until_event <= window_days:
        return RiskFlag(
            name='upcoming_fomc_event',
            description=f'Upcoming FOMC event in {days_until_event} days',
            severity='high',
            is_hard_exclusion=False
        )
    return None


def generate_risk_flags(
    volume: float,
    open_interest: float,
    confidence: float,
    data_age_hours: float,
    volatility: float,
    liquidity_score: Optional[float],
    earnings_date: Optional[datetime],
    dividend_date: Optional[datetime],
    economic_event_date: Optional[datetime],
    fomc_event_date: Optional[datetime],
    event_window_days: int = 30
) -> RiskFlags:
    """Generate all risk flags for an opportunity."""
    # Create RiskFlags object
    risk_flags = RiskFlags()
    
    # Generate basic risk flags
    basic_flags = [
        check_illiquid_contract(volume, open_interest),
        check_wide_spread(volume),
        check_low_confidence(confidence),
        check_stale_data(data_age_hours),
        check_high_volatility(volatility),
        check_poor_liquidity(liquidity_score) if liquidity_score is not None else None
    ]
    
    # Filter out None values
    basic_flags = [flag for flag in basic_flags if flag is not None]
    
    # Assign basic flags to appropriate attributes
    for flag in basic_flags:
        if flag.name == 'illiquid_contract':
            risk_flags.illiquid_contract = flag
        elif flag.name == 'wide_spread':
            risk_flags.wide_spread = flag
        elif flag.name == 'low_confidence':
            risk_flags.low_confidence = flag
        elif flag.name == 'stale_data':
            risk_flags.stale_data = flag
        elif flag.name == 'high_volatility':
            risk_flags.high_volatility = flag
        elif flag.name == 'poor_liquidity':
            risk_flags.poor_liquidity = flag
    
    # Generate event risk flags
    event_flags = [
        check_upcoming_earnings(earnings_date, event_window_days),
        check_upcoming_dividend(dividend_date, event_window_days),
        check_upcoming_economic_event(economic_event_date, event_window_days),
        check_upcoming_fomc_event(fomc_event_date, event_window_days)
    ]
    
    # Filter out None values
    event_flags = [flag for flag in event_flags if flag is not None]
    
    # Assign event flags to appropriate attributes
    for flag in event_flags:
        if flag.name == 'upcoming_earnings':
            risk_flags.upcoming_earnings = flag
        elif flag.name == 'upcoming_dividend':
            risk_flags.upcoming_dividend = flag
        elif flag.name == 'upcoming_economic_event':
            risk_flags.upcoming_economic_event = flag
        elif flag.name == 'upcoming_fomc_event':
            risk_flags.upcoming_fomc_event = flag
    
    return risk_flags
