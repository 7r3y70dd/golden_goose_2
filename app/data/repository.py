import logging
from pathlib import Path
from typing import List, Optional

import pandas as pd

from app.data.schemas import EquityBar, OptionContract

logger = logging.getLogger(__name__)


class DataRepository:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_historical_bars(self, symbol: str, bars: List[EquityBar]) -> None:
        """Save historical bars to parquet file."""
        if not bars:
            logger.warning(f"No bars to save for {symbol}")
            return

        df = pd.DataFrame([bar.dict() for bar in bars])
        file_path = self.data_dir / f"{symbol}_bars.parquet"
        df.to_parquet(file_path, index=False)
        logger.info(f"Saved {len(bars)} bars for {symbol}")

    def save_options_chain(self, symbol: str, options_chain: List[OptionContract]) -> None:
        """Save options chain to parquet file."""
        if not options_chain:
            logger.warning(f"No options to save for {symbol}")
            return

        df = pd.DataFrame([option.dict() for option in options_chain])
        file_path = self.data_dir / f"{symbol}_options.parquet"
        df.to_parquet(file_path, index=False)
        logger.info(f"Saved {len(options_chain)} options for {symbol}")

    def load_historical_bars(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[EquityBar]:
        """Load historical bars from parquet file."""
        file_path = self.data_dir / f"{symbol}_bars.parquet"
        if not file_path.exists():
            logger.warning(f"No bars found for {symbol}")
            return []

        df = pd.read_parquet(file_path)
        # Convert back to EquityBar objects
        return [EquityBar(**row) for _, row in df.iterrows()]

    def load_options_chain(self, symbol: str) -> List[OptionContract]:
        """Load options chain from parquet file."""
        file_path = self.data_dir / f"{symbol}_options.parquet"
        if not file_path.exists():
            logger.warning(f"No options found for {symbol}")
            return []

        df = pd.read_parquet(file_path)
        # Convert back to OptionContract objects
        return [OptionContract(**row) for _, row in df.iterrows()]