import numpy as np
import librosa


def extract_harmonic_features(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """Analyze harmonic and percussive components."""

    if audio is None or len(audio) == 0:
        return {
            "harmonic_ratio": 0.0,
            "percussive_ratio": 0.0
        }

    harmonic, percussive = librosa.effects.hpss(
        audio.astype(np.float32)
    )

    total_energy = (
        np.sum(harmonic ** 2) +
        np.sum(percussive ** 2)
    )

    if total_energy < 1e-10:
        return {
            "harmonic_ratio": 0.0,
            "percussive_ratio": 0.0
        }

    return {
        "harmonic_ratio": float(
            np.sum(harmonic ** 2) /
            total_energy
        ),
        "percussive_ratio": float(
            np.sum(percussive ** 2) /
            total_energy
        )
    }