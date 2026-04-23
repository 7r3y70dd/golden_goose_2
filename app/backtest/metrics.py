from typing import List, Tuple
import math


def calculate_hit_rate(predictions: List[bool], actual_outcomes: List[bool]) -> float:
    """
    Calculate hit rate (accuracy) of predictions.
    
    Args:
        predictions: List of boolean predictions (True for bullish, False for bearish)
        actual_outcomes: List of boolean actual outcomes (True for bullish, False for bearish)
        
    Returns:
        Hit rate as a float between 0 and 1
    """
    if len(predictions) != len(actual_outcomes):
        raise ValueError("Predictions and outcomes must have the same length")
    
    if len(predictions) == 0:
        return 0.0
    
    hits = sum(1 for pred, actual in zip(predictions, actual_outcomes) if pred == actual)
    return hits / len(predictions)


def calculate_precision_recall(predictions: List[bool], actual_outcomes: List[bool]) -> Tuple[float, float]:
    """
    Calculate precision and recall metrics.
    
    Args:
        predictions: List of boolean predictions (True for bullish, False for bearish)
        actual_outcomes: List of boolean actual outcomes (True for bullish, False for bearish)
        
    Returns:
        Tuple of (precision, recall)
    """
    if len(predictions) != len(actual_outcomes):
        raise ValueError("Predictions and outcomes must have the same length")
    
    if len(predictions) == 0:
        return 0.0, 0.0
    
    true_positives = sum(1 for pred, actual in zip(predictions, actual_outcomes) if pred and actual)
    false_positives = sum(1 for pred, actual in zip(predictions, actual_outcomes) if pred and not actual)
    false_negatives = sum(1 for pred, actual in zip(predictions, actual_outcomes) if not pred and actual)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    
    return precision, recall


def calculate_simple_pnl(predictions: List[bool], actual_outcomes: List[bool]) -> float:
    """
    Calculate simple PnL based on prediction accuracy.
    
    Args:
        predictions: List of boolean predictions (True for bullish, False for bearish)
        actual_outcomes: List of boolean actual outcomes (True for bullish, False for bearish)
        
    Returns:
        Total PnL as a float
    """
    if len(predictions) != len(actual_outcomes):
        raise ValueError("Predictions and outcomes must have the same length")
    
    total_pnl = 0.0
    
    for pred, actual in zip(predictions, actual_outcomes):
        if pred == actual:
            # Correct prediction
            total_pnl += 1.0  # Simplified gain
        else:
            # Incorrect prediction
            total_pnl -= 1.0  # Simplified loss
    
    return total_pnl