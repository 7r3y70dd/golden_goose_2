from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from .types import ScorerOutput


class Scorer(ABC):
    """
    Abstract base class for all scorers in the application.
    
    This interface ensures that all scorers provide consistent
    score, confidence, and explanation outputs.
    """
    
    @abstractmethod
    def score(self, data: Any) -> ScorerOutput:
        """
        Compute a score for the given data.
        
        Args:
            data: Input data for scoring
        
        Returns:
            ScorerOutput containing score, confidence, and explanation
        """
        pass
