import pytest
from datetime import datetime
from app.data.schemas import EquityBar, OptionsContract
from app.data.validators import validate_equity_bar, validate_options_contract


def test_equity_bar_valid_data():
    bar = EquityBar(
        symbol="AAPL",
        timestamp=datetime.now(),
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume=1000000
    )
    assert validate_equity_bar(bar) is True


def test_equity_bar_invalid_ohlc():
    with pytest.raises(ValueError):
        bar = EquityBar(
            symbol="AAPL",
            timestamp=datetime.now(),
            open=-10.0,
            high=155.0,
            low=149.0,
            close=154.0,
            volume=1000000
        )


def test_equity_bar_invalid_low_high():
    with pytest.raises(ValueError):
        bar = EquityBar(
            symbol="AAPL",
            timestamp=datetime.now(),
            open=150.0,
            high=145.0,
            low=149.0,
            close=154.0,
            volume=1000000
        )


def test_options_contract_valid_data():
    contract = OptionsContract(
        symbol="AAPL230101C00150000",
        timestamp=datetime.now(),
        strike=150.0,
        expiry=datetime.now(),
        put_call="call",
        bid=2.5,
        ask=2.7,
        last=2.6,
        volume=1000,
        open_interest=500,
        iv=0.2
    )
    assert validate_options_contract(contract) is True


def test_options_contract_invalid_strike():
    with pytest.raises(ValueError):
        contract = OptionsContract(
            symbol="AAPL230101C00150000",
            timestamp=datetime.now(),
            strike=-10.0,
            expiry=datetime.now(),
            put_call="call",
            bid=2.5,
            ask=2.7,
            last=2.6,
            volume=1000,
            open_interest=500,
            iv=0.2
        )


def test_options_contract_invalid_put_call():
    with pytest.raises(ValueError):
        contract = OptionsContract(
            symbol="AAPL230101C00150000",
            timestamp=datetime.now(),
            strike=150.0,
            expiry=datetime.now(),
            put_call="forward",
            bid=2.5,
            ask=2.7,
            last=2.6,
            volume=1000,
            open_interest=500,
            iv=0.2
        )