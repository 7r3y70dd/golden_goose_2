from dataclasses import dataclass
from typing import Dict, Any, List, Union
from enum import Enum
import uuid
from datetime import datetime


class ExplanationType(str, Enum):
    BEARISH = "bearish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"


class Explanation:
    type: ExplanationType
    short: str
    detailed: str = ""
    fields: Dict[str, Union[str, int, float]] = None
    metadata: Dict[str, Any] = None
    # New fields for richer explanations
    top_positive_contributors: List[str] = None
    top_negative_contributors: List[str] = None
    liquidity_notes: List[str] = None
    event_risk_notes: List[str] = None
    volatility_notes: List[str] = None
    expiration_selection_rationale: str = ""


def generate_run_metadata() -> Dict[str, Any]:
    """Generate run metadata including unique identifier and timestamp."""
    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat()
    }


def generate_bearish_explanation(
    triggered_rules: List[str],
    features: Dict[str, Union[int, float]],
    score: float,
    hard_exclusions: List[str] = None,
    soft_penalties: List[str] = None
) -> Explanation:
    """Generate a concise bearish explanation from triggered rules and features."""
    if hard_exclusions:
        short = f"Hard exclusion due to: {', '.join(hard_exclusions)}"
    elif soft_penalties:
        short = f"Soft penalties: {', '.join(soft_penalties)}"
    elif "price_drop" in triggered_rules:
        short = "Price dropped significantly"
    elif "volume_spike" in triggered_rules and "price_drop" in triggered_rules:
        short = "Volume spike with price drop"
    else:
        short = "Multiple bearish indicators detected"

    detailed = f"Score: {score:.2f}. Triggered rules: {', '.join(triggered_rules)}."
    if hard_exclusions:
        detailed += f" Hard exclusions: {', '.join(hard_exclusions)}."
    if soft_penalties:
        detailed += f" Soft penalties: {', '.join(soft_penalties)} ."

    fields = {
        "score": score,
        "triggered_rules": triggered_rules,
        "features": features,
        "hard_exclusions": hard_exclusions or [],
        "soft_penalties": soft_penalties or []
    }

    metadata = generate_run_metadata()

    # Richer explanation fields
    top_positive_contributors = []
    top_negative_contributors = [
        "Price drop",
        "Volume spike",
        "High volatility"
    ]
    liquidity_notes = [
        "Low liquidity in underlying",
        "High bid-ask spread"
    ]
    event_risk_notes = [
        "Earnings announcement approaching",
        "Dividend payment expected"
    ]
    volatility_notes = [
        "Implied volatility spike",
        "Historical volatility above average"
    ]
    expiration_selection_rationale = "Short-term expirations preferred for higher gamma exposure"

    return Explanation(
        type=ExplanationType.BEARISH,
        short=short,
        detailed=detailed,
        fields=fields,
        metadata=metadata,
        top_positive_contributors=top_positive_contributors,
        top_negative_contributors=top_negative_contributors,
        liquidity_notes=liquidity_notes,
        event_risk_notes=event_risk_notes,
        volatility_notes=volatility_notes,
        expiration_selection_rationale=expiration_selection_rationale
    )


def generate_explanation(
    triggered_rules: List[str],
    features: Dict[str, Union[int, float]],
    score: float,
    hard_exclusions: List[str] = None,
    soft_penalties: List[str] = None
) -> Explanation:
    """Main entry point for generating explanations."""
    return generate_bearish_explanation(triggered_rules, features, score, hard_exclusions, soft_penalties)
