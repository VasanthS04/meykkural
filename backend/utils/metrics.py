"""
Metrics utilities for Meykkural voice analysis.
"""

from typing import Dict, Iterable, Optional

import numpy as np


def calculate_average(
    values: Iterable[float],
) -> float:
    """Calculate the average of numerical values."""

    values = list(values)

    if not values:
        return 0.0

    return round(
        float(np.mean(values)),
        2,
    )


def calculate_minimum(
    values: Iterable[float],
) -> float:
    """Calculate the minimum value."""

    values = list(values)

    if not values:
        return 0.0

    return round(
        float(np.min(values)),
        2,
    )


def calculate_maximum(
    values: Iterable[float],
) -> float:
    """Calculate the maximum value."""

    values = list(values)

    if not values:
        return 0.0

    return round(
        float(np.max(values)),
        2,
    )


def calculate_std(
    values: Iterable[float],
) -> float:
    """Calculate standard deviation."""

    values = list(values)

    if not values:
        return 0.0

    return round(
        float(np.std(values)),
        2,
    )


def calculate_statistics(
    values: Iterable[float],
) -> Dict[str, float]:
    """
    Calculate common statistics for a sequence.
    """

    values = list(values)

    if not values:
        return {
            "average": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "standard_deviation": 0.0,
        }

    return {
        "average": calculate_average(values),
        "minimum": calculate_minimum(values),
        "maximum": calculate_maximum(values),
        "standard_deviation": calculate_std(values),
    }


def calculate_risk_statistics(
    risk_scores: Iterable[float],
) -> Dict[str, float]:
    """
    Calculate statistics for a sequence of risk scores.
    """

    scores = [
        max(
            0.0,
            min(
                100.0,
                float(score),
            ),
        )
        for score in risk_scores
    ]

    statistics = calculate_statistics(
        scores
    )

    return {
        "average_risk": statistics["average"],
        "minimum_risk": statistics["minimum"],
        "maximum_risk": statistics["maximum"],
        "risk_variation": statistics[
            "standard_deviation"
        ],
    }


def calculate_model_statistics(
    model_scores: Dict[str, float],
) -> Dict[str, float]:
    """
    Calculate basic statistics across model scores.
    """

    if not model_scores:
        return {
            "average": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
        }

    values = [
        float(value)
        for value in model_scores.values()
    ]

    return {
        "average": calculate_average(values),
        "minimum": calculate_minimum(values),
        "maximum": calculate_maximum(values),
    }