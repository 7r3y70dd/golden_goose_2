from typing import Dict, Any, List
from datetime import datetime
from app.models.types import Trade


@dataclass
class BacktestMetrics:
    hit_rate: float
    precision: float
    recall: float
    pnl: float
    mse: float
    rmse: float
    mae: float
    mape: float


def calculate_hit_rate(predictions: pd.Series, outcomes: pd.Series) -> float:
    return (predictions == outcomes).mean()

def calculate_precision(predictions: pd.Series, outcomes: pd.Series) -> float:
    tp = (predictions == 1) & (outcomes == 1)
    fp = (predictions == 1) & (outcomes == 0)
    return tp.sum() / (tp.sum() + fp.sum()) if (tp.sum() + fp.sum()) > 0 else 0

def calculate_recall(predictions: pd.Series, outcomes: pd.Series) -> float:
    tp = (predictions == 1) & (outcomes == 1)
    fn = (predictions == 0) & (outcomes == 1)
    return tp.sum() / (tp.sum() + fn.sum()) if (tp.sum() + fn.sum()) > 0 else 0

def calculate_pnl(predictions: pd.Series, outcomes: pd.Series) -> float:
    return (predictions * outcomes).sum() - ((1 - predictions) * outcomes).sum()


def evaluate_rolling_metrics(predictions: pd.DataFrame, outcomes: pd.DataFrame, window_size: int = 5):
    # Merge predictions and outcomes on date
    data = pd.merge(predictions, outcomes, on='date', how='inner')

    # Calculate rolling metrics
    data['hit_rate'] = calculate_hit_rate(data['prediction'], data['outcome'])
    data['hit_rate'] = data['hit_rate'].rolling(window=window_size).mean()

    # Precision
    precision = calculate_precision(data['prediction'], data['outcome'])
    data['precision'] = precision.rolling(window=window_size).mean()

    # Recall
    recall = calculate_recall(data['prediction'], data['outcome'])
    data['recall'] = recall.rolling(window=window_size).mean()

    # PnL
    pnl = calculate_pnl(data['prediction'], data['outcome'])
    data['pnl'] = pnl.rolling(window=window_size).sum()

    return data[['date', 'hit_rate', 'precision', 'recall', 'pnl']]


def calculate_performance_summary(tracked_trades: List[dict]) -> Dict[str, Any]:
    """Calculate performance summary from tracked trades."""
    if not tracked_trades:
        return {
            'total_trades': 0,
            'resolved_trades': 0,
            'unresolved_trades': 0,
            'success_rate': 0.0,
            'average pnl': 0.0,
            'total_pnl': 0.0,
            'by_strategy': {},
            'by_score_bucket': {}
        }

    total_trades = len(tracked_trades)
    resolved_trades = [trade for trade in tracked_trades if trade.get('resolution') is not None]
    unresolved_trades = [trade for trade in tracked_trades if trade.get('resolution') is None]
    
    success_rate = len(resolved_trades) / total_trades if total_trades > 0 else 0.0
    
    total_pnl = sum(trade.get('pnl', 0) for trade in resolved_trades)
    average_pnl = total_pnl / len(resolved_trades) if resolved_trades else 0.0
    
    # Group by strategy
    by_strategy = {}
    for trade in resolved_trades:
        strategy = trade.get('strategy', 'unknown')
        if strategy not in by_strategy:
            by_strategy[strategy] = {'count': 0, 'total_pnl': 0.0, 'total_success': 0}
        by_strategy[strategy]['count'] += 1
        by_strategy[strategy]['total_pnl'] += trade.get('pnl', 0)
        if trade.get('resolution') == 1:
            by_strategy[strategy]['total_success'] += 1
    
    # Group by score bucket
    by_score_bucket = {}
    for trade in resolved_trades:
        score = trade.get('score', 0)
        bucket = f'{int(score // 0.1) * 0.1:.1f}'  # Group by 0.1 buckets
        if bucket not in by_score_bucket:
            by_score_bucket[bucket] = {'count': 0, 'total_pnl': 0.0, 'total_success': 0}
        by_score_bucket[bucket]['count'] += 1
        by_score_bucket[bucket]['total_pnl'] += trade.get('pnl', 0)
        if trade.get('resolution') == 1:
            by_score_bucket[bucket]['total_success'] += 1
    
    # Calculate success rate by bucket
    for bucket in by_score_bucket:
        total = by_score_bucket[bucket]['count']
        success = by_score_bucket[bucket]['total_success']
        by_score_bucket[bucket]['success_rate'] = success / total if total > 0 else 0
    
    return {
        'total_trades': total_trades,
        'resolved_trades': len(resolved_trades),
        'unresolved_trades': len(unresolved_trades),
        'success_rate': success_rate,
        'average pnl': average_pnl,
        'total_pnl': total_pnl,
        'by_strategy': by_strategy,
        'by_score_bucket': by_score_bucket
    }


