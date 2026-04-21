from dataclasses import dataclass
from typing import List, Dict, Any

from app.backtest.metrics import BacktestMetrics


dataclass
class BacktestReport:
    metrics: BacktestMetrics
    trades: List[Dict[str, Any]]
    portfolio_value_history: List[Dict[str, Any]]
    # Add other fields as needed


def serialize_report(report: BacktestReport) -> Dict[str, Any]:
    return {
        'metrics': report.metrics.__dict__,
        'trades': report.trades,
        'portfolio_value_history': report.portfolio_value_history,
    }

def deserialize_report(data: Dict[str, Any]) -> BacktestReport:
    return BacktestReport(
        metrics=BacktestMetrics(**data['metrics']),
        trades=data['trades'],
        portfolio_value_history=data['portfolio_value_history'],
    )

def _generate_json_report(report: BacktestReport) -> str:
    import json
    return json.dumps(serialize_report(report), sort_keys=True, indent=2)