from typing import Dict

import numpy as np
import torch

from .model import AASISTModel


class AASISTInference:
    """
    Inference interface for AASIST.
    """

    def __init__(
        self,
        model: AASISTModel | None = None,
    ):
        self.model = model or AASISTModel()

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

        tensor = torch.from_numpy(
            audio
        ).float()

        return tensor.unsqueeze(0)

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

        if output.numel() == 0:
            return 0.0

        score = torch.sigmoid(
            output.reshape(-1)[0]
        ).item()

        return round(
            max(0.0, min(100.0, score * 100)),
            2,
        )

    def analyze(
        self,
        audio: np.ndarray,
    ) -> Dict[str, float]:

        score = self.predict(audio)

        return {
            "model": "AASIST",
            "spoof_score": score,
        }