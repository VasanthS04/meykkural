import numpy as np


def clamp_score(score: float) -> float:
    """Keep a score within the 0-100 range."""

    return float(
        np.clip(
            float(score),
            0.0,
            100.0
        )
    )


def normalize_score(
    score: float,
    input_min: float = 0.0,
    input_max: float = 1.0
) -> float:
    """
    Convert a model probability/score into 0-100.
    """

    if input_max <= input_min:
        raise ValueError(
            "input_max must be greater than input_min"
        )

    normalized = (
        (float(score) - input_min)
        / (input_max - input_min)
    ) * 100.0

    return clamp_score(
        normalized
    )


def calibrate_probability(
    probability: float
) -> float:
    """
    Convert a probability in [0,1] to a risk score [0,100].
    """

    probability = float(
        np.clip(
            probability,
            0.0,
            1.0
        )
    )

    return probability * 100.0


def calibrate_scores(
    scores: dict
) -> dict:
    """
    Calibrate model scores.

    Model outputs are expected to be probabilities
    between 0 and 1.

    Returns scores in the range 0-100.
    """

    calibrated = {}

    for model, score in scores.items():
        try:
            value = float(score)
        except (TypeError, ValueError):
            value = 0.0

        calibrated[model] = round(
            calibrate_probability(value)
            if 0.0 <= value <= 1.0
            else clamp_score(value),
            2
        )

    return calibrated