from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class CallSession:
    """
    Represents one active Meykkural call.

    No call audio is stored in this object.
    Only session metadata is maintained.
    """

    session_id: str
    call_id: str
    caller_id: Optional[str] = None
    receiver_id: Optional[str] = None

    status: str = "RINGING"

    started_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    risk_score: float = 0.0
    risk_level: str = "LOW"

    metadata: dict = field(
        default_factory=dict
    )

    def answer(self):
        """Mark the call as answered."""

        if self.status == "ENDED":
            return

        self.status = "ACTIVE"

        now = datetime.now(
            timezone.utc
        )

        if self.started_at is None:
            self.started_at = now

        self.answered_at = now

    def end(self):
        """End the call session."""

        self.status = "ENDED"

        now = datetime.now(
            timezone.utc
        )

        self.ended_at = now

    def update_risk(
        self,
        score: float,
        level: str
    ):
        """Update the latest voice risk information."""

        self.risk_score = max(
            0.0,
            min(100.0, float(score))
        )

        self.risk_level = str(
            level
        ).upper()

    def duration_seconds(self) -> float:
        """Return call duration in seconds."""

        if self.answered_at is None:
            return 0.0

        end_time = (
            self.ended_at
            or datetime.now(timezone.utc)
        )

        return max(
            0.0,
            (
                end_time -
                self.answered_at
            ).total_seconds()
        )

    def to_dict(self) -> dict:
        """Return frontend-safe session information."""

        return {
            "session_id": self.session_id,
            "call_id": self.call_id,
            "caller_id": self.caller_id,
            "receiver_id": self.receiver_id,
            "status": self.status,
            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),
            "answered_at": (
                self.answered_at.isoformat()
                if self.answered_at
                else None
            ),
            "ended_at": (
                self.ended_at.isoformat()
                if self.ended_at
                else None
            ),
            "risk_score": round(
                self.risk_score,
                2
            ),
            "risk_level": self.risk_level,
            "duration_seconds": round(
                self.duration_seconds(),
                2
            ),
            "metadata": self.metadata
        }