import numpy as np
import librosa


def extract_pitch(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """Extract fundamental-frequency/pitch statistics."""

    if audio is None or len(audio) == 0:
        return {
            "pitch_mean": 0.0,
            "pitch_std": 0.0,
            "pitch_min": 0.0,
            "pitch_max": 0.0
        }

    try:
        f0, voiced_flag, _ = librosa.pyin(
            audio.astype(np.float32),
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=sample_rate,
            frame_length=1024,
            hop_length=160
        )

        pitch = f0[
            ~np.isnan(f0)
        ]

        if len(pitch) == 0:
            return {
                "pitch_mean": 0.0,
                "pitch_std": 0.0,
                "pitch_min": 0.0,
                "pitch_max": 0.0
            }

        return {
            "pitch_mean": float(np.mean(pitch)),
            "pitch_std": float(np.std(pitch)),
            "pitch_min": float(np.min(pitch)),
            "pitch_max": float(np.max(pitch))
        }

    except Exception:
        return {
            "pitch_mean": 0.0,
            "pitch_std": 0.0,
            "pitch_min": 0.0,
            "pitch_max": 0.0
        }