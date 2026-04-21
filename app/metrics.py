from app.backtest.metrics import *

# Re-export n_metrics from backtest metrics if it exists, otherwise define it
try:
    from app.backtest.metrics import n_metrics
except ImportError:
    # Define n_metrics as a simple metrics collector if not present
    n_metrics = None

# If n_metrics is not defined, create a basic implementation
if n_metrics is None:
    # Simple metrics implementation
    class _Metrics:
        def __init__(self):
            self.counters = {}
            self.timers = {}
            self.gauges = {}

        def increment_counter(self, name, value=1):
            self.counters[name] = self.counters.get(name, 0) + value

        def get_counter(self, name):
            return self.counters.get(name, 0)

        def record_timer(self, name, value):
            if name not in self.timers:
                self.timers[name] = []
            self.timers[name].append(value)

        def get_timer_stats(self, name):
            if name not in self.timers:
                return {}
            values = self.timers[name]
            return {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values)
            }

        def set_gauge(self, name, value):
            self.gauges[name] = value

        def get_gauge(self, name):
            return self.gauges.get(name)

        def get_all_metrics(self):
            return {
                'counters': self.counters,
                'timers': self.timers,
                'gauges': self.gauges
            }

    n_metrics = _Metrics()
