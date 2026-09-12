"""
Central privacy manager for Meykkural.
"""

from typing import Any, Dict

import numpy as np

from .memory_buffer import PrivacyMemoryBuffer
from .storage_policy import StoragePolicy


class PrivacyManager:
    """
    Controls temporary audio handling and privacy status.

    Raw audio is never written to persistent storage.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        max_seconds: float = 10.0,
    ):
        self.sample_rate = sample_rate

        max_samples = int(
            sample_rate * max_seconds
        )

        self.buffer = PrivacyMemoryBuffer(
            max_samples=max_samples
        )

        self.analysis_active = False

    def start_analysis(self) -> None:
        """Start an in-memory analysis session."""

        self.analysis_active = True
        self.buffer.clear()

    def add_audio(
        self,
        audio: np.ndarray,
    ) -> None:
        """Temporarily hold audio in memory."""

        if not self.analysis_active:
            return

        self.buffer.add(audio)

    def get_audio(self) -> np.ndarray:
        """
        Get temporary audio for inference.

        The returned array must not be persisted.
        """

        return self.buffer.get()

    def clear_audio(self) -> None:
        """Immediately discard temporary audio."""

        self.buffer.clear()

    def stop_analysis(self) -> None:
        """
        Stop analysis and discard all temporary audio.
        """

        self.clear_audio()
        self.analysis_active = False

    def privacy_status(self) -> Dict[str, Any]:
        """Return the current privacy state."""

        return {
            "analysis_active": self.analysis_active,
            "audio_in_memory": not self.buffer.is_empty(),
            "audio_stored": False,
            "audio_recorded": False,
            "persistent_audio_files": False,
            "storage_allowed": (
                StoragePolicy.allows_storage()
            ),
            "processing": "in-memory",
        }

    def get_policy(self) -> Dict[str, Any]:
        """Return the configured storage policy."""

        return StoragePolicy.get_policy()

    def get_buffer_duration(self) -> float:
        """Return temporary audio duration."""

        return self.buffer.duration(
            self.sample_rate
        )


privacy_manager = PrivacyManager()


def privacy_policy() -> dict:
    """
    Compatibility helper used by existing backend code.
    """

    return {
        **StoragePolicy.get_policy(),
        "processing": "in-memory",
        "description": StoragePolicy.describe(),
    }