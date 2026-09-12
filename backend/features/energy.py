import numpy as np
import librosa


def extract_energy(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """Extract energy-related features."""

    if audio is None or len(audio) == 0:
        return {
            "rms_mean": 0.0,
            "rms_std": 0.0,
            "energy_mean": 0.0,
            "energy_std": 0.0
        }

    rms = librosa.feature.rms(
        y=audio.astype(np.float32),
        frame_length=512,
        hop_length=160
    )[0]

    energy = rms ** 2

    return {
        "rms_mean": float(np.mean(rms)),
        "rms_std": float(np.std(rms)),
        "energy_mean": float(np.mean(energy)),
        "energy_std": float(np.std(energy))
    }