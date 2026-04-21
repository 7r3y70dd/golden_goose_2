from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union


class Scorer(ABC):
    """Abstract base class for model scorers."""

    @abstractmethod
    def score(self, data: Any) -> float:
        """Calculate and return a score for the given data."""
        pass

    @abstractmethod
    def confidence(self, data: Any) -> float:
        """Return confidence level of the score."""
        pass

    @abstractmethod
    def explanation(self, data: Any) -> Dict[str, Any]:
        """Return explanation of the score calculation."""
        pass
