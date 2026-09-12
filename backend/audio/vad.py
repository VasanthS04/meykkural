import numpy as np


def calculate_rms(
    audio: np.ndarray
) -> float:
    """Calculate RMS energy."""

    if audio is None or len(audio) == 0:
        return 0.0

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    return float(
        np.sqrt(
            np.mean(
                np.square(audio)
            )
        )
    )


def detect_voice(
    audio: np.ndarray,
    threshold: float = 0.01
) -> bool:
    """
    Basic energy-based voice activity detection.

    Returns True when the audio contains
    sufficient energy to be considered speech.
    """

    if audio is None or len(audio) == 0:
        return False

    return calculate_rms(audio) >= threshold


def voice_ratio(
    audio: np.ndarray,
    sample_rate: int = 16000,
    frame_ms: int = 30,
    threshold: float = 0.01
) -> float:
    """
    Calculate the percentage of frames containing voice.
    """

    if audio is None or len(audio) == 0:
        return 0.0

    frame_size = int(
        sample_rate *
        frame_ms /
        1000
    )

    if frame_size <= 0:
        return 0.0

    voiced_frames = 0
    total_frames = 0

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

        total_frames += 1

        if calculate_rms(frame) >= threshold:
            voiced_frames += 1

    if total_frames == 0:
        return 0.0

    return float(
        voiced_frames / total_frames
    )


def estimate_speech_activity(
    audio: np.ndarray,
    sample_rate: int = 16000,
    threshold: float = 0.01
) -> dict:
    """
    Return basic VAD information for the
    real-time analysis pipeline.
    """

    rms = calculate_rms(audio)

    ratio = voice_ratio(
        audio,
        sample_rate=sample_rate,
        threshold=threshold
    )

    return {
        "speech": ratio > 0.1,
        "rms": round(rms, 6),
        "voice_ratio": round(ratio, 4)
    }