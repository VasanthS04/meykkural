from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn


class XLSRModel(nn.Module):
    """
    XLS-R anti-deepfake model wrapper.

    XLS-R is a speech representation model. For Meykkural,
    it must be combined with a fine-tuned anti-spoofing head.
    """

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        super().__init__()

        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.checkpoint_loaded = False
        self.network = None

        if checkpoint_path:
            self.load_checkpoint(
                checkpoint_path
            )

    def load_checkpoint(
        self,
        checkpoint_path: str,
    ) -> bool:

        path = Path(checkpoint_path)

        if not path.exists():
            return False

        self.checkpoint = torch.load(
            path,
            map_location=self.device,
        )

        self.checkpoint_loaded = True

        return True

    def forward(
        self,
        audio: torch.Tensor,
    ) -> torch.Tensor:

        if self.network is None:
            raise RuntimeError(
                "XLS-R anti-deepfake architecture "
                "has not been connected yet."
            )

        return self.network(audio)