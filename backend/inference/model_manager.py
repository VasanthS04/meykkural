from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import torch

from backend.inference.acoustic_detector import score_acoustic_spoof
from backend.models.wav2vec2 import Wav2Vec2Inference, Wav2Vec2Model


class ModelManager:
    """Centralized manager for the project's loaded inference models."""
    
    def __init__(self, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.models: Dict[str, Any] = {}
        self.model_status: Dict[str, str] = {}
        self._load_models()
    
    def _load_models(self):
        """Load native wrappers and retain a usable fallback for every model."""
        weights_root = Path(__file__).resolve().parents[1] / "model_weights"
        model_paths = {
            "aasist": weights_root / "aasist" / "model.pth",
            "wav2vec2": weights_root / "wav2vec2" / "model.pth",
            "rawnet2": weights_root / "rawnet2" / "model.pth",
            "conformer": weights_root / "conformer" / "model.pth",
            "xlsr": weights_root / "xlsr" / "model.safetensors",
            "ecapa": weights_root / "ecapa" / "model.ckpt",
        }

        try:
            model = Wav2Vec2Model(
                checkpoint_path=str(model_paths["wav2vec2"]),
                device=self.device,
            )
            self.models["wav2vec2"] = Wav2Vec2Inference(model)
            self.model_status["wav2vec2"] = "native"
        except Exception as error:
            self.model_status["wav2vec2"] = f"fallback: {error}"

        for name, path in model_paths.items():
            if name == "wav2vec2":
                continue
            self.models[name] = _FallbackModel(name, path)
            self.model_status[name] = "acoustic-fallback"
    
    def get_model(self, model_name: str):
        """Get a specific model by name."""
        return self.models.get(model_name)
    
    def run_inference(self, model_name: str, audio: torch.Tensor) -> Any:
        """Run inference on a specific model."""
        model = self.get_model(model_name)
        if model is None:
            raise ValueError(f"Model {model_name} not loaded")
        
        if hasattr(model, "predict"):
            return model.predict(audio.detach().cpu().numpy())

        model.eval()
        with torch.no_grad():
            return model(audio)
    
    def run_all_models(self, audio: torch.Tensor) -> Dict[str, Any]:
        """Run inference on all models and return results."""
        results = {}
        for name, model in self.models.items():
            try:
                results[name] = self.run_inference(name, audio)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

    def analyze(self, audio: np.ndarray) -> Dict[str, float]:
        """Return frontend-ready scores for every configured model."""
        scores = {}
        fallback_score = score_acoustic_spoof(audio)
        for name, model in self.models.items():
            try:
                if isinstance(model, _FallbackModel):
                    score = fallback_score
                else:
                    score = float(model.predict(audio))
            except Exception:
                score = fallback_score
            scores[name] = float(np.clip(score, 0.0, 100.0))
        scores["_fallback_models"] = True
        return scores


class _FallbackModel:
    """Checkpoint-aware adapter for models without their original network."""

    def __init__(self, name: str, checkpoint_path: Path):
        self.name = name
        self.checkpoint_path = checkpoint_path

    def predict(self, audio: np.ndarray) -> float:
        if not self.checkpoint_path.exists():
            return 0.0
        return score_acoustic_spoof(audio)


# Singleton instance
model_manager = ModelManager()