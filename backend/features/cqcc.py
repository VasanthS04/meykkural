import numpy as np
import librosa


def extract_cqcc(
    audio: np.ndarray,
    sample_rate: int = 16000,
    n_coefficients: int = 20
) -> np.ndarray:
    """
    CQT-based cepstral representation.

    This provides a practical CQCC-style feature representation
    for the prototype. A dedicated CQCC implementation can
    replace this function during model training.
    """

    if audio is None or len(audio) == 0:
        return np.empty(
            (n_coefficients, 0),
            dtype=np.float32
        )

    cqt = np.abs(
        librosa.cqt(
            audio.astype(np.float32),
            sr=sample_rate,
            hop_length=160,
            fmin=librosa.note_to_hz("C1"),
            n_bins=84,
            bins_per_octave=12
        )
    )

    log_cqt = np.log(
        np.maximum(cqt, 1e-10)
    )

    cqcc = librosa.feature.mfcc(
        S=log_cqt,
        n_mfcc=n_coefficients
    )

    return cqcc.astype(np.float32)