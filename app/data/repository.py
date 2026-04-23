import json
from typing import List, Dict
from app.data.schemas import EquityBar, OptionsChain


def save_equity_data(equity_data: EquityBar):
    """
    Save equity data to a persistent storage (e.g., file or database).
    """
    # In a real implementation, this would save to a database or file
    print(f"Saving equity data: {equity_data.__dict__}")


def save_options_data(options_data: List[OptionsChain]):
    """
    Save options data to a persistent storage (e.g., file or database).
    """
    # In a real implementation, this would save to a database or file
    print(f"Saving options data: {options_data}")
