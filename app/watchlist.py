import json
from typing import List


class Watchlist:
    def __init__(self, watchlist_path: str):
        self.watchlist_path = watchlist_path

    def load_symbols(self) -> List[str]:
        """Load symbols from watchlist file."""
        try:
            with open(self.watchlist_path, 'r') as f:
                data = json.load(f)
                symbols = data.get('symbols', [])
                # Normalize symbols to uppercase
                normalized_symbols = [symbol.upper() for symbol in symbols]
                # Remove duplicates while preserving order
                seen = set()
                unique_symbols = []
                for symbol in normalized_symbols:
                    if symbol not in seen:
                        seen.add(symbol)
                        unique_symbols.append(symbol)
                return unique_symbols
        except Exception as e:
            print(f"Error loading watchlist: {e}")
            return []

class WatchlistIngestor:
    def __init__(self, watchlist_path: str):
        self.watchlist = Watchlist(watchlist_path)

    def ingest(self) -> List[str]:
        return self.watchlist.load_symbols()