"""
Application logging configuration for Meykkural.
"""

import logging
import sys
from typing import Optional


LOGGER_NAME = "meykkural"


def configure_logger(
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure and return the Meykkural logger.
    """

    logger = logging.getLogger(
        LOGGER_NAME
    )

    logger.setLevel(level)

    if not logger.handlers:

        handler = logging.StreamHandler(
            sys.stdout
        )

        formatter = logging.Formatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    logger.propagate = False

    return logger


logger = configure_logger()


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Return the Meykkural logger or a child logger.
    """

    if not name:
        return logger

    return logging.getLogger(
        f"{LOGGER_NAME}.{name}"
    )


def log_info(
    message: str,
) -> None:
    """Log an informational message."""

    logger.info(message)


def log_warning(
    message: str,
) -> None:
    """Log a warning message."""

    logger.warning(message)


def log_error(
    message: str,
) -> None:
    """Log an error message."""

    logger.error(message)


def log_debug(
    message: str,
) -> None:
    """Log a debug message."""

    logger.debug(message)