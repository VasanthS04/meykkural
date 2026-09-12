"""
Temporary in-memory audio buffer.

Audio exists only for the duration required for analysis.
"""

from collections import deque
from typing import Optional

import numpy as np


class PrivacyMemoryBuffer:
    """
    Rolling in-memory audio buffer.

    No audio is written to disk.
    """

    def __init__(
        self,
        max_samples: int = 16000 * 10,
    ):
        self.max_samples = max_samples
        self._buffer = deque()
        self._sample_count = 0

    def add(self, audio: np.ndarray) -> None:
        """Add audio samples to the temporary buffer."""

        if audio is None:
            return

        audio = np.asarray(
            audio,
            dtype=np.float32,
        ).flatten()

        if len(audio) == 0:
            return

        self._buffer.append(audio)
        self._sample_count += len(audio)

        self._trim()

    def _trim(self) -> None:
        """Keep only the most recent samples."""

        while self._sample_count > self.max_samples:
            oldest = self._buffer.popleft()
            self._sample_count -= len(oldest)

    def get(self) -> np.ndarray:
        """Return a copy of the current in-memory audio."""

        if not self._buffer:
            return np.array(
                [],
                dtype=np.float32,
            )

        return np.concatenate(
            list(self._buffer)
        ).astype(np.float32)

    def get_latest(
        self,
        samples: int,
    ) -> np.ndarray:
        """Return only the latest requested samples."""

        audio = self.get()

        if samples <= 0:
            return np.array(
                [],
                dtype=np.float32,
            )

        return audio[-samples:]

    def clear(self) -> None:
        """
        Immediately remove all temporary audio references.
        """

        self._buffer.clear()
        self._sample_count = 0

    def size(self) -> int:
        """Return number of samples currently in memory."""
        return self._sample_count

    def is_empty(self) -> bool:
        """Check whether the buffer is empty."""
        return self._sample_count == 0

    def duration(
        self,
        sample_rate: int = 16000,
    ) -> float:
        """Return current buffer duration in seconds."""

        if sample_rate <= 0:
            return 0.0

        return self._sample_count / sample_rate