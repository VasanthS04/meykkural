from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn


class ConformerModel(nn.Module):
    """
    Conformer anti-spoofing model wrapper.
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

        self.checkpoint_path = checkpoint_path
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
                "Conformer architecture has not been connected yet."
            )

        return self.network(audio)

    def to_device(self):
        self.to(self.device)
        return self