def calculate_time_to_resolution(tracked_trades: List[dict]) -> Dict[str, Any]:
    """Calculate time to resolution statistics."""
    if not tracked_trades:
        return {}
    
    # Filter only resolved trades
    resolved_trades = [trade for trade in tracked_trades if trade.get('resolution') is not None]
    
    if not resolved_trades:
        return {}
    
    # Calculate time to resolution (assuming timestamps are in ISO format)
    import datetime
    time_differences = []
    
    for trade in resolved_trades:
        timestamp = trade.get('timestamp')
        resolution_time = trade.get('resolution_time')
        
        if timestamp and resolution_time:
            try:
                ts = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                rt = datetime.datetime.fromisoformat(resolution_time.replace('Z', '+00:00'))
                diff = rt - ts
                time_differences.append(diff.total_seconds() / 3600)  # Convert to hours
            except ValueError:
                continue  # Skip invalid timestamps
    
    if not time_differences:
        return {}
    
    return {
        'avg_hours_to_resolution': sum(time_differences) / len(time_differences),
        'min_hours_to_resolution': min(time_differences),
        'max_hours_to_resolution': max(time_differences)
    }


def calculate_score_bucket_metrics(tracked_trades: List[dict]) -> Dict[str, Any]:
    """Calculate detailed metrics by score bucket including success rates and time to resolution."""
    if not tracked_trades:
        return {}
    
    # Filter only resolved trades
    resolved_trades = [trade for trade in tracked_trades if trade.get('resolution') is not None]
    
    if not resolved_trades:
        return {}
    
    # Group by score bucket
    by_score_bucket = {}
    time_differences = []
    
    for trade in resolved_trades:
        score = trade.get('score', 0)
        bucket = f'{int(score // 0.1) * 0.1:.1f}'  # Group by 0.1 buckets
        
        if bucket not in by_score_bucket:
            by_score_bucket[bucket] = {
                'count': 0,
                'total_pnl': 0.0,
                'total_success': 0,
                'success_rate': 0.0,
                'total_time_to_resolution': 0.0,
                'time_to_resolution_count': 0
            }
        
        by_score_bucket[bucket]['count'] += 1
        by_score_bucket[bucket]['total_pnl'] += trade.get('pnl', 0)
        
        if trade.get('resolution') == 1:
            by_score_bucket[bucket]['total_success'] += 1
        
        # Calculate time to resolution
        timestamp = trade.get('timestamp')
        resolution_time = trade.get('resolution_time')
        
        if timestamp and resolution_time:
            try:
                ts = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                rt = datetime.datetime.fromisoformat(resolution_time.replace('Z', '+00:00'))
                diff = rt - ts
                hours = diff.total_seconds() / 3600  # Convert to hours
                by_score_bucket[bucket]['total_time_to_resolution'] += hours
                by_score_bucket[bucket]['time_to_resolution_count'] += 1
            except ValueError:
                continue  # Skip invalid timestamps
    
    # Calculate success rates and average time to resolution
    for bucket in by_score_bucket:
        total = by_score_bucket[bucket]['count']
        success = by_score_bucket[bucket]['total_success']
        by_score_bucket[bucket]['success_rate'] = success / total if total > 0 else 0
        
        time_count = by_score_bucket[bucket]['time_to_resolution_count']
        if time_count > 0:
            by_score_bucket[bucket]['avg_hours_to_resolution'] = \
                by_score_bucket[bucket]['total_time_to_resolution'] / time_count
        else:
            by_score_bucket[bucket]['avg_hours_to_resolution'] = 0
    
    return by_score_bucket
