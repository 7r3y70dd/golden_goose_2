from typing import TypedDict, Optional
from dataclasses import dataclass


class ScorerOutput(TypedDict):
    score: float
    confidence: Optional[float]
    explanation: Optional[str]


class ScorerMetadata(TypedDict):
    score: float
    confidence: Optional[float]
    explanation: Optional[str]
