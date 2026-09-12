import numpy as np

from backend.features.energy import extract_energy
from backend.features.pitch import extract_pitch


def extract_prosody(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> dict:
    """
    Extract speech prosody characteristics.

    Includes:
    - Pitch variation
    - Energy variation
    - Speaking activity
    - Pause ratio
    """

    if audio is None or len(audio) == 0:
        return {
            "pitch_variation": 0.0,
            "energy_variation": 0.0,
            "pause_ratio": 1.0,
            "speaking_activity": 0.0
        }

    energy = extract_energy(
        audio,
        sample_rate
    )

    pitch = extract_pitch(
        audio,
        sample_rate
    )

    frame_size = int(
        sample_rate * 0.03
    )

    if frame_size <= 0:
        return {
            "pitch_variation": pitch["pitch_std"],
            "energy_variation": energy["rms_std"],
            "pause_ratio": 0.0,
            "speaking_activity": 1.0
        }

    pauses = 0
    frames = 0

    threshold = 0.01

    for start in range(
        0,
        len(audio),
        frame_size
    ):
        frame = audio[
            start:start + frame_size
        ]

        if len(frame) < frame_size:
            continue

        frames += 1

        rms = np.sqrt(
            np.mean(
                frame ** 2
            )
        )

        if rms < threshold:
            pauses += 1

    pause_ratio = (
        pauses / frames
        if frames > 0
        else 0.0
    )

    return {
        "pitch_variation": float(
            pitch["pitch_std"]
        ),
        "energy_variation": float(
            energy["rms_std"]
        ),
        "pause_ratio": float(
            pause_ratio
        ),
        "speaking_activity": float(
            1.0 - pause_ratio
        )
    }