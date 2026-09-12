import uuid
from typing import Dict, Optional

from backend.call.call_session import CallSession


class SessionManager:
    """
    Manages active Meykkural call sessions.

    Audio is not stored here.
    """

    def __init__(self):
        self._sessions: Dict[
            str,
            CallSession
        ] = {}

    def create_session(
        self,
        call_id: Optional[str] = None,
        caller_id: Optional[str] = None,
        receiver_id: Optional[str] = None
    ) -> CallSession:
        """Create a new call session."""

        session_id = str(
            uuid.uuid4()
        )

        if call_id is None:
            call_id = str(
                uuid.uuid4()
            )

        session = CallSession(
            session_id=session_id,
            call_id=call_id,
            caller_id=caller_id,
            receiver_id=receiver_id
        )

        self._sessions[
            session_id
        ] = session

        return session

    def get_session(
        self,
        session_id: str
    ) -> Optional[CallSession]:
        """Get a session by ID."""

        return self._sessions.get(
            session_id
        )

    def answer_session(
        self,
        session_id: str
    ) -> Optional[CallSession]:
        """Mark a session as active."""

        session = self.get_session(
            session_id
        )

        if session is None:
            return None

        session.answer()

        return session

    def end_session(
        self,
        session_id: str
    ) -> Optional[CallSession]:
        """End a session."""

        session = self.get_session(
            session_id
        )

        if session is None:
            return None

        session.end()

        return session

    def update_risk(
        self,
        session_id: str,
        score: float,
        level: str
    ) -> Optional[CallSession]:
        """Update session risk."""

        session = self.get_session(
            session_id
        )

        if session is None:
            return None

        session.update_risk(
            score,
            level
        )

        return session

    def remove_session(
        self,
        session_id: str
    ) -> bool:
        """
        Remove session metadata from memory.

        This does not store or archive audio.
        """

        if session_id not in self._sessions:
            return False

        del self._sessions[
            session_id
        ]

        return True

    def list_active_sessions(self):
        """Return currently active sessions."""

        return [
            session
            for session in self._sessions.values()
            if session.status in {
                "RINGING",
                "ACTIVE"
            }
        ]

    def count_active(self) -> int:
        """Return number of active sessions."""

        return len(
            self.list_active_sessions()
        )


session_manager = SessionManager()