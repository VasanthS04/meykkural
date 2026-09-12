"""
General helper functions used throughout Meykkural.
"""

from typing import Any


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """Keep a value within a specified range."""

    value = float(value)

    return max(
        minimum,
        min(maximum, value),
    )


def normalize_score(
    score: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """Normalize a score to the 0-100 range."""

    if maximum <= minimum:
        return 0.0

    score = clamp(
        score,
        minimum,
        maximum,
    )

    normalized = (
        (score - minimum)
        / (maximum - minimum)
    ) * 100.0

    return round(
        normalized,
        2,
    )


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """Safely convert a value to float."""

    try:
        return float(value)
    except (
        TypeError,
        ValueError,
    ):
        return default


def safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """Safely convert a value to integer."""

    try:
        return int(value)
    except (
        TypeError,
        ValueError,
    ):
        return default


def format_duration(
    seconds: float,
) -> str:
    """Convert seconds into HH:MM:SS format."""

    seconds = max(
        0,
        int(seconds),
    )

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining = seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining:02d}"
    )


def format_percentage(
    value: float,
    decimals: int = 2,
) -> str:
    """Format a numerical value as a percentage."""

    return f"{float(value):.{decimals}f}%"


def is_valid_audio(
    audio: Any,
) -> bool:
    """Check whether an audio object contains samples."""

    if audio is None:
        return False

    try:
        return len(audio) > 0
    except TypeError:
        return False