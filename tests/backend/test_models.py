import numpy as np
import soundfile as sf
from pathlib import Path

from backend.inference.acoustic_detector import score_acoustic_spoof
from backend.inference.engine import run_inference


def test_wav2vec2_inference_returns_bounded_score():
    scores = run_inference(np.zeros(16000, dtype=np.float32))
    expected_models = {
        "aasist",
        "wav2vec2",
        "rawnet2",
        "conformer",
        "xlsr",
        "ecapa",
        "_fallback_models",
    }
    assert set(scores) == expected_models
    assert all(0.0 <= score <= 100.0 for score in scores.values())
    assert scores["_fallback_models"] is True


def test_acoustic_detector_handles_silence_and_audio():
    silence = score_acoustic_spoof(np.zeros(16000, dtype=np.float32))
    tone = score_acoustic_spoof(
        np.sin(2 * np.pi * 220 * np.arange(16000) / 16000).astype(np.float32)
    )
    assert silence == 0.0
    assert 0.0 <= tone <= 100.0


def test_fixture_scores_follow_ai_risk_polarity():
    root = Path("datasets/testing/generated")
    bonafide, _ = sf.read(root / "bonafide" / "real_000.wav", dtype="float32")
    spoof, _ = sf.read(root / "spoof" / "synthetic_000.wav", dtype="float32")

    bonafide_score = score_acoustic_spoof(bonafide)
    spoof_score = score_acoustic_spoof(spoof)

    assert spoof_score > bonafide_score