from typing import List, Optional, Dict, Any
from app.data.repository import DataRepository
from app.models.tracked_trade import TrackedTrade
from app.models.outcome_rules import evaluate_outcome
import logging

logger = logging.getLogger(__name__)


def refresh_tracked_trades(
    repository: DataRepository,
    unresolved_only: bool = True,
    min_age_days: Optional[int] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Refresh tracked trade outcomes for eligible trades.
    
    Args:
        repository: Data repository instance
        unresolved_only: If True, only refresh unresolved trades
        min_age_days: Minimum age in days for trades to be refreshed
        dry_run: If True, don't persist changes
    
    Returns:
        Dictionary with refresh results
    """
    logger.info("Starting tracked trade refresh")
    
    # Get eligible trades
    trades = repository.get_unresolved_tracked_trades() if unresolved_only else repository.get_tracked_trades()
    
    # Apply age filter if specified
    if min_age_days is not None:
        # This is a placeholder - in a real implementation, you'd need to calculate
        # the age based on timestamps
        pass
    
    updated_count = 0
    skipped_count = 0
    failed_count = 0
    
    for trade in trades:
        try:
            # Create TrackedTrade object from dict
            tracked_trade = TrackedTrade(**trade)
            
            # Evaluate outcome
            new_resolution = evaluate_outcome(tracked_trade)
            
            if new_resolution != tracked_trade.resolution:
                # Update the trade
                updated_trade = {
                    **trade,
                    'resolution': new_resolution,
                    'resolution_time': '2023-01-01T00:00:00Z'  # Placeholder timestamp
                }
                
                if not dry_run:
                    repository.save_tracked_trade(updated_trade)
                
                updated_count += 1
            else:
                skipped_count += 1
                
        except Exception as e:
            logger.error(f"Failed to refresh trade {trade.get('trade_id', 'unknown')}: {str(e)}")
            failed_count += 1
    
    logger.info(f"Tracked trade refresh completed. Updated: {updated_count}, Skipped: {skipped_count}, Failed: {failed_count}")
    
    return {
        'updated': updated_count,
        'skipped': skipped_count,
        'failed': failed_count,
        'total_processed': len(trades)
    }