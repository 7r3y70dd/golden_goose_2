import pytest
from unittest.mock import patch, MagicMock
from app.data.jobs.ingest_watchlist import ingest_watchlist_data, fetch_and_save_equity_data, fetch_and_save_options_data


def test_fetch_and_save_equity_data_success():
    with patch('app.data.jobs.ingest_watchlist.save_equity_data') as mock_save:
        mock_save.return_value = None
        result = fetch_and_save_equity_data("AAPL")
        assert result is True


def test_fetch_and_save_equity_data_failure():
    with patch('app.data.jobs.ingest_watchlist.save_equity_data') as mock_save:
        mock_save.side_effect = Exception("Database error")
        result = fetch_and_save_equity_data("AAPL")
        assert result is False


def test_fetch_and_save_options_data_success():
    with patch('app.data.jobs.ingest_watchlist.save_options_data') as mock_save:
        mock_save.return_value = None
        result = fetch_and_save_options_data("AAPL")
        assert result is True


def test_fetch_and_save_options_data_failure():
    with patch('app.data.jobs.ingest_watchlist.save_options_data') as mock_save:
        mock_save.side_effect = Exception("Database error")
        result = fetch_and_save_options_data("AAPL")
        assert result is False


def test_ingest_watchlist_data_success():
    with patch('app.data.jobs.ingest_watchlist.get_watchlist_symbols') as mock_symbols,
         patch('app.data.jobs.ingest_watchlist.fetch_and_save_equity_data') as mock_equity,
         patch('app.data.jobs.ingest_watchlist.fetch_and_save_options_data') as mock_options:
        
        mock_symbols.return_value = ["AAPL"]
        mock_equity.return_value = True
        mock_options.return_value = True
        
        ingest_watchlist_data(retries=1)
        # If we reach here without exception, test passes


def test_ingest_watchlist_data_failure():
    with patch('app.data.jobs.ingest_watchlist.get_watchlist_symbols') as mock_symbols,
         patch('app.data.jobs.ingest_watchlist.fetch_and_save_equity_data') as mock_equity,
         patch('app.data.jobs.ingest_watchlist.fetch_and_save_options_data') as mock_options:
        
        mock_symbols.return_value = ["AAPL"]
        mock_equity.return_value = False
        mock_options.return_value = False
        
        ingest_watchlist_data(retries=1)
        # If we reach here without exception, test passes
