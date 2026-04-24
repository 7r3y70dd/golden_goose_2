from datetime import datetime, timedelta
from typing import List, Optional

from app.data.schemas import EquityBar, OptionsContract
from app.data.providers.base import MarketDataProvider


class MockMarketDataProvider(MarketDataProvider):
    """
    Mock implementation of MarketDataProvider for development and testing.
    
    Returns deterministic sample data for all methods.
    """

    def get_latest_quote(self, symbol: str) -> Optional[EquityBar]:
        # Return a deterministic sample equity bar
        return EquityBar(
            symbol=symbol,
            timestamp=datetime.now(),
            open=100.0,
            high=105.0,
            low=95.0,
            close=102.0,
            volume=1000000
        )

    def get_historical_bars(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d"
    ) -> List[EquityBar]:
        # Generate sample bars for the date range
        bars = []
        current_date = start_date
        
        while current_date <= end_date:
            bars.append(EquityBar(
                symbol=symbol,
                timestamp=current_date,
                open=100.0 + (current_date.day % 10),
                high=105.0 + (current_date.day % 10),
                low=95.0 + (current_date.day % 10),
                close=102.0 + (current_date.day % 10),
                volume=1000000 + (current_date.day * 1000)
            ))
            current_date += timedelta(days=1)
        
        return bars

    def get_options_chain(
        self,
        symbol: str,
        expiration_date: Optional[datetime] = None
    ) -> List[OptionsContract]:
        # Return a deterministic sample options chain
        contracts = []
        
        # Generate sample contracts for different strikes and expirations
        strikes = [95.0, 100.0, 105.0, 110.0]
        expirations = [
            datetime.now() + timedelta(days=30),
            datetime.now() + timedelta(days=60),
            datetime.now() + timedelta(days=90)
        ]
        
        for strike in strikes:
            for exp in expirations:
                contracts.append(OptionsContract(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    strike=strike,
                    expiry=exp,
                    put_call='call' if strike > 100.0 else 'put',
                    bid=0.5 + (strike / 100.0),
                    ask=0.6 + (strike / 100.0),
                    last=0.55 + (strike / 100.0),
                    volume=1000 + (strike * 10),
                    open_interest=500 + (strike * 5),
                    iv=0.2 + (strike / 1000.0)
                ))
        
        return contracts