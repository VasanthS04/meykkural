from typing import Dict

from backend.fusion.calibration import (
    calibrate_scores,
    clamp_score
)


class ScoreFusion:
    """
    Combines multiple anti-spoofing model scores.

    The weights are provisional and should be calibrated
    using a validation dataset before final deployment.
    """

    DEFAULT_WEIGHTS = {
        "aasist": 0.25,
        "wav2vec2": 0.20,
        "rawnet2": 0.15,
        "conformer": 0.15,
        "xlsr": 0.15,
        "ecapa": 0.10
    }

    def __init__(
        self,
        weights: Dict[str, float] = None
    ):
        self.weights = (
            weights.copy()
            if weights
            else self.DEFAULT_WEIGHTS.copy()
        )

        self._normalize_weights()

    def _normalize_weights(self):
        """Ensure all fusion weights sum to 1."""

        total = sum(
            max(0.0, float(weight))
            for weight in self.weights.values()
        )

        if total <= 0:
            self.weights = (
                self.DEFAULT_WEIGHTS.copy()
            )
            total = sum(
                self.weights.values()
            )

        self.weights = {
            model: max(
                0.0,
                float(weight)
            ) / total
            for model, weight
            in self.weights.items()
        }

    def fuse(
        self,
        model_scores: Dict[str, float]
    ) -> float:
        """
        Produce a final 0-100 spoof risk score.

        Input model scores may be probabilities [0,1]
        or already calibrated scores [0,100].
        """

        if not model_scores:
            return 0.0

        total = 0.0
        weight_sum = 0.0
        fallback_scores = []

        for model, weight in self.weights.items():

            if model not in model_scores:
                continue

            try:
                score = float(
                    model_scores[model]
                )
            except (TypeError, ValueError):
                continue

            # Model probabilities
            if 0.0 <= score <= 1.0:
                score *= 100.0

            score = clamp_score(score)

            if model != "wav2vec2" and model_scores.get("_fallback_models"):
                fallback_scores.append(score)
                continue

            total += (
                score * weight
            )

            weight_sum += weight

        if fallback_scores:
            total += (sum(fallback_scores) / len(fallback_scores)) * 0.35
            weight_sum += 0.35

        if weight_sum <= 0:
            return 0.0

        return round(
            clamp_score(
                total / weight_sum
            ),
            2
        )

    def fuse_with_details(
        self,
        model_scores: Dict[str, float]
    ) -> dict:
        """Return final score together with calibrated scores."""

        calibrated = calibrate_scores(
            model_scores
        )

        score = self.fuse(
            calibrated
        )

        return {
            "risk_score": score,
            "model_scores": calibrated,
            "weights": self.weights
        }


score_fusion = ScoreFusion()


def fuse_scores(
    model_scores: Dict[str, float]
) -> float:
    """Convenience function for the inference pipeline."""

    return score_fusion.fuse(
        model_scores
    )