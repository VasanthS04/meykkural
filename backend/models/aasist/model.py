from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn


class AASISTModel(nn.Module):
    """
    AASIST model wrapper.

    The actual AASIST architecture/checkpoint should be loaded
    when the official pretrained implementation is integrated.
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

        # Placeholder for the official AASIST network.
        self.network = None

        if checkpoint_path:
            self.load_checkpoint(checkpoint_path)

    def load_checkpoint(self, checkpoint_path: str) -> bool:
        """
        Load an AASIST checkpoint.

        The checkpoint must match the exact AASIST architecture.
        """

        path = Path(checkpoint_path)

        if not path.exists():
            return False

        checkpoint = torch.load(
            path,
            map_location=self.device,
        )

        # The actual official AASIST state_dict loading
        # will be connected here.
        self.checkpoint = checkpoint
        self.checkpoint_loaded = True

        return True

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        """
        Run AASIST forward inference.
        """

        if self.network is None:
            raise RuntimeError(
                "AASIST architecture has not been connected yet."
            )

        return self.network(audio)

    def to_device(self):
        """Move model to the selected device."""
        self.to(self.device)
        return self