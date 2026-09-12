import torch
from .model import RawNet2Model


class RawNet2Inference:
    """Inference wrapper for RawNet2."""

    def __init__(self, model_path: str, device: str = None):
        self.model = RawNet2Model(checkpoint_path=model_path, device=device)
        self.model.eval()

    def predict(self, audio: torch.Tensor) -> float:
        """Run inference and return spoofing score."""
        with torch.no_grad():
            output = self.model(audio)
            # Assuming output is logits; convert to probability
            probability = torch.sigmoid(output).item()
        return probability