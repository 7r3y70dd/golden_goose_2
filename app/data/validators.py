from typing import Optional
from .schemas import EquityBar, OptionsContract


def validate_equity_bar(bar: EquityBar) -> bool:
    if bar.open < 0 or bar.high < 0 or bar.low < 0 or bar.close < 0:
        return False
    if bar.volume < 0:
        return False
    return True


def validate_options_contract(contract: OptionsContract) -> bool:
    if contract.strike < 0:
        return False
    if contract.volume < 0:
        return False
    if contract.open_interest < 0:
        return False
    if contract.put_call not in ['call', 'put']:
        return False
    if contract.bid is not None and contract.bid < 0:
        return False
    if contract.ask is not None and contract.ask < 0:
        return False
    if contract.iv is not None and contract.iv < 0:
        return False
    return True
