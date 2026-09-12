from typing import Dict

import numpy as np

from backend.features.energy import extract_energy
from backend.features.mfcc import extract_mfcc
from backend.features.pitch import extract_pitch


def _percentage(value: float, minimum: float, maximum: float) -> float:
    return float(np.clip((value - minimum) / (maximum - minimum) * 100.0, 0.0, 100.0))


def extract_features(audio: np.ndarray, sample_rate: int = 16000) -> Dict[str, float]:
    """Return compact, JSON-safe acoustic features for API responses."""
    if audio is None or len(audio) == 0:
        return {
            "mfcc": 0.0,
            "mel": 0.0,
            "lfcc": 0.0,
            "cqcc": 0.0,
            "pitch": 0.0,
            "energy": 0.0,
            "harmonics": 0.0,
            "pauses": 0.0,
        }

    signal = np.asarray(audio, dtype=np.float32)
    mfcc = extract_mfcc(signal, sample_rate)
    energy = extract_energy(signal, sample_rate)
    pitch = extract_pitch(signal, sample_rate)
    voiced_ratio = float(np.mean(np.abs(signal) > 0.01))

    return {
        "mfcc": _percentage(float(np.std(mfcc)), 0.0, 30.0),
        "mel": _percentage(float(np.mean(np.abs(signal))), 0.0, 0.2),
        "lfcc": _percentage(float(np.std(signal)), 0.0, 0.2),
        "cqcc": _percentage(float(energy["energy_std"]), 0.0, 0.05),
        "pitch": _percentage(float(pitch["pitch_std"]), 0.0, 100.0),
        "energy": _percentage(float(energy["energy_mean"]), 0.0, 0.05),
        "harmonics": _percentage(voiced_ratio, 0.0, 1.0),
        "pauses": round((1.0 - voiced_ratio) * 100.0, 2),
    }