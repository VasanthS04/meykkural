from typing import Dict, Any

from backend.alerts.thresholds import get_risk_level


class NotificationManager:
    """
    Creates notifications for the frontend security-alert UI.

    This module does not send SMS, email, or push notifications.
    It currently prepares real-time application notifications.
    """

    def create_notification(
        self,
        risk_score: float
    ) -> Dict[str, Any]:

        risk_score = max(
            0.0,
            min(100.0, float(risk_score))
        )

        level = get_risk_level(risk_score)

        if level == "HIGH":
            return {
                "type": "security_alert",
                "level": "HIGH",
                "title": "High Risk Voice Detected",
                "message": (
                    "Strong indicators of a possible "
                    "AI-generated or cloned voice were detected."
                ),
                "action": (
                    "Perform secondary verification before "
                    "sharing sensitive information."
                ),
                "risk": round(risk_score, 2),
                "notify_user": True
            }

        if level == "MEDIUM":
            return {
                "type": "security_alert",
                "level": "MEDIUM",
                "title": "Voice Verification Recommended",
                "message": (
                    "The current voice analysis contains "
                    "suspicious characteristics."
                ),
                "action": (
                    "Continue monitoring and consider "
                    "secondary verification."
                ),
                "risk": round(risk_score, 2),
                "notify_user": True
            }

        return {
            "type": "security_status",
            "level": "LOW",
            "title": "Low Risk",
            "message": (
                "No strong voice-cloning indicators "
                "were detected."
            ),
            "action": "Continue monitoring.",
            "risk": round(risk_score, 2),
            "notify_user": False
        }


notification_manager = NotificationManager()


def create_notification(risk_score: float) -> Dict[str, Any]:
    return notification_manager.create_notification(
        risk_score
    )