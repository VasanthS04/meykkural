"""Wav2Vec2 voice authenticity model."""

from .model import Wav2Vec2Model
from .inference import Wav2Vec2Inference

__all__ = [
    "Wav2Vec2Model",
    "Wav2Vec2Inference",
]