import unittest
from datetime import datetime
from app.backtest.engine import BacktestEngine, BacktestResult
from app.data.schemas import EquityBar


class TestBacktestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BacktestEngine()

    def test_evaluate_predictions(self):
        # Create sample data
        predictions = [
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 1), open=100, high=110, low=95, close=105, volume=1000),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 2), open=105, high=115, low=100, close=110, volume=1200),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 3), open=110, high=120, low=105, close=115, volume=1100),
        ]
        
        actual_outcomes = [
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 1), open=100, high=110, low=95, close=105, volume=1000),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 2), open=105, high=115, low=100, close=110, volume=1200),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 3), open=110, high=120, low=105, close=115, volume=1100),
        ]
        
        result = self.engine.evaluate_predictions(predictions, actual_outcomes)
        
        self.assertIsInstance(result, BacktestResult)
        self.assertEqual(result.total_predictions, 3)
        # Since all predictions match actual outcomes, hit rate should be 1.0
        self.assertEqual(result.hit_rate, 1.0)
        self.assertIsNotNone(result.pnl)

    def test_evaluate_predictions_mixed(self):
        # Create mixed sample data
        predictions = [
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 1), open=100, high=110, low=95, close=105, volume=1000),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 2), open=105, high=115, low=100, close=110, volume=1200),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 3), open=110, high=120, low=105, close=115, volume=1100),
        ]
        
        actual_outcomes = [
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 1), open=100, high=110, low=95, close=105, volume=1000),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 2), open=105, high=115, low=100, close=100, volume=1200),
            EquityBar(symbol="AAPL", timestamp=datetime(2023, 1, 3), open=110, high=120, low=105, close=115, volume=1100),
        ]
        
        result = self.engine.evaluate_predictions(predictions, actual_outcomes)
        
        self.assertIsInstance(result, BacktestResult)
        self.assertEqual(result.total_predictions, 3)
        # Only first and third predictions match actual outcomes
        self.assertEqual(result.hit_rate, 2/3)
        self.assertIsNotNone(result.pnl)

    def test_evaluate_predictions_empty(self):
        # Test with empty lists
        result = self.engine.evaluate_predictions([], [])
        
        self.assertIsInstance(result, BacktestResult)
        self.assertEqual(result.total_predictions, 0)
        self.assertEqual(result.hit_rate, 0.0)
        self.assertIsNone(result.pnl)


n__main__ == "__test__":
    unittest.main()