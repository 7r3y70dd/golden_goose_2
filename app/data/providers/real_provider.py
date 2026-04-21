from typing import List, Optional, Dict, Any

from app.data.providers.base import Provider


class RealProvider(Provider):
    """
    A stub implementation of a real market data provider.

    This class serves as a scaffold for a future real implementation.
    It implements the Provider interface but does not perform actual network calls.
    """

    def __init__(self):
        # TODO: Implement authentication logic
        pass

    def get_latest_quote(self, symbol: str) -> Dict[str, Any]:
        # TODO: Implement fetch logic for latest quote
        # TODO: Implement normalization logic
        # TODO: Implement retry logic
        raise NotImplementedError("This is a stub implementation")

    def get_historical_bars(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> List[Dict[str, Any]]:
        # TODO: Implement fetch logic for historical bars
        # TODO: Implement normalization logic
        # TODO: Implement retry logic
        raise NotImplementedError("This is a stub implementation")

    def get_options_chain(self, symbol: str) -> Dict[str, Any]:
        # TODO: Implement fetch logic for options chain
        # TODO: Implement normalization logic
        # TODO: Implement retry logic
        raise NotImplementedError("This is a stub implementation")
