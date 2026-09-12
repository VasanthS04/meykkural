from typing import Dict, Any


class AlertEngine:
    """
    Generates security alerts from the fused voice-risk score.
    """

    LOW_THRESHOLD = 30
    HIGH_THRESHOLD = 70

    def evaluate(self, risk_score: float) -> Dict[str, Any]:
        """
        Convert a numerical risk score into a security alert.
        """

        risk_score = max(0.0, min(100.0, float(risk_score)))

        if risk_score >= self.HIGH_THRESHOLD:
            return {
                "level": "HIGH",
                "title": "Potential Voice Clone Detected",
                "message": (
                    "The voice shows strong indicators of "
                    "AI-generated or cloned speech."
                ),
                "action": (
                    "Verify the caller using a trusted secondary method "
                    "before sharing sensitive information."
                ),
                "risk": round(risk_score, 2)
            }

        if risk_score >= self.LOW_THRESHOLD:
            return {
                "level": "MEDIUM",
                "title": "Voice Requires Verification",
                "message": (
                    "Some characteristics of the voice require "
                    "additional verification."
                ),
                "action": (
                    "Continue monitoring the call and consider "
                    "secondary verification."
                ),
                "risk": round(risk_score, 2)
            }

        return {
            "level": "LOW",
            "title": "Voice Appears Normal",
            "message": (
                "No strong voice-cloning indicators were detected "
                "by the current analysis."
            ),
            "action": "Continue monitoring.",
            "risk": round(risk_score, 2)
        }


def generate_alert(risk: float) -> str:
    """
    Compatibility helper used by main.py.
    """

    alert_engine = AlertEngine()
    result = alert_engine.evaluate(risk)

    return result["message"]