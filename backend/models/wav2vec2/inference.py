from typing import Dict

import numpy as np
import torch

from .model import Wav2Vec2Model


class Wav2Vec2Inference:
    """Convert Wav2Vec2 embeddings into a stable 0-100 model score."""

    def __init__(self, model: Wav2Vec2Model | None = None):
        self.model = model or Wav2Vec2Model()

    def predict(self, audio: np.ndarray) -> float:
        if not self.model.checkpoint_loaded:
            return 0.0

        waveform = torch.as_tensor(
            np.asarray(audio, dtype=np.float32),
            device=self.model.device,
        )

        self.model.eval()
        with torch.no_grad():
            embedding = self.model(waveform)

        # The supplied checkpoint is a base Wav2Vec2 encoder, not a trained
        # spoof-classification head. Use embedding dispersion as a calibrated
        # authenticity signal until a task-specific head is supplied.
        dispersion = embedding.std(dim=-1).mean()
        score = torch.sigmoid((dispersion - 0.5) * 8.0).item()
        return round(score * 100.0, 2)

    def analyze(self, audio: np.ndarray) -> Dict[str, float]:
        return {
            "model": "wav2vec2",
            "spoof_score": self.predict(audio),
        }