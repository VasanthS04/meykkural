import numpy as np
import librosa


def extract_mfcc(
    audio: np.ndarray,
    sample_rate: int = 16000,
    n_mfcc: int = 13
) -> np.ndarray:
    """Extract Mel-Frequency Cepstral Coefficients."""

    if audio is None or len(audio) == 0:
        return np.empty((n_mfcc, 0), dtype=np.float32)

    mfcc = librosa.feature.mfcc(
        y=audio.astype(np.float32),
        sr=sample_rate,
        n_mfcc=n_mfcc,
        n_fft=512,
        hop_length=160
    )

    return mfcc.astype(np.float32)


def mfcc_statistics(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """Return statistical MFCC features."""

    mfcc = extract_mfcc(
        audio,
        sample_rate
    )

    if mfcc.size == 0:
        return {
            "mfcc_mean": [],
            "mfcc_std": []
        }

    return {
        "mfcc_mean": np.mean(
            mfcc,
            axis=1
        ).round(6).tolist(),

        "mfcc_std": np.std(
            mfcc,
            axis=1
        ).round(6).tolist()
    }