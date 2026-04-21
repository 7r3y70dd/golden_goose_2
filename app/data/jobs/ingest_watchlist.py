import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from app.alerts.notifications import AlertManager, Alert

logger = logging.getLogger(__name__)


# Initialize alert manager
alert_manager = AlertManager(cooldown_minutes=5)


def generate_run_metadata() -> Dict[str, Any]:
    """Generate run metadata including unique identifier and timestamp."""
    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat()
    }


def log_with_metadata(message: str, metadata: Dict[str, Any]) -> None:
    """Log message with run metadata."""
    logger.info(f"{message} - Run ID: {metadata['run_id']}")


def evaluate_watchlist_alerts(watchlist_symbols: list) -> None:
    """Evaluate watchlist symbols for alert conditions."""
    # Example alert conditions - can be extended
    for symbol in watchlist_symbols:
        # Simulate alert conditions
        if symbol == "AAPL":
            alert = Alert(symbol, "score_threshold", "Score crossed 0.8 threshold")
            alert_manager.add_alert(alert)
        elif symbol == "MSFT":
            alert = Alert(symbol, "volatility_spike", "Implied volatility spiked above 2.0")
            alert_manager.add_alert(alert)
        elif symbol == "GOOGL":
            alert = Alert(symbol, "unusual_volume", "Unusual volume detected")
            alert_manager.add_alert(alert)