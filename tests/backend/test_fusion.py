from backend.fusion.risk_engine import calculate_risk, risk_level
from backend.fusion.score_fusion import ScoreFusion


def test_wav2vec2_score_fuses_into_risk():
    fusion = ScoreFusion({"wav2vec2": 1.0})
    assert fusion.fuse({"wav2vec2": 82.5}) == 82.5
    assert calculate_risk({"wav2vec2": 82.5}) == 82
    assert risk_level(82) == "HIGH"


def test_fusion_preserves_calibrated_scores():
    fusion = ScoreFusion({"wav2vec2": 1.0})
    assert fusion.fuse_with_details({"wav2vec2": 82.5})["risk_score"] == 82.5


def test_bonafide_risk_is_lower_than_spoof_risk():
    fusion = ScoreFusion({"aasist": 1.0})
    assert fusion.fuse({"aasist": 0.0}) < fusion.fuse({"aasist": 9.0})