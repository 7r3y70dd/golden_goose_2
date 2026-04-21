import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class Alert:
    def __init__(self, symbol: str, rule_type: str, message: str, timestamp: datetime = None):
        self.symbol = symbol
        self.rule_type = rule_type
        self.message = message
        self.timestamp = timestamp or datetime.utcnow()
        self.id = f"{symbol}_{rule_type}_{self.timestamp.isoformat()}"


class AlertManager:
    def __init__(self, cooldown_minutes: int = 5):
        self.cooldown_minutes = cooldown_minutes
        self.alert_cooldowns = {}
        self.alerts_history = []

    def should_alert(self, alert: Alert) -> bool:
        """Check if alert should be triggered based on cooldown logic."""
        if alert.id in self.alert_cooldowns:
            last_alert_time = self.alert_cooldowns[alert.id]
            if datetime.utcnow() - last_alert_time < timedelta(minutes=self.cooldown_minutes):
                return False
        
        self.alert_cooldowns[alert.id] = datetime.utcnow()
        return True

    def add_alert(self, alert: Alert) -> None:
        """Add alert to history and trigger notification if not suppressed."""
        if self.should_alert(alert):
            self.alerts_history.append(alert)
            self._notify(alert)
        else:
            logger.debug(f"Alert suppressed due to cooldown: {alert.id}")

    def _notify(self, alert: Alert) -> None:
        """Handle notification delivery - can be extended for email/webhook."""
        logger.info(f"ALERT: {alert.symbol} - {alert.rule_type}: {alert.message}")
        # In future versions, this could send email or webhook payloads


class NotificationPayload:
    def __init__(self, alert: Alert):
        self.alert = alert
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert.id,
            "symbol": self.alert.symbol,
            "rule_type": self.alert.rule_type,
            "message": self.alert.message,
            "timestamp": self.timestamp
        }

    def to_email_payload(self) -> Dict[str, Any]:
        """Format for email delivery."""
        return {
            "subject": f"Option Alert: {self.alert.symbol}",
            "body": f"{self.alert.rule_type}: {self.alert.message}"
        }

    def to_webhook_payload(self) -> Dict[str, Any]:
        """Format for webhook delivery."""
        return self.to_dict()