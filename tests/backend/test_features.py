import numpy as np

from backend.features.extractor import extract_features


def test_feature_extractor_returns_frontend_contract():
    features = extract_features(np.zeros(16000, dtype=np.float32))
    assert set(features) == {
        "mfcc", "mel", "lfcc", "cqcc", "pitch", "energy",
        "harmonics", "pauses",
    }
    assert all(0.0 <= value <= 100.0 for value in features.values())