import pytest
from datetime import datetime
from app.data.schemas import EquityBar, OptionsContract, OptionsChain
from app.data.validators import validate_equity_bar, validate_options_contract


def test_equity_bar_schema():
    bar = EquityBar(
        symbol='AAPL',
        timestamp=datetime.now(),
        open=100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000
    )
    assert bar.symbol == 'AAPL'
    assert bar.open == 100.0
    assert bar.volume == 1000


def test_options_contract_schema():
    contract = OptionsContract(
        symbol='AAPL',
        timestamp=datetime.now(),
        strike=100.0,
        expiry=datetime.now(),
        put_call='call',
        bid=1.0,
        ask=1.2,
        last=1.1,
        volume=100,
        open_interest=500,
        iv=0.2
    )
    assert contract.symbol == 'AAPL'
    assert contract.strike == 100.0
    assert contract.put_call == 'call'
    assert contract.iv == 0.2


def test_equity_bar_validation():
    bar = EquityBar(
        symbol='AAPL',
        timestamp=datetime.now(),
        open=100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000
    )
    assert validate_equity_bar(bar) is True


def test_options_contract_validation():
    contract = OptionsContract(
        symbol='AAPL',
        timestamp=datetime.now(),
        strike=100.0,
        expiry=datetime.now(),
        put_call='call',
        bid=1.0,
        ask=1.2,
        last=1.1,
        volume=100,
        open_interest=500,
        iv=0.2
    )
    assert validate_options_contract(contract) is True


def test_invalid_equity_bar_validation():
    bar = EquityBar(
        symbol='AAPL',
        timestamp=datetime.now(),
        open=-100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000
    )
    assert validate_equity_bar(bar) is False


def test_invalid_options_contract_validation():
    contract = OptionsContract(
        symbol='AAPL',
        timestamp=datetime.now(),
        strike=-100.0,
        expiry=datetime.now(),
        put_call='call',
        bid=1.0,
        ask=1.2,
        last=1.1,
        volume=100,
        open_interest=500,
        iv=0.2
    )
    assert validate_options_contract(contract) is False
