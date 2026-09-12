from backend.alerts.notification import create_notification
from backend.fusion.risk_engine import risk_level


def test_alert_thresholds_are_consistent():
    assert risk_level(10) == "LOW"
    assert risk_level(50) == "MEDIUM"
    assert risk_level(90) == "HIGH"
    assert create_notification(90)["notify_user"] is True