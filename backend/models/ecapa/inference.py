from typing import Dict

import numpy as np
import torch

from .model import ECAPAModel


class ECAPAInference:
    """
    ECAPA-TDNN speaker verification inference.
    """

    def __init__(
        self,
        model: ECAPAModel | None = None,
    ):
        self.model = model or ECAPAModel()

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

    def extract_embedding(
        self,
        audio: np.ndarray,
    ) -> torch.Tensor:

        if not self.model.checkpoint_loaded:
            raise RuntimeError(
                "ECAPA-TDNN checkpoint is not loaded."
            )

        tensor = self.prepare_audio(
            audio
        ).to(self.model.device)

        self.model.eval()

        with torch.no_grad():
            embedding = self.model(
                tensor
            )

        return embedding

    def analyze(
        self,
        audio: np.ndarray,
    ) -> Dict[str, float]:

        if not self.model.checkpoint_loaded:
            return {
                "model": "ECAPA-TDNN",
                "speaker_score": 0.0,
            }

        embedding = self.extract_embedding(
            audio
        )

        score = float(
            torch.norm(embedding)
            .item()
        )

        return {
            "model": "ECAPA-TDNN",
            "speaker_score": score,
        }