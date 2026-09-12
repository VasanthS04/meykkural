import numpy as np
import librosa


def extract_mel_spectrogram(
    audio: np.ndarray,
    sample_rate: int = 16000,
    n_mels: int = 80
) -> np.ndarray:
    """Extract log-Mel spectrogram."""

    if audio is None or len(audio) == 0:
        return np.empty((n_mels, 0), dtype=np.float32)

    mel = librosa.feature.melspectrogram(
        y=audio.astype(np.float32),
        sr=sample_rate,
        n_fft=512,
        hop_length=160,
        n_mels=n_mels,
        power=2.0
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    return mel_db.astype(np.float32)