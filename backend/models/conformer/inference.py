from typing import Dict

import numpy as np
import torch

from .model import ConformerModel


class ConformerInference:

    def __init__(
        self,
        model: ConformerModel | None = None,
    ):
        self.model = model or ConformerModel()

    @staticmethod
    def prepare_audio(
        audio: np.ndarray,
    ) -> torch.Tensor:

        if audio is None or len(audio) == 0:
            raise ValueError("Audio is empty.")

        audio = np.asarray(
            audio,
            dtype=np.float32,
        )

        return torch.from_numpy(
            audio
        ).float().unsqueeze(0)

    def predict(
        self,
        audio: np.ndarray,
    ) -> float:

        if not self.model.checkpoint_loaded:
            return 0.0

        tensor = self.prepare_audio(
            audio
        ).to(self.model.device)

        self.model.eval()

        with torch.no_grad():
            output = self.model(tensor)

        score = torch.sigmoid(
            output.reshape(-1)[0]
        ).item()

        return round(
            score * 100,
            2,
        )

    def analyze(
        self,
        audio: np.ndarray,
    ) -> Dict[str, float]:

        return {
            "model": "Conformer",
            "spoof_score": self.predict(audio),
        }