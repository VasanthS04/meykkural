import numpy as np
import librosa


def extract_cqt(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> np.ndarray:
    """Extract Constant-Q Transform magnitude."""

    if audio is None or len(audio) == 0:
        return np.empty(
            (0, 0),
            dtype=np.float32
        )

    cqt = librosa.cqt(
        audio.astype(np.float32),
        sr=sample_rate,
        hop_length=160,
        fmin=librosa.note_to_hz("C1"),
        n_bins=84,
        bins_per_octave=12
    )

    return np.abs(
        cqt
    ).astype(np.float32)