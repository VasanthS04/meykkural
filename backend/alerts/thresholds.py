from dataclasses import dataclass


@dataclass(frozen=True)
class RiskThresholds:
    """
    Risk thresholds used by Meykkural.
    """

    low_max: float = 29.0
    medium_max: float = 69.0
    high_min: float = 70.0

    def classify(self, score: float) -> str:
        score = max(0.0, min(100.0, float(score)))

        if score >= self.high_min:
            return "HIGH"

        if score > self.low_max:
            return "MEDIUM"

        return "LOW"


THRESHOLDS = RiskThresholds()


def get_risk_level(score: float) -> str:
    return THRESHOLDS.classify(score)


def is_high_risk(score: float) -> bool:
    return float(score) >= THRESHOLDS.high_min


def is_medium_risk(score: float) -> bool:
    score = float(score)
    return THRESHOLDS.low_max < score < THRESHOLDS.high_min


def is_low_risk(score: float) -> bool:
    return float(score) <= THRESHOLDS.low_max