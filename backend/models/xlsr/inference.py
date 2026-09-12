from typing import Dict

import numpy as np
import torch

from .model import XLSRModel


class XLSRInference:

    def __init__(
        self,
        model: XLSRModel | None = None,
    ):
        self.model = model or XLSRModel()

    def predict(
        self,
        audio: np.ndarray,
    ) -> float:

        if not self.model.checkpoint_loaded:
            return 0.0

        audio = np.asarray(
            audio,
            dtype=np.float32,
        )

        tensor = torch.from_numpy(
            audio
        ).float().unsqueeze(0)

        tensor = tensor.to(
            self.model.device
        )

        self.model.eval()

        with torch.no_grad():
            output = self.model(
                tensor
            )

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
            "model": "XLS-R",
            "spoof_score": self.predict(audio),
        }