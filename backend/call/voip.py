from dataclasses import dataclass
from typing import Optional


@dataclass
class VoIPCall:
    """
    Represents the state of a WebRTC/VoIP call.

    This class contains call metadata only.
    Audio is streamed separately through WebSocket/WebRTC.
    """

    call_id: str
    session_id: Optional[str] = None

    state: str = "IDLE"

    caller: Optional[str] = None
    receiver: Optional[str] = None

    muted: bool = False
    analysis_enabled: bool = True

    def incoming(self):
        """Mark the call as incoming."""

        self.state = "RINGING"

    def answer(self):
        """Answer the incoming call."""

        self.state = "ACTIVE"

    def reject(self):
        """Reject the incoming call."""

        self.state = "REJECTED"

    def end(self):
        """End the call."""

        self.state = "ENDED"

    def mute(self):
        """Mute the local call."""

        self.muted = True

    def unmute(self):
        """Unmute the local call."""

        self.muted = False

    def enable_analysis(self):
        """Enable Meykkural voice analysis."""

        self.analysis_enabled = True

    def disable_analysis(self):
        """Disable Meykkural voice analysis."""

        self.analysis_enabled = False

    def to_dict(self) -> dict:
        """Return VoIP call state."""

        return {
            "call_id": self.call_id,
            "session_id": self.session_id,
            "state": self.state,
            "caller": self.caller,
            "receiver": self.receiver,
            "muted": self.muted,
            "analysis_enabled": (
                self.analysis_enabled
            )
        }


class VoIPManager:
    """Manages active VoIP call objects."""

    def __init__(self):
        self._calls = {}

    def create_call(
        self,
        call_id: str,
        session_id: Optional[str] = None,
        caller: Optional[str] = None,
        receiver: Optional[str] = None
    ) -> VoIPCall:

        call = VoIPCall(
            call_id=call_id,
            session_id=session_id,
            caller=caller,
            receiver=receiver
        )

        self._calls[call_id] = call

        return call

    def get_call(
        self,
        call_id: str
    ) -> Optional[VoIPCall]:

        return self._calls.get(
            call_id
        )

    def remove_call(
        self,
        call_id: str
    ) -> bool:

        if call_id not in self._calls:
            return False

        del self._calls[
            call_id
        ]

        return True

    def active_calls(self):
        """Return active/ringing calls."""

        return [
            call
            for call in self._calls.values()
            if call.state in {
                "RINGING",
                "ACTIVE"
            }
        ]


voip_manager = VoIPManager()