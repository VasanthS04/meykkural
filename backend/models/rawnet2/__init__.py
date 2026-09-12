"""
RawNet2 anti-spoofing model.
"""

from .model import RawNet2Model
from .inference import RawNet2Inference

__all__ = [
    "RawNet2Model",
    "RawNet2Inference",
]