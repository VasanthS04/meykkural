import numpy as np

from backend.audio.buffer import AudioBuffer
from backend.audio.decoder import decode_audio
from backend.audio.preprocessing import preprocess_audio


class AudioStreamProcessor:
    """
    Processes incoming real-time audio chunks.

    Audio remains in memory only.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        buffer_seconds: int = 10
    ):
        self.sample_rate = sample_rate
        self.channels = channels

        self.buffer = AudioBuffer(
            max_samples=(
                sample_rate *
                buffer_seconds
            )
        )

    def process_chunk(
        self,
        audio_bytes: bytes,
        input_sample_rate: int = 16000,
        encoding: str = "pcm16"
    ) -> np.ndarray:
        """
        Decode, preprocess and buffer one incoming chunk.
        """

        audio = decode_audio(
            audio_bytes,
            encoding=encoding,
            channels=self.channels
        )

        if len(audio) == 0:
            return np.array(
                [],
                dtype=np.float32
            )

        audio = preprocess_audio(
            audio,
            original_rate=input_sample_rate,
            target_rate=self.sample_rate
        )

        self.buffer.add(
            audio
        )

        return audio

    def get_audio(self) -> np.ndarray:
        """Return current buffered audio."""

        return self.buffer.get()

    def get_latest(
        self,
        seconds: float
    ) -> np.ndarray:
        """Return the latest requested duration."""

        samples = int(
            seconds * self.sample_rate
        )

        return self.buffer.get_latest(
            samples
        )

    def clear(self):
        """Discard all in-memory audio."""

        self.buffer.clear()

    def duration(self) -> float:
        """Return current buffered duration."""

        return self.buffer.get_duration(
            self.sample_rate
        )