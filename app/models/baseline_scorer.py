from .base import Scorer
from .types import ScorerOutput
import random


class BaselineScorer(Scorer):
    """
    A simple baseline scorer that returns random scores.
    
    This is a placeholder implementation that conforms to the Scorer interface
    and can be replaced with more sophisticated scoring logic later.
    """
    
    def score(self, data: Any) -> ScorerOutput:
        """
        Compute a random score for the given data.
        
        Args:
            data: Input data for scoring
        
        Returns:
            ScorerOutput containing score, confidence, and explanation
        """
        # In a real implementation, this would process the data
        # and compute meaningful scores, confidence, and explanations
        score = random.uniform(0.0, 1.0)
        confidence = random.uniform(0.0, 1.0)
        explanation = f"Baseline score computed for {type(data).__name__}"
        
        return ScorerOutput(
            score=score,
            confidence=confidence,
            explanation=explanation
        )
