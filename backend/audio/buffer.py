import numpy as np


class AudioBuffer:
    """
    In-memory rolling audio buffer.

    Audio is never written to disk.
    """

    def __init__(
        self,
        max_samples: int = 16000 * 10
    ):
        self.max_samples = max_samples
        self._buffer = np.array(
            [],
            dtype=np.float32
        )

    def add(self, audio: np.ndarray):
        """Add audio samples to the rolling buffer."""

        if audio is None or len(audio) == 0:
            return

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        self._buffer = np.concatenate(
            [self._buffer, audio]
        )

        if len(self._buffer) > self.max_samples:
            self._buffer = self._buffer[
                -self.max_samples:
            ]

    def get(self) -> np.ndarray:
        """Return a copy of buffered audio."""

        return self._buffer.copy()

    def get_latest(
        self,
        samples: int
    ) -> np.ndarray:
        """Return the latest N samples."""

        samples = max(0, int(samples))

        if samples == 0:
            return np.array(
                [],
                dtype=np.float32
            )

        return self._buffer[-samples:].copy()

    def get_duration(
        self,
        sample_rate: int
    ) -> float:
        """Return buffered duration in seconds."""

        if sample_rate <= 0:
            return 0.0

        return len(self._buffer) / sample_rate

    def clear(self):
        """Immediately discard buffered audio."""

        self._buffer = np.array(
            [],
            dtype=np.float32
        )

    def is_full(self) -> bool:
        """Check whether the buffer reached its maximum size."""

        return len(self._buffer) >= self.max_samples

    def __len__(self):
        return len(self._buffer)