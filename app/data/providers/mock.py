from typing import List, Dict, Any
from app.data.providers.base import Provider


class MockProvider(Provider):
    """
    Mock provider for development and testing.
    Returns deterministic sample data.

    This implementation serves as a reference for how to implement the Provider interface.
    All methods return well-formed data that matches the expected input/output shapes.
    """

    def get_latest_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Return a mock latest quote for the given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :return: Dictionary containing quote data with keys: symbol, price, change, change_percent, volume, timestamp
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")
        
        return {
            'symbol': symbol,
            'price': 150.00,
            'change': 2.50,
            'change_percent': 1.69,
            'volume': 1000000,
            'timestamp': '2023-01-01T10:00:00Z'
        }

    def get_historical_bars(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> List[Dict[str, Any]]:
        """
        Return mock historical bars for the given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :param start_date: Start date in YYYY-MM-DD format
        :param end_date: End date in YYYY-MM-DD format
        :param interval: Time interval (e.g., '1d', '1h', '5m')
        :return: List of bar dictionaries with keys: date, open, high, low, close, volume
        :raises ValueError: If dates are invalid or interval is unsupported
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")
        if not start_date or not isinstance(start_date, str):
            raise ValueError("Start date must be a non-empty string")
        if not end_date or not isinstance(end_date, str):
            raise ValueError("End date must be a non-empty string")
        if interval not in ['1d', '1h', '5m']:
            raise ValueError("Unsupported interval. Must be one of: '1d', '1h', '5m'")
        
        return [
            {
                'date': '2023-01-01',
                'open': 145.0,
                'high': 152.0,
                'low': 144.0,
                'close': 150.0,
                'volume': 1000000
            },
            {
                'date': '2023-01-02',
                'open': 150.0,
                'high': 155.0,
                'low': 148.0,
                'close': 153.0,
                'volume': 1200000
            }
        ]

    def get_options_chain(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch the options chain for a given symbol.

        :param symbol: Ticker symbol (e.g., 'AAPL')
        :return: Dictionary containing options chain data with keys: symbol, expiration_dates, calls, puts
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")
        
        return {
            'symbol': symbol,
            'expiration_dates': ['2023-01-15', '2023-02-15', '2023-03-15'],
            'calls': [
                {'strike': 140.0, 'last': 10.0, 'change': 0.5, 'volume': 1000},
                {'strike': 145.0, 'last': 7.0, 'change': 0.3, 'volume': 800}
            ],
            'puts': [
                {'strike': 140.0, 'last': 2.0, 'change': 0.1, 'volume': 500},
                {'strike': 145.0, 'last': 3.5, 'change': 0.2, 'volume': 600}
            ]
        }

    def get_watchlist(self) -> List[str]:
        """
        Return a mock watchlist of symbols.

        :return: List of ticker symbols
        """
        return ['AAPL', 'MSFT', 'GOOGL']