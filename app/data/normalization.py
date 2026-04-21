from typing import Dict, Any
from .schemas import EquityBar, OptionsContract, OptionsChain
from .validators import validate_equity_bar, validate_options_contract, validate_options_chain


def normalize_equity_bar(provider_data: Dict[str, Any]) -> EquityBar:
    """Normalize provider equity bar data to internal schema."""
    # Example mapping: provider field 'o' -> internal 'open'
    normalized_data = {
        'symbol': provider_data.get('symbol'),
        'timestamp': provider_data.get('timestamp'),
        'open': provider_data.get('o'),
        'high': provider_data.get('h'),
        'low': provider_data.get('l'),
        'close': provider_data.get('c'),
        'volume': provider_data.get('v')
    }
    return validate_equity_bar(normalized_data)


def normalize_options_contract(provider_data: Dict[str, Any]) -> OptionsContract:
    """Normalize provider options contract data to internal schema."""
    normalized_data = {
        'symbol': provider_data.get('symbol'),
        'timestamp': provider_data.get('timestamp'),
        'strike': provider_data.get('strike'),
        'expiry': provider_data.get('expiry'),
        'put_call': provider_data.get('put_call'),
        'bid': provider_data.get('bid'),
        'ask': provider_data.get('ask'),
        'last': provider_data.get('last'),
        'volume': provider_data.get('volume'),
        'open_interest': provider_data.get('open_interest'),
        'iv': provider_data.get('iv')
    }
    return validate_options_contract(normalized_data)


def normalize_options_chain(provider_data: Dict[str, Any]) -> OptionsChain:
    """Normalize provider options chain data to internal schema."""
    normalized_contracts = [
        normalize_options_contract(contract) for contract in provider_data.get('contracts', [])
    ]
    normalized_data = {
        'symbol': provider_data.get('symbol'),
        'timestamp': provider_data.get('timestamp'),
        'contracts': normalized_contracts
    }
    return validate_options_chain(normalized_data)