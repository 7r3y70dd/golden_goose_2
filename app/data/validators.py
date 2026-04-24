from typing import Union
from .schemas import EquityBar, OptionsContract


def validate_equity_bar(bar: EquityBar) -> bool:
    try:
        bar.__post_init__()
        return True
    except ValueError:
        return False


def validate_options_contract(contract: OptionsContract) -> bool:
    try:
        contract.__post_init__()
        return True
    except ValueError:
        return False


def validate_market_data(data: Union[EquityBar, OptionsContract]) -> bool:
    if isinstance(data, EquityBar):
        return validate_equity_bar(data)
    elif isinstance(data, OptionsContract):
        return validate_options_contract(data)
    else:
        return False