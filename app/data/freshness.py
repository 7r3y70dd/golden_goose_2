import datetime
from typing import Optional, Dict, Any

# Default freshness thresholds in minutes
DEFAULT_FRESHNESS_THRESHOLDS = {
    'options': 10,
    'price': 10,
    'fundamentals': 1440,  # 24 hours
    'news': 1440,
}



def is_data_fresh(
    last_updated: Optional[datetime.datetime],
    threshold_minutes: int = DEFAULT_FRESHNESS_THRESHOLDS['options']
) -> bool:
    """
    Check if the data is fresh based on the last updated timestamp.

    Args:
        last_updated: The timestamp when the data was last updated.
        threshold_minutes: The maximum allowed age of data in minutes.

    Returns:
        True if data is fresh, False otherwise.
    """
    if last_updated is None:
        return False

    now = datetime.datetime.now(datetime.timezone.utc)
    age = (now - last_updated).total_seconds() / 60
    return age <= threshold_minutes


def get_freshness_status(
    last_updated: Optional[datetime.datetime],
    threshold_minutes: int = DEFAULT_FRESHNESS_THRESHOLDS['options']
) -> Dict[str, Any]:
    """
    Get detailed freshness status including state and age.

    Args:
        last_updated: The timestamp when the data was last updated.
        threshold_minutes: The maximum allowed age of data in minutes.

    Returns:
        Dictionary with freshness status information.
    """
    if last_updated is None:
        return {
            'is_fresh': False,
            'state': 'stale',
            'age_minutes': None,
            'message': 'No data available'
        }

    now = datetime.datetime.now(datetime.timezone.utc)
    age = (now - last_updated).total_seconds() / 60
    
    if age <= threshold_minutes:
        state = 'fresh'
        message = f'Data is fresh (age: {age:.1f} minutes)'
    elif age <= threshold_minutes * 2:
        state = 'warning'
        message = f'Data is approaching stale (age: {age:.1f} minutes)'
    else:
        state = 'stale'
        message = f'Data is stale (age: {age:.1f} minutes)'

    return {
        'is_fresh': age <= threshold_minutes,
        'state': state,
        'age_minutes': age,
        'message': message
    }


class FreshnessError(Exception):
    """Custom exception raised when data is stale."""
    pass


def is_data_stale(data_freshness: Dict[str, Any]) -> bool:
    """
    Check if data is stale based on freshness metadata.

    Args:
        data_freshness: Dictionary containing freshness information.

    Returns:
        True if data is stale, False otherwise.
    """
    if not data_freshness:
        return True
    
    return not data_freshness.get('is_fresh', False)


def get_freshness_thresholds() -> Dict[str, int]:
    """
    Get all configured freshness thresholds.

    Returns:
        Dictionary of thresholds by data type.
    """
    return DEFAULT_FRESHNESS_THRESHOLDS.copy()