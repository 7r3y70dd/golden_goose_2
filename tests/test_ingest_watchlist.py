import pytest
from unittest.mock import Mock, patch

from app.data.jobs.ingest_watchlist import ingest_watchlist
from app.data.providers.base import MarketDataProvider
from app.data.repository import DataRepository


def test_ingest_watchlist_success():
    # Mock provider and repository
    provider = Mock(spec=MarketDataProvider)
    repository = Mock(spec=DataRepository)

    # Mock data
    provider.get_historical_bars.return_value = [
        Mock(symbol="AAPL", open=100, high=110, low=90, close=105, volume=1000)
    ]
    provider.get_options_chain.return_value = [
        Mock(symbol="AAPL", strike=100, expiry="2023-12-01", option_type="call")
    ]

    # Mock watchlist
    with patch("app.watchlist.load_watchlist", return_value=["AAPL"]):
        ingest_watchlist(provider, repository)

    # Verify calls
    provider.get_historical_bars.assert_called_once_with("AAPL", days=30)
    provider.get_options_chain.assert_called_once_with("AAPL")
    repository.save_historical_bars.assert_called_once()
    repository.save_options_chain.assert_called_once()


def test_ingest_watchlist_with_exception():
    # Mock provider and repository
    provider = Mock(spec=MarketDataProvider)
    repository = Mock(spec=DataRepository)

    # Mock provider to raise an exception
    provider.get_historical_bars.side_effect = Exception("Network error")

    # Mock watchlist
    with patch("app.watchlist.load_watchlist", return_value=["AAPL"]):
        ingest_watchlist(provider, repository)

    # Verify that the exception was handled and logging occurred
    provider.get_historical_bars.assert_called_once_with("AAPL", days=30)
    repository.save_historical_bars.assert_not_called()