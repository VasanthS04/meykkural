from pathlib import Path
from typing import Optional
import torch
import torch.nn as nn

from .architecture import RawNet


class RawNet2Model(nn.Module):
    """RawNet2 anti-spoofing model wrapper."""

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        device: Optional[str] = None,
        architecture_version: str = "itw",  # 'itw' or 'clean' or 'baseline'
    ):
        super().__init__()

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.checkpoint_loaded = False

        # Instantiate the architecture
        self.network = RawNet()

        if checkpoint_path:
            self.load_checkpoint(checkpoint_path)

        self.to(self.device)

    def load_checkpoint(self, checkpoint_path: str) -> bool:
        path = Path(checkpoint_path)
        if not path.exists():
            return False

        checkpoint = torch.load(path, map_location=self.device)

        # Handle different checkpoint formats
        if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
        else:
            state_dict = checkpoint

        if isinstance(state_dict, dict):
            self.network.load_state_dict(state_dict, strict=False)
        self.checkpoint_loaded = True
        self.to(self.device)
        return True

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        if self.network is None:
            raise RuntimeError("RawNet2 architecture has not been initialized.")
        return self.network(audio)

    def to_device(self):
        self.to(self.device)
        return self