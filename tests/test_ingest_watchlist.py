import unittest
from unittest.mock import patch, MagicMock
from app.data.jobs.ingest_watchlist import ingest_watchlist_data


class TestIngestWatchlist(unittest.TestCase):

    @patch('app.data.jobs.ingest_watchlist.get_watchlist_symbols')
    @patch('app.data.jobs.ingest_watchlist.get_provider')
    def test_ingest_watchlist_data_success(self, mock_provider, mock_symbols):
        # Setup
        mock_symbols.return_value = ['AAPL']
        mock_provider_instance = MagicMock()
        mock_provider.return_value = mock_provider_instance
        mock_provider_instance.get_equity_data.return_value = {'symbol': 'AAPL', 'open': 100.0}
        mock_provider_instance.get_options_data.return_value = [{'symbol': 'AAPL', 'strike': 100.0}]

        # Execute
        ingest_watchlist_data()

        # Verify
        mock_provider_instance.get_equity_data.assert_called_once_with('AAPL')
        mock_provider_instance.get_options_data.assert_called_once_with('AAPL')

    @patch('app.data.jobs.ingest_watchlist.get_watchlist_symbols')
    @patch('app.data.jobs.ingest_watchlist.get_provider')
    def test_ingest_watchlist_data_failure(self, mock_provider, mock_symbols):
        # Setup
        mock_symbols.return_value = ['AAPL']
        mock_provider_instance = MagicMock()
        mock_provider.return_value = mock_provider_instance
        mock_provider_instance.get_equity_data.side_effect = Exception("Network error")

        # Execute
        ingest_watchlist_data()

        # Verify
        # The function should not crash even if one symbol fails
        mock_provider_instance.get_equity_data.assert_called_once_with('AAPL')
