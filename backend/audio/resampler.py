import math

import numpy as np
from scipy.signal import resample_poly


def resample_audio(
    audio: np.ndarray,
    original_rate: int,
    target_rate: int = 16000
) -> np.ndarray:
    """
    Resample audio using polyphase filtering.
    """

    if audio is None or len(audio) == 0:
        return np.array(
            [],
            dtype=np.float32
        )

    if original_rate <= 0:
        raise ValueError(
            "original_rate must be greater than 0"
        )

    if target_rate <= 0:
        raise ValueError(
            "target_rate must be greater than 0"
        )

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    if original_rate == target_rate:
        return audio.copy()

    divisor = math.gcd(
        original_rate,
        target_rate
    )

    up = target_rate // divisor
    down = original_rate // divisor

    resampled = resample_poly(
        audio,
        up,
        down
    )

    return np.asarray(
        resampled,
        dtype=np.float32
    )