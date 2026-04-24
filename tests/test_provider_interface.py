import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.data.providers.base import MarketDataProvider
from app.data.providers.mock import MockMarketDataProvider
from app.data.schemas import EquityBar, OptionsContract


class TestMarketDataProviderInterface(unittest.TestCase):
    def setUp(self):
        self.provider = MockMarketDataProvider()

    def test_interface_is_abstract(self):
        # Verify that the base class cannot be instantiated
        with self.assertRaises(TypeError):
            MarketDataProvider()

    def test_get_latest_quote_returns_equity_bar(self):
        result = self.provider.get_latest_quote("AAPL")
        self.assertIsInstance(result, EquityBar)
        self.assertEqual(result.symbol, "AAPL")

    def test_get_historical_bars_returns_list_of_equity_bars(self):
        start_date = datetime.now() - timedelta(days=5)
        end_date = datetime.now()
        result = self.provider.get_historical_bars("AAPL", start_date, end_date)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], EquityBar)

    def test_get_options_chain_returns_list_of_options_contracts(self):
        result = self.provider.get_options_chain("AAPL")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], OptionsContract)

    def test_get_options_chain_with_expiration_filter(self):
        expiration = datetime.now() + timedelta(days=30)
        result = self.provider.get_options_chain("AAPL", expiration)
        self.assertIsInstance(result, list)
        # Mock implementation doesn't filter by expiration, but should still return valid data
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], OptionsContract)


if __name__ == '__main__':
    unittest.main()