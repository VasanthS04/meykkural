from typing import Dict, Any
import numpy as np

from backend.audio.preprocessing import preprocess_audio
from backend.audio.vad import detect_voice
from backend.features.extractor import extract_features
from backend.inference.model_manager import model_manager
from backend.fusion.risk_engine import (
    calculate_risk,
    risk_level,
)
from backend.alerts.notification import create_notification


class InferencePipeline:
    """
    Complete Meykkural real-time inference pipeline.

    Audio flow:

    Audio
      ↓
    Preprocessing
      ↓
    VAD
      ↓
    Feature extraction
      ↓
    AI models
      ↓
    Score fusion
      ↓
    Risk level
      ↓
    Notification
    """

    def __init__(
        self,
        sample_rate: int = 16000
    ):
        self.sample_rate = sample_rate

    def process(
        self,
        audio: np.ndarray,
        original_sample_rate: int = 16000
    ) -> Dict[str, Any]:

        if audio is None or len(audio) == 0:
            return self._empty_result()

        # --------------------------------------------------
        # 1. PREPROCESSING
        # --------------------------------------------------

        processed_audio = preprocess_audio(
            audio,
            original_sample_rate,
            self.sample_rate
        )

        if len(processed_audio) == 0:
            return self._empty_result()

        # --------------------------------------------------
        # 2. VOICE ACTIVITY DETECTION
        # --------------------------------------------------

        speech_detected = detect_voice(
            processed_audio
        )

        if not speech_detected:
            return {
                "speech": False,
                "risk": 0,
                "risk_level": "LOW",
                "models": {},
                "features": {},
                "notification": None,
                "privacy": {
                    "audio_stored": False
                }
            }

        # --------------------------------------------------
        # 3. FEATURE EXTRACTION
        # --------------------------------------------------

        features = extract_features(
            processed_audio,
            self.sample_rate
        )

        # --------------------------------------------------
        # 4. AI MODEL INFERENCE
        # --------------------------------------------------

        model_scores = model_manager.analyze(
            processed_audio
        )

        # --------------------------------------------------
        # 5. SCORE FUSION
        # --------------------------------------------------

        risk = calculate_risk(
            model_scores
        )

        # --------------------------------------------------
        # 6. RISK CLASSIFICATION
        # --------------------------------------------------

        level = risk_level(
            risk
        )

        # --------------------------------------------------
        # 7. NOTIFICATION
        # --------------------------------------------------

        notification = create_notification(
            risk
        )

        # --------------------------------------------------
        # 8. RESULT
        # --------------------------------------------------

        result = {
            "speech": True,
            "risk": risk,
            "risk_level": level,
            "models": model_scores,
            "features": features,
            "speaker": 0.0,
            "notification": notification,
            "privacy": {
                "audio_stored": False,
                "processing": "in-memory"
            }
        }

        # Explicitly release local reference.
        del processed_audio

        return result

    def _empty_result(self) -> Dict[str, Any]:
        """
        Return a safe empty-analysis result.
        """

        return {
            "speech": False,
            "risk": 0,
            "risk_level": "LOW",
            "models": {},
            "features": {},
            "notification": None,
            "privacy": {
                "audio_stored": False,
                "processing": "in-memory"
            }
        }


pipeline = InferencePipeline()


def process_audio(
    audio: np.ndarray,
    sample_rate: int = 16000
) -> Dict[str, Any]:
    """
    Compatibility helper for API/WebSocket code.
    """

    return pipeline.process(
        audio,
        sample_rate
    )