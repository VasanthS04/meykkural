import numpy as np

from backend.audio.resampler import resample_audio


def pcm16_to_float32(data: bytes) -> np.ndarray:
    """Decode little-endian signed PCM16 bytes into mono float audio."""
    if not data:
        return np.array([], dtype=np.float32)

    samples = np.frombuffer(data, dtype="<i2")
    return (samples.astype(np.float32) / 32768.0).clip(-1.0, 1.0)


def normalize_audio(
    audio: np.ndarray
) -> np.ndarray:
    """Peak-normalize audio."""

    if audio is None or len(audio) == 0:
        return np.array(
            [],
            dtype=np.float32
        )

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    peak = np.max(
        np.abs(audio)
    )

    if peak < 1e-8:
        return audio.copy()

    return (
        audio / peak
    ).astype(np.float32)


def remove_dc_offset(
    audio: np.ndarray
) -> np.ndarray:
    """Remove the mean/DC component from audio."""

    if audio is None or len(audio) == 0:
        return np.array(
            [],
            dtype=np.float32
        )

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    return (
        audio - np.mean(audio)
    ).astype(np.float32)


def preprocess_audio(
    audio: np.ndarray,
    original_rate: int,
    target_rate: int = 16000
) -> np.ndarray:
    """
    Standard Meykkural audio preprocessing pipeline.

    Steps:
        1. Convert to float32
        2. Remove DC offset
        3. Resample to 16 kHz
        4. Normalize
    """

    if audio is None or len(audio) == 0:
        return np.array(
            [],
            dtype=np.float32
        )

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    audio = remove_dc_offset(
        audio
    )

    audio = resample_audio(
        audio,
        original_rate,
        target_rate
    )

    audio = normalize_audio(
        audio
    )

    return audio.astype(
        np.float32
    )