import numpy as np
import librosa


def extract_spectral_features(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """Extract spectral characteristics."""

    if audio is None or len(audio) == 0:
        return {
            "spectral_centroid": 0.0,
            "spectral_bandwidth": 0.0,
            "spectral_rolloff": 0.0,
            "spectral_flatness": 0.0,
            "zero_crossing_rate": 0.0
        }

    audio = audio.astype(
        np.float32
    )

    centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sample_rate,
        hop_length=160
    )[0]

    bandwidth = librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sample_rate,
        hop_length=160
    )[0]

    rolloff = librosa.feature.spectral_rolloff(
        y=audio,
        sr=sample_rate,
        hop_length=160
    )[0]

    flatness = librosa.feature.spectral_flatness(
        y=audio,
        hop_length=160
    )[0]

    zcr = librosa.feature.zero_crossing_rate(
        audio,
        hop_length=160
    )[0]

    return {
        "spectral_centroid": float(
            np.mean(centroid)
        ),
        "spectral_bandwidth": float(
            np.mean(bandwidth)
        ),
        "spectral_rolloff": float(
            np.mean(rolloff)
        ),
        "spectral_flatness": float(
            np.mean(flatness)
        ),
        "zero_crossing_rate": float(
            np.mean(zcr)
        )
    }