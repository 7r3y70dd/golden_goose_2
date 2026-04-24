import json
from pathlib import Path
from typing import List

WATCHLIST_FILE = Path("watchlist.json")


def load_watchlist() -> List[str]:
    """Load watchlist symbols from file."""
    if not WATCHLIST_FILE.exists():
        return []

    with open(WATCHLIST_FILE, "r") as f:
        data = json.load(f)
        return data.get("symbols", [])