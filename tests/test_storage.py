import os
import tempfile
from datetime import datetime
from app.data.schemas import EquityBar, OptionsContract
from app.data.storage import MarketDataStorage


def test_save_and_load_bars():
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = MarketDataStorage(temp_dir)
        
        # Create sample bars
        bars = [
            EquityBar(
                symbol="AAPL",
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                high=105.0,
                low=95.0,
                close=102.0,
                volume=1000000
            ),
            EquityBar(
                symbol="AAPL",
                timestamp=datetime(2023, 1, 2),
                open=102.0,
                high=107.0,
                low=98.0,
                close=105.0,
                volume=1200000
            )
        ]
        
        # Save bars
        storage.save_bars("AAPL", bars)
        
        # Load bars
        loaded_bars = storage.load_bars("AAPL")
        
        # Verify
        assert len(loaded_bars) == 2
        assert loaded_bars[0].close == 102.0
        assert loaded_bars[1].close == 105.0
        
        # Test with date filters
        filtered_bars = storage.load_bars("AAPL", start_date=datetime(2023, 1, 2))
        assert len(filtered_bars) == 1
        assert filtered_bars[0].timestamp == datetime(2023, 1, 2)
        

def test_save_and_load_options():
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = MarketDataStorage(temp_dir)
        
        # Create sample options
        options = [
            OptionsContract(
                symbol="AAPL",
                timestamp=datetime(2023, 1, 1),
                strike=100.0,
                expiry=datetime(2023, 2, 1),
                put_call="call",
                bid=1.5,
                ask=1.7,
                last=1.6,
                volume=1000,
                open_interest=500,
                iv=0.2
            ),
            OptionsContract(
                symbol="AAPL",
                timestamp=datetime(2023, 1, 1),
                strike=105.0,
                expiry=datetime(2023, 2, 1),
                put_call="put",
                bid=0.8,
                ask=1.0,
                last=0.9,
                volume=800,
                open_interest=400,
                iv=0.15
            )
        ]
        
        # Save options
        storage.save_options("AAPL", options)
        
        # Load options
        loaded_options = storage.load_options("AAPL")
        
        # Verify
        assert len(loaded_options) == 2
        assert loaded_options[0].strike == 100.0
        assert loaded_options[1].strike == 105.0
        assert loaded_options[0].put_call == "call"
        assert loaded_options[1].put_call == "put"
        
        # Test with date filters
        filtered_options = storage.load_options("AAPL", start_date=datetime(2023, 1, 2))
        assert len(filtered_options) == 0