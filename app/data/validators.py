from typing import Any
from pydantic import ValidationError
from .schemas import EquityBar, OptionsContract, OptionsChain

def validate_equity_bar(data: Any) -> EquityBar:
    try:
        return EquityBar(**data)
    except ValidationError as e:
        raise ValueError(f'Invalid equity bar data: {e}')

def validate_options_contract(data: Any) -> OptionsContract:
    try:
        return OptionsContract(**data)
    except ValidationError as e:
        raise ValueError(f'Invalid options contract data: {e}')

def validate_options_chain(data: Any) -> OptionsChain:
    try:
        return OptionsChain(**data)
    except ValidationError as e:
        raise ValueError(f'Invalid options chain data: {e}')
