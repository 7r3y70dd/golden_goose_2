import logging
import sys
from typing import Optional

# Centralized logging configuration

def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
) -> None:
    """
    Set up centralized logging configuration.

    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string for logs
        handler: Custom logging handler (default: StreamHandler to stdout)
    """
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    if handler is None:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)

    # Prevent propagation to avoid duplicate logs
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)