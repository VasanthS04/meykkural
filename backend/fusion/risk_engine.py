from backend.fusion.score_fusion import fuse_scores
from backend.fusion.calibration import clamp_score


LOW_THRESHOLD = 30.0
HIGH_THRESHOLD = 70.0


def calculate_risk(
    model_scores: dict
) -> int:
    """
    Calculate the final voice-cloning risk score.

    Returns:
        0-100 integer risk score.
    """

    risk = fuse_scores(
        model_scores
    )

    return int(
        round(
            clamp_score(risk)
        )
    )


def risk_level(
    risk: float
) -> str:
    """Convert risk score into LOW/MEDIUM/HIGH."""

    risk = clamp_score(
        risk
    )

    if risk >= HIGH_THRESHOLD:
        return "HIGH"

    if risk >= LOW_THRESHOLD:
        return "MEDIUM"

    return "LOW"


def risk_details(
    model_scores: dict
) -> dict:
    """
    Return complete risk information for the frontend.
    """

    risk = calculate_risk(
        model_scores
    )

    level = risk_level(
        risk
    )

    return {
        "risk": risk,
        "risk_level": level,
        "models": model_scores
    }