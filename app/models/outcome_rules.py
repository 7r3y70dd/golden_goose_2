from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Union

class OutcomeStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"

@dataclass
class OutcomeRule:
    """Configuration for outcome evaluation rules."""
    target_stock_move: Optional[float] = None  # e.g., 0.05 for 5% move
    target_option_return: Optional[float] = None  # e.g., 0.1 for 10% return
    max_holding_period: Optional[int] = None  # in days
    stop_loss_percentage: Optional[float] = None  # e.g., -0.1 for 10% stop loss
    expiration_based_failure: bool = False

@dataclass
class OutcomeEvaluation:
    """Result of outcome evaluation."""
    status: OutcomeStatus
    reason: Optional[str] = None
    timestamp: Optional[datetime] = None


def evaluate_outcome(
    trade_data: dict,
    rule: OutcomeRule,
    current_time: datetime,
    expiration_date: datetime,
    stock_price_history: list,
    option_price_history: list
) -> OutcomeEvaluation:
    """Evaluate if a trade has succeeded or failed based on configured rules."""
    # Check if enough time has passed for evaluation
    if rule.max_holding_period is not None:
        holding_period = (current_time - trade_data['entry_time']).days
        if holding_period < rule.max_holding_period:
            return OutcomeEvaluation(
                status=OutcomeStatus.PENDING,
                reason="Holding period not yet complete"
            )

    # Check expiration
    if rule.expiration_based_failure and current_time >= expiration_date:
        return OutcomeEvaluation(
            status=OutcomeStatus.FAILURE,
            reason="Trade expired without meeting criteria"
        )

    # Check stock move
    if rule.target_stock_move is not None:
        # Simplified: compare entry stock price to current price
        entry_price = trade_data.get('entry_stock_price')
        current_price = stock_price_history[-1] if stock_price_history else None
        if current_price and entry_price:
            stock_move = (current_price - entry_price) / entry_price
            if stock_move >= rule.target_stock_move:
                return OutcomeEvaluation(
                    status=OutcomeStatus.SUCCESS,
                    reason="Target stock move achieved"
                )
            elif stock_move < 0 and rule.stop_loss_percentage is not None:
                if stock_move <= rule.stop_loss_percentage:
                    return OutcomeEvaluation(
                        status=OutcomeStatus.FAILURE,
                        reason="Stop loss triggered"
                    )

    # Check option return
    if rule.target_option_return is not None:
        entry_option_price = trade_data.get('entry_option_price')
        current_option_price = option_price_history[-1] if option_price_history else None
        if current_option_price and entry_option_price:
            option_return = (current_option_price - entry_option_price) / entry_option_price
            if option_return >= rule.target_option_return:
                return OutcomeEvaluation(
                    status=OutcomeStatus.SUCCESS,
                    reason="Target option return achieved"
                )

    # Default to failure if no criteria met
    return OutcomeEvaluation(
        status=OutcomeStatus.FAILURE,
        reason="No success criteria met"
    )